from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Sum, Avg, Count, F
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
            # Get user's risk assessments
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

            # Calculate overall risk metrics
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
            # Get user's purchase history to base forecasts on
            user_orders = Order.objects.filter(user=request.user)
            if not user_orders.exists():
                return Response({
                    'success': True,
                    'forecasts': [],
                    'message': 'No purchase history available for forecasting.'
                })

            # Get products user has purchased
            purchased_products = Product.objects.filter(
                orderproduct__order__user=request.user
            ).distinct()[:10]

            forecasts = []
            for product in purchased_products:
                product_forecasts = SalesForecast.objects.filter(
                    product=product,
                    forecast_date__gte=date.today()
                ).order_by('forecast_date')[:7]  # Next 7 days

                # Transform forecasts to match frontend expectations
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
            # Get user's interested products based on purchase history
            user_orders = Order.objects.filter(user=request.user)
            if not user_orders.exists():
                return Response({
                    'success': True,
                    'demand_forecasts': [],
                    'message': 'No purchase history available for demand analysis.'
                })

            # Get categories user has purchased from
            user_categories = Product.objects.filter(
                orderproduct__order__user=request.user
            ).values_list('categories__id', flat=True).distinct()

            # Get products from those categories
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
            # Get user's purchase patterns
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
                from .models import ProductCategory
                try:
                    category = ProductCategory.objects.get(id=pattern.category_id)
                    category_name = category.name
                except ProductCategory.DoesNotExist:
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

            # Calculate summary
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
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            # Global purchase patterns analysis
            all_patterns = UserPurchasePattern.objects.all()
            
            if not all_patterns.exists():
                return Response({
                    'success': True,
                    'global_patterns': {},
                    'category_analysis': [],
                    'message': 'No purchase patterns data available.'
                })

            # Group by category
            category_stats = defaultdict(list)
            for pattern in all_patterns:
                category_stats[pattern.category_id].append(pattern)

            category_analysis = []
            for category_id, patterns in category_stats.items():
                from .models import ProductCategory
                try:
                    category = ProductCategory.objects.get(id=category_id)
                    category_name = category.name
                except ProductCategory.DoesNotExist:
                    category_name = f"Category {category_id}"

                avg_frequency = sum(float(p.purchase_frequency) for p in patterns) / len(patterns)
                avg_order_value = sum(float(p.average_order_value) for p in patterns) / len(patterns)
                
                preferred_times = [p.preferred_time_of_day for p in patterns]
                most_common_time = max(set(preferred_times), key=preferred_times.count) if preferred_times else "Unknown"

                category_analysis.append({
                    'category_id': category_id,
                    'category_name': category_name,
                    'user_count': len(patterns),
                    'average_frequency': round(avg_frequency, 2),
                    'average_order_value': round(avg_order_value, 2),
                    'most_common_time': most_common_time
                })

            # Sort by user count
            category_analysis.sort(key=lambda x: x['user_count'], reverse=True)

            global_patterns = {
                'total_patterns': len(all_patterns),
                'unique_categories': len(category_stats),
                'top_categories': category_analysis[:5]
            }

            return Response({
                'success': True,
                'global_patterns': global_patterns,
                'category_analysis': category_analysis
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminProductRecommendationsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            # Get product recommendation statistics
            from .models import UserProductRecommendation, ProductSimilarity
            
            # Recommendation statistics
            total_recommendations = UserProductRecommendation.objects.count()
            active_users = UserProductRecommendation.objects.values('user').distinct().count()
            
            # Algorithm distribution
            algorithm_stats = UserProductRecommendation.objects.values('recommendation_type').annotate(
                count=Count('id'),
                avg_score=Avg('score')
            ).order_by('-count')

            # Product similarity statistics  
            similarity_stats = ProductSimilarity.objects.values('similarity_type').annotate(
                count=Count('id'),
                avg_similarity=Avg('similarity_score')
            ).order_by('-count')

            # Top recommended products
            top_products = UserProductRecommendation.objects.values(
                'product_id', 'product__name'
            ).annotate(
                recommendation_count=Count('id'),
                avg_score=Avg('score')
            ).order_by('-recommendation_count')[:10]

            return Response({
                'success': True,
                'recommendation_stats': {
                    'total_recommendations': total_recommendations,
                    'active_users': active_users,
                    'algorithm_distribution': list(algorithm_stats),
                    'similarity_stats': list(similarity_stats)
                },
                'top_products': list(top_products)
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminChurnPredictionView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            # Get churn risk assessments
            churn_risks = RiskAssessment.objects.filter(
                risk_type='customer_churn'
            ).order_by('-assessment_date')

            # Group by risk level
            high_risk = churn_risks.filter(risk_score__gte=0.7).count()
            medium_risk = churn_risks.filter(risk_score__gte=0.4, risk_score__lt=0.7).count()
            low_risk = churn_risks.filter(risk_score__lt=0.4).count()

            # Recent assessments
            recent_assessments = []
            for risk in churn_risks[:20]:
                try:
                    user = User.objects.get(id=risk.entity_id)
                    recent_assessments.append({
                        'user_id': risk.entity_id,
                        'username': user.username,
                        'risk_score': float(risk.risk_score),
                        'confidence': float(risk.confidence),
                        'mitigation': risk.mitigation_suggestion,
                        'created_at': risk.assessment_date.strftime('%Y-%m-%d %H:%M')
                    })
                except User.DoesNotExist:
                    continue

            return Response({
                'success': True,
                'churn_overview': {
                    'total_assessments': churn_risks.count(),
                    'high_risk_users': high_risk,
                    'medium_risk_users': medium_risk,
                    'low_risk_users': low_risk
                },
                'recent_assessments': recent_assessments
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyShoppingInsightsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get comprehensive shopping insights for current user"""
        user = request.user
        
        try:
            # Basic user statistics
            user_orders = Order.objects.filter(user=user)
            total_orders = user_orders.count()
            
            if total_orders == 0:
                return Response({
                    'success': True,
                    'message': 'Not enough data yet',
                    'shopping_profile': {
                        'total_orders': 0,
                        'total_spent': 0,
                        'average_order_value': 0,
                        'favorite_category': 'None',
                        'shopping_frequency': 'Never',
                        'days_since_last_order': 999,
                        'loyalty_score': 0
                    },
                    'spending_patterns': [],
                    'category_preferences': [],
                    'seasonal_insights': {
                        'best_month': 'N/A',
                        'seasonal_pattern': 'No data'
                    },
                    'recommendations': {
                        'next_purchase_prediction': 'No prediction available',
                        'suggested_categories': [],
                        'budget_recommendation': 'Start shopping to get personalized recommendations'
                    }
                })

            # Calculate comprehensive statistics
            total_spent = sum(
                order_product.product.price * order_product.quantity
                for order in user_orders
                for order_product in order.orderproduct_set.all()
            )
            
            avg_order_value = total_spent / total_orders if total_orders > 0 else 0
            
            # Last order date
            last_order = user_orders.order_by('-date_order').first()
            days_since_last_order = (timezone.now().date() - last_order.date_order.date()).days if last_order else 999
            
            # Category analysis
            category_spending = defaultdict(float)
            category_counts = defaultdict(int)
            
            for order in user_orders:
                for order_product in order.orderproduct_set.all():
                    value = float(order_product.product.price * order_product.quantity)
                    for category in order_product.product.categories.all():
                        category_spending[category.name] += value
                        category_counts[category.name] += 1
            
            favorite_category = max(category_spending, key=category_spending.get) if category_spending else 'None'
            
            # Shopping frequency
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
            
            # Loyalty score (0-100)
            loyalty_score = min(100, (total_orders * 5) + (min(total_spent/1000, 50)) + (max(0, 30 - days_since_last_order)))
            
            # Monthly spending patterns
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            spending_patterns = []
            try:
                # Calculate monthly spending manually due to complex aggregation
                monthly_totals = defaultdict(float)
                for order in user_orders:
                    month = order.date_order.month
                    for order_product in order.orderproduct_set.all():
                        monthly_totals[month] += float(order_product.product.price * order_product.quantity)
                
                # Convert to list format
                for month, total in sorted(monthly_totals.items()):
                    spending_patterns.append({
                        'month': month_names[month - 1],
                        'total_spent': total
                    })
            except Exception:
                spending_patterns = []
            
            # Category preferences (top 5)
            category_preferences = []
            sorted_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for category, spending in sorted_categories:
                category_preferences.append({
                    'category': category,
                    'total_spent': spending,
                    'order_count': category_counts[category],
                    'percentage': (spending / total_spent * 100) if total_spent > 0 else 0
                })
            
            # Seasonal insights
            best_month = max(spending_patterns, key=lambda x: x['total_spent'])['month'] if spending_patterns else 'N/A'
            
            # Next purchase prediction
            if days_since_last_order < 30:
                next_purchase_prediction = f"Likely within {30 - days_since_last_order} days"
            elif days_since_last_order < 60:
                next_purchase_prediction = "May purchase within 2-4 weeks"
            else:
                next_purchase_prediction = "Unlikely to purchase soon"
            
            # Budget recommendation
            if avg_order_value > 0:
                budget_recommendation = f"Your typical order value is ${avg_order_value:.2f}. Consider budgeting ${avg_order_value * 1.2:.2f} for your next purchase."
            else:
                budget_recommendation = "Start with a small budget to explore products."

            return Response({
                'success': True,
                'shopping_profile': {
                    'total_orders': total_orders,
                    'total_spent': round(total_spent, 2),
                    'average_order_value': round(avg_order_value, 2),
                    'favorite_category': favorite_category,
                    'shopping_frequency': shopping_frequency,
                    'days_since_last_order': days_since_last_order,
                    'loyalty_score': round(loyalty_score, 1)
                },
                'spending_patterns': spending_patterns,
                'category_preferences': category_preferences,
                'seasonal_insights': {
                    'best_month': best_month,
                    'seasonal_pattern': 'Your spending varies by season' if len(spending_patterns) > 3 else 'Limited seasonal data'
                },
                'recommendations': {
                    'next_purchase_prediction': next_purchase_prediction,
                    'suggested_categories': [cat['category'] for cat in category_preferences[:3]],
                    'budget_recommendation': budget_recommendation
                }
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)