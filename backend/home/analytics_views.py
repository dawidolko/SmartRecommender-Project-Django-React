"""
Predictive Analytics API Views for SmartRecommender E-commerce System.

Authors: Dawid Olko & Piotr Smoła
Date: 2025-11-02
Version: 2.0

This module contains REST API views for advanced analytics including:
    - Risk dashboard (churn prediction, fraud detection)
    - Sales forecasting (ARIMA-inspired time series)
    - Purchase probability prediction (Naive Bayes)
    - Product demand forecasting for inventory management
    - User purchase pattern analysis (RFM segmentation)

Key Features:
    - Real-time predictive analytics
    - Personalized insights for users
    - Admin dashboard with comprehensive metrics
    - Machine learning-based forecasting
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Sum, Avg, Count, F, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal
from collections import defaultdict

from .models import (
    User,
    Order,
    OrderProduct, 
    Product,
    PurchaseProbability,
    SalesForecast,
    UserPurchasePattern,
    ProductDemandForecast,
    RiskAssessment,
)
from .serializers import ProductSerializer


class RiskDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_risks = RiskAssessment.objects.filter(
                entity_type="user",
                entity_id=request.user.id
            ).order_by('-assessment_date')[:5]

            risk_data = []
            for risk in user_risks:
                risk_data.append({
                    'risk_type': risk.risk_type,
                    'risk_score': float(risk.risk_score),
                    'confidence': float(risk.confidence),
                    'mitigation': risk.mitigation_suggestion,
                    'created_at': risk.assessment_date.strftime('%Y-%m-%d')
                })

            recent_risk = user_risks.first() if user_risks else None
            overall_risk = {
                'current_risk_score': float(recent_risk.risk_score) if recent_risk else 0.5,
                'risk_level': 'High' if (recent_risk and recent_risk.risk_score > 0.7) else 'Medium' if (recent_risk and recent_risk.risk_score > 0.4) else 'Low',
                'confidence': float(recent_risk.confidence) if recent_risk else 0.0,
                'recommendation': recent_risk.mitigation_suggestion if recent_risk else "No specific recommendations at this time."
            }

            return Response({
                'success': True,
                'risk_assessments': risk_data,
                'overall_risk': overall_risk,
                'total_assessments': len(risk_data)
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SalesForecastView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_orders = Order.objects.filter(user=request.user)
            if not user_orders.exists():
                return Response({
                    'success': True,
                    'forecasts': [],
                    'message': 'No purchase history available for forecasting.'
                })

            purchased_products = Product.objects.filter(
                orderproduct__order__user=request.user
            ).distinct()[:10]

            forecasts = []
            for product in purchased_products:
                product_forecasts = SalesForecast.objects.filter(
                    product=product,
                    forecast_date__gte=date.today()
                ).order_by('forecast_date')[:7]

                for forecast in product_forecasts:
                    forecasts.append({
                        'product': {
                            'id': product.id,
                            'name': product.name
                        },
                        'forecast_date': forecast.forecast_date.strftime('%Y-%m-%d'),
                        'predicted_quantity': forecast.predicted_quantity,
                        'confidence_lower': forecast.confidence_interval_lower,
                        'confidence_upper': forecast.confidence_interval_upper,
                        'accuracy': float(forecast.historical_accuracy) if forecast.historical_accuracy else 75.0
                    })

            return Response({
                'success': True,
                'forecasts': forecasts,
                'total_products': len(forecasts)
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDemandView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_orders = Order.objects.filter(user=request.user)
            if not user_orders.exists():
                return Response({
                    'success': True,
                    'demand_forecasts': [],
                    'message': 'No purchase history available for demand analysis.'
                })

            user_categories = Product.objects.filter(
                orderproduct__order__user=request.user
            ).values_list('categories__id', flat=True).distinct()

            relevant_products = Product.objects.filter(
                categories__id__in=user_categories
            ).distinct()[:10]

            demand_data = []
            for product in relevant_products:
                demand_forecasts = ProductDemandForecast.objects.filter(
                    product=product,
                    period_start__gte=date.today()
                ).order_by('period_start')

                product_data = {
                    'product_id': product.id,
                    'product_name': product.name,
                    'demand_by_period': {}
                }

                for forecast in demand_forecasts:
                    product_data['demand_by_period'][forecast.forecast_period] = {
                        'expected_demand': float(forecast.expected_demand),
                        'demand_variance': float(forecast.demand_variance),
                        'reorder_point': forecast.reorder_point,
                        'suggested_stock': forecast.suggested_stock_level,
                        'period_start': forecast.period_start.strftime('%Y-%m-%d')
                    }

                demand_data.append(product_data)

            return Response({
                'success': True,
                'demand_forecasts': demand_data,
                'total_products': len(demand_data)
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserPurchasePatternsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patterns = UserPurchasePattern.objects.filter(user=request.user)
            
            if not patterns.exists():
                return Response({
                    'success': True,
                    'patterns': [],
                    'summary': {},
                    'message': 'No purchase patterns available yet.'
                })

            pattern_data = []
            total_frequency = 0
            total_value = 0
            preferred_times = []

            for pattern in patterns:
                from .models import Category
                try:
                    category = Category.objects.get(id=pattern.category_id)
                    category_name = category.name
                except Category.DoesNotExist:
                    category_name = f"Category {pattern.category_id}"

                pattern_info = {
                    'category_id': pattern.category_id,
                    'category_name': category_name,
                    'purchase_frequency': float(pattern.purchase_frequency),
                    'average_order_value': float(pattern.average_order_value),
                    'preferred_time': pattern.preferred_time_of_day,
                    'seasonality': pattern.seasonality_factor
                }
                pattern_data.append(pattern_info)
                
                total_frequency += float(pattern.purchase_frequency)
                total_value += float(pattern.average_order_value)
                preferred_times.append(pattern.preferred_time_of_day)

            avg_frequency = total_frequency / len(patterns) if patterns else 0
            avg_order_value = total_value / len(patterns) if patterns else 0
            most_common_time = max(set(preferred_times), key=preferred_times.count) if preferred_times else "Any time"

            summary = {
                'total_categories': len(patterns),
                'average_purchase_frequency': round(avg_frequency, 2),
                'average_order_value': round(avg_order_value, 2),
                'most_preferred_time': most_common_time
            }

            return Response({
                'success': True,
                'patterns': pattern_data,
                'summary': summary
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminPurchasePatternsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            users = User.objects.filter(order__isnull=False).distinct()[:10]
            
            purchase_patterns_data = []
            for user in users:
                patterns = UserPurchasePattern.objects.filter(user=user)
                
                user_patterns = []
                for pattern in patterns:
                    try:
                        from .models import Category
                        category = Category.objects.get(id=pattern.category_id)
                        category_name = category.name
                    except Category.DoesNotExist:
                        category_name = f"Category {pattern.category_id}"
                    
                    user_patterns.append({
                        'category': category_name,
                        'purchase_frequency': float(pattern.purchase_frequency),
                        'average_order_value': float(pattern.average_order_value),
                        'preferred_time': pattern.preferred_time_of_day
                    })
                
                if user_patterns:
                    purchase_patterns_data.append({
                        'user': {
                            'id': user.id,
                            'email': user.email
                        },
                        'patterns': user_patterns
                    })

            return Response({
                'purchase_patterns': purchase_patterns_data,
                'summary': {
                    'total_users': len(purchase_patterns_data),
                    'total_patterns': sum(len(u['patterns']) for u in purchase_patterns_data)
                }
            })

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminProductRecommendationsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            users = User.objects.filter(order__isnull=False).distinct()[:10]
            
            user_recommendations_data = []
            for user in users:
                probabilities = PurchaseProbability.objects.filter(user=user).order_by('-probability')[:5]
                
                recommendations = []
                for prob in probabilities:
                    recommendations.append({
                        'product': prob.product.name,
                        'probability': float(prob.probability),
                        'confidence': float(prob.confidence_level),
                        'price': float(prob.product.price)
                    })
                
                if recommendations:
                    user_recommendations_data.append({
                        'user': {
                            'id': user.id,
                            'email': user.email
                        },
                        'recommendations': recommendations
                    })

            return Response({
                'user_recommendations': user_recommendations_data
            })

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminChurnPredictionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            churn_risks = RiskAssessment.objects.filter(risk_type='customer_churn')
            
            high_risk = churn_risks.filter(risk_score__gte=0.7).count()
            medium_risk = churn_risks.filter(risk_score__gte=0.4, risk_score__lt=0.7).count()
            low_risk = churn_risks.filter(risk_score__lt=0.4).count()

            churn_predictions = []
            for risk in churn_risks[:20]:
                try:
                    user = User.objects.get(id=risk.entity_id)
                    churn_predictions.append({
                        'user_name': user.email,
                        'risk_score': float(risk.risk_score),
                        'confidence': float(risk.confidence),
                        'mitigation': risk.mitigation_suggestion or "No mitigation suggested"
                    })
                except User.DoesNotExist:
                    continue

            return Response({
                'churn_predictions': churn_predictions,
                'summary': {
                    'high_risk_users': high_risk,
                    'medium_risk_users': medium_risk,
                    'low_risk_users': low_risk
                }
            })

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyShoppingInsightsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        try:
            user_orders = Order.objects.filter(user=user)
            total_orders = user_orders.count()
            
            if total_orders == 0:
                sample_products = Product.objects.annotate(
                    order_count=Count('orderproduct')
                ).order_by('-order_count')[:6]

                personalized_suggestions = []

                max_orders = sample_products.first().order_count if sample_products.exists() else 1

                for product in sample_products:
                    product_photos = product.photoproduct_set.all()
                    photos_data = []
                    if product_photos.exists():
                        photos_data = [{
                            'id': photo.id,
                            'path': photo.path,
                            'sequence': getattr(photo, 'sequence', 1)
                        } for photo in product_photos]

                    if max_orders > 0:
                        match_score = 50 + int((product.order_count / max_orders) * 30)
                    else:
                        match_score = 50

                    personalized_suggestions.append({
                        'id': product.id,
                        'name': product.name,
                        'price': float(product.price),
                        'match_score': match_score,
                        'image_url': None,
                        'photos': photos_data
                    })
                
                return Response({
                    'success': True,
                    'message': 'Welcome! Start shopping to get personalized insights.',
                    'personalized_suggestions': personalized_suggestions,
                    'your_shopping_profile': {
                        'total_orders': 0,
                        'total_spent': 0.0,
                        'average_order_value': 0.0,
                        'favorite_category': 'Not yet determined',
                        'shopping_frequency': 'New customer',
                        'days_since_last_order': None,
                        'loyalty_score': 0,
                        'best_shopping_time': 'Anytime',
                        'savings_potential': 'Start shopping to calculate'
                    },
                    'spending_patterns': [],
                    'category_preferences': [],
                    'seasonal_insights': {
                        'best_month': 'N/A',
                        'seasonal_pattern': 'No data available yet'
                    },
                    'recommendations': {
                        'next_purchase_prediction': 'Make your first purchase!',
                        'suggested_categories': ['Electronics', 'Books', 'Clothing'],
                        'budget_recommendation': 'Start with a small budget to explore our products.',
                        'seasonal_tips': [
                            'Welcome to our platform! Explore our product categories.',
                            'Check out our featured products for great deals.',
                            'Sign up for our newsletter to get exclusive offers.'
                        ]
                    }
                })

            total_spent = Decimal('0.00')
            category_spending = defaultdict(Decimal)
            category_counts = defaultdict(int)
            monthly_spending = defaultdict(Decimal)
            
            for order in user_orders:
                for order_product in order.orderproduct_set.all():
                    item_total = Decimal(str(order_product.product.price)) * order_product.quantity
                    total_spent += item_total
                    
                    for category in order_product.product.categories.all():
                        category_spending[category.name] += item_total
                        category_counts[category.name] += 1
                    
                    month_key = order.date_order.strftime('%Y-%m')
                    monthly_spending[month_key] += item_total
            
            avg_order_value = total_spent / total_orders if total_orders > 0 else Decimal('0.00')
            
            last_order = user_orders.order_by('-date_order').first()
            days_since_last_order = (timezone.now().date() - last_order.date_order.date()).days if last_order else 999
            
            favorite_category = max(category_spending, key=category_spending.get) if category_spending else 'None'
            
            if user_orders.exists():
                first_order = user_orders.order_by('date_order').first()
                days_active = (timezone.now().date() - first_order.date_order.date()).days
                months_active = max(days_active / 30, 1)
                orders_per_month = total_orders / months_active
                
                if orders_per_month >= 2:
                    shopping_frequency = 'Very Active'
                elif orders_per_month >= 1:
                    shopping_frequency = 'Active'
                elif orders_per_month >= 0.5:
                    shopping_frequency = 'Moderate'
                else:
                    shopping_frequency = 'Occasional'
            else:
                shopping_frequency = 'Never'
            
            loyalty_score = min(100, (total_orders * 5) + (min(float(total_spent)/1000, 50)) + (max(0, 30 - days_since_last_order)))
            
            personalized_suggestions = self._generate_personalized_suggestions(user, category_spending)
            
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            spending_patterns = []
            
            current_year = timezone.now().year
            for month_num in range(1, 13):
                month_key = f"{current_year}-{month_num:02d}"
                total = float(monthly_spending.get(month_key, 0))
                spending_patterns.append({
                    'month': month_names[month_num - 1],
                    'total_spent': total
                })
            
            category_preferences = []
            sorted_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for category, spending in sorted_categories:
                category_preferences.append({
                    'category': category,
                    'total_spent': float(spending),
                    'order_count': category_counts[category],
                    'percentage': (float(spending) / float(total_spent) * 100) if total_spent > 0 else 0
                })
            
            best_month = max(spending_patterns, key=lambda x: x['total_spent'])['month'] if any(p['total_spent'] > 0 for p in spending_patterns) else 'N/A'
            
            if days_since_last_order < 30:
                next_purchase_prediction = f"Likely within {30 - days_since_last_order} days"
            elif days_since_last_order < 60:
                next_purchase_prediction = "May purchase within 2-4 weeks"
            else:
                next_purchase_prediction = "Consider browsing our latest products"
            
            if avg_order_value > 0:
                budget_recommendation = f"Your typical order value is ${float(avg_order_value):.2f}. Consider budgeting ${float(avg_order_value * Decimal('1.2')):.2f} for your next purchase."
            else:
                budget_recommendation = "Start with a small budget to explore products."
            
            seasonal_tips = self._generate_seasonal_tips(favorite_category, shopping_frequency, days_since_last_order)
            
            best_shopping_time = self._determine_best_shopping_time(user_orders)
            
            savings_potential = self._calculate_savings_potential(total_spent, avg_order_value)

            return Response({
                'success': True,
                'personalized_suggestions': personalized_suggestions,
                'your_shopping_profile': {
                    'total_orders': total_orders,
                    'total_spent': float(total_spent),
                    'average_order_value': float(avg_order_value),
                    'favorite_category': favorite_category,
                    'shopping_frequency': shopping_frequency,
                    'days_since_last_order': days_since_last_order,
                    'loyalty_score': round(loyalty_score, 1),
                    'best_shopping_time': best_shopping_time,
                    'savings_potential': savings_potential
                },
                'spending_patterns': spending_patterns,
                'category_preferences': category_preferences,
                'seasonal_insights': {
                    'best_month': best_month,
                    'seasonal_pattern': 'Your spending varies by season' if len([p for p in spending_patterns if p['total_spent'] > 0]) > 3 else 'Limited seasonal data'
                },
                'recommendations': {
                    'next_purchase_prediction': next_purchase_prediction,
                    'suggested_categories': [cat['category'] for cat in category_preferences[:3]] or ['Electronics', 'Books', 'Clothing'],
                    'budget_recommendation': budget_recommendation,
                    'seasonal_tips': seasonal_tips
                }
            })

        except Exception as e:
            print(f"Error in MyShoppingInsightsView: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return Response({
                'success': False,
                'error': f'Unable to load shopping insights: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _generate_personalized_suggestions(self, user, category_spending):
        try:
            suggestions = []
            
            if category_spending:
                favorite_categories = list(category_spending.keys())[:3]
                products = Product.objects.filter(
                    categories__name__in=favorite_categories
                ).exclude(
                    orderproduct__order__user=user
                ).distinct()[:10]
            else:
                products = Product.objects.all().order_by('?')[:10]
            
            for i, product in enumerate(products):
                product_photos = product.photoproduct_set.all()
                photos_data = []
                if product_photos.exists():
                    photos_data = [{
                        'id': photo.id,
                        'path': photo.path,
                        'sequence': getattr(photo, 'sequence', 1)
                    } for photo in product_photos]
                
                if category_spending:
                    product_categories = [cat.name for cat in product.categories.all()]
                    match_score = 0
                    total_spending = sum(category_spending.values())

                    for cat in product_categories:
                        if cat in category_spending:
                            category_weight = (category_spending[cat] / total_spending) * 100
                            match_score += category_weight

                    match_score = min(95, max(60, int(match_score)))
                else:
                    order_count = product.orderproduct_set.count()
                    match_score = min(80, 50 + int(order_count * 0.3))
                
                suggestions.append({
                    'id': product.id,
                    'name': product.name,
                    'price': float(product.price),
                    'match_score': match_score,
                    'image_url': None,
                    'photos': photos_data
                })
            
            return suggestions[:6]
            
        except Exception as e:
            print(f"Error generating suggestions: {e}")
            return []

    def _generate_seasonal_tips(self, favorite_category, shopping_frequency, days_since_last_order):
        tips = []
        
        if days_since_last_order > 60:
            tips.append("We miss you! Check out our latest arrivals and special offers.")
        elif days_since_last_order < 7:
            tips.append("Thanks for being an active customer! Look out for our loyalty rewards.")
        
        if favorite_category and favorite_category != 'None':
            tips.append(f"Since you love {favorite_category}, check out our newest {favorite_category.lower()} products.")
        
        if shopping_frequency == 'Very Active':
            tips.append("As a frequent shopper, you might enjoy our VIP member benefits.")
        elif shopping_frequency == 'Occasional':
            tips.append("Consider setting up wishlist alerts for products you're interested in.")
        
        current_month = timezone.now().month
        if current_month in [12, 1, 2]:
            tips.append("Winter season: Great time for electronics and indoor products.")
        elif current_month in [3, 4, 5]:
            tips.append("Spring season: Perfect time for home & garden products.")
        elif current_month in [6, 7, 8]:
            tips.append("Summer season: Check out our outdoor and sports categories.")
        else:
            tips.append("Fall season: Great deals on back-to-school and winter prep items.")
        
        return tips[:4]

    def _determine_best_shopping_time(self, user_orders):
        if not user_orders.exists():
            return "Anytime"
        
        hour_counts = defaultdict(int)
        weekday_counts = defaultdict(int)
        
        for order in user_orders:
            hour_counts[order.date_order.hour] += 1
            weekday_counts[order.date_order.weekday()] += 1
        
        best_hour = max(hour_counts, key=hour_counts.get) if hour_counts else 12
        
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        best_day = weekdays[max(weekday_counts, key=weekday_counts.get)] if weekday_counts else "Wednesday"
        
        if best_hour < 12:
            time_period = f"{best_hour}:00 AM"
        elif best_hour == 12:
            time_period = "12:00 PM"
        else:
            time_period = f"{best_hour-12}:00 PM"
        
        return f"{best_day}s around {time_period}"

    def _calculate_savings_potential(self, total_spent, avg_order_value):
        if total_spent == 0:
            return "Start shopping to calculate potential savings"
        
        potential_savings = float(total_spent) * 0.15
        return f"Up to ${potential_savings:.2f} per year with smart shopping"
    
class PurchasePredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            user_orders = Order.objects.filter(user=user)
            
            if not user_orders.exists():
                return Response({
                    'success': True,
                    'predictions': [],
                    'message': 'No purchase history available for predictions.'
                })

            predictions = []

            user_category_spending = (
                OrderProduct.objects.filter(order__user=user)
                .values('product__categories__name')
                .annotate(
                    total_spent=Sum('product__price'),
                    order_count=Count('order', distinct=True)
                )
                .order_by('-total_spent')
            )

            favorite_categories = [item['product__categories__name'] for item in user_category_spending if item['product__categories__name']][:3]

            if favorite_categories:
                products = Product.objects.filter(
                    categories__name__in=favorite_categories
                ).exclude(
                    orderproduct__order__user=user
                ).annotate(
                    popularity=Count('orderproduct')
                ).order_by('-popularity')[:10]
            else:
                products = Product.objects.annotate(
                    popularity=Count('orderproduct')
                ).order_by('-popularity')[:10]

            total_spent_in_favs = sum(item['total_spent'] for item in user_category_spending if item['product__categories__name'] in favorite_categories)

            for product in products:
                product_categories = [cat.name for cat in product.categories.all()]

                category_match_score = 0
                for item in user_category_spending:
                    cat_name = item['product__categories__name']
                    if cat_name in product_categories and total_spent_in_favs > 0:
                        category_match_score += (item['total_spent'] / total_spent_in_favs) * 50

                popularity_score = min(30, product.popularity * 3) if hasattr(product, 'popularity') else 0

                probability = min(95, 60 + int(category_match_score) + int(popularity_score))

                predictions.append({
                    'name': product.name,
                    'purchase_probability': probability
                })

            return Response({
                'success': True,
                'predictions': predictions
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'predictions': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)