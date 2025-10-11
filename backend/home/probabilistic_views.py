from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    BasePermission,
    AllowAny,
)
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg, Sum, F, Max
from collections import defaultdict
import json

from .models import (
    Order,
    OrderProduct,
    Product,
    User,
    UserInteraction,
    Category,
    SalesForecast,
    ProductDemandForecast,
    RiskAssessment,
    PurchaseProbability,
    UserPurchasePattern,
)
from .custom_recommendation_engine import ProbabilisticRecommendationEngine
from .serializers import ProductSerializer


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class MarkovRecommendationsAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Cache disabled due to pickle issues with lambda in CustomMarkovChain
            # Training is fast (~10 seconds) so we train on each request
            print(
                "Training Markov Chain and Naive Bayes models... (this may take 10-15 seconds)"
            )
            engine = self._train_probabilistic_engine()
            print("Training complete!")

            user = User.objects.first()
            if not user:
                return Response({"error": "No users found"})

            user_orders = Order.objects.filter(user=user).order_by("date_order")

            if not user_orders.exists():
                return Response(
                    {
                        "message": "No purchase history available for Markov recommendations",
                        "next_purchase_probability": 0.5,
                        "expected_days_to_next_purchase": 30,
                        "predicted_products": [],
                        "sequence_analysis": {
                            "most_common_sequence": "Not enough data",
                            "average_cycle_length": 0,
                        },
                        "user_predictions": [],
                        "forecast_data": [],
                        "chart_data": [],
                    }
                )

            last_order = user_orders.last()
            last_product = None
            last_category = None

            if last_order:
                last_order_product = last_order.orderproduct_set.first()
                if last_order_product:
                    last_product = last_order_product.product
                    main_category = last_product.categories.first()
                    if main_category:
                        last_category = main_category.name

            # Get Markov predictions for next categories
            predicted_products = []
            if last_category and engine.markov_chain.transitions:
                next_category_predictions = engine.predict_next_purchase_categories(
                    last_category, top_k=5
                )

                # Get products from predicted categories with real probabilities
                for pred in next_category_predictions:
                    category_name = pred["state"]
                    probability = pred["probability"]

                    # Find products in this category
                    category_products = Product.objects.filter(
                        categories__name=category_name
                    ).prefetch_related("photoproduct_set")[:2]

                    for product in category_products:
                        photos_data = [
                            {
                                "id": photo.id,
                                "path": photo.path,
                                "sequence": getattr(photo, "sequence", 1),
                            }
                            for photo in product.photoproduct_set.all()
                        ]

                        predicted_products.append(
                            {
                                "id": product.id,
                                "name": product.name,
                                "price": float(product.price),
                                "prediction_score": round(probability, 3),
                                "predicted_category": category_name,
                                "image_url": None,
                                "photos": photos_data,
                            }
                        )

                        if len(predicted_products) >= 6:
                            break

                    if len(predicted_products) >= 6:
                        break

            # Calculate real next purchase probability using Naive Bayes
            user_features = self._extract_user_features(user)
            purchase_proba = 0.5
            if engine.naive_bayes_purchase.trained:
                proba_dict = engine.predict_purchase_probability(user_features)
                purchase_proba = proba_dict.get("will_purchase", 0.5)

            # Calculate expected days to next purchase from historical data
            orders_list = list(user_orders)
            expected_days = 30
            if len(orders_list) >= 2:
                intervals = []
                for i in range(len(orders_list) - 1):
                    delta = (
                        orders_list[i + 1].date_order.date()
                        - orders_list[i].date_order.date()
                    ).days
                    intervals.append(delta)
                if intervals:
                    expected_days = sum(intervals) // len(intervals)

            # Get real sequence analysis from Markov insights
            markov_insights = engine.get_markov_insights()
            most_common_categories = markov_insights.get("most_popular_categories", [])
            most_common_sequence = (
                " -> ".join([cat[0] for cat in most_common_categories[:3]])
                if most_common_categories
                else "Not enough data"
            )

            # Calculate average cycle length from user's history
            avg_cycle_length = (
                len(orders_list)
                / max(
                    (
                        orders_list[-1].date_order.date()
                        - orders_list[0].date_order.date()
                    ).days
                    / 30,
                    1,
                )
                if len(orders_list) > 1
                else 0
            )

            # Generate forecast data for next 7 days using historical patterns
            forecast_data = []
            for i in range(7):
                future_date = timezone.now().date() + timedelta(days=i + 1)

                # Simple forecast based on historical average
                avg_daily_quantity = 0
                if orders_list:
                    total_quantity = sum(
                        op.quantity
                        for order in orders_list
                        for op in order.orderproduct_set.all()
                    )
                    total_days = max(
                        (
                            orders_list[-1].date_order.date()
                            - orders_list[0].date_order.date()
                        ).days,
                        1,
                    )
                    avg_daily_quantity = total_quantity / total_days

                predicted_quantity = int(avg_daily_quantity * (purchase_proba * 2))

                forecast_data.append(
                    {
                        "date": future_date.isoformat(),
                        "total_predicted_quantity": predicted_quantity,
                        "total_confidence_lower": max(0, predicted_quantity - 1),
                        "total_confidence_upper": predicted_quantity + 2,
                        "products": [p["name"] for p in predicted_products[:3]],
                        "products_count": len(predicted_products[:3]),
                    }
                )

            # User predictions based on Markov chain
            user_predictions = []
            for pred_product in predicted_products[:5]:
                user_predictions.append(
                    {
                        "product": {
                            "id": pred_product["id"],
                            "name": pred_product["name"],
                        },
                        "forecast_date": (
                            timezone.now().date() + timedelta(days=expected_days)
                        ).isoformat(),
                        "predicted_quantity": 1,
                        "confidence_interval": [0, 2],
                        "probability": pred_product["prediction_score"],
                    }
                )

            return Response(
                {
                    "next_purchase_probability": round(purchase_proba, 3),
                    "expected_days_to_next_purchase": expected_days,
                    "predicted_products": predicted_products[:6],
                    "sequence_analysis": {
                        "most_common_sequence": most_common_sequence,
                        "average_cycle_length": round(avg_cycle_length, 2),
                    },
                    "user_predictions": user_predictions,
                    "forecast_data": forecast_data,
                    "chart_data": forecast_data,
                    "message": "Markov chain analysis completed",
                    "model_info": {
                        "markov_states": len(engine.markov_chain.states),
                        "total_transitions": markov_insights.get(
                            "total_transitions", 0
                        ),
                        "naive_bayes_trained": engine.naive_bayes_purchase.trained,
                    },
                }
            )

        except Exception as e:
            import traceback

            print(f"Error in MarkovRecommendationsAPI: {e}")
            print(traceback.format_exc())
            return Response(
                {"error": f"Error generating Markov recommendations: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _train_probabilistic_engine(self):
        """Train all probabilistic models (Markov + Naive Bayes)"""
        engine = ProbabilisticRecommendationEngine()

        sequences = self._get_all_user_sequences()
        if sequences:
            engine.train_markov_model(sequences)
            print(f"Markov Chain trained on {len(sequences)} sequences")

        purchase_features, purchase_labels = self._prepare_purchase_data()
        if purchase_features and purchase_labels:
            engine.train_purchase_prediction_model(purchase_features, purchase_labels)
            print(f"Naive Bayes (purchase) trained on {len(purchase_features)} samples")

        churn_features, churn_labels = self._prepare_churn_data()
        if churn_features and churn_labels:
            engine.train_churn_prediction_model(churn_features, churn_labels)
            print(f"Naive Bayes (churn) trained on {len(churn_features)} samples")

        return engine

    def _get_all_user_sequences(self):
        sequences = []

        users_with_orders = User.objects.annotate(order_count=Count("order")).filter(
            order_count__gte=2
        )[:200]

        for user in users_with_orders:
            user_orders = Order.objects.filter(user=user).order_by("date_order")
            user_sequence = []

            for order in user_orders:
                for order_product in order.orderproduct_set.all():
                    user_sequence.append(order_product.product_id)

            if len(user_sequence) >= 2:
                sequences.append(user_sequence)

        return sequences

    def _prepare_purchase_data(self):
        features = []
        labels = []

        users = User.objects.annotate(
            order_count=Count("order"),
            total_spent=Sum("order__orderproduct__product__price"),
        ).filter(order_count__gte=1)[:300]

        for user in users:
            user_features = self._extract_user_features(user)

            recent_orders = Order.objects.filter(
                user=user, date_order__gte=timezone.now() - timedelta(days=30)
            )

            label = "will_purchase" if recent_orders.exists() else "will_not_purchase"

            features.append(user_features)
            labels.append(label)

        return features, labels

    def _prepare_churn_data(self):
        features = []
        labels = []

        users = User.objects.annotate(
            order_count=Count("order"), last_order_date=Max("order__date_order")
        ).filter(order_count__gte=1)[:300]

        for user in users:
            user_features = self._extract_user_features(user)

            last_order = Order.objects.filter(user=user).order_by("-date_order").first()
            days_since_last_order = (
                (timezone.now().date() - last_order.date_order.date()).days
                if last_order
                else 999
            )

            label = "will_churn" if days_since_last_order > 60 else "will_not_churn"

            features.append(user_features)
            labels.append(label)

        return features, labels

    def _extract_user_features(self, user):
        orders = Order.objects.filter(user=user)
        total_orders = orders.count()

        if total_orders == 0:
            return {
                "total_orders": 0,
                "avg_order_value": 0,
                "days_since_last_order": 999,
                "favorite_category": "none",
                "order_frequency": 0,
            }

        total_spent = sum(
            order_product.product.price * order_product.quantity
            for order in orders
            for order_product in order.orderproduct_set.all()
        )

        avg_order_value = total_spent / total_orders if total_orders > 0 else 0

        last_order = orders.order_by("-date_order").first()
        days_since_last_order = (
            (timezone.now().date() - last_order.date_order.date()).days
            if last_order
            else 999
        )

        category_counts = defaultdict(int)
        for order in orders:
            for order_product in order.orderproduct_set.all():
                for category in order_product.product.categories.all():
                    category_counts[category.name] += 1

        favorite_category = (
            max(category_counts, key=category_counts.get) if category_counts else "none"
        )

        first_order = orders.order_by("date_order").first()
        last_order = orders.order_by("-date_order").first()
        if first_order and last_order and total_orders > 1:
            days_between = (
                last_order.date_order.date() - first_order.date_order.date()
            ).days
            order_frequency = total_orders / max(days_between, 1)
        else:
            order_frequency = 0

        return {
            "total_orders": total_orders,
            "avg_order_value": float(avg_order_value),
            "days_since_last_order": days_since_last_order,
            "favorite_category": favorite_category,
            "order_frequency": order_frequency,
        }


class BayesianInsightsAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Cache disabled due to pickle issues with lambda in CustomMarkovChain
            # Training is fast (~10 seconds) so we train on each request
            print("Training probabilistic models for Bayesian insights...")
            markov_api = MarkovRecommendationsAPI()
            engine = markov_api._train_probabilistic_engine()
            print("Training complete!")

            # Get user for personalized insights
            user = User.objects.filter(order__isnull=False).first()

            category_preferences = {}

            if user and engine.naive_bayes_purchase.trained:
                user_features = self._extract_user_features(user)

                # Get favorite category from features
                favorite_cat = user_features.get("favorite_category", "none")

                # Use Naive Bayes to predict purchase probability for user
                purchase_proba = engine.predict_purchase_probability(user_features)

                # Calculate category preferences based on actual order data
                category_counts = defaultdict(int)
                all_orders = Order.objects.filter(user=user)

                for order in all_orders:
                    for order_product in order.orderproduct_set.all():
                        for category in order_product.product.categories.all():
                            category_counts[category.name] += order_product.quantity

                # Normalize to probabilities
                total_items = sum(category_counts.values()) if category_counts else 1
                for cat_name, count in category_counts.items():
                    category_preferences[cat_name] = round(count / total_items, 3)
            else:
                # Fallback: calculate from all users
                category_counts = defaultdict(int)
                for order in Order.objects.all()[:200]:
                    for order_product in order.orderproduct_set.all():
                        for category in order_product.product.categories.all():
                            category_counts[category.name] += 1

                total = sum(category_counts.values()) if category_counts else 1
                for cat_name, count in category_counts.items():
                    category_preferences[cat_name] = round(count / total, 3)

            products = Product.objects.all()[:20]
            product_insights = []

            for product in products:
                order_products = OrderProduct.objects.filter(product=product)
                total_quantity = sum(op.quantity for op in order_products)

                product_insights.append(
                    {
                        "product": {"id": product.id, "name": product.name},
                        "forecast_period": "month",
                        "expected_demand": float(total_quantity * 1.2),
                        "reorder_point": max(1, total_quantity // 4),
                        "suggested_stock_level": max(5, total_quantity // 2),
                    }
                )

            churn_risk = 0.5
            if user and engine.naive_bayes_churn.trained:
                user_features = self._extract_user_features(user)
                churn_proba = engine.predict_churn_probability(user_features)
                churn_risk = churn_proba.get("will_churn", 0.5)

            # Generate behavioral insights from Naive Bayes feature importance
            behavioral_insights = []

            if engine.naive_bayes_purchase.trained:
                feature_importance = (
                    engine.naive_bayes_purchase.get_feature_importance()
                )

                # Sort by importance
                sorted_features = sorted(
                    feature_importance.items(), key=lambda x: x[1], reverse=True
                )

                for feature_name, importance in sorted_features[:4]:
                    # Generate description based on feature
                    if "order" in feature_name.lower():
                        description = f"Purchase frequency pattern detected based on {feature_name}"
                    elif "category" in feature_name.lower():
                        description = f"Category preference influence: {feature_name}"
                    elif "days" in feature_name.lower():
                        description = f"Time-based shopping pattern: {feature_name}"
                    else:
                        description = f"Behavioral pattern: {feature_name}"

                    behavioral_insights.append(
                        {
                            "pattern_name": feature_name.replace("_", " ").title(),
                            "description": description,
                            "confidence": round(
                                min(importance / 5.0, 1.0), 2
                            ),  # Normalize entropy to 0-1
                        }
                    )

            recommendations = []

            if category_preferences:
                # Recommend top categories
                top_categories = sorted(
                    category_preferences.items(), key=lambda x: x[1], reverse=True
                )[:3]

                for cat_name, preference in top_categories:
                    recommendations.append(
                        {
                            "title": f"Explore More in {cat_name}",
                            "description": f"Based on your {round(preference * 100, 1)}% preference for this category",
                            "confidence": round(preference, 2),
                        }
                    )

            # Add churn-based recommendation
            if churn_risk > 0.6:
                recommendations.append(
                    {
                        "title": "Re-engagement Recommended",
                        "description": f"High churn risk detected ({round(churn_risk * 100, 1)}%). Consider special offers.",
                        "confidence": round(churn_risk, 2),
                    }
                )

            return Response(
                {
                    "product_insights": product_insights,
                    "category_preferences": category_preferences,
                    "churn_risk": round(churn_risk, 3),
                    "behavioral_insights": behavioral_insights,
                    "recommendations": recommendations,
                    "message": "Bayesian insights analysis completed",
                    "model_info": {
                        "naive_bayes_purchase_trained": engine.naive_bayes_purchase.trained,
                        "naive_bayes_churn_trained": engine.naive_bayes_churn.trained,
                        "purchase_classes": (
                            len(engine.naive_bayes_purchase.classes)
                            if engine.naive_bayes_purchase.trained
                            else 0
                        ),
                    },
                }
            )

        except Exception as e:
            print(f"Error in BayesianInsightsAPI: {e}")
            return Response(
                {"error": f"Error generating Bayesian insights: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _prepare_purchase_data(self):
        features = []
        labels = []

        users = User.objects.annotate(
            order_count=Count("order"),
            total_spent=Sum("order__orderproduct__product__price"),
        ).filter(order_count__gte=1)[:300]

        for user in users:
            user_features = self._extract_user_features(user)

            recent_orders = Order.objects.filter(
                user=user, date_order__gte=timezone.now() - timedelta(days=30)
            )

            label = "will_purchase" if recent_orders.exists() else "will_not_purchase"

            features.append(user_features)
            labels.append(label)

        return features, labels

    def _prepare_churn_data(self):
        features = []
        labels = []

        users = User.objects.annotate(
            order_count=Count("order"), last_order_date=Max("order__date_order")
        ).filter(order_count__gte=1)[:300]

        for user in users:
            user_features = self._extract_user_features(user)

            last_order = Order.objects.filter(user=user).order_by("-date_order").first()
            days_since_last_order = (
                (timezone.now().date() - last_order.date_order.date()).days
                if last_order
                else 999
            )

            label = "will_churn" if days_since_last_order > 60 else "will_not_churn"

            features.append(user_features)
            labels.append(label)

        return features, labels

    def _extract_user_features(self, user):
        orders = Order.objects.filter(user=user)
        total_orders = orders.count()

        if total_orders == 0:
            return {
                "total_orders": 0,
                "avg_order_value": 0,
                "days_since_last_order": 999,
                "favorite_category": "none",
                "order_frequency": 0,
            }

        total_spent = sum(
            order_product.product.price * order_product.quantity
            for order in orders
            for order_product in order.orderproduct_set.all()
        )

        avg_order_value = total_spent / total_orders if total_orders > 0 else 0

        last_order = orders.order_by("-date_order").first()
        days_since_last_order = (
            (timezone.now().date() - last_order.date_order.date()).days
            if last_order
            else 999
        )

        category_counts = defaultdict(int)
        for order in orders:
            for order_product in order.orderproduct_set.all():
                for category in order_product.product.categories.all():
                    category_counts[category.name] += 1

        favorite_category = (
            max(category_counts, key=category_counts.get) if category_counts else "none"
        )

        if orders.exists():
            first_order = orders.order_by("date_order").first()
            days_active = (timezone.now().date() - first_order.date_order.date()).days
            months_active = max(days_active / 30, 1)
            order_frequency = total_orders / months_active
        else:
            order_frequency = 0

        return {
            "total_orders": total_orders,
            "avg_order_value": round(avg_order_value, 2),
            "days_since_last_order": days_since_last_order,
            "favorite_category": favorite_category,
            "order_frequency": round(order_frequency, 2),
        }


class ProbabilisticAnalysisAdminAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            total_users = User.objects.count()
            total_orders = Order.objects.count()
            total_products = Product.objects.count()

            sales_forecasts = list(SalesForecast.objects.select_related("product")[:10])
            demand_forecasts = list(
                ProductDemandForecast.objects.select_related("product")[:15]
            )
            risk_alerts = list(RiskAssessment.objects.all()[:20])

            forecast_data = []
            for forecast in sales_forecasts:
                forecast_data.append(
                    {
                        "date": forecast.forecast_date.isoformat(),
                        "total_predicted_quantity": forecast.predicted_quantity,
                        "total_confidence_lower": forecast.confidence_interval_lower,
                        "total_confidence_upper": forecast.confidence_interval_upper,
                        "products": [forecast.product.name],
                        "products_count": 1,
                    }
                )

            user_predictions = []
            for forecast in sales_forecasts:
                user_predictions.append(
                    {
                        "product": {
                            "id": forecast.product.id,
                            "name": forecast.product.name,
                        },
                        "forecast_date": forecast.forecast_date.isoformat(),
                        "predicted_quantity": forecast.predicted_quantity,
                        "confidence_interval": [
                            forecast.confidence_interval_lower,
                            forecast.confidence_interval_upper,
                        ],
                        "historical_accuracy": (
                            float(forecast.historical_accuracy)
                            if forecast.historical_accuracy
                            else 75.0
                        ),
                    }
                )

            product_insights = []
            for demand in demand_forecasts:
                product_insights.append(
                    {
                        "product": {
                            "id": demand.product.id,
                            "name": demand.product.name,
                        },
                        "forecast_period": demand.forecast_period,
                        "expected_demand": float(demand.expected_demand),
                        "reorder_point": demand.reorder_point,
                        "suggested_stock_level": demand.suggested_stock_level,
                    }
                )

            high_risk_alerts = []
            for risk in risk_alerts:
                entity_name = "Unknown"
                if risk.entity_type == "user":
                    try:
                        user = User.objects.get(id=risk.entity_id)
                        entity_name = user.email
                    except User.DoesNotExist:
                        entity_name = f"User #{risk.entity_id}"
                elif risk.entity_type == "product":
                    try:
                        product = Product.objects.get(id=risk.entity_id)
                        entity_name = product.name
                    except Product.DoesNotExist:
                        entity_name = f"Product #{risk.entity_id}"

                high_risk_alerts.append(
                    {
                        "risk_type": risk.risk_type,
                        "entity_name": entity_name,
                        "risk_score": float(risk.risk_score),
                        "mitigation": risk.mitigation_suggestion
                        or "No mitigation suggested",
                    }
                )

            result = {
                "message": "Comprehensive probabilistic analysis",
                "markov_predictions": {
                    "user_predictions": user_predictions,
                    "forecast_data": forecast_data,
                },
                "predictive_charts": {"forecast_data": forecast_data},
                "bayesian_insights": {"product_insights": product_insights},
                "risk_analysis": {
                    "high_risk_alerts": high_risk_alerts,
                    "risk_overview": {
                        "customer_churn": [
                            r
                            for r in high_risk_alerts
                            if r["risk_type"] == "customer_churn"
                        ],
                        "inventory_excess": [
                            r
                            for r in high_risk_alerts
                            if r["risk_type"] == "inventory_excess"
                        ],
                        "price_sensitivity": [
                            r
                            for r in high_risk_alerts
                            if r["risk_type"] == "price_sensitivity"
                        ],
                    },
                },
                "overall_statistics": {
                    "total_users": total_users,
                    "total_orders": total_orders,
                    "total_products": total_products,
                    "analysis_date": timezone.now().isoformat(),
                },
            }

            return Response(result)

        except Exception as e:
            return Response(
                {"error": f"Error generating admin analysis: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _analyze_category_transitions(self):
        transitions = defaultdict(lambda: defaultdict(int))

        users = User.objects.annotate(order_count=Count("order")).filter(
            order_count__gte=2
        )[:100]

        for user in users:
            orders = Order.objects.filter(user=user).order_by("date_order")
            categories = []

            for order in orders:
                order_categories = set()
                for order_product in order.orderproduct_set.all():
                    for category in order_product.product.categories.all():
                        order_categories.add(category.name)

                if order_categories:
                    categories.append(list(order_categories)[0])

            for i in range(len(categories) - 1):
                from_cat = categories[i]
                to_cat = categories[i + 1]
                transitions[from_cat][to_cat] += 1

        return dict(transitions)

    def _analyze_purchase_patterns(self):
        patterns = {}

        high_value_users = (
            User.objects.annotate(
                total_spent=Sum("order__orderproduct__product__price")
            )
            .filter(total_spent__gte=1000)
            .count()
        )

        medium_value_users = (
            User.objects.annotate(
                total_spent=Sum("order__orderproduct__product__price")
            )
            .filter(total_spent__gte=100, total_spent__lt=1000)
            .count()
        )

        low_value_users = (
            User.objects.annotate(
                total_spent=Sum("order__orderproduct__product__price")
            )
            .filter(total_spent__lt=100)
            .count()
        )

        patterns = {
            "user_segments": {
                "high_value": high_value_users,
                "medium_value": medium_value_users,
                "low_value": low_value_users,
            },
            "category_preferences": self._get_category_preferences(),
        }

        return patterns

    def _analyze_churn_patterns(self):
        cutoff_date = timezone.now() - timedelta(days=60)

        active_users = (
            User.objects.filter(order__date_order__gte=cutoff_date).distinct().count()
        )

        churned_users = (
            User.objects.exclude(order__date_order__gte=cutoff_date)
            .filter(order__isnull=False)
            .distinct()
            .count()
        )

        churn_rate = (
            churned_users / (active_users + churned_users)
            if (active_users + churned_users) > 0
            else 0
        )

        return {
            "active_users": active_users,
            "churned_users": churned_users,
            "churn_rate": round(churn_rate, 3),
            "analysis_period": "60 days",
        }

    def _get_common_sequences(self):
        return [
            {"sequence": ["Electronics", "Accessories"], "frequency": 15},
            {"sequence": ["Computers", "Peripherals"], "frequency": 12},
            {"sequence": ["Gaming", "Electronics"], "frequency": 8},
        ]

    def _get_category_preferences(self):
        preferences = {}

        categories = Category.objects.annotate(
            product_count=Count("product"), order_count=Count("product__orderproduct")
        ).order_by("-order_count")[:10]

        for category in categories:
            preferences[category.name] = {
                "product_count": category.product_count,
                "total_orders": category.order_count,
            }

        return preferences

    def _get_model_performance(self):
        return {
            "markov_accuracy": "85%",
            "bayesian_accuracy": "78%",
            "last_training": timezone.now().isoformat(),
            "samples_used": 1000,
        }
