from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg, F, Q
from datetime import date, datetime, timedelta
from decimal import Decimal
from home.models import (
    User,
    Product,
    Order,
    OrderProduct,
    PurchaseProbability,
    SalesForecast,
    UserPurchasePattern,
    ProductDemandForecast,
    RiskAssessment,
)
from home.permissions import IsAdminUser
from home.serializers import ProductSerializer


class UserPurchasePredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        predicted_products = (
            PurchaseProbability.objects.filter(user=user)
            .select_related("product")
            .order_by("-probability")[:10]
        )

        predictions = []
        for prediction in predicted_products:
            product_data = ProductSerializer(prediction.product).data
            product_data["purchase_probability"] = float(prediction.probability)
            product_data["confidence"] = float(prediction.confidence_level)
            predictions.append(product_data)

        return Response(
            {
                "predictions": predictions,
                "message": f"Based on your purchase history, these products might interest you.",
            }
        )


class PersonalizedRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        purchase_patterns = UserPurchasePattern.objects.filter(user=user)

        recommendations = []
        for pattern in purchase_patterns:
            category_products = Product.objects.filter(
                categories=pattern.category
            ).prefetch_related("photoproduct_set")

            already_purchased = OrderProduct.objects.filter(
                order__user=user
            ).values_list("product_id", flat=True)

            new_products = category_products.exclude(id__in=already_purchased)

            for product in new_products[:3]:
                recommendations.append(
                    {
                        "product": ProductSerializer(product).data,
                        "category": pattern.category.name,
                        "purchase_frequency": float(pattern.purchase_frequency),
                        "average_order_value": float(pattern.average_order_value),
                        "next_purchase_likely": self.calculate_next_purchase_time(
                            pattern
                        ),
                    }
                )

        return Response(
            {
                "recommendations": recommendations,
                "user_insights": {
                    "most_active_category": self.get_most_active_category(user),
                    "preferred_shopping_time": self.get_preferred_time(user),
                },
            }
        )

    def calculate_next_purchase_time(self, pattern):
        if pattern.purchase_frequency > 0:
            days_until_next = 30 / pattern.purchase_frequency
            return f"in {int(days_until_next)} days"
        return "unknown"

    def get_most_active_category(self, user):
        most_active = (
            UserPurchasePattern.objects.filter(user=user)
            .order_by("-purchase_frequency")
            .first()
        )

        if most_active:
            return most_active.category.name
        return "No data"

    def get_preferred_time(self, user):
        times = UserPurchasePattern.objects.filter(user=user).values_list(
            "preferred_time_of_day", flat=True
        )

        if times:
            return max(set(times), key=lambda x: list(times).count(x))
        return "No preference"


class SalesForecastView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        current_date = date.today()
        end_date = current_date + timedelta(days=30)

        forecasts = (
            SalesForecast.objects.filter(
                forecast_date__gte=current_date, forecast_date__lte=end_date
            )
            .select_related("product")
            .order_by("forecast_date")
        )

        print(
            f"Found {forecasts.count()} forecasts for period {current_date} to {end_date}"
        )

        forecasts_by_date = {}
        detailed_results = []

        for forecast in forecasts:
            date_str = forecast.forecast_date.strftime("%Y-%m-%d")

            detailed_results.append(
                {
                    "product": {
                        "id": forecast.product.id,
                        "name": forecast.product.name,
                    },
                    "forecast_date": forecast.forecast_date,
                    "predicted_quantity": forecast.predicted_quantity,
                    "confidence_interval": [
                        forecast.confidence_interval_lower,
                        forecast.confidence_interval_upper,
                    ],
                    "historical_accuracy": float(forecast.historical_accuracy or 0),
                }
            )

            if date_str not in forecasts_by_date:
                forecasts_by_date[date_str] = {
                    "date": forecast.forecast_date,
                    "total_predicted": 0,
                    "total_lower": 0,
                    "total_upper": 0,
                    "count": 0,
                    "products": [],
                }

            forecasts_by_date[date_str][
                "total_predicted"
            ] += forecast.predicted_quantity
            forecasts_by_date[date_str][
                "total_lower"
            ] += forecast.confidence_interval_lower
            forecasts_by_date[date_str][
                "total_upper"
            ] += forecast.confidence_interval_upper
            forecasts_by_date[date_str]["count"] += 1
            forecasts_by_date[date_str]["products"].append(forecast.product.name)

        chart_data = []
        for date_str in sorted(forecasts_by_date.keys()):
            data = forecasts_by_date[date_str]
            chart_data.append(
                {
                    "date": date_str,
                    "forecast_date": data["date"],
                    "total_predicted_quantity": data["total_predicted"],
                    "total_confidence_lower": data["total_lower"],
                    "total_confidence_upper": data["total_upper"],
                    "products_count": data["count"],
                    "products": data["products"][
                        :5
                    ], 
                }
            )

        print(
            f"Returning {len(chart_data)} aggregated chart points and {len(detailed_results)} detailed results"
        )

        return Response(
            {
                "forecasts": detailed_results,
                "chart_data": chart_data,
                "summary": {
                    "total_predicted_units": sum(
                        f["predicted_quantity"] for f in detailed_results
                    ),
                    "period": f"30 days",
                    "from_date": current_date,
                    "to_date": end_date,
                    "unique_dates": len(chart_data),
                    "total_products": len(
                        set(f["product"]["id"] for f in detailed_results)
                    ),
                },
            }
        )


class ProductDemandView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        demands = ProductDemandForecast.objects.select_related("product").order_by(
            "period_start"
        )

        print(f"Found {demands.count()} demand forecasts")

        results = []
        for demand in demands:
            results.append(
                {
                    "product": {"id": demand.product.id, "name": demand.product.name},
                    "forecast_period": demand.forecast_period,
                    "period_start": demand.period_start,
                    "expected_demand": float(demand.expected_demand),
                    "demand_variance": float(demand.demand_variance),
                    "reorder_point": demand.reorder_point,
                    "suggested_stock_level": demand.suggested_stock_level,
                }
            )

        low_stock_alerts = []
        for demand in demands:
            if demand.forecast_period == "month":
                if demand.expected_demand > demand.reorder_point:
                    low_stock_alerts.append(
                        {
                            "product": demand.product.name,
                            "action_needed": "Reorder needed",
                            "suggested_quantity": demand.suggested_stock_level,
                        }
                    )

        return Response(
            {
                "demand_forecasts": results,
                "alerts": low_stock_alerts,
                "summary": {
                    "products_analyzed": len(demands),
                    "action_required": len(low_stock_alerts),
                },
            }
        )


class RiskDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        recent_risks = RiskAssessment.objects.order_by("-assessment_date")

        print(f"Found {recent_risks.count()} risk assessments")

        risk_by_type = {}
        for risk in recent_risks:
            if risk.risk_type not in risk_by_type:
                risk_by_type[risk.risk_type] = []

            risk_by_type[risk.risk_type].append(
                {
                    "entity_type": risk.entity_type,
                    "entity_id": risk.entity_id,
                    "risk_score": float(risk.risk_score),
                    "confidence": float(risk.confidence),
                    "mitigation": risk.mitigation_suggestion,
                }
            )

        high_risk_items = RiskAssessment.objects.filter(risk_score__gte=0.7).order_by(
            "-risk_score"
        )

        high_risk_alerts = []
        for risk in high_risk_items:
            if risk.entity_type == "user":
                try:
                    entity_name = User.objects.get(id=risk.entity_id).email
                except User.DoesNotExist:
                    entity_name = f"User #{risk.entity_id}"
            else:
                try:
                    entity_name = Product.objects.get(id=risk.entity_id).name
                except Product.DoesNotExist:
                    entity_name = f"Product #{risk.entity_id}"

            high_risk_alerts.append(
                {
                    "risk_type": risk.risk_type,
                    "entity_name": entity_name,
                    "risk_score": float(risk.risk_score),
                    "mitigation": risk.mitigation_suggestion,
                }
            )

        print(f"High risk alerts: {len(high_risk_alerts)}")

        return Response(
            {
                "risk_overview": risk_by_type,
                "high_risk_alerts": high_risk_alerts,
                "summary": {
                    "total_assessments": recent_risks.count(),
                    "high_risk_count": len(high_risk_alerts),
                },
            }
        )


class UserInsightsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        purchase_patterns = UserPurchasePattern.objects.filter(user=user)

        patterns_data = []
        for pattern in purchase_patterns:
            patterns_data.append(
                {
                    "category": pattern.category.name,
                    "purchase_frequency": float(pattern.purchase_frequency),
                    "average_order_value": float(pattern.average_order_value),
                    "preferred_time": pattern.preferred_time_of_day,
                    "seasonality": pattern.seasonality_factor,
                }
            )

        top_probabilities = (
            PurchaseProbability.objects.filter(user=user)
            .select_related("product")
            .order_by("-probability")[:10]
        )

        probability_data = []
        for prob in top_probabilities:
            probability_data.append(
                {
                    "product": prob.product.name,
                    "probability": float(prob.probability),
                    "confidence": float(prob.confidence_level),
                }
            )

        user_risks = RiskAssessment.objects.filter(
            entity_type="user", entity_id=user_id
        ).order_by("-assessment_date")

        risks_data = []
        for risk in user_risks:
            risks_data.append(
                {
                    "risk_type": risk.risk_type,
                    "risk_score": float(risk.risk_score),
                    "confidence": float(risk.confidence),
                    "mitigation": risk.mitigation_suggestion,
                    "assessment_date": risk.assessment_date,
                }
            )

        return Response(
            {
                "user_profile": {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "date_joined": user.date_joined,
                },
                "purchase_patterns": patterns_data,
                "purchase_probabilities": probability_data,
                "risk_assessment": risks_data,
                "insights": {
                    "total_lifetime_value": self.calculate_lifetime_value(user),
                    "churn_risk": self.get_churn_risk(user),
                    "next_likely_purchase": self.predict_next_purchase(user),
                },
            }
        )

    def calculate_lifetime_value(self, user):
        lifetime_value = (
            OrderProduct.objects.filter(order__user=user).aggregate(
                total=Sum(F("quantity") * F("product__price"))
            )["total"]
            or 0
        )
        return float(lifetime_value)

    def get_churn_risk(self, user):
        churn_risk = (
            RiskAssessment.objects.filter(
                entity_type="user", entity_id=user.id, risk_type="customer_churn"
            )
            .order_by("-assessment_date")
            .first()
        )

        if churn_risk:
            return {
                "risk_score": float(churn_risk.risk_score),
                "confidence": float(churn_risk.confidence),
            }
        return None

    def predict_next_purchase(self, user):
        last_order = Order.objects.filter(user=user).order_by("-date_order").first()
        if not last_order:
            return None

        orders = Order.objects.filter(user=user).order_by("date_order")
        if orders.count() < 2:
            return None

        time_diffs = []
        for i in range(1, orders.count()):
            diff = (orders[i].date_order - orders[i - 1].date_order).days
            time_diffs.append(diff)

        if time_diffs:
            avg_days_between = sum(time_diffs) / len(time_diffs)
            next_purchase_date = last_order.date_order + timedelta(
                days=avg_days_between
            )

            return {
                "predicted_date": next_purchase_date,
                "confidence": "medium" if len(time_diffs) > 3 else "low",
                "days_until": (next_purchase_date - datetime.now()).days,
            }

        return None


class ClientProbabilisticInsightsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        top_products = (
            PurchaseProbability.objects.filter(user=user)
            .select_related("product")
            .order_by("-probability")[:5]
        )

        product_suggestions = []
        for prob in top_products:
            product_data = ProductSerializer(prob.product).data
            product_data["match_score"] = int(float(prob.probability) * 100)
            product_suggestions.append(product_data)

        patterns = UserPurchasePattern.objects.filter(user=user)

        best_category = patterns.order_by("-purchase_frequency").first()

        preferred_time = None
        if patterns:
            times = [p.preferred_time_of_day for p in patterns]
            if times:
                preferred_time = max(set(times), key=times.count)

        return Response(
            {
                "personalized_suggestions": product_suggestions,
                "your_shopping_profile": {
                    "favorite_category": (
                        best_category.category.name if best_category else None
                    ),
                    "best_shopping_time": preferred_time,
                    "savings_potential": self.calculate_savings_potential(user),
                },
                "recommendations": {
                    "next_purchase_timing": self.get_optimal_purchase_time(user),
                    "seasonal_tips": self.get_seasonal_recommendations(user),
                },
            }
        )

    def calculate_savings_potential(self, user):
        recent_orders = Order.objects.filter(
            user=user, date_order__gte=datetime.now() - timedelta(days=30)
        )

        if recent_orders:
            return "15-20% by timing your purchases better"
        return "No recent purchase data"

    def get_optimal_purchase_time(self, user):
        patterns = UserPurchasePattern.objects.filter(user=user)

        if patterns:
            times = [p.preferred_time_of_day for p in patterns]
            if times:
                most_common_time = max(set(times), key=times.count)

                time_mapping = {
                    "morning": "Consider shopping in the morning for a wider selection",
                    "afternoon": "Afternoon deals are often available - check for flash sales",
                    "evening": "Evening shopping may have fewer users, faster checkout",
                    "night": "Late night shopping often has fewer competitors for deals",
                }

                return time_mapping.get(
                    most_common_time, "Shop when it's convenient for you"
                )

        return "No specific recommendation based on your history"

    def get_seasonal_recommendations(self, user):
        current_month = datetime.now().month

        patterns = UserPurchasePattern.objects.filter(user=user)
        seasonal_tips = []

        for pattern in patterns:
            if pattern.seasonality_factor:
                current_month_purchases = pattern.seasonality_factor.get(
                    str(current_month), 0
                )

                if current_month_purchases > 0:
                    seasonal_tips.append(
                        f"You often buy {pattern.category.name} products in this month"
                    )

        if not seasonal_tips:
            seasonal_tips.append("No specific seasonal patterns found")

        return seasonal_tips


class AdminPurchasePatternsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        all_patterns = UserPurchasePattern.objects.all().select_related(
            "user", "category"
        )

        patterns_by_user = {}
        for pattern in all_patterns:
            if pattern.user.id not in patterns_by_user:
                patterns_by_user[pattern.user.id] = {
                    "user": {"id": pattern.user.id, "email": pattern.user.email},
                    "patterns": [],
                }

            patterns_by_user[pattern.user.id]["patterns"].append(
                {
                    "category": pattern.category.name,
                    "purchase_frequency": float(pattern.purchase_frequency),
                    "average_order_value": float(pattern.average_order_value),
                    "preferred_time": pattern.preferred_time_of_day,
                    "seasonality": pattern.seasonality_factor,
                }
            )

        return Response(
            {
                "purchase_patterns": list(patterns_by_user.values()),
                "summary": {
                    "total_users": len(patterns_by_user),
                    "total_patterns": all_patterns.count(),
                },
            }
        )


class AdminProductRecommendationsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.filter(role="client")

        recommendations_by_user = []
        for user in users:
            top_probabilities = (
                PurchaseProbability.objects.filter(user=user)
                .select_related("product")
                .order_by("-probability")[:5]
            )

            user_recommendations = {
                "user": {"id": user.id, "email": user.email},
                "recommendations": [],
            }

            for prob in top_probabilities:
                user_recommendations["recommendations"].append(
                    {
                        "product": prob.product.name,
                        "product_id": prob.product.id,
                        "probability": float(prob.probability),
                        "confidence": float(prob.confidence_level),
                        "price": (
                            float(prob.product.price)
                            if hasattr(prob.product, "price")
                            else None
                        ),
                    }
                )

            recommendations_by_user.append(user_recommendations)

        return Response(
            {
                "user_recommendations": recommendations_by_user,
                "summary": {
                    "total_users": len(recommendations_by_user),
                    "recommendation_threshold": 0.5,
                },
            }
        )


class AdminChurnPredictionView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        churn_risks = RiskAssessment.objects.filter(
            risk_type="customer_churn", entity_type="user"
        ).order_by("-risk_score")

        churn_data = []
        for risk in churn_risks:
            try:
                user = User.objects.get(id=risk.entity_id)
                user_name = (
                    f"{user.first_name} {user.last_name}"
                    if user.first_name
                    else user.email
                )
            except User.DoesNotExist:
                user_name = f"User #{risk.entity_id}"

            churn_data.append(
                {
                    "user_id": risk.entity_id,
                    "user_name": user_name,
                    "risk_score": float(risk.risk_score),
                    "confidence": float(risk.confidence),
                    "mitigation": risk.mitigation_suggestion,
                    "assessment_date": risk.assessment_date,
                }
            )

        return Response(
            {
                "churn_predictions": churn_data,
                "summary": {
                    "total_users_analyzed": len(churn_data),
                    "high_risk_users": len(
                        [data for data in churn_data if data["risk_score"] > 0.7]
                    ),
                    "medium_risk_users": len(
                        [
                            data
                            for data in churn_data
                            if 0.4 <= data["risk_score"] <= 0.7
                        ]
                    ),
                    "low_risk_users": len(
                        [data for data in churn_data if data["risk_score"] < 0.4]
                    ),
                },
            }
        )
