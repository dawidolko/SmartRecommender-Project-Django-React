"""
Django Admin Panel Configuration for SmartRecommender E-commerce System.

This module customizes the Django admin interface for managing all database
models. Each ModelAdmin class defines how data is displayed, filtered, and
searched in the admin panel.

Admin Features:
    - list_display: Columns shown in list view
    - list_filter: Sidebar filters for quick data filtering
    - search_fields: Search bar functionality (uses LIKE queries)
    - Custom actions: Bulk operations on selected records

Access:
    URL: /admin/
    Permissions: superuser or is_staff=True required
    
Security:
    - Admin panel requires separate authentication from JWT API
    - Uses Django's built-in session authentication
    - CSRF protection enabled

Authors: Dawid Olko & Piotr Smoła
Date: 2025-11-02
Version: 2.0
"""

from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin interface for User model.
    
    Features:
        - List View: username, email, role (client/admin), active status
        - Filters: Filter by role or active status
        - Search: Find users by username or email
    
    Usage:
        Admin can view all registered users, change roles, deactivate accounts.
    """
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Category model.
    
    Features:
        - List View: category name, description
        - Search: Find categories by name
    
    Usage:
        Admin can create/edit product categories (e.g., "Electronics", "Clothing").
    """
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Admin interface for Sale model.
    
    Features:
        - List View: discount amount, start date, end date
        - Filters: Filter by date range
    
    Usage:
        Admin can create time-limited sales (e.g., "Black Friday: 20% off").
        Sales are automatically applied to products based on date range.
    """
    list_display = ('discount_amount', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for Product model.
    
    Features:
        - List View: product name, current price, old price, active sale
        - Filters: Filter by categories or active sales
        - Search: Find products by name
    
    Usage:
        Admin can manage product catalog:
        - Add new products with price, description, categories
        - Edit product details
        - Apply sales to products
        - Delete discontinued products
    """
    list_display = ('name', 'price', 'old_price', 'sale')
    list_filter = ('categories', 'sale')
    search_fields = ('name',)


@admin.register(PhotoProduct)
class PhotoProductAdmin(admin.ModelAdmin):
    """
    Admin interface for PhotoProduct model.
    
    Features:
        - List View: related product, photo path
    
    Usage:
        Admin can manage product images:
        - Upload multiple photos per product
        - View photo file paths
        - Delete unused photos
    
    Note:
        Photos are stored in /media/products/ directory.
    """
    list_display = ('product', 'path')


@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    """
    Admin interface for Opinion model.
    
    Features:
        - List View: product, user, rating (1-5 stars)
        - Filters: Filter by rating
        - Search: Find reviews by product name or username
    
    Usage:
        Admin can moderate product reviews:
        - View all customer reviews
        - Delete inappropriate reviews
        - Monitor product ratings
    
    Integration:
        Creating/editing opinion triggers handle_sentiment_analysis signal
        which automatically analyzes review sentiment.
    """
    list_display = ('product', 'user', 'rating')
    list_filter = ('rating',)
    search_fields = ('product__name', 'user__username')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Order model.
    
    Features:
        - List View: order ID, customer, order date, status
        - Filters: Filter by status (pending/completed/cancelled) or date
    
    Usage:
        Admin can manage customer orders:
        - View all orders
        - Change order status (pending → completed)
        - Cancel fraudulent orders
        - Monitor order history
    
    Order Statuses:
        - pending: Just created, payment pending
        - completed: Payment received, shipped
        - cancelled: Cancelled by customer or admin
    
    Integration:
        Creating order triggers handle_new_order_and_analytics signal
        which generates analytics and recommendations.
    """
    list_display = ('id', 'user', 'date_order', 'status')
    list_filter = ('status', 'date_order')


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    """
    Admin interface for OrderProduct model (junction table).
    
    Features:
        - List View: order, product, quantity
    
    Usage:
        Admin can view order line items:
        - See which products are in each order
        - Check quantities ordered
    
    Data Model:
        OrderProduct is a many-to-many relationship with extra fields:
        Order ←1---N→ OrderProduct ←N---1→ Product
        
        Extra fields: quantity, price_at_purchase
    """
    list_display = ('order', 'product', 'quantity')


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    """
    Admin interface for Complaint model.
    
    Features:
        - List View: related order, cause, status, submission date
        - Filters: Filter by status or submission date
    
    Usage:
        Admin can manage customer complaints:
        - View all complaints
        - Read complaint descriptions
        - Change status (pending → resolved)
        - Track complaint resolution
    
    Complaint Statuses:
        - pending: Submitted, awaiting review
        - in_progress: Being handled by support team
        - resolved: Issue fixed, customer satisfied
        - rejected: Complaint deemed invalid
    """
    list_display = ('order', 'cause', 'status', 'submission_date')
    list_filter = ('status', 'submission_date')


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    """
    Admin interface for Specification model.
    
    Features:
        - List View: product, parameter name, specification value
        - Search: Find specs by parameter name
    
    Usage:
        Admin can manage product technical specifications:
        - Add specs (e.g., "RAM: 16GB", "CPU: Intel i7")
        - Edit spec values
        - Delete outdated specs
    
    Example Specifications:
        Product: "Gaming Laptop"
        - parameter_name: "RAM", specification: "16GB DDR4"
        - parameter_name: "CPU", specification: "Intel i7-11800H"
        - parameter_name: "GPU", specification: "RTX 3070"
        - parameter_name: "Storage", specification: "1TB NVMe SSD"
    """
    list_display = ('product', 'parameter_name', 'specification')
    search_fields = ('parameter_name',)
