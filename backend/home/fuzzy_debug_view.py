from rest_framework.views import APIView
from rest_framework.response import Response


class FuzzyLogicDebugView(APIView):
    """
    Debug endpoint dla Fuzzy Logic - pokazuje funkcje przynależności,
    profil użytkownika, aktywacje reguł i defuzzyfikację
    """

    permission_classes = []

    def get(self, request):
        try:
            from home.fuzzy_logic_engine import (
                FuzzyMembershipFunctions,
                FuzzyUserProfile,
                SimpleFuzzyInference,
            )
            from home.models import Product

            product_id = request.GET.get("product_id")
            user_id = request.GET.get("user_id")

            mf = FuzzyMembershipFunctions()

            user = None
            if user_id:
                from django.contrib.auth import get_user_model

                User = get_user_model()
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    user = None

            user_profile = FuzzyUserProfile(user=user)
            profile_summary = user_profile.get_profile_summary()

            inference = SimpleFuzzyInference(mf, user_profile)

            response_data = {
                "algorithm": "Fuzzy Logic Inference System (Mamdani-style)",
                "description": "System rekomendacji oparty na logice rozmytej z uproszczoną defuzzyfikacją",
            }

            response_data["membership_functions"] = {
                "price": {
                    "cheap": {
                        "range": f"[0, {mf.price_low}] → [{mf.price_low}, {mf.price_mid_low}]",
                        "description": f"μ = 1.0 dla ceny ≤ {mf.price_low} PLN, spada do 0 przy {mf.price_mid_low} PLN",
                    },
                    "medium": {
                        "range": f"[300, 500] → [500, 1200] → [1200, 1500]",
                        "description": "Trapezoidalna: wzrost 300-500, plateau 500-1200, spadek 1200-1500",
                    },
                    "expensive": {
                        "range": f"[1000, {mf.price_high}] → [{mf.price_high}, ∞]",
                        "description": f"μ = 0 dla ceny ≤ 1000 PLN, wzrasta do 1.0 przy {mf.price_high} PLN",
                    },
                },
                "quality": {
                    "low": {
                        "range": f"[0, {mf.rating_low}] → [{mf.rating_low}, {mf.rating_mid}]",
                        "description": f"μ = 1.0 dla ratingu ≤ {mf.rating_low}, spada do 0 przy {mf.rating_mid}",
                    },
                    "medium": {
                        "range": f"[{mf.rating_low}, {mf.rating_mid}, {mf.rating_high}]",
                        "description": f"Triangular centered at {mf.rating_mid}",
                    },
                    "high": {
                        "range": f"[{mf.rating_mid}, {mf.rating_high}] → [{mf.rating_high}, 5.0]",
                        "description": f"μ = 0 dla ratingu < {mf.rating_mid}, wzrasta do 1.0 przy {mf.rating_high}",
                    },
                },
                "popularity": {
                    "low": {
                        "range": f"[0, {mf.pop_low}] → [{mf.pop_low}, {mf.pop_mid}]",
                        "description": f"μ = 1.0 dla wyświetleń ≤ {mf.pop_low}, spada do 0 przy {mf.pop_mid}",
                    },
                    "medium": {
                        "range": f"[{mf.pop_low}, {mf.pop_mid}] → [{mf.pop_mid}, {mf.pop_high}]",
                        "description": f"Trapezoidalna: plateau {mf.pop_low}-{mf.pop_mid}, spadek do {mf.pop_high}",
                    },
                    "high": {
                        "range": f"[{mf.pop_mid}, {mf.pop_high}] → [{mf.pop_high}, ∞]",
                        "description": f"μ = 0 dla wyświetleń < {mf.pop_mid}, wzrasta do 1.0 przy {mf.pop_high}",
                    },
                },
            }

            response_data["user_profile"] = {
                "user_id": user.id if user else None,
                "username": user.username if user else "Guest/Default",
                "profile_type": profile_summary["profile_type"],
                "price_sensitivity": round(user_profile.price_sensitivity, 3),
                "price_sensitivity_label": (
                    "Very High (Budget-conscious)"
                    if user_profile.price_sensitivity > 0.8
                    else (
                        "High"
                        if user_profile.price_sensitivity > 0.6
                        else (
                            "Medium"
                            if user_profile.price_sensitivity > 0.4
                            else (
                                "Low"
                                if user_profile.price_sensitivity > 0.2
                                else "Very Low (Premium buyer)"
                            )
                        )
                    )
                ),
                "category_interests": {
                    cat: round(interest, 3)
                    for cat, interest in profile_summary["top_interests"]
                },
                "total_categories_tracked": len(user_profile.category_interests),
            }

            rule_explanations = inference.get_rule_explanations()
            response_data["fuzzy_rules"] = [
                {
                    "name": rule["rule"],
                    "condition": rule["condition"],
                    "consequence": rule["consequence"],
                    "interpretation": rule["interpretation"],
                }
                for rule in rule_explanations
            ]

            if product_id:
                try:
                    from django.db.models import Avg, Count

                    product = (
                        Product.objects.prefetch_related("categories", "tags")
                        .annotate(
                            avg_rating=Avg("opinion__rating"),
                            order_count=Count("orderproduct", distinct=True),
                        )
                        .get(id=product_id)
                    )

                    product_data = {
                        "price": float(product.price),
                        "rating": (
                            float(product.avg_rating) if product.avg_rating else 0.0
                        ),
                        "view_count": product.order_count,
                    }

                    price_fuzzy = mf.get_price_fuzzy_set(product_data["price"])
                    quality_fuzzy = mf.get_quality_fuzzy_set(product_data["rating"])
                    popularity_fuzzy = mf.get_popularity_fuzzy_set(
                        product_data["view_count"]
                    )

                    product_categories = [cat.name for cat in product.categories.all()]
                    category_matches = {}
                    max_category_match = 0.0

                    for cat in product_categories:
                        match = user_profile.fuzzy_category_match(cat)
                        category_matches[cat] = round(match, 3)
                        max_category_match = max(max_category_match, match)

                    evaluation = inference.evaluate_product(
                        product_data, max_category_match
                    )

                    response_data["selected_product"] = {
                        "id": product.id,
                        "name": product.name,
                        "price": product_data["price"],
                        "rating": round(product_data["rating"], 2),
                        "view_count": product_data["view_count"],
                        "categories": product_categories,
                        "tags": [tag.name for tag in product.tags.all()],
                    }

                    response_data["fuzzification"] = {
                        "price": {
                            "value": product_data["price"],
                            "cheap": round(price_fuzzy["cheap"], 3),
                            "medium": round(price_fuzzy["medium"], 3),
                            "expensive": round(price_fuzzy["expensive"], 3),
                            "dominant": max(price_fuzzy, key=price_fuzzy.get),
                        },
                        "quality": {
                            "value": product_data["rating"],
                            "low": round(quality_fuzzy["low"], 3),
                            "medium": round(quality_fuzzy["medium"], 3),
                            "high": round(quality_fuzzy["high"], 3),
                            "dominant": max(quality_fuzzy, key=quality_fuzzy.get),
                        },
                        "popularity": {
                            "value": product_data["view_count"],
                            "low": round(popularity_fuzzy["low"], 3),
                            "medium": round(popularity_fuzzy["medium"], 3),
                            "high": round(popularity_fuzzy["high"], 3),
                            "dominant": max(popularity_fuzzy, key=popularity_fuzzy.get),
                        },
                    }

                    response_data["category_matching"] = {
                        "max_match": round(max_category_match, 3),
                        "category_details": category_matches,
                        "explanation": (
                            f"Najlepsza zgodność kategorii: {round(max_category_match * 100, 1)}%. "
                            f"Obliczona na podstawie hierarchii kategorii i zainteresowań użytkownika."
                        ),
                    }

                    response_data["inference"] = {
                        "rule_activations": evaluation["rule_activations"],
                        "final_fuzzy_score": evaluation["fuzzy_score"],
                        "final_percentage": round(evaluation["fuzzy_score"] * 100, 1),
                        "defuzzification_method": "Weighted Average",
                        "calculation": {
                            "description": "Defuzzyfikacja: weighted_sum / weight_sum",
                            "weighted_sum": round(
                                sum(
                                    activation * inference.rules[idx]["weight"]
                                    for idx, activation in enumerate(
                                        evaluation["rule_activations"].values()
                                    )
                                ),
                                4,
                            ),
                            "weight_sum": round(
                                sum(rule["weight"] for rule in inference.rules), 4
                            ),
                        },
                    }

                except Product.DoesNotExist:
                    response_data["error"] = f"Product with ID {product_id} not found"

            else:
                from django.db.models import Avg, Count

                products = (
                    Product.objects.prefetch_related("categories", "tags")
                    .annotate(
                        avg_rating=Avg("opinion__rating"),
                        order_count=Count("orderproduct", distinct=True),
                    )
                    .all()[:20]
                )

                product_scores = []
                for prod in products:
                    product_data = {
                        "price": float(prod.price),
                        "rating": float(prod.avg_rating) if prod.avg_rating else 0.0,
                        "view_count": prod.order_count,
                    }

                    product_categories = [cat.name for cat in prod.categories.all()]
                    max_category_match = 0.0
                    for cat in product_categories:
                        match = user_profile.fuzzy_category_match(cat)
                        max_category_match = max(max_category_match, match)

                    evaluation = inference.evaluate_product(
                        product_data, max_category_match
                    )

                    product_scores.append(
                        {
                            "id": prod.id,
                            "name": prod.name,
                            "price": product_data["price"],
                            "rating": round(product_data["rating"], 2),
                            "fuzzy_score": evaluation["fuzzy_score"],
                            "fuzzy_percentage": round(
                                evaluation["fuzzy_score"] * 100, 1
                            ),
                            "category_match": round(max_category_match, 3),
                            "categories": product_categories[:3],
                        }
                    )

                product_scores.sort(key=lambda x: x["fuzzy_score"], reverse=True)

                response_data["top_products"] = {
                    "count": min(10, len(product_scores)),
                    "products": product_scores[:10],
                    "description": "Top 10 produktów według fuzzy score dla wybranego profilu użytkownika",
                }

            total_products = Product.objects.count()
            response_data["system_stats"] = {
                "total_products": total_products,
                "total_rules": len(inference.rules),
                "membership_function_types": "Triangular & Trapezoidal",
                "defuzzification_method": "Weighted Average (Simplified Mamdani)",
            }

            return Response(response_data)

        except Exception as e:
            import traceback

            return Response(
                {
                    "status": "error",
                    "message": str(e),
                    "traceback": traceback.format_exc(),
                },
                status=500,
            )
