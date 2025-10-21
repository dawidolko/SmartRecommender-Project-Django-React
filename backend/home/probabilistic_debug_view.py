from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum
from collections import defaultdict


class ProbabilisticDebugView(APIView):
    """
    Debug endpoint dla Probabilistic Models - pokazuje Markov Chain transitions,
    Naive Bayes probabilities, i user predictions
    """

    permission_classes = []

    def get(self, request):
        try:
            from home.custom_recommendation_engine import (
                ProbabilisticRecommendationEngine,
            )
            from home.models import Order, OrderProduct, Product, User, Category

            user_id = request.GET.get("user_id")
            product_id = request.GET.get("product_id")

            engine = ProbabilisticRecommendationEngine()

            users = User.objects.all()
            user_purchase_sequences = []
            user_features_list = []
            purchase_labels = []
            churn_labels = []

            for user in users:
                orders = (
                    Order.objects.filter(user=user)
                    .prefetch_related("orderproduct_set__product__categories")
                    .order_by("date_order")
                )

                if orders.exists():
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
                        else 999
                    )

                    features = {
                        "total_orders": total_orders,
                        "avg_order_value": avg_order_value,
                        "days_since_last_order": days_since_last,
                    }
                    user_features_list.append(features)

            if user_features_list:
                from django.utils import timezone
                from datetime import timedelta

                for user in users:
                    orders = Order.objects.filter(user=user)

                    if orders.exists():
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

            if user_purchase_sequences:
                print("Training Markov model...")
                engine.train_markov_model(user_purchase_sequences)
                print(
                    f"Markov transitions after training: {len(engine.markov_chain.transitions)}"
                )

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

            response_data = {
                "algorithm": "Probabilistic Models (Markov Chain + Naive Bayes)",
                "description": "System rekomendacji oparty na łańcuchach Markova i klasyfikatorze Naive Bayes",
            }

            markov_transitions = {}
            total_transitions = 0

            for from_state, to_states in engine.markov_chain.transitions.items():
                markov_transitions[from_state] = {}
                state_total = sum(to_states.values())
                total_transitions += state_total

                for to_state, count in to_states.items():
                    probability = count / state_total if state_total > 0 else 0
                    markov_transitions[from_state][to_state] = {
                        "count": count,
                        "probability": round(probability, 4),
                    }

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

            response_data["naive_bayes_purchase"] = {
                "trained": len(engine.naive_bayes_purchase.class_priors) > 0,
                "class_priors": {
                    str(k): round(v, 4)
                    for k, v in engine.naive_bayes_purchase.class_priors.items()
                },
                "num_features": len(engine.naive_bayes_purchase.feature_likelihoods),
                "classes": list(engine.naive_bayes_purchase.class_priors.keys()),
            }

            response_data["naive_bayes_churn"] = {
                "trained": len(engine.naive_bayes_churn.class_priors) > 0,
                "class_priors": {
                    str(k): round(v, 4)
                    for k, v in engine.naive_bayes_churn.class_priors.items()
                },
                "num_features": len(engine.naive_bayes_churn.feature_likelihoods),
                "classes": list(engine.naive_bayes_churn.class_priors.keys()),
            }

            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    orders = Order.objects.filter(user=user).order_by("date_order")

                    if orders.exists():
                        last_order = orders.last()
                        last_category = None
                        purchase_sequence = []

                        for order in orders:
                            for op in order.orderproduct_set.all():
                                cat = op.product.categories.first()
                                if cat:
                                    purchase_sequence.append(cat.name)

                        if purchase_sequence:
                            last_category = purchase_sequence[-1]

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

            if product_id:
                try:
                    product = Product.objects.prefetch_related("categories").get(
                        id=product_id
                    )
                    main_category = product.categories.first()

                    if main_category:
                        category_name = main_category.name

                        next_categories = markov_transitions.get(category_name, {})

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
            import traceback

            return Response(
                {
                    "status": "error",
                    "message": str(e),
                    "traceback": traceback.format_exc(),
                },
                status=500,
            )
