from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q, Avg, F
from django.core.cache import cache
from django.conf import settings
from .models import Product, ProductSentimentSummary, SentimentAnalysis
from .serializers import ProductSerializer
from .custom_recommendation_engine import CustomFuzzySearch


class SentimentSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get("q", "").strip()

        if not query:
            return Response([], status=200)

        products = (
            Product.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(categories__name__icontains=query)
                | Q(specification__parameter_name__icontains=query)
                | Q(specification__specification__icontains=query)
            )
            .select_related("sentiment_summary")
            .prefetch_related("categories", "photoproduct_set")
            .distinct()
        )

        products = products.order_by(
            F("sentiment_summary__average_sentiment_score").desc(nulls_last=True),
            "name",
        )

        serializer = ProductSerializer(products, many=True)

        data = serializer.data
        for i, product in enumerate(products):
            if hasattr(product, "sentiment_summary") and product.sentiment_summary:
                data[i]["sentiment_score"] = float(
                    product.sentiment_summary.average_sentiment_score
                )
                data[i]["total_opinions"] = product.sentiment_summary.total_opinions
            else:
                data[i]["sentiment_score"] = 0
                data[i]["total_opinions"] = 0

        return Response(data)

class FuzzySearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get("q", "").strip()
        price_range = request.GET.get("price_range", "")
        fuzzy_threshold = float(request.GET.get("fuzzy_threshold", "0.5"))
        max_results = int(request.GET.get("max_results", "50"))

        if not query:
            return Response([], status=200)

        if len(query) < 2:
            return Response({"error": "Query too short"}, status=400)

        try:
            cache_key = f"fuzzy_sentiment_search_{hash(query)}_{price_range}_{fuzzy_threshold}_{max_results}"
            cached_result = cache.get(cache_key)
            if cached_result:
                return Response(cached_result)

            products_query = Product.objects.select_related("sentiment_summary").prefetch_related(
                "categories", "photoproduct_set", "specification_set", "tags"
            )
            
            if len(query) >= 3:
                products_query = products_query.filter(
                    Q(name__icontains=query[:3]) |
                    Q(description__icontains=query[:3]) |
                    Q(categories__name__icontains=query[:3])
                ).distinct()
            
            products = list(products_query[:1000])

            fuzzy_results = self._simple_fuzzy_search(query, products, fuzzy_threshold)

            if price_range:
                filtered_results = []
                for result in fuzzy_results:
                    if self.match_price_range(result["product"].price, price_range):
                        filtered_results.append(result)
                fuzzy_results = filtered_results

            fuzzy_results = fuzzy_results[:max_results]
            sorted_products = [result["product"] for result in fuzzy_results]

            if not fuzzy_results:
                return Response([])

            serializer = ProductSerializer(sorted_products, many=True)
            data = serializer.data
            
            for i, result in enumerate(fuzzy_results):
                product = result["product"]
                data[i]["fuzzy_score"] = float(result["score"])
                data[i]["name_score"] = float(result["name_score"])
                data[i]["desc_score"] = float(result["desc_score"])
                data[i]["category_score"] = float(result["category_score"])
                data[i]["spec_score"] = float(result["spec_score"])
                data[i]["tag_score"] = float(result.get("tag_score", 0))

                if hasattr(product, "sentiment_summary") and product.sentiment_summary:
                    data[i]["sentiment_score"] = float(
                        product.sentiment_summary.average_sentiment_score
                    )
                    data[i]["sentiment_confidence"] = float(
                        min(product.sentiment_summary.total_opinions / 10.0, 1.0)
                    )
                    data[i]["sentiment_variance"] = float(
                        abs(0.5 - abs(float(product.sentiment_summary.average_sentiment_score))) * 2
                    )
                else:
                    data[i]["sentiment_score"] = 0
                    data[i]["sentiment_confidence"] = 0
                    data[i]["sentiment_variance"] = 0

            cache.set(cache_key, data, timeout=900)
            return Response(data)
            
        except Exception as e:
            return Response({"error": f"Search error: {str(e)}"}, status=500)

    def _simple_fuzzy_search(self, query, products, threshold):
        results = []
        query_lower = query.lower()
        query_words = query_lower.split()
        
        for product in products:
            name_lower = product.name.lower()
            desc_lower = (product.description or "").lower()
            
            name_score = 0.0
            if query_lower in name_lower:
                name_score = 1.0
            else:
                word_matches = sum(1 for word in query_words if word in name_lower)
                name_score = word_matches / len(query_words) if query_words else 0.0
            
            desc_score = 0.0
            if query_lower in desc_lower:
                desc_score = 0.8
            else:
                word_matches = sum(1 for word in query_words if word in desc_lower)
                desc_score = (word_matches / len(query_words)) * 0.8 if query_words else 0.0
            
            category_score = 0.0
            for cat in product.categories.all():
                cat_name = cat.name.lower()
                if query_lower in cat_name:
                    category_score = 0.6
                    break
                else:
                    word_matches = sum(1 for word in query_words if word in cat_name)
                    if word_matches > 0:
                        category_score = max(category_score, (word_matches / len(query_words)) * 0.6)
            
            spec_score = 0.0
            try:
                for spec in product.specification_set.all()[:5]:
                    spec_text = f"{spec.parameter_name} {spec.specification}".lower()
                    if query_lower in spec_text:
                        spec_score = 0.4
                        break
                    else:
                        word_matches = sum(1 for word in query_words if word in spec_text)
                        if word_matches > 0:
                            spec_score = max(spec_score, (word_matches / len(query_words)) * 0.4)
            except:
                pass
            
            tag_score = 0.0
            try:
                for tag in product.tags.all():
                    tag_name = tag.name.lower()
                    if query_lower in tag_name:
                        tag_score = 0.3
                        break
                    else:
                        word_matches = sum(1 for word in query_words if word in tag_name)
                        if word_matches > 0:
                            tag_score = max(tag_score, (word_matches / len(query_words)) * 0.3)
            except:
                pass
            
            total_score = (name_score * 0.4 + desc_score * 0.3 + 
                          category_score * 0.2 + spec_score * 0.05 + tag_score * 0.05)
            
            if total_score >= threshold:
                results.append({
                    "product": product,
                    "score": round(total_score, 3),
                    "name_score": round(name_score, 3),
                    "desc_score": round(desc_score, 3),
                    "category_score": round(category_score, 3),
                    "spec_score": round(spec_score, 3),
                    "tag_score": round(tag_score, 3)
                })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def match_price_range(self, price, price_range):
        try:
            if price_range == "cheap":
                return price < 100
            elif price_range == "medium":
                return 100 <= price <= 500
            elif price_range == "expensive":
                return price > 500
            return True
        except:
            return True