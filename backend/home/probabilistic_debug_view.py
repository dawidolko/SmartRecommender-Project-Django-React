"""
Probabilistic Recommendation Models Debug API.

This module provides comprehensive debugging for probabilistic recommendation
algorithms including Markov Chains and Naive Bayes classifiers.

Probabilistic Models Overview:
==============================

1. Markov Chain (Next Purchase Prediction)
   - First-order Markov model: P(state_t | state_t-1)
   - Predicts next product category based on last purchase
   - Example: After buying "Laptop", 65% chance next is "Accessories"

2. Naive Bayes (Purchase Probability)
   - Classifies users as "will_purchase" or "will_not_purchase"
   - Features: total_orders, avg_order_value, days_since_last_order
   - Uses Bayes theorem with independence assumption

3. Naive Bayes (Churn Prediction)
   - Classifies users as "will_churn" or "will_not_churn"
   - Same features as purchase prediction
   - Churn defined as: no purchase in 60+ days

Mathematical Formulas:
=====================

1. Markov Chain Transition Probability:
   P(S_t = j | S_t-1 = i) = count(i → j) / Σ_k count(i → k)
   
   Example:
   User bought: Laptop → Mouse → Keyboard → Mouse
   Transitions: Laptop→Mouse(1), Mouse→Keyboard(1), Keyboard→Mouse(1)
   P(Mouse | Laptop) = 1/1 = 1.0
   P(Keyboard | Mouse) = 1/2 = 0.5
   P(Mouse | Keyboard) = 1/1 = 1.0

2. Naive Bayes Classification:
   P(class | features) = P(features | class) × P(class) / P(features)
   
   With independence assumption:
   P(features | class) = Π P(feature_i | class)
   
   Example:
   Features: {total_orders: 5, avg_order_value: 250, days_since_last: 10}
   P(will_purchase | features) = 
       P(orders=5 | will_purchase) × 
       P(avg=250 | will_purchase) × 
       P(days=10 | will_purchase) × 
       P(will_purchase) / P(features)

3. Prior Probability:
   P(class) = count(class) / total_samples
   
   Example:
   Active buyers: 75 users
   Inactive buyers: 25 users
   P(will_purchase) = 75/100 = 0.75
   P(will_not_purchase) = 25/100 = 0.25

Endpoint Usage:
==============
GET /api/probabilistic-debug/
Query Parameters:
    - user_id (optional): Analyze specific user's probabilities
    - product_id (optional): Analyze product category transitions

Response Structure:
==================
{
    "algorithm": "Probabilistic Models (Markov Chain + Naive Bayes)",
    "markov_chain": {
        "total_states": 15,
        "total_transitions": 234,
        "order": 1,
        "top_transitions": [
            {"from": "Laptop", "to": "Mouse", "probability": 0.65, "count": 13}
        ]
    },
    "naive_bayes_purchase": {
        "trained": true,
        "class_priors": {"will_purchase": 0.75, "will_not_purchase": 0.25}
    },
    "naive_bayes_churn": {
        "trained": true,
        "class_priors": {"will_churn": 0.30, "will_not_churn": 0.70}
    },
    "user_analysis": {
        "purchase_probability": {"active_buyer": 0.82, "inactive": 0.18},
        "churn_probability": {"will_churn": 0.15, "will_stay": 0.85}
    }
}

Use Cases:
==========
- Next purchase prediction: "After buying X, recommend Y"
- Churn prevention: Identify users likely to stop buying
- Marketing campaigns: Target users with high purchase probability
- Inventory management: Stock products likely to be bought next

Authors: Dawid Olko & Piotr Smoła
Date: 2025-11-02
Version: 2.0
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum
from collections import defaultdict


class ProbabilisticDebugView(APIView):
    """
    API endpoint for probabilistic recommendation models debugging.
    
    Endpoint: GET /api/probabilistic-debug/?user_id=123&product_id=456
    Permission: AllowAny (public access for debugging)
    
    Query Parameters:
        user_id (int, optional): Specific user to analyze
        product_id (int, optional): Product whose category transitions to show
    
    Response Sections:
        1. markov_chain: State transitions and probabilities
        2. naive_bayes_purchase: Purchase prediction model details
        3. naive_bayes_churn: Churn prediction model details
        4. user_analysis: User-specific predictions (if user_id provided)
        5. product_analysis: Product category transitions (if product_id provided)
        6. system_stats: General system statistics
    
    Training Process:
        1. Markov Chain:
           - Extract purchase sequences: [prod1, prod2, prod3, ...]
           - Count transitions: prod1 → prod2, prod2 → prod3, ...
           - Calculate probabilities: P(j|i) = count(i→j) / total(i→*)
        
        2. Naive Bayes Purchase:
           - Features: total_orders, avg_order_value, days_since_last_order
           - Label: "will_purchase" if recent order (30 days), else "will_not_purchase"
           - Train classifier: Learn P(features | class)
        
        3. Naive Bayes Churn:
           - Same features as purchase prediction
           - Label: "will_churn" if days_since_last_order > 60, else "will_not_churn"
           - Train classifier: Learn P(features | class)
    
    Markov Chain States:
        - States = Product IDs or Category names
        - First-order Markov: Only depends on last state
        - Example transitions:
          * Laptop (ID=1) → Mouse (ID=5): P = 0.65
          * Mouse (ID=5) → Keyboard (ID=8): P = 0.45
    
    Naive Bayes Features:
        - total_orders: Number of orders user has made
        - avg_order_value: Average spending per order (PLN)
        - days_since_last_order: Recency of last purchase
    
    Performance:
        - Trains models on ALL users on each request (no caching)
        - For production: Cache trained models, retrain periodically
        - Typical execution: 2-5 seconds for 1000 users
    """
    permission_classes = []  # AllowAny for debugging

    def get(self, request):
        """
        Debug probabilistic models with comprehensive analysis.
        
        Args:
            request: HTTP GET request with optional query params
        
        Returns:
            Response: Detailed probabilistic analysis
        
        Query Examples:
            1. General system overview:
               GET /api/probabilistic-debug/
            
            2. Analyze specific user:
               GET /api/probabilistic-debug/?user_id=42
            
            3. Analyze product category:
               GET /api/probabilistic-debug/?product_id=123
            
            4. Combined analysis:
               GET /api/probabilistic-debug/?user_id=42&product_id=123
        """
        try:
            # Import probabilistic engine
            from home.custom_recommendation_engine import (
                ProbabilisticRecommendationEngine,
            )
            from home.models import Order, OrderProduct, Product, User, Category

            # Extract query parameters
            user_id = request.GET.get("user_id")
            product_id = request.GET.get("product_id")

            # Initialize probabilistic engine
            engine = ProbabilisticRecommendationEngine()

            # Collect training data from all users
            users = User.objects.all()
            user_purchase_sequences = []  # For Markov Chain
            user_features_list = []  # For Naive Bayes
            purchase_labels = []  # For purchase prediction
            churn_labels = []  # For churn prediction

            # Extract purchase sequences and user features
            for user in users:
                orders = (
                    Order.objects.filter(user=user)
                    .prefetch_related("orderproduct_set__product__categories")
                    .order_by("date_order")
                )

                if orders.exists():
                    # Build purchase sequence for Markov Chain
                    sequence = []
                    for order in orders:
                        order_products = order.orderproduct_set.all()
                        for order_product in order_products:
                            sequence.append(order_product.product_id)

                    if sequence:
                        user_purchase_sequences.append(sequence)
                        print(
                            f"User {user.username}: {len(sequence)} purchases in sequence"
                        )

                    # Calculate user features for Naive Bayes
                    total_orders = orders.count()
                    total_spent = sum(
                        float(op.product.price) * op.quantity
                        for order in orders
                        for op in order.orderproduct_set.all()
                    )
                    avg_order_value = (
                        total_spent / total_orders if total_orders > 0 else 0
                    )

                    from django.utils import timezone

                    last_order = orders.last()
                    days_since_last = (
                        (timezone.now() - last_order.date_order).days
                        if last_order
                        else 999  # Very inactive user
                    )

                    features = {
                        "total_orders": total_orders,
                        "avg_order_value": avg_order_value,
                        "days_since_last_order": days_since_last,
                    }
                    user_features_list.append(features)

            # Generate labels for Naive Bayes classifiers
            if user_features_list:
                from django.utils import timezone
                from datetime import timedelta

                for user in users:
                    orders = Order.objects.filter(user=user)

                    if orders.exists():
                        # Purchase prediction label (30-day window)
                        recent_orders = Order.objects.filter(
                            user=user,
                            date_order__gte=timezone.now() - timedelta(days=30),
                        )
                        purchase_label = (
                            "will_purchase"
                            if recent_orders.exists()
                            else "will_not_purchase"
                        )
                        purchase_labels.append(purchase_label)

                        # Churn prediction label (60-day threshold)
                        last_order = orders.order_by("-date_order").first()
                        days_since_last_order = (
                            (timezone.now().date() - last_order.date_order.date()).days
                            if last_order
                            else 999
                        )
                        churn_label = (
                            "will_churn"
                            if days_since_last_order > 60
                            else "will_not_churn"
                        )
                        churn_labels.append(churn_label)

            print(
                f"Total user_purchase_sequences collected: {len(user_purchase_sequences)}"
            )
            print(
                f"Sequences: {user_purchase_sequences[:3] if len(user_purchase_sequences) >= 3 else user_purchase_sequences}"
            )

            # Train Markov Chain model
            if user_purchase_sequences:
                print("Training Markov model...")
                engine.train_markov_model(user_purchase_sequences)
                print(
                    f"Markov transitions after training: {len(engine.markov_chain.transitions)}"
                )

            # Train Naive Bayes models
            if user_features_list:
                print(f"Training Naive Bayes models on {len(user_features_list)} users")
                print(
                    f"Purchase labels: {purchase_labels.count('will_purchase')} will_purchase, {purchase_labels.count('will_not_purchase')} will_not_purchase"
                )
                print(
                    f"Churn labels: {churn_labels.count('will_churn')} will_churn, {churn_labels.count('will_not_churn')} will_not_churn"
                )
                engine.train_purchase_prediction_model(
                    user_features_list, purchase_labels
                )
                engine.train_churn_prediction_model(user_features_list, churn_labels)

            # Build response with algorithm description
            response_data = {
                "algorithm": "Probabilistic Models (Markov Chain + Naive Bayes)",
                "description": "System rekomendacji oparty na łańcuchach Markova i klasyfikatorze Naive Bayes",
            }

            # Section 1: Markov Chain Transitions
            markov_transitions = {}
            total_transitions = 0

            for from_state, to_states in engine.markov_chain.transitions.items():
                markov_transitions[from_state] = {}
                state_total = sum(to_states.values())
                total_transitions += state_total

                # Calculate transition probabilities
                for to_state, count in to_states.items():
                    probability = count / state_total if state_total > 0 else 0
                    markov_transitions[from_state][to_state] = {
                        "count": count,
                        "probability": round(probability, 4),
                    }

            # Find top transitions by probability
            top_transitions = []
            for from_state, to_states in markov_transitions.items():
                for to_state, data in to_states.items():
                    top_transitions.append(
                        {
                            "from": from_state,
                            "to": to_state,
                            "probability": data["probability"],
                            "count": data["count"],
                        }
                    )

            top_transitions.sort(key=lambda x: x["probability"], reverse=True)

            response_data["markov_chain"] = {
                "total_states": len(engine.markov_chain.transitions),
                "total_transitions": total_transitions,
                "order": engine.markov_chain.order,
                "top_transitions": top_transitions[:10],
                "all_transitions": markov_transitions,
            }

            # Section 2: Naive Bayes Purchase Prediction Model
            response_data["naive_bayes_purchase"] = {
                "trained": len(engine.naive_bayes_purchase.class_priors) > 0,
                "class_priors": {
                    str(k): round(v, 4)
                    for k, v in engine.naive_bayes_purchase.class_priors.items()
                },
                "num_features": len(engine.naive_bayes_purchase.feature_likelihoods),
                "classes": list(engine.naive_bayes_purchase.class_priors.keys()),
            }

            # Section 3: Naive Bayes Churn Prediction Model
            response_data["naive_bayes_churn"] = {
                "trained": len(engine.naive_bayes_churn.class_priors) > 0,
                "class_priors": {
                    str(k): round(v, 4)
                    for k, v in engine.naive_bayes_churn.class_priors.items()
                },
                "num_features": len(engine.naive_bayes_churn.feature_likelihoods),
                "classes": list(engine.naive_bayes_churn.class_priors.keys()),
            }

            # Section 4: User-Specific Analysis (if user_id provided)
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    orders = Order.objects.filter(user=user).order_by("date_order")

                    if orders.exists():
                        last_order = orders.last()
                        last_category = None
                        purchase_sequence = []

                        # Build category sequence from purchase history
                        for order in orders:
                            for op in order.orderproduct_set.all():
                                cat = op.product.categories.first()
                                if cat:
                                    purchase_sequence.append(cat.name)

                        if purchase_sequence:
                            last_category = purchase_sequence[-1]

                        # Markov prediction: Next likely categories
                        markov_predictions = []
                        if last_category and engine.markov_chain.transitions:
                            predictions = engine.predict_next_purchase_categories(
                                last_category, top_k=5
                            )
                            markov_predictions = [
                                {
                                    "category": pred["state"],
                                    "probability": round(pred["probability"], 4),
                                }
                                for pred in predictions
                            ]

                        # Calculate user features for Naive Bayes
                        total_orders = orders.count()
                        total_spent = sum(
                            float(op.product.price) * op.quantity
                            for order in orders
                            for op in order.orderproduct_set.all()
                        )
                        avg_order_value = (
                            total_spent / total_orders if total_orders > 0 else 0
                        )

                        from django.utils import timezone

                        days_since_last = (timezone.now() - last_order.date_order).days

                        user_features = {
                            "total_orders": total_orders,
                            "avg_order_value": avg_order_value,
                            "days_since_last_order": days_since_last,
                        }

                        # Predict purchase and churn probabilities
                        purchase_proba = engine.predict_purchase_probability(
                            user_features
                        )
                        churn_proba = engine.predict_churn_probability(user_features)

                        response_data["user_analysis"] = {
                            "user_id": user.id,
                            "username": user.username,
                            "total_orders": total_orders,
                            "total_spent": round(total_spent, 2),
                            "avg_order_value": round(avg_order_value, 2),
                            "days_since_last_order": days_since_last,
                            "last_category": last_category,
                            "purchase_sequence": purchase_sequence[-10:],  # Last 10
                            "markov_predictions": markov_predictions,
                            "purchase_probability": {
                                "active_buyer": round(
                                    purchase_proba.get("will_purchase", 0), 4
                                ),
                                "inactive": round(
                                    purchase_proba.get("will_not_purchase", 0), 4
                                ),
                            },
                            "churn_probability": {
                                "will_churn": round(
                                    churn_proba.get("will_churn", 0), 4
                                ),
                                "will_stay": round(
                                    churn_proba.get("will_not_churn", 0), 4
                                ),
                            },
                        }
                    else:
                        response_data["user_analysis"] = {
                            "error": "User has no purchase history"
                        }

                except User.DoesNotExist:
                    response_data["user_analysis"] = {
                        "error": f"User with ID {user_id} not found"
                    }

            # Section 5: Product-Specific Analysis (if product_id provided)
            if product_id:
                try:
                    product = Product.objects.prefetch_related("categories").get(
                        id=product_id
                    )
                    main_category = product.categories.first()

                    if main_category:
                        category_name = main_category.name

                        # Get transition probabilities from this category
                        next_categories = markov_transitions.get(category_name, {})

                        # Find products in likely next categories
                        predicted_next_products = []
                        for next_cat, data in sorted(
                            next_categories.items(),
                            key=lambda x: x[1]["probability"],
                            reverse=True,
                        )[:3]:
                            products_in_cat = Product.objects.filter(
                                categories__name=next_cat
                            )[:3]
                            for prod in products_in_cat:
                                predicted_next_products.append(
                                    {
                                        "id": prod.id,
                                        "name": prod.name,
                                        "price": float(prod.price),
                                        "category": next_cat,
                                        "transition_probability": data["probability"],
                                    }
                                )

                        response_data["product_analysis"] = {
                            "product_id": product.id,
                            "product_name": product.name,
                            "category": category_name,
                            "next_likely_categories": [
                                {
                                    "category": cat,
                                    "probability": data["probability"],
                                    "count": data["count"],
                                }
                                for cat, data in sorted(
                                    next_categories.items(),
                                    key=lambda x: x[1]["probability"],
                                    reverse=True,
                                )[:5]
                            ],
                            "predicted_next_products": predicted_next_products,
                        }
                    else:
                        response_data["product_analysis"] = {
                            "error": "Product has no category"
                        }

                except Product.DoesNotExist:
                    response_data["product_analysis"] = {
                        "error": f"Product with ID {product_id} not found"
                    }

            # Section 6: System Statistics
            response_data["system_stats"] = {
                "total_users_analyzed": len(user_purchase_sequences),
                "total_categories": len(
                    set(cat for seq in user_purchase_sequences for cat in seq)
                ),
                "markov_trained": engine.markov_chain.transitions != {},
                "naive_bayes_purchase_trained": len(
                    engine.naive_bayes_purchase.class_priors
                )
                > 0,
                "naive_bayes_churn_trained": len(engine.naive_bayes_churn.class_priors)
                > 0,
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
