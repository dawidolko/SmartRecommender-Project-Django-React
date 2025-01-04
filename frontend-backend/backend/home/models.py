from django.contrib.auth.models import AbstractUser
from django.db import models

# User model with roles
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    class Meta:
        db_table = 'user'
        verbose_name = "User"
        verbose_name_plural = "Users"

# Product category
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

# Promotions
class Sale(models.Model):
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Sale {self.discount_amount}%"

    class Meta:
        db_table = 'sale'
        verbose_name = "Sale"
        verbose_name_plural = "Sales"
        ordering = ['start_date']

# Products
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, blank=True, null=True)
    categories = models.ManyToManyField('Category', through='ProductCategory')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']

# Relationship between products and categories
class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} -> {self.category.name}"

    class Meta:
        unique_together = (('product', 'category'),)
        db_table = 'product_category'
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

# Product photos
class PhotoProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)

    def __str__(self):
        return f"Photo for {self.product.name}"

    class Meta:
        db_table = 'photo_product'
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

# Product reviews
class Opinion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"Opinion by {self.user.username} on {self.product.name}"

    class Meta:
        db_table = 'opinion'
        verbose_name = "Opinion"
        verbose_name_plural = "Opinions"
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1, rating__lte=5), name="rating_range")
        ]

# Orders
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    class Meta:
        db_table = 'order'
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-date_order']

# Relationship between orders and products
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order {self.order.id} -> {self.product.name}"

    class Meta:
        db_table = 'order_product'
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"

# Complaints regarding orders
class Complaint(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cause = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint for Order {self.order.id}"

    class Meta:
        db_table = 'complaint'
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"
        ordering = ['-submission_date']

# Product technical specifications
class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parameter_name = models.CharField(max_length=50)
    specification = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.parameter_name} for {self.product.name}"

    class Meta:
        db_table = 'specification'
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"
