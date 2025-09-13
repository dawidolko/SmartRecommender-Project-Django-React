from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
import calendar

from .models import Order, OrderProduct, Category


class SeasonalTrendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            user_orders = Order.objects.filter(user=user)
            
            if not user_orders.exists():
                return Response({
                    'success': True,
                    'seasonal_patterns': {},
                    'monthly_spending': [],
                    'recommendations': [
                        {
                            'category': 'Electronics',
                            'purchase_frequency': 2.5,
                            'next_purchase_likely': 'Within 2 weeks',
                            'seasonal_factor': 'High demand in winter'
                        },
                        {
                            'category': 'Clothing',
                            'purchase_frequency': 1.8,
                            'next_purchase_likely': 'Next month',
                            'seasonal_factor': 'Peak in spring and fall'
                        },
                        {
                            'category': 'Home & Garden',
                            'purchase_frequency': 1.2,
                            'next_purchase_likely': 'Next season',
                            'seasonal_factor': 'Summer peak activity'
                        }
                    ],
                    'insights': ['Start shopping to see seasonal patterns!'],
                    'message': 'No purchase history available for seasonal analysis.'
                })

            seasonal_patterns = {}
            monthly_spending = defaultdict(list)
            
            for order in user_orders:
                month = order.date_order.month
                season = self.get_season(month)
                order_value = sum(
                    float(order_product.product.price * order_product.quantity)
                    for order_product in order.orderproduct_set.all()
                )
                
                if season not in seasonal_patterns:
                    seasonal_patterns[season] = {
                        'total_spent': 0,
                        'order_count': 0,
                        'avg_order_value': 0
                    }
                
                seasonal_patterns[season]['total_spent'] += order_value
                seasonal_patterns[season]['order_count'] += 1
                monthly_spending[month].append(order_value)
            
            for season in seasonal_patterns:
                if seasonal_patterns[season]['order_count'] > 0:
                    seasonal_patterns[season]['avg_order_value'] = (
                        seasonal_patterns[season]['total_spent'] / 
                        seasonal_patterns[season]['order_count']
                    )

            monthly_summary = []
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            for month in range(1, 13):
                if month in monthly_spending:
                    avg_spending = sum(monthly_spending[month]) / len(monthly_spending[month])
                    monthly_summary.append({
                        'month': month_names[month - 1],
                        'avg_spending': round(avg_spending, 2),
                        'total_orders': len(monthly_spending[month])
                    })
                else:
                    monthly_summary.append({
                        'month': month_names[month - 1],
                        'avg_spending': 0,
                        'total_orders': 0
                    })
            
            best_months = sorted(
                monthly_summary, 
                key=lambda x: x['avg_spending'], 
                reverse=True
            )[:3]
            
            seasonal_tips = self.generate_seasonal_tips(seasonal_patterns, best_months)

            recommendations = [
                {
                    'category': 'Electronics',
                    'purchase_frequency': 2.5,
                    'next_purchase_likely': 'Within 2 weeks',
                    'seasonal_factor': 'High demand in winter'
                },
                {
                    'category': 'Clothing',
                    'purchase_frequency': 1.8,
                    'next_purchase_likely': 'Next month',
                    'seasonal_factor': 'Peak in spring and fall'
                },
                {
                    'category': 'Home & Garden',
                    'purchase_frequency': 1.2,
                    'next_purchase_likely': 'Next season',
                    'seasonal_factor': 'Summer peak activity'
                }
            ]

            return Response({
                'success': True,
                'seasonal_patterns': seasonal_patterns,
                'monthly_spending': monthly_summary,
                'recommendations': recommendations,
                'insights': seasonal_tips,
                'analysis_period': f"Based on {user_orders.count()} orders"
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'seasonal_patterns': {},
                'monthly_spending': [],
                'recommendations': [],
                'insights': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_season(self, month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Autumn'
    
    def generate_seasonal_tips(self, seasonal_patterns, best_months):
        tips = []
        
        if not seasonal_patterns:
            return ["Start shopping to get seasonal recommendations!"]
        
        best_season = max(seasonal_patterns.items(), key=lambda x: x[1]['total_spent'])
        tips.append(f"Your peak shopping season is {best_season[0]} - great time for major purchases!")
        
        if best_months:
            tips.append(f"You tend to shop most in {', '.join([m['month'] for m in best_months[:2]])} - plan your budget accordingly!")
        
        total_seasonal_spending = sum(season['total_spent'] for season in seasonal_patterns.values())
        if total_seasonal_spending > 0:
            winter_pct = (seasonal_patterns.get('Winter', {}).get('total_spent', 0) / total_seasonal_spending) * 100
            if winter_pct > 40:
                tips.append("You spend heavily in winter - consider setting aside money during autumn!")
            elif seasonal_patterns.get('Summer', {}).get('total_spent', 0) / total_seasonal_spending * 100 > 40:
                tips.append("Summer is your big spending season - perfect for vacation gear and outdoor equipment!")
        
        return tips[:3]