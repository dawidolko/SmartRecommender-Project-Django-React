# home/probabilistic_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg, F, Q
from datetime import date, datetime, timedelta
from decimal import Decimal
from home.models import (
    User, Product, Order, OrderProduct,
    PurchaseProbability, SalesForecast, UserPurchasePattern,
    ProductDemandForecast, RiskAssessment
)
from home.permissions import IsAdminUser
from home.serializers import ProductSerializer


class UserPurchasePredictionView(APIView):
    """Przewidywanie następnego zakupu użytkownika"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Pobierz top 10 produktów z największym prawdopodobieństwem zakupu
        predicted_products = PurchaseProbability.objects.filter(
            user=user
        ).select_related('product').order_by('-probability')[:10]
        
        predictions = []
        for prediction in predicted_products:
            product_data = ProductSerializer(prediction.product).data
            product_data['purchase_probability'] = float(prediction.probability)
            product_data['confidence'] = float(prediction.confidence_level)
            predictions.append(product_data)
        
        return Response({
            'predictions': predictions,
            'message': f"Based on your purchase history, these products might interest you."
        })


class PersonalizedRecommendationsView(APIView):
    """Personalizowane rekomendacje oparte o modele probabilistyczne"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Analizuj wzorce zakupowe użytkownika
        purchase_patterns = UserPurchasePattern.objects.filter(user=user)
        
        recommendations = []
        for pattern in purchase_patterns:
            # Znajdź produkty w tej kategorii
            category_products = Product.objects.filter(
                categories=pattern.category
            ).prefetch_related('photoproduct_set')
            
            # Filtruj produkty, które użytkownik już kupił
            already_purchased = OrderProduct.objects.filter(
                order__user=user
            ).values_list('product_id', flat=True)
            
            new_products = category_products.exclude(id__in=already_purchased)
            
            for product in new_products[:3]:  # Pobierz top 3 z każdej kategorii
                recommendations.append({
                    'product': ProductSerializer(product).data,
                    'category': pattern.category.name,
                    'purchase_frequency': float(pattern.purchase_frequency),
                    'average_order_value': float(pattern.average_order_value),
                    'next_purchase_likely': self.calculate_next_purchase_time(pattern)
                })
        
        return Response({
            'recommendations': recommendations,
            'user_insights': {
                'most_active_category': self.get_most_active_category(user),
                'preferred_shopping_time': self.get_preferred_time(user)
            }
        })
    
    def calculate_next_purchase_time(self, pattern):
        """Oblicza przewidywany czas następnego zakupu"""
        if pattern.purchase_frequency > 0:
            days_until_next = 30 / pattern.purchase_frequency
            return f"in {int(days_until_next)} days"
        return "unknown"
    
    def get_most_active_category(self, user):
        """Zwraca najbardziej aktywną kategorię użytkownika"""
        most_active = UserPurchasePattern.objects.filter(
            user=user
        ).order_by('-purchase_frequency').first()
        
        if most_active:
            return most_active.category.name
        return "No data"
    
    def get_preferred_time(self, user):
        """Zwraca preferowaną porę zakupów"""
        times = UserPurchasePattern.objects.filter(
            user=user
        ).values_list('preferred_time_of_day', flat=True)
        
        if times:
            # Zwróć najczęściej występującą porę
            return max(set(times), key=lambda x: list(times).count(x))
        return "No preference"


class SalesForecastView(APIView):
    """Widok prognoz sprzedaży dla admina"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        current_date = date.today()
        end_date = current_date + timedelta(days=30)
        
        forecasts = SalesForecast.objects.filter(
            forecast_date__gte=current_date,
            forecast_date__lte=end_date
        ).select_related('product').order_by('forecast_date')
        
        print(f"Found {forecasts.count()} forecasts for period {current_date} to {end_date}")
        
        results = []
        for forecast in forecasts:
            results.append({
                'product': {
                    'id': forecast.product.id,
                    'name': forecast.product.name
                },
                'forecast_date': forecast.forecast_date,
                'predicted_quantity': forecast.predicted_quantity,
                'confidence_interval': [
                    forecast.confidence_interval_lower,
                    forecast.confidence_interval_upper
                ],
                'historical_accuracy': float(forecast.historical_accuracy or 0)
            })
        
        print(f"Returning {len(results)} results")
        
        return Response({
            'forecasts': results,
            'summary': {
                'total_predicted_units': sum(f['predicted_quantity'] for f in results),
                'period': f"30 days",
                'from_date': current_date,
                'to_date': end_date
            }
        })


class ProductDemandView(APIView):
    """Widok zapotrzebowania na produkty"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        demands = ProductDemandForecast.objects.select_related(
            'product'
        ).order_by('period_start')
        
        print(f"Found {demands.count()} demand forecasts")
        
        results = []
        for demand in demands:
            results.append({
                'product': {
                    'id': demand.product.id,
                    'name': demand.product.name
                },
                'forecast_period': demand.forecast_period,
                'period_start': demand.period_start,
                'expected_demand': float(demand.expected_demand),
                'demand_variance': float(demand.demand_variance),
                'reorder_point': demand.reorder_point,
                'suggested_stock_level': demand.suggested_stock_level
            })
        
        low_stock_alerts = []
        for demand in demands:
            if demand.forecast_period == 'month':
                if demand.expected_demand > demand.reorder_point:
                    low_stock_alerts.append({
                        'product': demand.product.name,
                        'action_needed': 'Reorder needed',
                        'suggested_quantity': demand.suggested_stock_level
                    })
        
        return Response({
            'demand_forecasts': results,
            'alerts': low_stock_alerts,
            'summary': {
                'products_analyzed': len(demands),
                'action_required': len(low_stock_alerts)
            }
        })


class RiskDashboardView(APIView):
    """Dashboard oceny ryzyka"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        recent_risks = RiskAssessment.objects.order_by('-assessment_date')
        
        print(f"Found {recent_risks.count()} risk assessments")
        
        risk_by_type = {}
        for risk in recent_risks:
            if risk.risk_type not in risk_by_type:
                risk_by_type[risk.risk_type] = []
            
            risk_by_type[risk.risk_type].append({
                'entity_type': risk.entity_type,
                'entity_id': risk.entity_id,
                'risk_score': float(risk.risk_score),
                'confidence': float(risk.confidence),
                'mitigation': risk.mitigation_suggestion
            })
        
        high_risk_items = RiskAssessment.objects.filter(
            risk_score__gte=0.7
        ).order_by('-risk_score')
        
        high_risk_alerts = []
        for risk in high_risk_items:
            if risk.entity_type == 'user':
                try:
                    entity_name = User.objects.get(id=risk.entity_id).email
                except User.DoesNotExist:
                    entity_name = f"User #{risk.entity_id}"
            else:  # product
                try:
                    entity_name = Product.objects.get(id=risk.entity_id).name
                except Product.DoesNotExist:
                    entity_name = f"Product #{risk.entity_id}"
            
            high_risk_alerts.append({
                'risk_type': risk.risk_type,
                'entity_name': entity_name,
                'risk_score': float(risk.risk_score),
                'mitigation': risk.mitigation_suggestion
            })
        
        print(f"High risk alerts: {len(high_risk_alerts)}")
        
        return Response({
            'risk_overview': risk_by_type,
            'high_risk_alerts': high_risk_alerts,
            'summary': {
                'total_assessments': recent_risks.count(),
                'high_risk_count': len(high_risk_alerts)
            }
        })


class UserInsightsView(APIView):
    """Szczegółowe analizy użytkownika dla admina"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Wzorce zakupowe
        purchase_patterns = UserPurchasePattern.objects.filter(user=user)
        
        patterns_data = []
        for pattern in purchase_patterns:
            patterns_data.append({
                'category': pattern.category.name,
                'purchase_frequency': float(pattern.purchase_frequency),
                'average_order_value': float(pattern.average_order_value),
                'preferred_time': pattern.preferred_time_of_day,
                'seasonality': pattern.seasonality_factor
            })
        
        # Prawdopodobieństwa zakupu
        top_probabilities = PurchaseProbability.objects.filter(
            user=user
        ).select_related('product').order_by('-probability')[:10]
        
        probability_data = []
        for prob in top_probabilities:
            probability_data.append({
                'product': prob.product.name,
                'probability': float(prob.probability),
                'confidence': float(prob.confidence_level)
            })
        
        # Ocena ryzyka dla użytkownika
        user_risks = RiskAssessment.objects.filter(
            entity_type='user',
            entity_id=user_id
        ).order_by('-assessment_date')
        
        risks_data = []
        for risk in user_risks:
            risks_data.append({
                'risk_type': risk.risk_type,
                'risk_score': float(risk.risk_score),
                'confidence': float(risk.confidence),
                'mitigation': risk.mitigation_suggestion,
                'assessment_date': risk.assessment_date
            })
        
        return Response({
            'user_profile': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined
            },
            'purchase_patterns': patterns_data,
            'purchase_probabilities': probability_data,
            'risk_assessment': risks_data,
            'insights': {
                'total_lifetime_value': self.calculate_lifetime_value(user),
                'churn_risk': self.get_churn_risk(user),
                'next_likely_purchase': self.predict_next_purchase(user)
            }
        })
    
    def calculate_lifetime_value(self, user):
        """Oblicza całkowitą wartość klienta"""
        lifetime_value = OrderProduct.objects.filter(
            order__user=user
        ).aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0
        return float(lifetime_value)
    
    def get_churn_risk(self, user):
        """Pobiera ryzyko odpływu klienta"""
        churn_risk = RiskAssessment.objects.filter(
            entity_type='user',
            entity_id=user.id,
            risk_type='customer_churn'
        ).order_by('-assessment_date').first()
        
        if churn_risk:
            return {
                'risk_score': float(churn_risk.risk_score),
                'confidence': float(churn_risk.confidence)
            }
        return None
    
    def predict_next_purchase(self, user):
        """Przewiduje następny zakup"""
        last_order = Order.objects.filter(user=user).order_by('-date_order').first()
        if not last_order:
            return None
        
        # Analiza średniego czasu między zakupami
        orders = Order.objects.filter(user=user).order_by('date_order')
        if orders.count() < 2:
            return None
        
        time_diffs = []
        for i in range(1, orders.count()):
            diff = (orders[i].date_order - orders[i-1].date_order).days
            time_diffs.append(diff)
        
        if time_diffs:
            avg_days_between = sum(time_diffs) / len(time_diffs)
            next_purchase_date = last_order.date_order + timedelta(days=avg_days_between)
            
            return {
                'predicted_date': next_purchase_date,
                'confidence': 'medium' if len(time_diffs) > 3 else 'low',
                'days_until': (next_purchase_date - datetime.now()).days
            }
        
        return None


class ClientProbabilisticInsightsView(APIView):
    """Widok dla klienta z personalizowanymi insightami"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Najbardziej prawdopodobne produkty
        top_products = PurchaseProbability.objects.filter(
            user=user
        ).select_related('product').order_by('-probability')[:5]
        
        product_suggestions = []
        for prob in top_products:
            product_data = ProductSerializer(prob.product).data
            product_data['match_score'] = int(float(prob.probability) * 100)
            product_suggestions.append(product_data)
        
        # Analiza wzorców
        patterns = UserPurchasePattern.objects.filter(user=user)
        
        # Najlepsza kategoria
        best_category = patterns.order_by('-purchase_frequency').first()
        
        # Rekomendowane portorę zakupów
        preferred_time = None
        if patterns:
            times = [p.preferred_time_of_day for p in patterns]
            if times:
                preferred_time = max(set(times), key=times.count)
        
        return Response({
            'personalized_suggestions': product_suggestions,
            'your_shopping_profile': {
                'favorite_category': best_category.category.name if best_category else None,
                'best_shopping_time': preferred_time,
                'savings_potential': self.calculate_savings_potential(user)
            },
            'recommendations': {
                'next_purchase_timing': self.get_optimal_purchase_time(user),
                'seasonal_tips': self.get_seasonal_recommendations(user)
            }
        })
    
    def calculate_savings_potential(self, user):
        """Oblicza potencjalne oszczędności na podstawie wzorców zakupowych"""
        # To jest uproszczona wersja - w rzeczywistości użyłbyś bardziej zaawansowanej analizy
        recent_orders = Order.objects.filter(
            user=user,
            date_order__gte=datetime.now() - timedelta(days=30)
        )
        
        if recent_orders:
            return "15-20% by timing your purchases better"
        return "No recent purchase data"
    
    def get_optimal_purchase_time(self, user):
        """Sugeruje optymalny czas na zakupy"""
        patterns = UserPurchasePattern.objects.filter(user=user)
        
        if patterns:
            # Znajdź najczęstszą porę dnia
            times = [p.preferred_time_of_day for p in patterns]
            if times:
                most_common_time = max(set(times), key=times.count)
                
                time_mapping = {
                    'morning': "Consider shopping in the morning for a wider selection",
                    'afternoon': "Afternoon deals are often available - check for flash sales",
                    'evening': "Evening shopping may have fewer users, faster checkout",
                    'night': "Late night shopping often has fewer competitors for deals"
                }
                
                return time_mapping.get(most_common_time, "Shop when it's convenient for you")
        
        return "No specific recommendation based on your history"
    
    def get_seasonal_recommendations(self, user):
        """Daje sezonowe rekomendacje"""
        current_month = datetime.now().month
        
        patterns = UserPurchasePattern.objects.filter(user=user)
        seasonal_tips = []
        
        for pattern in patterns:
            if pattern.seasonality_factor:
                current_month_purchases = pattern.seasonality_factor.get(str(current_month), 0)
                
                if current_month_purchases > 0:
                    seasonal_tips.append(f"You often buy {pattern.category.name} products in this month")
        
        if not seasonal_tips:
            seasonal_tips.append("No specific seasonal patterns found")
        
        return seasonal_tips