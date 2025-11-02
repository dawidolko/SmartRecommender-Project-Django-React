"""
Fuzzy Logic Recommendation System Debug API.

This module provides a comprehensive debugging interface for the fuzzy logic
recommendation engine. It exposes membership functions, user profiles, rule
activations, and defuzzification details for analysis and optimization.

Fuzzy Logic Overview:
====================
Fuzzy logic allows reasoning with imprecise or vague information using
membership functions that assign degrees of truth (0.0 to 1.0) instead of
binary true/false values.

System Architecture:
===================
1. Fuzzification: Convert crisp values to fuzzy sets
   - Price: 599 PLN → {cheap: 0.2, medium: 0.7, expensive: 0.1}
   - Rating: 4.3 stars → {low: 0.0, medium: 0.3, high: 0.7}
   
2. Inference: Apply fuzzy rules to fuzzy sets
   - IF price is cheap AND quality is high THEN recommendation is strong
   - Calculate rule activation (min of antecedents)
   
3. Defuzzification: Convert fuzzy output to crisp score
   - Weighted average of rule activations
   - Final score: 0.0 to 1.0

Mathematical Formulas:
=====================
1. Triangular Membership Function:
   μ(x) = max(0, min((x - a)/(b - a), (c - x)/(c - b)))
   where a = left base, b = peak, c = right base

2. Trapezoidal Membership Function:
   μ(x) = max(0, min((x - a)/(b - a), 1, (d - x)/(d - c)))
   where a, b = left edge, c, d = right edge

3. Rule Activation (Mamdani):
   activation = min(μ₁, μ₂, ..., μₙ)
   where μᵢ are membership degrees of antecedents

4. Defuzzification (Weighted Average):
   score = Σ(activation_i × weight_i) / Σ(weight_i)

Endpoint Usage:
==============
GET /api/fuzzy-logic-debug/
Query Parameters:
    - product_id (optional): Analyze specific product
    - user_id (optional): Use specific user's profile

Response Structure:
==================
{
    "algorithm": "Fuzzy Logic Inference System (Mamdani-style)",
    "membership_functions": {
        "price": {"cheap": {...}, "medium": {...}, "expensive": {...}},
        "quality": {"low": {...}, "medium": {...}, "high": {...}},
        "popularity": {...}
    },
    "user_profile": {
        "price_sensitivity": 0.75,
        "category_interests": {"Electronics": 0.9, "Books": 0.3}
    },
    "fuzzy_rules": [
        {
            "name": "Rule 1",
            "condition": "IF price is cheap AND quality is high",
            "consequence": "THEN recommendation is strong"
        }
    ],
    "fuzzification": {
        "price": {"cheap": 0.2, "medium": 0.7, "expensive": 0.1}
    },
    "inference": {
        "rule_activations": {"Rule1": 0.65, "Rule2": 0.23},
        "final_fuzzy_score": 0.78
    }
}

Use Cases:
==========
- Algorithm tuning: Adjust membership function parameters
- Rule optimization: Identify which rules fire most often
- User profiling: Understand user preferences in fuzzy terms
- Product analysis: See how products score across dimensions

Authors: Dawid Olko & Piotr Smoła
Date: 2025-11-02
Version: 2.0
"""

from rest_framework.views import APIView
from rest_framework.response import Response


class FuzzyLogicDebugView(APIView):
    """
    API endpoint for fuzzy logic recommendation system debugging.
    
    Endpoint: GET /api/fuzzy-logic-debug/?product_id=123&user_id=456
    Permission: AllowAny (public access for debugging)
    
    Query Parameters:
        product_id (int, optional): Specific product to analyze
        user_id (int, optional): User whose profile to use
    
    Response Sections:
        1. membership_functions: Fuzzy set definitions for price/quality/popularity
        2. user_profile: User's fuzzy profile (price sensitivity, interests)
        3. fuzzy_rules: All inference rules with conditions and consequences
        4. selected_product: Product details (if product_id provided)
        5. fuzzification: Crisp values → fuzzy sets conversion
        6. category_matching: User interest in product categories
        7. inference: Rule activations and final score calculation
        8. top_products: Top 10 recommendations (if no product_id)
        9. system_stats: General system statistics
    
    Fuzzy Variables:
        Price (PLN):
            - cheap: [0, 300] → [300, 500]
            - medium: [300, 500] → [500, 1200] → [1200, 1500]
            - expensive: [1000, 2000] → [2000, ∞]
        
        Quality (rating 0-5):
            - low: [0, 2.0] → [2.0, 3.0]
            - medium: [2.0, 3.0, 4.0]
            - high: [3.0, 4.0] → [4.0, 5.0]
        
        Popularity (view count):
            - low: [0, 10] → [10, 50]
            - medium: [10, 50] → [50, 200]
            - high: [50, 200] → [200, ∞]
    
    Example Fuzzy Rules:
        Rule 1: IF price is cheap AND quality is high 
                THEN recommendation is very_strong (weight: 1.0)
        
        Rule 2: IF price is medium AND quality is medium 
                THEN recommendation is moderate (weight: 0.6)
        
        Rule 3: IF price is expensive AND quality is low 
                THEN recommendation is very_weak (weight: 0.1)
    
    Defuzzification:
        Uses weighted average method:
        
        final_score = Σ(activation_i × weight_i) / Σ(weight_i)
        
        Example:
            Rule1: activation=0.7, weight=1.0 → contribution = 0.7
            Rule2: activation=0.3, weight=0.6 → contribution = 0.18
            Rule3: activation=0.0, weight=0.1 → contribution = 0.0
            
            final_score = (0.7 + 0.18 + 0.0) / (1.0 + 0.6 + 0.1) = 0.518
    
    Performance:
        - No caching (debug endpoint)
        - Analyzes up to 20 products without product_id
        - Single product analysis with product_id (faster)
    """
    permission_classes = []  # AllowAny for debugging

    def get(self, request):
        """
        Debug fuzzy logic recommendation system with detailed insights.
        
        Args:
            request: HTTP GET request with optional query params
        
        Returns:
            Response: Comprehensive fuzzy logic analysis
        
        Query Examples:
            1. General system overview:
               GET /api/fuzzy-logic-debug/
            
            2. Analyze specific product:
               GET /api/fuzzy-logic-debug/?product_id=42
            
            3. Use specific user's profile:
               GET /api/fuzzy-logic-debug/?user_id=123&product_id=42
        """
        try:
            # Import fuzzy logic engine components
            from home.fuzzy_logic_engine import (
                FuzzyMembershipFunctions,
                FuzzyUserProfile,
                SimpleFuzzyInference,
            )
            from home.models import Product

            # Extract query parameters
            product_id = request.GET.get("product_id")
            user_id = request.GET.get("user_id")

            # Initialize membership function definitions
            mf = FuzzyMembershipFunctions()

            # Load user profile (or use default guest profile)
            user = None
            if user_id:
                from django.contrib.auth import get_user_model

                User = get_user_model()
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    user = None

            # Create fuzzy user profile with preference modeling
            user_profile = FuzzyUserProfile(user=user)
            profile_summary = user_profile.get_profile_summary()

            # Initialize fuzzy inference engine
            inference = SimpleFuzzyInference(mf, user_profile)

            # Build response with algorithm description
            response_data = {
                "algorithm": "Fuzzy Logic Inference System (Mamdani-style)",
                "description": "System rekomendacji oparty na logice rozmytej z uproszczoną defuzzyfikacją",
            }

            # Section 1: Membership Function Definitions
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

            # Section 2: User Profile (fuzzy representation of user preferences)
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

            # Section 3: Fuzzy Rules (IF-THEN rules for inference)
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

            # Section 4-7: Product-Specific Analysis (if product_id provided)
            if product_id:
                try:
                    from django.db.models import Avg, Count

                    # Fetch product with aggregated ratings and order count
                    product = (
                        Product.objects.prefetch_related("categories", "tags")
                        .annotate(
                            avg_rating=Avg("opinion__rating"),
                            order_count=Count("orderproduct", distinct=True),
                        )
                        .get(id=product_id)
                    )

                    # Prepare crisp product data for fuzzification
                    product_data = {
                        "price": float(product.price),
                        "rating": (
                            float(product.avg_rating) if product.avg_rating else 0.0
                        ),
                        "view_count": product.order_count,
                    }

                    # Fuzzification: Convert crisp values to fuzzy sets
                    price_fuzzy = mf.get_price_fuzzy_set(product_data["price"])
                    quality_fuzzy = mf.get_quality_fuzzy_set(product_data["rating"])
                    popularity_fuzzy = mf.get_popularity_fuzzy_set(
                        product_data["view_count"]
                    )

                    # Category matching: Calculate user interest in product categories
                    product_categories = [cat.name for cat in product.categories.all()]
                    category_matches = {}
                    max_category_match = 0.0

                    for cat in product_categories:
                        match = user_profile.fuzzy_category_match(cat)
                        category_matches[cat] = round(match, 3)
                        max_category_match = max(max_category_match, match)

                    # Inference: Apply fuzzy rules and calculate final score
                    evaluation = inference.evaluate_product(
                        product_data, max_category_match
                    )

                    # Section 4: Selected Product Details
                    response_data["selected_product"] = {
                        "id": product.id,
                        "name": product.name,
                        "price": product_data["price"],
                        "rating": round(product_data["rating"], 2),
                        "view_count": product_data["view_count"],
                        "categories": product_categories,
                        "tags": [tag.name for tag in product.tags.all()],
                    }

                    # Section 5: Fuzzification Results
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

                    # Section 6: Category Matching Details
                    response_data["category_matching"] = {
                        "max_match": round(max_category_match, 3),
                        "category_details": category_matches,
                        "explanation": (
                            f"Najlepsza zgodność kategorii: {round(max_category_match * 100, 1)}%. "
                            f"Obliczona na podstawie hierarchii kategorii i zainteresowań użytkownika."
                        ),
                    }

                    # Section 7: Inference Results (rule activations + defuzzification)
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

            # Section 8: Top Products (if no product_id specified)
            else:
                from django.db.models import Avg, Count

                # Fetch first 20 products for analysis
                products = (
                    Product.objects.prefetch_related("categories", "tags")
                    .annotate(
                        avg_rating=Avg("opinion__rating"),
                        order_count=Count("orderproduct", distinct=True),
                    )
                    .all()[:20]
                )

                # Calculate fuzzy score for each product
                product_scores = []
                for prod in products:
                    product_data = {
                        "price": float(prod.price),
                        "rating": float(prod.avg_rating) if prod.avg_rating else 0.0,
                        "view_count": prod.order_count,
                    }

                    # Calculate category matching
                    product_categories = [cat.name for cat in prod.categories.all()]
                    max_category_match = 0.0
                    for cat in product_categories:
                        match = user_profile.fuzzy_category_match(cat)
                        max_category_match = max(max_category_match, match)

                    # Evaluate product with fuzzy inference
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

                # Sort by fuzzy score (best recommendations first)
                product_scores.sort(key=lambda x: x["fuzzy_score"], reverse=True)

                response_data["top_products"] = {
                    "count": min(10, len(product_scores)),
                    "products": product_scores[:10],
                    "description": "Top 10 produktów według fuzzy score dla wybranego profilu użytkownika",
                }

            # Section 9: System Statistics
            total_products = Product.objects.count()
            response_data["system_stats"] = {
                "total_products": total_products,
                "total_rules": len(inference.rules),
                "membership_function_types": "Triangular & Trapezoidal",
                "defuzzification_method": "Weighted Average (Simplified Mamdani)",
            }

            return Response(response_data)

        except Exception as e:
            # Error handling with traceback for debugging
            import traceback

            return Response(
                {
                    "status": "error",
                    "message": str(e),
                    "traceback": traceback.format_exc(),
                },
                status=500,
            )
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
