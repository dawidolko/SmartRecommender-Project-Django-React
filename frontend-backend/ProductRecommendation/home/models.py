from django.contrib.auth.models import AbstractUser
from django.db import models

# Model użytkownika z rolami
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)


# Model promocji
class Sale(models.Model):
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Sale {self.discount_amount}%"


# Model produktu
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, blank=True, null=True)
    categories = models.ManyToManyField('Category', through='ProductCategory')

    def __str__(self):
        return self.name


# Relacja między produktami a kategoriami
class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('product', 'category'),)
        db_table = 'product_category'  # Opcjonalnie zmień nazwę tabeli w bazie danych


# Zdjęcia produktów
class PhotoProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)

    def __str__(self):
        return f"Photo for {self.product.name}"


# Opinie o produktach
class Opinion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"Opinion by {self.user.username} on {self.product.name}"


# Zamówienia
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


# Relacja między zamówieniami a produktami
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


# Reklamacje dotyczące zamówień
class Complaint(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cause = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    submission_date = models.DateTimeField(auto_now_add=True)


# Specyfikacje techniczne produktów
class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parameter_name = models.CharField(max_length=50)
    specification = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.parameter_name} for {self.product.name}"
