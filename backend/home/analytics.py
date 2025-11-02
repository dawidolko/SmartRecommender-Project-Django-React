"""
Advanced Analytics Module for E-commerce Predictive Intelligence.

This module implements probabilistic models and forecasting algorithms for:
    - Purchase probability prediction (Naive Bayes-inspired)
    - Sales forecasting with confidence intervals
    - User purchase pattern analysis (RFM segmentation)
    - Product demand forecasting (time series)
    - Customer churn risk assessment
    - Seasonality analysis

Mathematical Models:
    - Purchase Probability: P(purchase|history, category, recency)
    - Sales Forecast: ARIMA-inspired with seasonal factors
    - Churn Risk: Logistic regression simulation
    - Demand Forecast: Moving average with trend analysis

Key Algorithms:
    1. Naive Bayes Purchase Prediction
    2. Time Series Decomposition (Trend + Seasonality)
    3. RFM (Recency, Frequency, Monetary) Analysis
    4. Confidence Interval Estimation (±15% margin)

Data Sources:
    - Order history (OrderProduct, Order)
    - Product metadata (Product, Category)
    - User behavior patterns (UserPurchasePattern)
    - Historical sales data (SalesForecast)

Authors: Dawid Olko & Piotr Smoła
Date: 2025-11-02
Version: 2.0
"""

from datetime import timedelta, date
from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum, Avg, F, Count
import random
from home.models import (
    PurchaseProbability,
    SalesForecast,
    UserPurchasePattern,
    ProductDemandForecast,
    RiskAssessment,
    Order,
    OrderProduct,
    Product,
)


def generate_purchase_probabilities_for_user(user):
    """
    Calculate purchase probabilities for all products for a given user.
    
    Uses Naive Bayes-inspired approach considering:
        - Purchase history (has user bought this product before?)
        - Category affinity (has user bought from same category?)
        - Recency (recent orders increase probability)
    
    Algorithm (Naive Bayes Simulation):
        P(purchase|product) = base_prob × recency_boost × confidence
        
        Where base_prob depends on:
        - Already purchased: 0.7-0.9 (70-90% chance of repeat purchase)
        - Same category: 0.4-0.6 (40-60% chance of related purchase)
        - New category: 0.1-0.2 (10-20% chance of exploration)
    
    Args:
        user (User): User instance to generate probabilities for
    
    Returns:
        None (creates/updates PurchaseProbability records in database)
    
    Database Updates:
        - PurchaseProbability: One record per (user, product) pair
        - Fields updated: probability, confidence_level
    
    Example:
        User bought "Laptop" (Electronics category) recently:
        - "Laptop" → probability=0.85 (high repeat purchase chance)
        - "Mouse" (Electronics) → probability=0.55 (same category)
        - "Book" (Books) → probability=0.15 (new category)
    
    Mathematical Formula:
        base_prob = {
            0.7 + rand(0.2)  if product already purchased
            0.4 + rand(0.2)  if category match
            0.1 + rand(0.1)  otherwise
        }
        
        final_prob = min(base_prob + 0.1, 0.95) if recent_order else base_prob
        confidence = 0.6 + rand(0.3)
    """
    user_orders = Order.objects.filter(user=user)
    products = Product.objects.all()
    
    # Get categories user has purchased from
    purchased_categories = (
        OrderProduct.objects.filter(order__in=user_orders)
        .values_list("product__categories__id", flat=True)
        .distinct()
    )
    
    for product in products:
        # Calculate base probability based on purchase history
        if product.id in user_orders.values_list("orderproduct__product_id", flat=True):
            # User already bought this product → high repeat purchase probability
            base_probability = Decimal("0.7") + Decimal(random.uniform(0.0, 0.2))
        elif product.categories.filter(id__in=purchased_categories).exists():
            # User bought from same category → moderate probability
            base_probability = Decimal("0.4") + Decimal(random.uniform(0.0, 0.2))
        else:
            # New category for user → low probability
            base_probability = Decimal("0.1") + Decimal(random.uniform(0.0, 0.1))
        
        # Recency boost: Recent orders increase probability
        recent_orders = user_orders.filter(
            date_order__gte=timezone.now() - timedelta(days=30)
        )
        if recent_orders.exists():
            base_probability = min(base_probability + Decimal("0.1"), Decimal("0.95"))
        
        # Confidence level (how sure we are about this prediction)
        confidence = Decimal("0.6") + Decimal(random.uniform(0.0, 0.3))
        
        # Save to database
        PurchaseProbability.objects.update_or_create(
            user=user,
            product=product,
            defaults={
                "probability": base_probability.quantize(Decimal("0.001")),
                "confidence_level": confidence.quantize(Decimal("0.001")),
            },
        )


def generate_user_purchase_patterns_for_user(user):
    """
    Analyze and generate purchase pattern statistics for a user per category.
    
    Implements RFM (Recency, Frequency, Monetary) Analysis for each category:
        - Frequency: How often user buys from category (orders/month)
        - Monetary: Average order value in category
        - Temporal: Preferred time of day for purchases
        - Seasonality: Monthly purchase distribution
    
    Algorithm (RFM Analysis):
        purchase_frequency = total_orders / months_active
        average_order_value = total_spent / total_orders
        preferred_time = mode(order_hours)
        seasonality_factor = monthly_distribution
    
    Args:
        user (User): User instance to analyze patterns for
    
    Returns:
        None (creates/updates UserPurchasePattern records)
    
    Database Updates:
        - UserPurchasePattern: One record per (user, category) pair
        - Fields: purchase_frequency, average_order_value, preferred_time_of_day, seasonality_factor
    
    Example:
        User bought from "Electronics" category:
        - 6 orders over 3 months → frequency = 2.0 orders/month
        - Total spent: $1800 → avg_order_value = $300
        - Orders at 14:00, 15:00, 16:00 → preferred_time = "afternoon"
        - Seasonality: {"11": 3, "12": 2, "1": 1} → holiday spike
    
    Mathematical Formulas:
        Frequency = N_orders / (days_active / 30)
        Avg_Value = Σ(price × quantity) / N_orders
        Seasonality[month] = count_of_orders_in_month
    """
    user_orders = Order.objects.filter(user=user)
    if not user_orders.exists():
        return
    
    # Aggregate statistics per category
    category_stats = (
        OrderProduct.objects.filter(order__in=user_orders)
        .values("product__categories__id")
        .annotate(
            total_quantity=Sum("quantity"),
            total_value=Sum(F("quantity") * F("product__price")),
            order_count=Count("order__id", distinct=True),
        )
    )
    
    for stat in category_stats:
        category_id = stat["product__categories__id"]
        if not category_id:
            continue
        
        # Calculate months active (for frequency calculation)
        days_active = (
            user_orders.last().date_order - user_orders.first().date_order
        ).days or 30
        months_active = max(days_active / 30, 1)
        
        # Purchase frequency: orders per month
        purchase_frequency = Decimal(stat["order_count"]) / Decimal(months_active)
        
        # Average order value: total spent / number of orders
        avg_order_value = (
            stat["total_value"] / stat["order_count"]
            if stat["order_count"] > 0
            else Decimal("0")
        )
        
        # Temporal analysis: preferred time of day
        preferred_time = analyze_preferred_time(user_orders)
        
        # Seasonality analysis: monthly distribution
        seasonality_factor = analyze_seasonality(user, category_id)
        
        # Save pattern to database
        UserPurchasePattern.objects.update_or_create(
            user=user,
            category_id=category_id,
            defaults={
                "purchase_frequency": purchase_frequency.quantize(Decimal("0.01")),
                "average_order_value": avg_order_value.quantize(Decimal("0.01")),
                "preferred_time_of_day": preferred_time,
                "seasonality_factor": seasonality_factor,
            },
        )


def generate_risk_assessment_for_user(user):
    """
    Assess customer churn risk using recency-based logistic model.
    
    Predicts probability of customer churning (stopping purchases) based on:
        - Recency: Time since last order (30-day threshold)
        - Frequency: Historical order count
        - Engagement: Recent activity level
    
    Algorithm (Logistic Regression Simulation):
        risk_score = 1 / (1 + e^(-z))
        where z = β₀ + β₁(recency) + β₂(frequency)
        
        Simplified:
        - No orders in 30 days → high risk (0.7-0.9)
        - Recent orders → low risk (0.2-0.4)
    
    Args:
        user (User): User to assess churn risk for
    
    Returns:
        None (creates RiskAssessment record)
    
    Database Updates:
        - RiskAssessment: New record with churn prediction
        - Fields: risk_score, confidence, mitigation_suggestion
    
    Example:
        User A (last order 45 days ago):
        - risk_score = 0.82 → HIGH RISK
        - confidence = 0.85
        - mitigation = "Send personalized offer or discount"
        
        User B (ordered yesterday):
        - risk_score = 0.25 → LOW RISK
        - confidence = 0.75
        - mitigation = "Maintain current inventory levels"
    
    Risk Thresholds:
        - High risk (>0.7): Inactive for 30+ days
        - Medium risk (0.4-0.7): Irregular activity
        - Low risk (<0.4): Recent purchases
    """
    # Check for recent orders (30-day window)
    recent_orders = Order.objects.filter(
        user=user, date_order__gte=timezone.now() - timedelta(days=30)
    )
    
    if not recent_orders.exists():
        # No recent orders → HIGH CHURN RISK
        risk_score = Decimal("0.7") + Decimal(random.uniform(0.0, 0.2))
        confidence = Decimal("0.8") + Decimal(random.uniform(0.0, 0.2))
        mitigation = "Send a personalized offer or discount to encourage return."
    else:
        # Recent orders → LOW CHURN RISK
        risk_score = Decimal("0.2") + Decimal(random.uniform(0.0, 0.2))
        confidence = Decimal("0.7") + Decimal(random.uniform(0.0, 0.1))
        mitigation = "Maintain current inventory levels."
    
    # Save risk assessment to database
    RiskAssessment.objects.create(
        risk_type="customer_churn",
        entity_type="user",
        entity_id=user.id,
        risk_score=risk_score.quantize(Decimal("0.001")),
        confidence=confidence.quantize(Decimal("0.001")),
        mitigation_suggestion=mitigation,
    )


def generate_sales_forecasts_for_products(product_ids):
    """
    Generate 30-day sales forecasts for specified products using time series analysis.
    
    Implements ARIMA-inspired forecasting with seasonal decomposition:
        Forecast(t) = Trend(t) × Seasonal(t) × Random_noise
        
        Components:
        - Trend: Linear growth/decline (+/-5% to +10% per year)
        - Seasonal: Monthly multiplier (e.g., December = 1.5x, February = 0.85x)
        - Confidence Interval: ±15% margin around prediction
    
    Algorithm:
        1. Calculate average sales per order (historical baseline)
        2. For each day in next 30 days:
            a. Apply trend factor (1 + days/365 × growth_rate)
            b. Apply seasonal factor (monthly multiplier)
            c. Add random noise (±10%)
            d. Calculate confidence bounds (prediction ± 15%)
    
    Args:
        product_ids (list): List of product IDs to forecast
    
    Returns:
        None (creates/updates SalesForecast records)
    
    Database Updates:
        - SalesForecast: 30 records per product (one per day)
        - Fields: predicted_quantity, confidence_interval_lower/upper, historical_accuracy
    
    Example:
        Product "Laptop" (avg 10 units/day):
        - Day 1 (January): predicted=9, lower=7, upper=10 (seasonal=0.9)
        - Day 15 (January): predicted=10, lower=8, upper=11
        - Day 30 (February): predicted=8, lower=6, upper=9 (seasonal=0.85)
    
    Mathematical Formulas:
        base_forecast = avg_per_order × trend × seasonal
        trend = 1 + (days_ahead / 365) × growth_rate
        seasonal = get_seasonal_factor(month)
        predicted = base_forecast × random(0.9, 1.1)
        margin = predicted × 0.15
        lower_bound = max(0, predicted - margin)
        upper_bound = predicted + margin
    
    Accuracy Tracking:
        historical_accuracy = 75% ± 5-10% (simulated)
        Real implementation should compare predictions vs actuals
    """
    current_date = date.today()
    
    for product in Product.objects.filter(id__in=product_ids):
        # Calculate historical average sales
        sales = OrderProduct.objects.filter(product=product).aggregate(
            total=Sum("quantity"), avg=Avg("quantity")
        )
        avg_per_order = sales["avg"] or 1
        
        # Generate forecasts for next 30 days
        for days_ahead in range(1, 31):
            forecast_date = current_date + timedelta(days=days_ahead)
            
            # Apply seasonal factor (monthly multiplier)
            seasonal = get_seasonal_factor(forecast_date.month)
            
            # Apply trend factor (linear growth/decline)
            trend = 1 + (days_ahead / 365) * random.uniform(-0.05, 0.1)
            
            # Calculate base forecast
            base_forecast = float(avg_per_order) * trend * seasonal
            
            # Add random noise (±10%)
            predicted = int(base_forecast * random.uniform(0.9, 1.1))
            
            # Calculate confidence interval (±15% margin)
            margin = predicted * 0.15
            lower = max(0, int(predicted - margin))
            upper = int(predicted + margin)
            
            # Historical accuracy (simulated 75% ± 5-10%)
            accuracy = Decimal("75.00") + Decimal(random.uniform(-5.0, 10.0))
            
            # Save forecast to database
            SalesForecast.objects.update_or_create(
                product=product,
                forecast_date=forecast_date,
                defaults={
                    "predicted_quantity": predicted,
                    "confidence_interval_lower": lower,
                    "confidence_interval_upper": upper,
                    "historical_accuracy": accuracy.quantize(Decimal("0.01")),
                },
            )


def generate_product_demand_forecasts_for_products(product_ids):
    """
    Generate demand forecasts for multiple time horizons (week, month, quarter).
    
    Calculates expected demand and optimal inventory levels using:
        - Historical average demand
        - Demand variance (volatility)
        - Reorder point (when to replenish stock)
        - Suggested stock level (safety stock + expected demand)
    
    Algorithm (Inventory Management):
        expected_demand = avg_daily_sales × period_days × (1 ± 10%)
        demand_variance = expected_demand × 0.15 (15% variability)
        reorder_point = expected_demand × 0.2 (20% threshold)
        suggested_stock = expected_demand × 1.5 (safety buffer)
    
    Args:
        product_ids (list): List of product IDs to forecast
    
    Returns:
        None (creates/updates ProductDemandForecast records)
    
    Database Updates:
        - ProductDemandForecast: 3 records per product (week, month, quarter)
        - Fields: expected_demand, demand_variance, reorder_point, suggested_stock_level
    
    Example:
        Product "Mouse" (avg 5 units/day):
        
        Week Forecast (7 days):
        - expected_demand = 5 × 7 × 1.05 = 36.75 ≈ 37 units
        - demand_variance = 37 × 0.15 = 5.55 units (±15%)
        - reorder_point = 37 × 0.2 = 7 units (order when <7 left)
        - suggested_stock = 37 × 1.5 = 55 units (keep 55 in stock)
        
        Month Forecast (30 days):
        - expected_demand = 5 × 30 × 1.05 = 157.5 ≈ 158 units
        - suggested_stock = 158 × 1.5 = 237 units
        
        Quarter Forecast (90 days):
        - expected_demand = 5 × 90 × 1.05 = 472.5 ≈ 473 units
        - suggested_stock = 473 × 1.5 = 710 units
    
    Inventory Formulas:
        Expected_Demand = avg_quantity × days × variability_factor
        Reorder_Point = Expected_Demand × 0.2  (order when 20% left)
        Safety_Stock = Expected_Demand × 0.5   (50% buffer)
        Suggested_Level = Expected_Demand + Safety_Stock
    
    Period Calculations:
        - Week: current_date + 7 days
        - Month: first day of next month
        - Quarter: first day of next quarter
    """
    current_date = date.today()
    periods = [("week", 7), ("month", 30), ("quarter", 90)]
    
    for product in Product.objects.filter(id__in=product_ids):
        # Calculate historical average demand
        demand = OrderProduct.objects.filter(product=product).aggregate(
            total=Sum("quantity"), avg=Avg("quantity")
        )
        avg_quantity = demand["avg"] or 1
        
        for period_type, days in periods:
            # Calculate period start date
            if period_type == "week":
                start = current_date + timedelta(days=7)
            elif period_type == "month":
                # First day of next month
                start = date(current_date.year, current_date.month + 1, 1)
            else:  # quarter
                # First day of next quarter
                q = (current_date.month - 1) // 3 + 1
                next_q = q + 1 if q < 4 else 1
                year = current_date.year if next_q > q else current_date.year + 1
                start = date(year, (next_q - 1) * 3 + 1, 1)
            
            # Calculate expected demand with variability
            expected = float(avg_quantity) * days * (1 + random.uniform(-0.1, 0.1))
            
            # Calculate demand variance (15% of expected)
            variance = expected * 0.15
            
            # Calculate reorder point (20% of expected)
            reorder = int(expected * 0.2)
            
            # Calculate suggested stock level (150% of expected for safety)
            suggested = int(expected * 1.5)
            
            # Save forecast to database
            ProductDemandForecast.objects.update_or_create(
                product=product,
                forecast_period=period_type,
                period_start=start,
                defaults={
                    "expected_demand": Decimal(expected).quantize(Decimal("0.01")),
                    "demand_variance": Decimal(variance).quantize(Decimal("0.01")),
                    "reorder_point": reorder,
                    "suggested_stock_level": suggested,
                },
            )


def get_seasonal_factor(month):
    """
    Get seasonal multiplier for a given month (for sales forecasting).
    
    Returns scaling factors based on typical e-commerce seasonality patterns:
        - Holiday season (Nov-Dec): 1.4-1.5x (140-150% of baseline)
        - Spring/Summer (Apr-Jul): 1.1-1.3x (110-130% of baseline)
        - Winter slump (Jan-Feb): 0.85-0.9x (85-90% of baseline)
        - Stable months (Mar, Aug-Oct): 1.0x (100% baseline)
    
    Args:
        month (int): Month number (1-12)
    
    Returns:
        float: Seasonal multiplier (0.85-1.5)
    
    Seasonal Pattern (E-commerce):
        January: 0.9 - Post-holiday slowdown
        February: 0.85 - Winter low point
        March: 1.0 - Spring recovery
        April: 1.1 - Spring increase
        May: 1.2 - Pre-summer boost
        June: 1.3 - Summer peak start
        July: 1.2 - Summer continuation
        August: 1.1 - Back-to-school
        September: 1.0 - Fall stabilization
        October: 1.0 - Pre-holiday steady
        November: 1.4 - Black Friday surge
        December: 1.5 - Holiday peak (Christmas)
    
    Example:
        get_seasonal_factor(12) → 1.5 (December = 150% of average)
        get_seasonal_factor(2) → 0.85 (February = 85% of average)
    
    Usage in Forecasting:
        base_sales = 100 units
        december_forecast = base_sales × 1.5 = 150 units
        february_forecast = base_sales × 0.85 = 85 units
    """
    return {
        1: 0.9,    # January - post-holiday slowdown
        2: 0.85,   # February - winter low
        3: 1.0,    # March - normal
        4: 1.1,    # April - spring increase
        5: 1.2,    # May - pre-summer boost
        6: 1.3,    # June - summer peak
        7: 1.2,    # July - summer continuation
        8: 1.1,    # August - back-to-school
        9: 1.0,    # September - fall stabilization
        10: 1.0,   # October - stable
        11: 1.4,   # November - Black Friday surge
        12: 1.5,   # December - holiday peak (Christmas)
    }.get(month, 1.0)


def analyze_preferred_time(orders):
    """
    Determine user's preferred time of day for purchases based on order history.
    
    Analyzes order timestamps to identify temporal shopping patterns.
    Useful for:
        - Targeted marketing campaigns (send emails at preferred time)
        - Personalized product recommendations
        - User segmentation (morning shoppers vs evening shoppers)
    
    Algorithm:
        1. Extract hour from each order timestamp (0-23)
        2. Calculate average hour across all orders
        3. Classify into time-of-day category
    
    Args:
        orders (QuerySet): Django QuerySet of Order objects
    
    Returns:
        str: Time category ('morning', 'afternoon', 'evening', 'night')
    
    Time Categories:
        - Morning: 6:00 - 11:59 (hours 6-11)
        - Afternoon: 12:00 - 17:59 (hours 12-17)
        - Evening: 18:00 - 23:59 (hours 18-23)
        - Night: 0:00 - 5:59 (hours 0-5)
    
    Example:
        User orders at: 14:00, 15:30, 16:45, 13:15
        Average hour: (14 + 15 + 16 + 13) / 4 = 14.5
        Result: "afternoon" (14.5 falls in 12-17 range)
    
    Edge Cases:
        - No orders: Return random category
        - Boundary hours (e.g., 12:00): Classified as afternoon
    """
    hours = [o.date_order.hour for o in orders]
    if not hours:
        return random.choice(["morning", "afternoon", "evening", "night"])
    
    # Calculate average hour across all orders
    avg_hour = sum(hours) / len(hours)
    
    # Classify into time-of-day category
    if 6 <= avg_hour < 12:
        return "morning"
    elif 12 <= avg_hour < 18:
        return "afternoon"
    elif 18 <= avg_hour < 24:
        return "evening"
    return "night"


def analyze_seasonality(user, category_id):
    """
    Analyze user's purchase seasonality for a specific category (monthly distribution).
    
    Calculates how user's purchases are distributed across months to identify:
        - Seasonal shopping patterns (e.g., holiday season spikes)
        - Recurring purchase cycles (e.g., back-to-school in September)
        - Irregular vs regular purchase behavior
    
    Algorithm:
        1. Get all user orders in specified category
        2. Group orders by month (aggregate by TruncMonth)
        3. Count orders per month
        4. Return dictionary with monthly counts
    
    Args:
        user (User): User instance to analyze
        category_id (int): Category ID to analyze seasonality for
    
    Returns:
        dict: Monthly order counts {month_str: count}
              Example: {"1": 2, "2": 0, "3": 3, "12": 5}
    
    Output Format:
        {
            "1": 2,   # 2 orders in January
            "2": 0,   # 0 orders in February
            "3": 3,   # 3 orders in March
            ...
            "12": 5   # 5 orders in December
        }
    
    Example:
        User buys "Electronics" category:
        - January: 1 order
        - March: 2 orders
        - November: 3 orders (Black Friday)
        - December: 4 orders (Christmas)
        
        Result: {"1": 1, "3": 2, "11": 3, "12": 4, ...}
        Pattern: Strong holiday seasonality (Nov-Dec spike)
    
    Usage:
        seasonality = analyze_seasonality(user, category_id=5)
        if seasonality["12"] > 3:
            print("User is a holiday shopper!")
    
    Mathematical Representation:
        Seasonality[month_i] = count(orders where month(date) = i)
        Sum(Seasonality) = total_orders
    """
    from django.db.models.functions import TruncMonth

    orders = Order.objects.filter(user=user)
    
    # Group orders by month and count
    monthly = (
        OrderProduct.objects.filter(
            order__in=orders, product__categories__id=category_id
        )
        .annotate(month=TruncMonth("order__date_order"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    
    # Initialize all months with 0
    seasonality = {str(i): 0 for i in range(1, 13)}
    
    # Fill in actual counts
    for item in monthly:
        if item["month"]:
            seasonality[str(item["month"].month)] = item["count"]
    
    return seasonality
