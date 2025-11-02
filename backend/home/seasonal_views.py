"""
Seasonal Trend Analysis API for SmartRecommender E-commerce System.

This module analyzes user purchase patterns across seasons and months to provide:
    - Seasonal spending patterns (Winter, Spring, Summer, Autumn)
    - Monthly spending trends with averages
    - Peak shopping period identification
    - Personalized seasonal shopping tips
    - Category-based purchase frequency predictions

Mathematical Analysis:
    1. Seasonal Aggregation:
       For each season s:
           Total Spent(s) = Σ(order_value for all orders in season s)
           Order Count(s) = count(orders in season s)
           Avg Order Value(s) = Total Spent(s) / Order Count(s)
    
    2. Monthly Averaging:
       For each month m:
           Avg Spending(m) = Σ(order_values in month m) / count(orders in m)
    
    3. Best Month Ranking:
       Best Months = top 3 months sorted by Avg Spending (descending)

Use Cases:
    - Budget planning: Users see which months they spend most
    - Inventory management: Admins predict seasonal demand
    - Marketing campaigns: Target users during their peak shopping seasons
    - Personalized tips: Suggest saving money during low-spend seasons

Authors: Dawid Olko & Piotr Smoła
Date: 2025-11-02
Version: 2.0
"""

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
    """
    API endpoint for seasonal shopping trend analysis.
    
    Endpoint: GET /api/seasonal-trends/
    Permission: IsAuthenticated (logged-in users only)
    
    Response Structure:
        {
            "success": true,
            "seasonal_patterns": {
                "Winter": {
                    "total_spent": 1250.50,
                    "order_count": 5,
                    "avg_order_value": 250.10
                },
                "Spring": {...},
                "Summer": {...},
                "Autumn": {...}
            },
            "monthly_spending": [
                {
                    "month": "Jan",
                    "avg_spending": 300.00,
                    "total_orders": 2
                },
                ...
            ],
            "recommendations": [
                {
                    "category": "Electronics",
                    "purchase_frequency": 2.5,
                    "next_purchase_likely": "Within 2 weeks",
                    "seasonal_factor": "High demand in winter"
                },
                ...
            ],
            "insights": [
                "Your peak shopping season is Winter - great time for major purchases!",
                "You tend to shop most in Jan, Dec - plan your budget accordingly!"
            ],
            "analysis_period": "Based on 25 orders"
        }
    
    Season Mapping:
        - Winter: December, January, February (months 12, 1, 2)
        - Spring: March, April, May (months 3, 4, 5)
        - Summer: June, July, August (months 6, 7, 8)
        - Autumn: September, October, November (months 9, 10, 11)
    
    Analysis Process:
        1. Fetch all user's orders
        2. For each order:
           - Extract month and determine season
           - Calculate order value (Σ product_price × quantity)
           - Aggregate by season and month
        3. Calculate averages and totals
        4. Generate personalized insights
        5. Return structured response
    
    Edge Cases:
        - No purchase history: Returns placeholder data with tips to start shopping
        - Single order: Shows data for that one order
        - Multiple orders same month: Averages spending across orders
    
    Business Value:
        - Users: Budget planning, see spending trends
        - Marketing: Target campaigns during user's peak shopping periods
        - Inventory: Stock products before high-demand seasons
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Analyze user's seasonal shopping trends.
        
        Args:
            request: HTTP GET request with authenticated user
        
        Returns:
            Response: JSON with seasonal patterns, monthly spending, and insights
        
        Example Query:
            GET /api/seasonal-trends/
            Headers: Authorization: Bearer <jwt_token>
        """
        try:
            user = request.user
            user_orders = Order.objects.filter(user=user)
            
            # Handle users with no purchase history
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

            # Initialize data structures for aggregation
            seasonal_patterns = {}
            monthly_spending = defaultdict(list)
            
            # Aggregate spending by season and month
            for order in user_orders:
                month = order.date_order.month
                season = self.get_season(month)
                
                # Calculate total order value: Σ(price × quantity)
                order_value = sum(
                    float(order_product.product.price * order_product.quantity)
                    for order_product in order.orderproduct_set.all()
                )
                
                # Initialize season data if first occurrence
                if season not in seasonal_patterns:
                    seasonal_patterns[season] = {
                        'total_spent': 0,
                        'order_count': 0,
                        'avg_order_value': 0
                    }
                
                # Aggregate seasonal data
                seasonal_patterns[season]['total_spent'] += order_value
                seasonal_patterns[season]['order_count'] += 1
                monthly_spending[month].append(order_value)
            
            # Calculate average order value per season
            for season in seasonal_patterns:
                if seasonal_patterns[season]['order_count'] > 0:
                    seasonal_patterns[season]['avg_order_value'] = (
                        seasonal_patterns[season]['total_spent'] / 
                        seasonal_patterns[season]['order_count']
                    )

            # Generate monthly summary with averages
            monthly_summary = []
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            for month in range(1, 13):
                if month in monthly_spending:
                    # Calculate average spending for months with orders
                    avg_spending = sum(monthly_spending[month]) / len(monthly_spending[month])
                    monthly_summary.append({
                        'month': month_names[month - 1],
                        'avg_spending': round(avg_spending, 2),
                        'total_orders': len(monthly_spending[month])
                    })
                else:
                    # Zero spending for months with no orders
                    monthly_summary.append({
                        'month': month_names[month - 1],
                        'avg_spending': 0,
                        'total_orders': 0
                    })
            
            # Identify top 3 spending months
            best_months = sorted(
                monthly_summary, 
                key=lambda x: x['avg_spending'], 
                reverse=True
            )[:3]
            
            # Generate personalized tips based on patterns
            seasonal_tips = self.generate_seasonal_tips(seasonal_patterns, best_months)

            # Static category recommendations (could be personalized in future)
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
            # Graceful error handling
            return Response({
                'success': False,
                'error': str(e),
                'seasonal_patterns': {},
                'monthly_spending': [],
                'recommendations': [],
                'insights': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_season(self, month):
        """
        Map month number to season name.
        
        Args:
            month (int): Month number (1-12)
        
        Returns:
            str: Season name ('Winter', 'Spring', 'Summer', 'Autumn')
        
        Season Mapping:
            - Winter: 12, 1, 2 (December, January, February)
            - Spring: 3, 4, 5 (March, April, May)
            - Summer: 6, 7, 8 (June, July, August)
            - Autumn: 9, 10, 11 (September, October, November)
        
        Example:
            get_season(1) → 'Winter'
            get_season(7) → 'Summer'
        """
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Autumn'
    
    def generate_seasonal_tips(self, seasonal_patterns, best_months):
        """
        Generate personalized shopping tips based on seasonal spending patterns.
        
        Args:
            seasonal_patterns (dict): Seasonal spending data
            best_months (list): Top 3 months by average spending
        
        Returns:
            list: Up to 3 personalized tips for the user
        
        Tip Types:
            1. Peak Season Tip:
               Identifies user's highest-spending season
               "Your peak shopping season is Winter - great time for major purchases!"
            
            2. Best Months Tip:
               Lists top 2 spending months
               "You tend to shop most in Jan, Dec - plan your budget accordingly!"
            
            3. Budget Planning Tip:
               If >40% spending in one season, suggest saving in advance
               "You spend heavily in winter - consider setting aside money during autumn!"
        
        Mathematical Logic:
            winter_pct = (Winter Total Spent / Total All Seasons Spent) × 100
            
            If winter_pct > 40%:
                → "You spend heavily in winter..."
            Else if summer_pct > 40%:
                → "Summer is your big spending season..."
        
        Example Output:
            [
                "Your peak shopping season is Winter - great time for major purchases!",
                "You tend to shop most in Jan, Dec - plan your budget accordingly!",
                "You spend heavily in winter - consider setting aside money during autumn!"
            ]
        """
        tips = []
        
        # Handle users with no seasonal data
        if not seasonal_patterns:
            return ["Start shopping to get seasonal recommendations!"]
        
        # Tip 1: Identify peak shopping season
        best_season = max(seasonal_patterns.items(), key=lambda x: x[1]['total_spent'])
        tips.append(f"Your peak shopping season is {best_season[0]} - great time for major purchases!")
        
        # Tip 2: Highlight best shopping months
        if best_months:
            tips.append(f"You tend to shop most in {', '.join([m['month'] for m in best_months[:2]])} - plan your budget accordingly!")
        
        # Tip 3: Budget planning based on seasonal concentration
        total_seasonal_spending = sum(season['total_spent'] for season in seasonal_patterns.values())
        if total_seasonal_spending > 0:
            # Calculate winter spending percentage
            winter_pct = (seasonal_patterns.get('Winter', {}).get('total_spent', 0) / total_seasonal_spending) * 100
            if winter_pct > 40:
                tips.append("You spend heavily in winter - consider setting aside money during autumn!")
            # Calculate summer spending percentage
            elif seasonal_patterns.get('Summer', {}).get('total_spent', 0) / total_seasonal_spending * 100 > 40:
                tips.append("Summer is your big spending season - perfect for vacation gear and outdoor equipment!")
        
        # Return maximum 3 tips
        return tips[:3]