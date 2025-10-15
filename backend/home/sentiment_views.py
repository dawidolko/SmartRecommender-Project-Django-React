from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models import Q, Avg, F, Count
from django.core.cache import cache
from django.conf import settings
from .models import Product, ProductSentimentSummary, SentimentAnalysis
from .serializers import ProductSerializer
from .custom_recommendation_engine import CustomFuzzySearch


class SentimentSearchAPIView(APIView):
    """
    Sentiment-based product search using lexicon-based sentiment analysis.

    Algorithm: Ranks products by sentiment score calculated from:
    - Customer opinions (weight: 40%)
    - Product description (weight: 25%)
    - Product name (weight: 15%)
    - Product specifications (weight: 12%)
    - Product categories (weight: 8%)

    Mathematical Formula (Liu, Bing 2012 - "Sentiment Analysis and Opinion Mining"):

    Sentiment_Score = (Positive_Count - Negative_Count) / Total_Words

    Where:
    - Positive_Count = number of positive words in text (from positive_words lexicon)
    - Negative_Count = number of negative words in text (from negative_words lexicon)
    - Total_Words = total number of words in text

    Score Range: [-1.0, +1.0]
    - Score > 0.1  → Positive sentiment
    - Score < -0.1 → Negative sentiment
    - Otherwise    → Neutral sentiment

    Multi-Source Aggregation (per product):
    Final_Score = (Opinion_Score * 0.40) + (Description_Score * 0.25) +
                  (Name_Score * 0.15) + (Spec_Score * 0.12) + (Category_Score * 0.08)

    Source: Liu, B. (2012). "Sentiment Analysis and Opinion Mining",
            Morgan & Claypool Publishers. Chapter 2: Sentiment Lexicons.

    Implementation: CustomSentimentAnalysis.analyze_sentiment() in custom_recommendation_engine.py
    """

    permission_classes = [AllowAny]

    def get(self, request):
        from .custom_recommendation_engine import CustomSentimentAnalysis

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
            .prefetch_related(
                "categories", "photoproduct_set", "specification_set", "opinion_set"
            )
            .distinct()
        )

        analyzer = CustomSentimentAnalysis()
        products_with_scores = []

        for product in products:
            opinion_scores = []
            opinions = product.opinion_set.all()[:20]
            for opinion in opinions:
                score, _ = analyzer.analyze_sentiment(opinion.content)
                opinion_scores.append(score)
            opinion_sentiment = (
                sum(opinion_scores) / len(opinion_scores) if opinion_scores else 0.0
            )

            desc_score, _ = analyzer.analyze_sentiment(product.description or "")

            name_score, _ = analyzer.analyze_sentiment(product.name)

            spec_texts = []
            for spec in product.specification_set.all()[:10]:
                spec_texts.append(f"{spec.parameter_name} {spec.specification}")
            spec_combined = " ".join(spec_texts)
            spec_score, _ = (
                analyzer.analyze_sentiment(spec_combined)
                if spec_combined
                else (0.0, "neutral")
            )

            category_names = " ".join([cat.name for cat in product.categories.all()])
            category_score, _ = (
                analyzer.analyze_sentiment(category_names)
                if category_names
                else (0.0, "neutral")
            )

            final_score = (
                opinion_sentiment * 0.40
                + desc_score * 0.25
                + name_score * 0.15
                + spec_score * 0.12
                + category_score * 0.08
            )

            products_with_scores.append(
                {
                    "product": product,
                    "final_score": final_score,
                    "opinion_score": opinion_sentiment,
                    "desc_score": desc_score,
                    "name_score": name_score,
                    "spec_score": spec_score,
                    "category_score": category_score,
                    "opinion_count": len(opinion_scores),
                }
            )

        products_with_scores.sort(key=lambda x: x["final_score"], reverse=True)

        serializer = ProductSerializer(
            [item["product"] for item in products_with_scores], many=True
        )
        data = serializer.data

        for i, item in enumerate(products_with_scores):
            product = item["product"]

            data[i]["sentiment_score"] = round(item["final_score"], 3)
            data[i]["sentiment_breakdown"] = {
                "opinion_score": round(item["opinion_score"], 3),
                "description_score": round(item["desc_score"], 3),
                "name_score": round(item["name_score"], 3),
                "specification_score": round(item["spec_score"], 3),
                "category_score": round(item["category_score"], 3),
            }
            data[i]["total_opinions"] = item["opinion_count"]

            if hasattr(product, "sentiment_summary") and product.sentiment_summary:
                data[i]["positive_count"] = product.sentiment_summary.positive_count
                data[i]["negative_count"] = product.sentiment_summary.negative_count
                data[i]["neutral_count"] = product.sentiment_summary.neutral_count
            else:
                data[i]["positive_count"] = 0
                data[i]["negative_count"] = 0
                data[i]["neutral_count"] = 0

        return Response(data)


class SentimentAnalysisDebugAPI(APIView):
    """
    Debug endpoint to verify sentiment analysis formulas and calculations.
    Shows analysis from all sources: opinions, description, name, specifications, categories.
    No authentication required for transparency.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        from .custom_recommendation_engine import CustomSentimentAnalysis
        from .models import Opinion

        product_id = request.GET.get("product_id")

        if not product_id:
            return Response({"error": "product_id parameter required"}, status=400)

        try:
            product = Product.objects.prefetch_related(
                "opinion_set", "specification_set", "categories"
            ).get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": f"Product {product_id} not found"}, status=404)

        analyzer = CustomSentimentAnalysis()

        opinions = Opinion.objects.filter(product=product)[:5]
        opinion_details = []
        opinion_scores = []

        for opinion in opinions:
            score, category = analyzer.analyze_sentiment(opinion.content)
            opinion_scores.append(score)

            words = opinion.content.lower().split()
            positive_count = sum(1 for word in words if word in analyzer.positive_words)
            negative_count = sum(1 for word in words if word in analyzer.negative_words)
            total_words = len(words)

            opinion_details.append(
                {
                    "opinion_id": opinion.id,
                    "opinion_excerpt": (
                        opinion.content[:100] + "..."
                        if len(opinion.content) > 100
                        else opinion.content
                    ),
                    "calculation": {
                        "positive_words_found": positive_count,
                        "negative_words_found": negative_count,
                        "total_words": total_words,
                        "formula": f"({positive_count} - {negative_count}) / {total_words} = {score:.3f}",
                        "sentiment_score": round(score, 3),
                        "category": category,
                    },
                }
            )

        opinion_avg = (
            sum(opinion_scores) / len(opinion_scores) if opinion_scores else 0.0
        )

        desc_text = product.description or ""
        desc_score, desc_category = analyzer.analyze_sentiment(desc_text)
        desc_words = desc_text.lower().split()
        desc_positive = sum(1 for word in desc_words if word in analyzer.positive_words)
        desc_negative = sum(1 for word in desc_words if word in analyzer.negative_words)

        name_score, name_category = analyzer.analyze_sentiment(product.name)
        name_words = product.name.lower().split()
        name_positive = sum(1 for word in name_words if word in analyzer.positive_words)
        name_negative = sum(1 for word in name_words if word in analyzer.negative_words)

        spec_texts = []
        spec_details = []
        for spec in product.specification_set.all()[:10]:
            spec_text = f"{spec.parameter_name} {spec.specification}"
            spec_texts.append(spec_text)

            spec_score_item, spec_cat_item = analyzer.analyze_sentiment(spec_text)
            spec_words = spec_text.lower().split()
            spec_pos = sum(1 for word in spec_words if word in analyzer.positive_words)
            spec_neg = sum(1 for word in spec_words if word in analyzer.negative_words)

            spec_details.append(
                {
                    "parameter": spec.parameter_name,
                    "value": spec.specification,
                    "score": round(spec_score_item, 3),
                    "category": spec_cat_item,
                    "positive_words": spec_pos,
                    "negative_words": spec_neg,
                }
            )

        spec_combined = " ".join(spec_texts)
        spec_score, spec_category = (
            analyzer.analyze_sentiment(spec_combined)
            if spec_combined
            else (0.0, "neutral")
        )

        category_names = " ".join([cat.name for cat in product.categories.all()])
        category_score, category_cat = (
            analyzer.analyze_sentiment(category_names)
            if category_names
            else (0.0, "neutral")
        )
        cat_words = category_names.lower().split()
        cat_positive = sum(1 for word in cat_words if word in analyzer.positive_words)
        cat_negative = sum(1 for word in cat_words if word in analyzer.negative_words)

        final_score = (
            opinion_avg * 0.40
            + desc_score * 0.25
            + name_score * 0.15
            + spec_score * 0.12
            + category_score * 0.08
        )

        return Response(
            {
                "product_id": product_id,
                "product_name": product.name,
                "multi_source_analysis": {
                    "opinions": {
                        "weight": "40%",
                        "count": len(opinion_scores),
                        "average_score": round(opinion_avg, 3),
                        "contribution_to_final": round(opinion_avg * 0.40, 3),
                        "sample_details": opinion_details,
                        "formula": f"Σ({len(opinion_scores)} scores) / {len(opinion_scores)} = {opinion_avg:.3f}",
                    },
                    "description": {
                        "weight": "25%",
                        "text_excerpt": (
                            desc_text[:150] + "..."
                            if len(desc_text) > 150
                            else desc_text
                        ),
                        "score": round(desc_score, 3),
                        "category": desc_category,
                        "contribution_to_final": round(desc_score * 0.25, 3),
                        "positive_words": desc_positive,
                        "negative_words": desc_negative,
                        "total_words": len(desc_words),
                        "formula": f"({desc_positive} - {desc_negative}) / {len(desc_words)} = {desc_score:.3f}",
                    },
                    "name": {
                        "weight": "15%",
                        "text": product.name,
                        "score": round(name_score, 3),
                        "category": name_category,
                        "contribution_to_final": round(name_score * 0.15, 3),
                        "positive_words": name_positive,
                        "negative_words": name_negative,
                        "total_words": len(name_words),
                        "formula": f"({name_positive} - {name_negative}) / {len(name_words)} = {name_score:.3f}",
                    },
                    "specifications": {
                        "weight": "12%",
                        "count": len(spec_details),
                        "combined_score": round(spec_score, 3),
                        "category": spec_category,
                        "contribution_to_final": round(spec_score * 0.12, 3),
                        "sample_details": spec_details[:5],
                    },
                    "categories": {
                        "weight": "8%",
                        "text": category_names,
                        "score": round(category_score, 3),
                        "category": category_cat,
                        "contribution_to_final": round(category_score * 0.08, 3),
                        "positive_words": cat_positive,
                        "negative_words": cat_negative,
                        "total_words": len(cat_words) if cat_words else 0,
                    },
                },
                "final_calculation": {
                    "formula": "Final = (Opinion×0.40) + (Desc×0.25) + (Name×0.15) + (Spec×0.12) + (Cat×0.08)",
                    "calculation": f"({opinion_avg:.3f}×0.40) + ({desc_score:.3f}×0.25) + ({name_score:.3f}×0.15) + ({spec_score:.3f}×0.12) + ({category_score:.3f}×0.08)",
                    "final_score": round(final_score, 3),
                    "final_category": (
                        "Positive"
                        if final_score > 0.1
                        else "Negative" if final_score < -0.1 else "Neutral"
                    ),
                    "breakdown": {
                        "from_opinions": round(opinion_avg * 0.40, 3),
                        "from_description": round(desc_score * 0.25, 3),
                        "from_name": round(name_score * 0.15, 3),
                        "from_specifications": round(spec_score * 0.12, 3),
                        "from_categories": round(category_score * 0.08, 3),
                    },
                },
                "formulas_used": {
                    "per_text": "Sentiment_Score = (Positive_Count - Negative_Count) / Total_Words",
                    "final_aggregation": "Final = (Opinion×0.40) + (Description×0.25) + (Name×0.15) + (Specification×0.12) + (Category×0.08)",
                    "thresholds": "Positive: score > 0.1, Negative: score < -0.1, Neutral: -0.1 ≤ score ≤ 0.1",
                },
                "lexicon_info": {
                    "positive_words_count": len(analyzer.positive_words),
                    "negative_words_count": len(analyzer.negative_words),
                    "examples_positive": list(analyzer.positive_words)[:10],
                    "examples_negative": list(analyzer.negative_words)[:10],
                },
                "source": "Liu, B. (2012). Sentiment Analysis and Opinion Mining, Morgan & Claypool Publishers, Chapter 2: Sentiment Lexicons",
            }
        )


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

            products_query = Product.objects.select_related(
                "sentiment_summary"
            ).prefetch_related(
                "categories", "photoproduct_set", "specification_set", "tags"
            )

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
                        abs(
                            0.5
                            - abs(
                                float(product.sentiment_summary.average_sentiment_score)
                            )
                        )
                        * 2
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
        """
        Enhanced fuzzy search using CustomFuzzySearch with advanced algorithms:

        Algorithms implemented in CustomFuzzySearch (custom_recommendation_engine.py):
        1. Levenshtein Distance - O(n*m) space-optimized character-level similarity
        2. Trigram Similarity - N-gram matching for spelling error tolerance
        3. Word-level Similarity - Exact + partial word matching with context
        4. Chunked Processing - Sliding window for long texts (150 chars + 30 overlap)

        Field Weights (from CustomFuzzySearch):
        - Name: 45%
        - Description: 25%
        - Category: 20%
        - Specifications: 10%
        """
        fuzzy_engine = CustomFuzzySearch()

        results = fuzzy_engine.search_products(query, products, threshold)

        if not results and products:
            test_results = fuzzy_engine.search_products(query, products[:10], 0.1)
            if test_results:
                print(f"   [DEBUG] Found {len(test_results)} with threshold=0.1")
                print(f"   [DEBUG] Top score: {test_results[0]['score']:.3f}")
                print(f"   [DEBUG] Your threshold {threshold} might be too high!")

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

class SentimentAnalysisDebugView(APIView):
    """
    Debug view for Sentiment Analysis system.
    Returns statistics and top products by sentiment.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            all_sentiments = SentimentAnalysis.objects.all()
            total_sentiments = all_sentiments.count()

            positive_count = all_sentiments.filter(sentiment_category="positive").count()
            negative_count = all_sentiments.filter(sentiment_category="negative").count()
            neutral_count = all_sentiments.filter(sentiment_category="neutral").count()

            positive_percentage = (
                round((positive_count / total_sentiments) * 100, 2)
                if total_sentiments > 0
                else 0
            )
            negative_percentage = (
                round((negative_count / total_sentiments) * 100, 2)
                if total_sentiments > 0
                else 0
            )
            neutral_percentage = (
                round((neutral_count / total_sentiments) * 100, 2)
                if total_sentiments > 0
                else 0
            )

            top_positive_data = []
            try:
                top_positive = (
                    ProductSentimentSummary.objects.filter(average_sentiment__gt=0)
                    .select_related("product")
                    .order_by("-average_sentiment")[:10]
                )

                for summary in top_positive:
                    try:
                        product = summary.product
                        review_count = getattr(summary, 'total_opinions', 0)
                        if not review_count:
                            review_count = product.opinion_set.count()
                        
                        top_positive_data.append({
                            "product_name": product.name,
                            "product_id": product.id,
                            "avg_sentiment": float(summary.average_sentiment),
                            "review_count": review_count,
                        })
                    except Exception:
                        continue
            except Exception:
                pass

            top_negative_data = []
            try:
                top_negative = (
                    ProductSentimentSummary.objects.filter(average_sentiment__lt=0)
                    .select_related("product")
                    .order_by("average_sentiment")[:10]
                )

                for summary in top_negative:
                    try:
                        product = summary.product
                        review_count = getattr(summary, 'total_opinions', 0)
                        if not review_count:
                            review_count = product.opinion_set.count()
                        
                        top_negative_data.append({
                            "product_name": product.name,
                            "product_id": product.id,
                            "avg_sentiment": float(summary.average_sentiment),
                            "review_count": review_count,
                        })
                    except Exception:
                        continue
            except Exception:
                pass

            return Response({
                "total_sentiments": total_sentiments,
                "positive_count": positive_count,
                "positive_percentage": positive_percentage,
                "negative_count": negative_count,
                "negative_percentage": negative_percentage,
                "neutral_count": neutral_count,
                "neutral_percentage": neutral_percentage,
                "top_positive": top_positive_data,
                "top_negative": top_negative_data,
            })

        except Exception as e:
            return Response({
                "total_sentiments": 0,
                "positive_count": 0,
                "positive_percentage": 0,
                "negative_count": 0,
                "negative_percentage": 0,
                "neutral_count": 0,
                "neutral_percentage": 0,
                "top_positive": [],
                "top_negative": [],
                "error_message": str(e)
            })
        
class FuzzyLogicRecommendationsAPIView(APIView):
    """
    Implements true fuzzy logic system with:
    - 1: Fuzzy Membership Functions (price, quality, popularity)
    - 2: Fuzzy User Profiling (category interests, price sensitivity)
    - 3: Simplified Fuzzy Inference Engine (Mamdani-style)

    Based on:
    - Zadeh, L. A. (1965). "Fuzzy sets". Information and Control.
    - Mamdani, E. H. (1975). "Application of fuzzy algorithms for control of simple dynamic plant"
    """

    def get(self, request):
        """
        Get fuzzy logic recommendations for the user.

        Query params:
        - limit: number of recommendations (default: 10)
        - debug: if 'true', returns detailed rule activations
        """
        from home.fuzzy_logic_engine import (
            FuzzyMembershipFunctions,
            FuzzyUserProfile,
            SimpleFuzzyInference,
        )

        limit = int(request.GET.get("limit", 10))
        debug_mode = request.GET.get("debug", "false").lower() == "true"

        cache_key = f"fuzzy_recommendations_{request.user.id if request.user.is_authenticated else 'guest'}_{limit}"

        if not debug_mode:
            cached_result = cache.get(cache_key)
            if cached_result:
                return Response({**cached_result, "cached": True})

        try:
            membership_functions = FuzzyMembershipFunctions()

            if request.user.is_authenticated:
                user_profile = FuzzyUserProfile(user=request.user)
            else:
                session_data = request.session.get("user_activity", {})
                user_profile = FuzzyUserProfile(session_data=session_data)

            fuzzy_engine = SimpleFuzzyInference(membership_functions, user_profile)

            products_query = Product.objects.all().annotate(
                review_count=Count("opinion"),
                avg_rating=Avg("opinion__rating"),
                order_count=Count("orderproduct", distinct=True)
            )

            products = list(products_query[:500])

            if not products:
                return Response(
                    {
                        "recommendations": [],
                        "message": "No products available",
                        "user_profile": user_profile.get_profile_summary(),
                    }
                )

            scored_products = []

            for product in products:
                product_categories = [cat.name for cat in product.categories.all()]

                category_match = 0.0
                for cat in product_categories:
                    match = user_profile.fuzzy_category_match(cat)
                    category_match = max(category_match, match)

                product_data = {
                    "price": float(product.price),
                    "rating": float(product.avg_rating) if product.avg_rating else 3.0,
                    "view_count": product.order_count if hasattr(product, "order_count") else 0,
                }

                fuzzy_result = fuzzy_engine.evaluate_product(
                    product_data, category_match
                )

                scored_products.append(
                    {
                        "product": product,
                        "fuzzy_score": fuzzy_result["fuzzy_score"],
                        "rule_activations": (
                            fuzzy_result["rule_activations"] if debug_mode else None
                        ),
                        "category_match": fuzzy_result["category_match"],
                    }
                )

            scored_products.sort(key=lambda x: x["fuzzy_score"], reverse=True)

            top_products = scored_products[:limit]

            recommendations = []
            for item in top_products:
                product_data = ProductSerializer(item["product"]).data

                rec = {
                    "product": product_data,
                    "fuzzy_score": item["fuzzy_score"],
                    "category_match": item["category_match"],
                }

                if debug_mode:
                    rec["rule_activations"] = item["rule_activations"]

                recommendations.append(rec)

            result = {
                "recommendations": recommendations,
                "total_evaluated": len(products),
                "user_profile": user_profile.get_profile_summary(),
                "fuzzy_system": {
                    "implementation": "VARIANT B+: Membership Functions + User Profile + Mamdani Inference",
                    "components": [
                        "OPTION 1: Fuzzy Membership Functions (triangular/trapezoidal)",
                        "OPTION 3: Fuzzy User Profiling (category interests, price sensitivity)",
                        "OPTION 4-lite: Simplified Mamdani Inference (5 rules, T-norms, weighted defuzzification)",
                    ],
                    "references": [
                        "Zadeh, L. A. (1965). Fuzzy sets. Information and Control.",
                        "Mamdani, E. H. (1975). Application of fuzzy algorithms for control of simple dynamic plant.",
                    ],
                },
                "cached": False,
            }

            if debug_mode:
                result["rule_explanations"] = fuzzy_engine.get_rule_explanations()

            if not debug_mode:
                cache.set(cache_key, result, timeout=3600)

            return Response(result)

        except Exception as e:
            print(f"Error in fuzzy logic recommendations: {e}")
            import traceback

            traceback.print_exc()

            return Response(
                {
                    "error": str(e),
                    "message": "Error generating fuzzy logic recommendations",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
