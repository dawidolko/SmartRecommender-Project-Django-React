from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'db_user'
        verbose_name = "User"
        verbose_name_plural = "Users"

class CartItem(models.Model):
    user = models.ForeignKey("home.User", on_delete=models.CASCADE)
    product = models.ForeignKey("home.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user} - {self.product} ({self.quantity})"

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'db_category'
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

class Sale(models.Model):
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Sale {self.discount_amount}%"

    class Meta:
        db_table = 'db_sale'
        verbose_name = "Sale"
        verbose_name_plural = "Sales"
        ordering = ['start_date']

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'db_tag'
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, blank=True, null=True)
    categories = models.ManyToManyField('Category', through='ProductCategory')
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'db_product'
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} -> {self.category.name}"

    class Meta:
        unique_together = (('product', 'category'),)
        db_table = 'db_product_category'
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

class PhotoProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)

    def __str__(self):
        return f"Photo for {self.product.name}"

    class Meta:
        db_table = 'db_photo_product'
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

class Opinion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"Opinion by {self.user.username} on {self.product.name}"

    class Meta:
        db_table = 'db_opinion'
        verbose_name = "Opinion"
        verbose_name_plural = "Opinions"
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1, rating__lte=5), name="rating_range"),
            models.UniqueConstraint(fields=['user', 'product'], name="unique_user_product_opinion")
        ]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    class Meta:
        db_table = 'db_order'
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-date_order']

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order {self.order.id} -> {self.product.name}"

    class Meta:
        db_table = 'db_order_product'
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"

class Complaint(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cause = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint for Order {self.order.id}"

    class Meta:
        db_table = 'db_complaint'
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"
        ordering = ['-submission_date']

class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parameter_name = models.CharField(max_length=50)
    specification = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.parameter_name} for {self.product.name}"

    class Meta:
        db_table = 'db_specification'
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"

class SentimentAnalysis(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    opinion = models.OneToOneField(Opinion, on_delete=models.CASCADE)
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=3)
    sentiment_category = models.CharField(max_length=20, choices=SENTIMENT_CHOICES)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'method_sentiment_analysis'
        verbose_name = "Sentiment Analysis"
        verbose_name_plural = "Sentiment Analyses"
        indexes = [
            models.Index(fields=['product'], name='home_senti_product_idx'),
            models.Index(fields=['sentiment_category'], name='home_senti_category_idx'),
        ]


class ProductSentimentSummary(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='sentiment_summary')
    average_sentiment_score = models.DecimalField(max_digits=5, decimal_places=3)
    positive_count = models.PositiveIntegerField(default=0)
    neutral_count = models.PositiveIntegerField(default=0)
    negative_count = models.PositiveIntegerField(default=0)
    total_opinions = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'method_product_sentiment_summary'
        verbose_name = "Product Sentiment Summary"
        verbose_name_plural = "Product Sentiment Summaries"

class UserInteraction(models.Model):
    INTERACTION_TYPES = [
        ('view', 'View'),
        ('click', 'Click'),
        ('add_to_cart', 'Add to Cart'),
        ('purchase', 'Purchase'),
        ('favorite', 'Favorite'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'method_user_interactions'
        indexes = [
            models.Index(fields=['user', 'product']),
            models.Index(fields=['interaction_type']),
        ]


class ProductSimilarity(models.Model):
    SIMILARITY_TYPES = [
        ('collaborative', 'Collaborative Filtering'),
        ('content_based', 'Content Based'),
    ]
    
    product1 = models.ForeignKey(Product, related_name='similarity_from', on_delete=models.CASCADE)
    product2 = models.ForeignKey(Product, related_name='similarity_to', on_delete=models.CASCADE)
    similarity_type = models.CharField(max_length=20, choices=SIMILARITY_TYPES)
    similarity_score = models.DecimalField(max_digits=5, decimal_places=3)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'method_product_similarity'
        unique_together = ('product1', 'product2', 'similarity_type')


class UserProductRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    recommendation_type = models.CharField(max_length=20, choices=ProductSimilarity.SIMILARITY_TYPES)
    score = models.DecimalField(max_digits=5, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'method_user_product_recommendation'
        unique_together = ('user', 'product', 'recommendation_type')
        ordering = ['-score']


class RecommendationSettings(models.Model):
    ALGORITHM_CHOICES = [
        ('collaborative', 'Collaborative Filtering'),
        ('content_based', 'Content Based'),
        ('fuzzy_logic', 'Fuzzy Logic'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active_algorithm = models.CharField(max_length=30, choices=ALGORITHM_CHOICES, default='collaborative')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'method_recommendation_settings'
        unique_together = ('user', 'active_algorithm')

class ProductAssociation(models.Model):
    product_1 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='associations_from')
    product_2 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='associations_to')
    support = models.FloatField()
    confidence = models.FloatField()
    lift = models.FloatField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'method_productassociation'
        unique_together = ('product_1', 'product_2')

class PurchaseProbability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    probability = models.DecimalField(max_digits=5, decimal_places=3)
    confidence_level = models.DecimalField(max_digits=5, decimal_places=3)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'method_purchase_probability'
        unique_together = ['user', 'product']
        
    def __str__(self):
        return f"{self.user.email} - {self.product.name}: {self.probability}"


class SalesForecast(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    forecast_date = models.DateField()
    predicted_quantity = models.PositiveIntegerField()
    confidence_interval_lower = models.PositiveIntegerField()
    confidence_interval_upper = models.PositiveIntegerField()
    historical_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'method_sales_forecast'
        unique_together = ['product', 'forecast_date']
        ordering = ['-forecast_date']
        
    def __str__(self):
        return f"Forecast for {self.product.name} on {self.forecast_date}"


class UserPurchasePattern(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    purchase_frequency = models.DecimalField(max_digits=5, decimal_places=2)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    preferred_time_of_day = models.CharField(max_length=20, choices=[
        ('morning', 'Morning (6-12)'),
        ('afternoon', 'Afternoon (12-18)'), 
        ('evening', 'Evening (18-24)'),
        ('night', 'Night (0-6)')
    ])
    seasonality_factor = models.JSONField(null=True, blank=True)
    last_computed = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'method_user_purchase_pattern'
        unique_together = ['user', 'category']
        
    def __str__(self):
        return f"{self.user.email} pattern for {self.category.name}"


class ProductDemandForecast(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    forecast_period = models.CharField(max_length=10, choices=[
        ('week', 'Weekly'),
        ('month', 'Monthly'),
        ('quarter', 'Quarterly')
    ])
    period_start = models.DateField()
    expected_demand = models.DecimalField(max_digits=10, decimal_places=2)
    demand_variance = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_point = models.PositiveIntegerField()
    suggested_stock_level = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'method_product_demand_forecast'
        unique_together = ['product', 'forecast_period', 'period_start']
        ordering = ['-period_start']
        
    def __str__(self):
        return f"Demand forecast for {self.product.name}: {self.forecast_period}"


class RiskAssessment(models.Model):
    RISK_TYPE_CHOICES = [
        ('customer_churn', 'Customer Churn Risk'),
        ('inventory_excess', 'Inventory Excess Risk'),
        ('price_sensitivity', 'Price Sensitivity Risk'),
        ('demand_fluctuation', 'Demand Fluctuation Risk')
    ]
    
    risk_type = models.CharField(max_length=50, choices=RISK_TYPE_CHOICES)
    entity_type = models.CharField(max_length=20, choices=[
        ('user', 'User'),
        ('product', 'Product')
    ])
    entity_id = models.PositiveIntegerField()
    risk_score = models.DecimalField(max_digits=5, decimal_places=3)
    confidence = models.DecimalField(max_digits=5, decimal_places=3)
    mitigation_suggestion = models.TextField(blank=True, null=True)
    assessment_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'method_risk_assessment'
        indexes = [
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['risk_type']),
        ]
        
    def __str__(self):
        return f"{self.risk_type} for {self.entity_type} #{self.entity_id}: {self.risk_score}"