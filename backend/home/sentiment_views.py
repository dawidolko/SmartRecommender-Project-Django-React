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
        # OBNIŻONE: domyślny próg z 0.6 na 0.5 dla lepszego pokrycia
        fuzzy_threshold = float(request.GET.get("fuzzy_threshold", "0.5"))
        max_results = int(request.GET.get("max_results", "50"))  # Limit results

        if not query:
            return Response([], status=200)

        if len(query) < 2:
            return Response({"error": "Query too short"}, status=400)

        try:
            # Cache check
            cache_key = f"fuzzy_sentiment_search_{hash(query)}_{price_range}_{fuzzy_threshold}_{max_results}"
            cached_result = cache.get(cache_key)
            if cached_result:
                return Response(cached_result)

            # Limit products for performance - first try pre-filtering
            products_query = Product.objects.select_related("sentiment_summary").prefetch_related(
                "categories", "photoproduct_set", "specification_set", "tags"
            )
            
            # Quick pre-filter to reduce dataset
            if len(query) >= 3:
                products_query = products_query.filter(
                    Q(name__icontains=query[:3]) |
                    Q(description__icontains=query[:3]) |
                    Q(categories__name__icontains=query[:3])
                ).distinct()
            
            products = list(products_query[:1000])  # Limit to 1000 products max

            # ULEPSZONE: Używamy nowej wersji CustomFuzzySearch z trigramami
            fuzzy_engine = CustomFuzzySearch()
            fuzzy_results = fuzzy_engine.search_products(query, products, fuzzy_threshold)

            if price_range:
                filtered_results = []
                for result in fuzzy_results:
                    if self.match_price_range(result["product"].price, price_range):
                        filtered_results.append(result)
                fuzzy_results = filtered_results

            # Limit final results
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
                # NOWE: Dodanie tag_score z ulepszonej wersji
                data[i]["tag_score"] = float(result.get("tag_score", 0))

                if hasattr(product, "sentiment_summary") and product.sentiment_summary:
                    data[i]["sentiment_score"] = float(
                        product.sentiment_summary.average_sentiment_score
                    )
                    # Dodatkowe metryki (obliczone dynamicznie na podstawie istniejących danych)
                    data[i]["sentiment_confidence"] = float(
                        min(product.sentiment_summary.total_opinions / 10.0, 1.0)  # Większa pewność z większą liczbą opinii
                    )
                    data[i]["sentiment_variance"] = float(
                        abs(0.5 - abs(product.sentiment_summary.average_sentiment_score)) * 2  # Wariancja na podstawie odchylenia od neutralności
                    )
                else:
                    data[i]["sentiment_score"] = 0
                    data[i]["sentiment_confidence"] = 0
                    data[i]["sentiment_variance"] = 0

            # Cache wyników na 15 minut
            cache.set(cache_key, data, timeout=900)
            return Response(data)
            
        except Exception as e:
            return Response({"error": f"Search error: {str(e)}"}, status=500)

    def match_price_range(self, price, price_range):
        """Enhanced price range matching with better categories"""
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
