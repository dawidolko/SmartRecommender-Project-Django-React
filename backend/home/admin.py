from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('discount_amount', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'old_price', 'sale')
    list_filter = ('categories', 'sale')
    search_fields = ('name',)

@admin.register(PhotoProduct)
class PhotoProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'path')

@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating')
    list_filter = ('rating',)
    search_fields = ('product__name', 'user__username')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_order', 'status')
    list_filter = ('status', 'date_order')

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('order', 'cause', 'status', 'submission_date')
    list_filter = ('status', 'submission_date')

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'parameter_name', 'specification')
    search_fields = ('parameter_name',)
