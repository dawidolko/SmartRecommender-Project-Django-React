from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q, Avg, F
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
        fuzzy_threshold = float(request.GET.get("fuzzy_threshold", "0.6"))

        if not query:
            return Response([], status=200)

        products = (
            Product.objects.select_related("sentiment_summary")
            .prefetch_related(
                "categories", "photoproduct_set", "specification_set", "tags"
            )
            .all()
        )

        fuzzy_engine = CustomFuzzySearch()
        fuzzy_results = fuzzy_engine.search_products(query, products, fuzzy_threshold)

        if price_range:
            filtered_results = []
            for result in fuzzy_results:
                if self.match_price_range(result["product"].price, price_range):
                    filtered_results.append(result)
            fuzzy_results = filtered_results

        sorted_products = [result["product"] for result in fuzzy_results]

        serializer = ProductSerializer(sorted_products, many=True)

        data = serializer.data
        for i, result in enumerate(fuzzy_results):
            product = result["product"]
            data[i]["fuzzy_score"] = float(result["score"])
            data[i]["name_score"] = float(result["name_score"])
            data[i]["desc_score"] = float(result["desc_score"])
            data[i]["category_score"] = float(result["category_score"])
            data[i]["spec_score"] = float(result["spec_score"])

            if hasattr(product, "sentiment_summary") and product.sentiment_summary:
                data[i]["sentiment_score"] = float(
                    product.sentiment_summary.average_sentiment_score
                )
            else:
                data[i]["sentiment_score"] = 0

        return Response(data)

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

        return Response(data)

    def calculate_fuzzy_score(self, query, text):
        if not text:
            return 0

        query = query.lower()
        text = text.lower()

        if query in text:
            return 1.0

        words = query.split()
        matches = sum(1 for word in words if word in text)
        word_score = matches / len(words) if words else 0

        shorter, longer = sorted([query, text], key=len)
        if len(longer) == 0:
            return 1.0

        similarity = (len(longer) - len(longer.replace(shorter, ""))) / len(longer)

        return max(word_score, similarity)

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
