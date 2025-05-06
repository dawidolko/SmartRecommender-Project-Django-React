from datetime import timedelta, date
from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum, Avg, F, Count
import random
from home.models import (
    PurchaseProbability, SalesForecast, UserPurchasePattern,
    ProductDemandForecast, RiskAssessment, Order, OrderProduct, Product
)

def generate_purchase_probabilities_for_user(user):
    user_orders = Order.objects.filter(user=user)
    products = Product.objects.all()
    purchased_categories = OrderProduct.objects.filter(order__in=user_orders).values_list('product__categories__id', flat=True).distinct()
    for product in products:
        if product.id in user_orders.values_list('orderproduct__product_id', flat=True):
            base_probability = Decimal('0.7') + Decimal(random.uniform(0.0, 0.2))
        elif product.categories.filter(id__in=purchased_categories).exists():
            base_probability = Decimal('0.4') + Decimal(random.uniform(0.0, 0.2))
        else:
            base_probability = Decimal('0.1') + Decimal(random.uniform(0.0, 0.1))
        recent_orders = user_orders.filter(date_order__gte=timezone.now() - timedelta(days=30))
        if recent_orders.exists():
            base_probability = min(base_probability + Decimal('0.1'), Decimal('0.95'))
        confidence = Decimal('0.6') + Decimal(random.uniform(0.0, 0.3))
        PurchaseProbability.objects.update_or_create(
            user=user,
            product=product,
            defaults={
                'probability': base_probability.quantize(Decimal('0.001')),
                'confidence_level': confidence.quantize(Decimal('0.001'))
            }
        )

def generate_user_purchase_patterns_for_user(user):
    user_orders = Order.objects.filter(user=user)
    if not user_orders.exists():
        return
    category_stats = OrderProduct.objects.filter(order__in=user_orders).values('product__categories__id').annotate(
        total_quantity=Sum('quantity'),
        total_value=Sum(F('quantity') * F('product__price')),
        order_count=Count('order__id', distinct=True)
    )
    for stat in category_stats:
        category_id = stat['product__categories__id']
        if not category_id:
            continue
        days_active = (user_orders.last().date_order - user_orders.first().date_order).days or 30
        months_active = max(days_active / 30, 1)
        purchase_frequency = Decimal(stat['order_count']) / Decimal(months_active)
        avg_order_value = stat['total_value'] / stat['order_count'] if stat['order_count'] > 0 else Decimal('0')
        preferred_time = analyze_preferred_time(user_orders)
        seasonality_factor = analyze_seasonality(user, category_id)
        UserPurchasePattern.objects.update_or_create(
            user=user,
            category_id=category_id,
            defaults={
                'purchase_frequency': purchase_frequency.quantize(Decimal('0.01')),
                'average_order_value': avg_order_value.quantize(Decimal('0.01')),
                'preferred_time_of_day': preferred_time,
                'seasonality_factor': seasonality_factor
            }
        )

def generate_risk_assessment_for_user(user):
    recent_orders = Order.objects.filter(user=user, date_order__gte=timezone.now() - timedelta(days=30))
    if not recent_orders.exists():
        risk_score = Decimal('0.7') + Decimal(random.uniform(0.0, 0.2))
        confidence = Decimal('0.8') + Decimal(random.uniform(0.0, 0.2))
        mitigation = "Send a personalized offer or discount to encourage return."
    else:
        risk_score = Decimal('0.2') + Decimal(random.uniform(0.0, 0.2))
        confidence = Decimal('0.7') + Decimal(random.uniform(0.0, 0.1))
        mitigation = "Maintain current inventory levels."
    RiskAssessment.objects.create(
        risk_type='customer_churn',
        entity_type='user',
        entity_id=user.id,
        risk_score=risk_score.quantize(Decimal('0.001')),
        confidence=confidence.quantize(Decimal('0.001')),
        mitigation_suggestion=mitigation
    )

def generate_sales_forecasts_for_products(product_ids):
    current_date = date.today()
    for product in Product.objects.filter(id__in=product_ids):
        sales = OrderProduct.objects.filter(product=product).aggregate(total=Sum('quantity'), avg=Avg('quantity'))
        avg_per_order = sales['avg'] or 1
        for days_ahead in range(1, 31):
            forecast_date = current_date + timedelta(days=days_ahead)
            seasonal = get_seasonal_factor(forecast_date.month)
            trend = 1 + (days_ahead / 365) * random.uniform(-0.05, 0.1)
            base_forecast = float(avg_per_order) * trend * seasonal
            predicted = int(base_forecast * random.uniform(0.9, 1.1))
            margin = predicted * 0.15
            lower = max(0, int(predicted - margin))
            upper = int(predicted + margin)
            accuracy = Decimal('75.00') + Decimal(random.uniform(-5.0, 10.0))
            SalesForecast.objects.update_or_create(
                product=product,
                forecast_date=forecast_date,
                defaults={
                    'predicted_quantity': predicted,
                    'confidence_interval_lower': lower,
                    'confidence_interval_upper': upper,
                    'historical_accuracy': accuracy.quantize(Decimal('0.01'))
                }
            )

def generate_product_demand_forecasts_for_products(product_ids):
    current_date = date.today()
    periods = [('week', 7), ('month', 30), ('quarter', 90)]
    for product in Product.objects.filter(id__in=product_ids):
        demand = OrderProduct.objects.filter(product=product).aggregate(total=Sum('quantity'), avg=Avg('quantity'))
        avg_quantity = demand['avg'] or 1
        for period_type, days in periods:
            if period_type == 'week':
                start = current_date + timedelta(days=7)
            elif period_type == 'month':
                start = date(current_date.year, current_date.month + 1, 1)
            else:
                q = (current_date.month - 1) // 3 + 1
                next_q = q + 1 if q < 4 else 1
                year = current_date.year if next_q > q else current_date.year + 1
                start = date(year, (next_q - 1) * 3 + 1, 1)
            expected = float(avg_quantity) * days * (1 + random.uniform(-0.1, 0.1))
            variance = expected * 0.15
            reorder = int(expected * 0.2)
            suggested = int(expected * 1.5)
            ProductDemandForecast.objects.update_or_create(
                product=product,
                forecast_period=period_type,
                period_start=start,
                defaults={
                    'expected_demand': Decimal(expected).quantize(Decimal('0.01')),
                    'demand_variance': Decimal(variance).quantize(Decimal('0.01')),
                    'reorder_point': reorder,
                    'suggested_stock_level': suggested
                }
            )

def get_seasonal_factor(month):
    return {
        1: 0.9, 2: 0.85, 3: 1.0, 4: 1.1, 5: 1.2, 6: 1.3,
        7: 1.2, 8: 1.1, 9: 1.0, 10: 1.0, 11: 1.4, 12: 1.5
    }.get(month, 1.0)

def analyze_preferred_time(orders):
    hours = [o.date_order.hour for o in orders]
    if not hours:
        return random.choice(['morning', 'afternoon', 'evening', 'night'])
    avg_hour = sum(hours) / len(hours)
    if 6 <= avg_hour < 12:
        return 'morning'
    elif 12 <= avg_hour < 18:
        return 'afternoon'
    elif 18 <= avg_hour < 24:
        return 'evening'
    return 'night'

def analyze_seasonality(user, category_id):
    from django.db.models.functions import TruncMonth
    orders = Order.objects.filter(user=user)
    monthly = OrderProduct.objects.filter(order__in=orders, product__categories__id=category_id).annotate(
        month=TruncMonth('order__date_order')
    ).values('month').annotate(count=Count('id')).order_by('month')
    seasonality = {str(i): 0 for i in range(1, 13)}
    for item in monthly:
        if item['month']:
            seasonality[str(item['month'].month)] = item['count']
    return seasonality
