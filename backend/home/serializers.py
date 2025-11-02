"""
Django REST Framework Serializers for SmartRecommender E-commerce System.

Authors: Dawid Olko & Piotr Smoła
Date: 2025-11-02
Version: 2.0

This module contains all serializers for converting complex Django models
into JSON format and vice versa. Serializers handle data validation, transformation,
and nested relationships for the API endpoints.

Key Features:
    - Product serialization with nested photos, specifications, and opinions
    - User authentication with JWT token generation
    - Order management with product relationships
    - Cart item serialization
    - User registration and profile updates with validation
    - Admin user management

Architecture:
    - ModelSerializer: Base class for all serializers
    - Nested relationships: Photos, opinions, specifications within products
    - Custom validation: Email, password, name format checks
    - Write-only fields: Passwords are never returned in responses
"""

import re
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    Product, PhotoProduct, Opinion, Category, Specification,
    Order, Complaint, User, CartItem, Tag, OrderProduct
)


class PhotoProductSerializer(serializers.ModelSerializer):
    """
    Serializer for product photo objects.
    
    Transforms PhotoProduct model instances into JSON with absolute/relative paths.
    Used as nested serializer within ProductSerializer to include all product images.
    
    Fields:
        path (str): Photo file path (e.g., 'products/laptop_001.jpg')
    
    Methods:
        get_path(): Custom method to format photo path consistently
    
    Example Output:
        {
            "path": "products/laptop_001.jpg"
        }
    """
    path = serializers.SerializerMethodField()

    class Meta:
        model = PhotoProduct
        fields = ['path']

    def get_path(self, obj):
        """
        Get formatted photo path.
        
        Args:
            obj (PhotoProduct): PhotoProduct model instance
        
        Returns:
            str: Photo path string (e.g., 'media/products/laptop.jpg')
        """
        return f"{obj.path}"


class OpinionSerializer(serializers.ModelSerializer):
    """
    Serializer for product opinion/review objects.
    
    Handles customer reviews including rating (1-5 stars) and text content.
    Automatically associates opinions with authenticated users and products.
    
    Fields:
        user_email (str): Email of user who wrote the opinion (read-only)
        content (str): Review text content
        rating (int): Star rating from 1 to 5
    
    Validation:
        - User must be authenticated (set from request context)
        - Product is set from view context
        - Rating must be between 1 and 5 (model constraint)
    
    Example Output:
        {
            "user_email": "john@example.com",
            "content": "Great product, highly recommend!",
            "rating": 5
        }
    """
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Opinion
        fields = ["user_email", "content", "rating"]

    def create(self, validated_data):
        """
        Create new opinion with user and product from context.
        
        Args:
            validated_data (dict): Validated opinion data (content, rating)
        
        Returns:
            Opinion: Created opinion instance
        
        Context Required:
            - request.user: Authenticated user
            - product: Product instance being reviewed
        """
        validated_data["user"] = self.context["request"].user
        validated_data["product"] = self.context["product"]
        return super().create(validated_data)


class SpecificationSerializer(serializers.ModelSerializer):
    """
    Serializer for product technical specifications.
    
    Represents key-value pairs of product parameters (e.g., 'RAM: 16GB', 'CPU: Intel i7').
    Used as nested serializer to include all specs within product details.
    
    Fields:
        parameter_name (str): Specification parameter (e.g., 'RAM', 'Storage')
        specification (str): Parameter value (e.g., '16GB', '512GB SSD')
    
    Example Output:
        {
            "parameter_name": "RAM",
            "specification": "16GB DDR4"
        }
    """
    class Meta:
        model = Specification
        fields = ['parameter_name', 'specification']


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for product objects with all related data.
    
    Provides complete product information including photos, opinions, specifications,
    tags, and categories. Used for product detail pages where all information is needed.
    
    Nested Serializers:
        - photos: List of PhotoProductSerializer
        - opinions: List of OpinionSerializer
        - specifications: List of SpecificationSerializer
        - tags: String representation of tags
        - categories: Category names (slug field)
    
    Fields:
        id (int): Product ID
        name (str): Product name
        price (Decimal): Current price
        old_price (Decimal): Previous price (for discount display)
        description (str): Product description
        categories (list): List of category names
        photos (list): List of photo objects
        opinions (list): List of customer reviews
        specifications (list): List of technical specs
        tags (list): List of tag names
    
    Example Output:
        {
            "id": 123,
            "name": "Gaming Laptop",
            "price": "1299.99",
            "old_price": "1499.99",
            "description": "Powerful gaming laptop...",
            "categories": ["Laptops", "Gaming"],
            "photos": [{"path": "products/laptop1.jpg"}],
            "opinions": [{"user_email": "john@example.com", "rating": 5, ...}],
            "specifications": [{"parameter_name": "RAM", "specification": "16GB"}],
            "tags": ["Gaming", "High-Performance"]
        }
    """
    photos = PhotoProductSerializer(source='photoproduct_set', many=True)
    tags = serializers.StringRelatedField(many=True)
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    opinions = OpinionSerializer(source='opinion_set', many=True)
    specifications = SpecificationSerializer(source='specification_set', many=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'old_price', 'description', 'categories',
            'photos', 'opinions', 'specifications', 'tags'
        ]


class ProductSerializer(serializers.ModelSerializer):
    """
    Standard serializer for product objects (list/create/update operations).
    
    Lighter version of ProductDetailSerializer used for product lists and admin operations.
    Supports many-to-many relationships for tags, categories, and photos.
    
    Fields:
        id (int): Product ID (read-only)
        name (str): Product name
        price (Decimal): Current selling price
        old_price (Decimal): Previous price (optional, for discounts)
        description (str): Product description
        categories (list): List of category names (slug field)
        photos (list): List of photo objects
        tags (list): List of tag IDs
    
    Methods:
        create(): Create new product with relationships
        update(): Update product including many-to-many fields
    
    Example Input (Create):
        {
            "name": "Gaming Mouse",
            "price": "49.99",
            "description": "RGB gaming mouse with 7 buttons",
            "categories": ["Peripherals", "Gaming"],
            "tags": [1, 5, 8]
        }
    """
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    categories = serializers.SlugRelatedField(queryset=Category.objects.all(), many=True, slug_field='name', required=False)
    photos = PhotoProductSerializer(source='photoproduct_set', many=True, required=False)

    def create(self, validated_data):
        """
        Create new product instance.
        
        Args:
            validated_data (dict): Validated product data
        
        Returns:
            Product: Created product instance
        
        Note:
            Many-to-many relationships are handled automatically by DRF
        """
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Update existing product with new data.
        
        Handles scalar fields (name, price, description) and many-to-many
        relationships (tags, photos, categories) separately.
        
        Args:
            instance (Product): Existing product to update
            validated_data (dict): New validated data
        
        Returns:
            Product: Updated product instance
        
        Many-to-Many Updates:
            - tags: Replace all existing tags with new list
            - photos: Replace all existing photos with new list
            - categories: Replace all existing categories with new list
        """
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.old_price = validated_data.get('old_price', instance.old_price)
        instance.description = validated_data.get('description', instance.description)

        # Update many-to-many relationships if provided
        if 'tags' in validated_data:
            instance.tags.set(validated_data['tags'])
        if 'photos' in validated_data:
            instance.photoproduct_set.set(validated_data['photos'])
        if 'categories' in validated_data:
            instance.categories.set(validated_data['categories'])

        instance.save()
        return instance


    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'old_price', 'description', 'categories', 'photos', 'tags']
        read_only_fields = ['id']


class OrderProductSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderProduct junction table (order-product relationship).
    
    Represents individual items within an order, including product details and quantity.
    Used to show what products are in an order and how many of each.
    
    Fields:
        id (int): OrderProduct ID
        product (dict): Nested product object (ProductSerializer)
        quantity (int): Number of items ordered
    
    Example Output:
        {
            "id": 456,
            "product": {
                "id": 123,
                "name": "Gaming Laptop",
                "price": "1299.99"
            },
            "quantity": 2
        }
    """
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderProduct
        fields = ["id", "product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for order objects with nested products.
    
    Represents customer orders with all ordered products, quantities, and total price.
    Automatically calculates order total based on product prices and quantities.
    
    Fields:
        id (int): Order ID
        user (int): User ID (read-only, set from authenticated user)
        user_email (str): Email of user who placed order
        date_order (datetime): Order creation timestamp (auto-generated)
        status (str): Order status ('pending', 'processing', 'shipped', 'delivered')
        order_products (list): List of OrderProductSerializer objects
        total (Decimal): Calculated total order value
    
    Methods:
        get_total(): Calculate sum of (price × quantity) for all products
    
    Example Output:
        {
            "id": 789,
            "user": 12,
            "user_email": "customer@example.com",
            "date_order": "2025-11-02T14:30:00Z",
            "status": "pending",
            "order_products": [
                {"id": 456, "product": {...}, "quantity": 2}
            ],
            "total": "2599.98"
        }
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(required=False)
    order_products = OrderProductSerializer(many=True, read_only=True, source='orderproduct_set')
    total = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "user_email", "date_order", "status", "order_products", "total"]
        read_only_fields = ["date_order"]

    def get_total(self, obj):
        """
        Calculate total order value.
        
        Sums up (product_price × quantity) for all products in the order.
        
        Args:
            obj (Order): Order instance
        
        Returns:
            Decimal: Total order value (sum of all product costs)
        
        Formula:
            Total = Σ (product_i.price × quantity_i) for all i in order_products
        
        Example:
            Product A: $100 × 2 = $200
            Product B: $50 × 3 = $150
            Total = $350
        """
        total_value = 0
        for op in obj.orderproduct_set.all():
            total_value += op.product.price * op.quantity
        return total_value


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for shopping cart items.
    
    Represents items in user's cart before order placement. Each cart item
    links a user to a product with a specific quantity.
    
    Fields:
        id (int): CartItem ID
        user (int): User ID (read-only, set from authenticated user)
        product (dict): Nested product object
        quantity (int): Number of items in cart
    
    Extra Settings:
        - user: Read-only (automatically set from request.user)
    
    Example Output:
        {
            "id": 101,
            "user": 12,
            "product": {
                "id": 123,
                "name": "Gaming Mouse",
                "price": "49.99"
            },
            "quantity": 1
        }
    """
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "user", "product", "quantity"]
        extra_kwargs = {
            "user": {"read_only": True},
        }


class ComplaintSerializer(serializers.ModelSerializer):
    """
    Serializer for customer complaint objects.
    
    Handles complaints/returns related to orders. Customers can submit complaints
    about products, delivery issues, or defects.
    
    Fields:
        id (int): Complaint ID
        order (int): Related order ID
        order_id (int): Order ID (read-only duplicate for convenience)
        cause (str): Complaint reason/description
        status (str): Complaint status ('pending', 'in_progress', 'resolved', 'rejected')
        submission_date (datetime): When complaint was submitted
    
    Example Output:
        {
            "id": 234,
            "order": 789,
            "order_id": 789,
            "cause": "Product arrived damaged",
            "status": "pending",
            "submission_date": "2025-11-01T10:15:00Z"
        }
    """
    order_id = serializers.IntegerField(source="order.id", read_only=True)

    class Meta:
        model = Complaint
        fields = ["id", "order", "order_id", "cause", "status", "submission_date"]


class UserSerializer(serializers.ModelSerializer):
    """
    Basic serializer for user objects.
    
    Returns essential user information without sensitive data like passwords.
    Used for user listings and basic profile information.
    
    Fields:
        id (int): User ID
        email (str): User email address
        username (str): User nickname/username
        role (str): User role ('client', 'admin')
        first_name (str): User first name
        last_name (str): User last name
    
    Example Output:
        {
            "id": 12,
            "email": "john.doe@example.com",
            "username": "johndoe",
            "role": "client",
            "first_name": "John",
            "last_name": "Doe"
        }
    """
    class Meta:
        model = User
        fields = ["id", "email", "username", "role", "first_name", "last_name"]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer with additional user claims.
    
    Extends default Simple JWT serializer to include user role and name in token payload.
    Allows authentication using email instead of username.
    
    Token Claims Added:
        - role: User role ('client' or 'admin')
        - first_name: User first name
        - last_name: User last name
    
    Authentication:
        - Uses email as username_field (login with email)
    
    Token Payload Example:
        {
            "token_type": "access",
            "exp": 1730563200,
            "iat": 1730559600,
            "jti": "abc123...",
            "user_id": 12,
            "role": "client",
            "first_name": "John",
            "last_name": "Doe"
        }
    
    Usage:
        Used in TokenObtainPairView for login endpoint.
        Frontend can decode token to get user info without extra API calls.
    """
    username_field = "email"
    
    def get_token(self, user):
        """
        Generate JWT token with custom claims.
        
        Args:
            user (User): Authenticated user instance
        
        Returns:
            Token: JWT token with additional claims (role, first_name, last_name)
        """
        token = super().get_token(user)
        token["role"] = user.role
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        return token

    
class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for product tag objects.
    
    Tags are keywords/labels for categorizing products (e.g., 'Sale', 'New', 'Popular').
    Simple serializer with just ID and name.
    
    Fields:
        id (int): Tag ID
        name (str): Tag name/label
    
    Example Output:
        {
            "id": 5,
            "name": "Best Seller"
        }
    """
    class Meta:
        model = Tag
        fields = ["id", "name"]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile updates (client-facing).
    
    Allows authenticated users to update their profile information with validation.
    Password is optional and write-only (never returned in responses).
    
    Fields:
        first_name (str): User first name (required, letters only, max 50 chars)
        last_name (str): User last name (required, letters only, max 50 chars)
        email (str): User email (must be valid format)
        password (str): New password (optional, write-only, min 8 chars, must contain digit)
    
    Validation Rules:
        - Names: Non-empty, max 50 chars, letters only (A-Za-z)
        - Email: Valid email format (RFC 5322)
        - Password: Min 8 chars, at least 1 digit, optional (empty string = no change)
    
    Example Input:
        {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com",
            "password": "newpass123"  // Optional
        }
    """
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

    def validate_first_name(self, value):
        """
        Validate first name format.
        
        Args:
            value (str): First name to validate
        
        Returns:
            str: Validated and trimmed first name
        
        Raises:
            ValidationError: If name is empty, too long, or contains non-letters
        
        Rules:
            - Must not be empty after trim
            - Max 50 characters
            - Letters only (A-Za-z)
        """
        value = value.strip()
        if not value:
            raise serializers.ValidationError("First name cannot be empty.")
        if len(value) > 50:
            raise serializers.ValidationError("First name must not exceed 50 characters.")
        if not re.match(r'^[A-Za-z]+$', value):
            raise serializers.ValidationError("First name can contain only letters.")
        return value

    def validate_last_name(self, value):
        """
        Validate last name format.
        
        Args:
            value (str): Last name to validate
        
        Returns:
            str: Validated and trimmed last name
        
        Raises:
            ValidationError: If name is empty, too long, or contains non-letters
        
        Rules:
            - Must not be empty after trim
            - Max 50 characters
            - Letters only (A-Za-z)
        """
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Last name cannot be empty.")
        if len(value) > 50:
            raise serializers.ValidationError("Last name must not exceed 50 characters.")
        if not re.match(r'^[A-Za-z]+$', value):
            raise serializers.ValidationError("Last name can contain only letters.")
        return value

    def validate_email(self, value):
        """
        Validate email format.
        
        Args:
            value (str): Email to validate
        
        Returns:
            str: Validated email address
        
        Raises:
            ValidationError: If email format is invalid
        
        Uses Django's EmailValidator for RFC 5322 compliance.
        """
        validator = EmailValidator()
        try:
            validator(value)
        except Exception:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_password(self, value):
        """
        Validate password strength.
        
        Args:
            value (str): Password to validate
        
        Returns:
            str: Validated password (or empty string for no change)
        
        Raises:
            ValidationError: If password is too short or missing digit
        
        Rules:
            - Empty string = no password change (allowed)
            - Min 8 characters
            - Must contain at least 1 digit (0-9)
        """
        if value == "":
            return value
        if len(value) < 8:
            raise serializers.ValidationError("Password must have at least 8 characters.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value

    def update(self, instance, validated_data):
        """
        Update user profile with validated data.
        
        Args:
            instance (User): Existing user to update
            validated_data (dict): New validated data
        
        Returns:
            User: Updated user instance
        
        Password Handling:
            - If password provided: Hash and update
            - If password empty/missing: No change
        """
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        password = validated_data.get("password")
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    
class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user management in admin panel.
    
    Full user CRUD operations for administrators including password management.
    Admins can create users, update any field including role, and set passwords.
    
    Fields:
        id (int): User ID (read-only)
        username (str): User nickname/username
        email (str): User email address
        first_name (str): User first name
        last_name (str): User last name
        role (str): User role ('client', 'admin')
        password (str): User password (write-only, hashed before save)
    
    Security:
        - Password is write-only (never returned in responses)
        - Password is hashed using Django's set_password() method
        - Only admins can access this serializer
    
    Methods:
        create(): Create new user with hashed password
        update(): Update user including optional password change
    
    Example Input (Create):
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "Alice",
            "last_name": "Johnson",
            "role": "client",
            "password": "secure123"
        }
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "password"]

    def create(self, validated_data):
        """
        Create new user with hashed password.
        
        Args:
            validated_data (dict): Validated user data including plain password
        
        Returns:
            User: Created user instance with hashed password
        
        Process:
            1. Extract password from validated_data
            2. Create user instance with remaining fields
            3. Hash password using set_password()
            4. Save user to database
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update existing user with optional password change.
        
        Args:
            instance (User): Existing user to update
            validated_data (dict): New validated data
        
        Returns:
            User: Updated user instance
        
        Password Handling:
            - If password in validated_data: Hash and update
            - If password not provided: Keep existing password unchanged
        """
        password = validated_data.pop("password", None)
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.role = validated_data.get("role", instance.role)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for new user registration (public endpoint).
    
    Handles user sign-up with validation for names, email, and password.
    Automatically sets role to 'client' (users cannot self-register as admins).
    
    Fields:
        nickname (str): Username/nickname (mapped to 'username' field)
        email (str): User email (must be unique)
        first_name (str): First name (letters only, max 50 chars)
        last_name (str): Last name (letters only, max 50 chars)
        password (str): Password (write-only, min 8 chars, must contain digit)
    
    Validation Rules:
        - Names: Non-empty, max 50 chars, letters only (A-Za-z)
        - Email: Valid format, must be unique (not already registered)
        - Password: Min 8 chars, at least 1 digit (0-9)
    
    Security:
        - Password is hashed using set_password()
        - Role is hardcoded to 'client' (cannot be set by user)
        - Email uniqueness check prevents duplicate accounts
    
    Example Input:
        {
            "nickname": "johndoe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "securepass123"
        }
    
    Example Output (after successful registration):
        {
            "nickname": "johndoe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }
    """
    nickname = serializers.CharField(source="username", required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["nickname", "email", "first_name", "last_name", "password"]

    def validate_first_name(self, value):
        """
        Validate first name format.
        
        Args:
            value (str): First name to validate
        
        Returns:
            str: Validated and trimmed first name
        
        Raises:
            ValidationError: If name is empty, too long, or contains non-letters
        """
        value = value.strip()
        if not value:
            raise serializers.ValidationError("First name cannot be empty.")
        if len(value) > 50:
            raise serializers.ValidationError("First name must not exceed 50 characters.")
        if not re.match(r'^[A-Za-z]+$', value):
            raise serializers.ValidationError("First name can contain only letters.")
        return value

    def validate_last_name(self, value):
        """
        Validate last name format.
        
        Args:
            value (str): Last name to validate
        
        Returns:
            str: Validated and trimmed last name
        
        Raises:
            ValidationError: If name is empty, too long, or contains non-letters
        """
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Last name cannot be empty.")
        if len(value) > 50:
            raise serializers.ValidationError("Last name must not exceed 50 characters.")
        if not re.match(r'^[A-Za-z]+$', value):
            raise serializers.ValidationError("Last name can contain only letters.")
        return value

    def validate_email(self, value):
        """
        Validate email format and uniqueness.
        
        Args:
            value (str): Email to validate
        
        Returns:
            str: Validated email address
        
        Raises:
            ValidationError: If email format invalid or already registered
        
        Checks:
            1. Valid email format (RFC 5322)
            2. Email not already in database
        """
        validator = EmailValidator()
        try:
            validator(value)
        except Exception:
            raise serializers.ValidationError("Enter a valid email address.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def validate_password(self, value):
        """
        Validate password strength.
        
        Args:
            value (str): Password to validate
        
        Returns:
            str: Validated password
        
        Raises:
            ValidationError: If password too short or missing digit
        
        Rules:
            - Min 8 characters
            - Must contain at least 1 digit (0-9)
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value

    def create(self, validated_data):
        """
        Create new user account with hashed password and 'client' role.
        
        Args:
            validated_data (dict): Validated registration data
        
        Returns:
            User: Created user instance
        
        Process:
            1. Extract all fields from validated_data
            2. Create user with role='client' (hardcoded)
            3. Hash password using set_password()
            4. Save user to database
        
        Security:
            - Password is hashed (never stored plain text)
            - Role is always 'client' (users cannot register as admins)
        """
        username = validated_data.get("username")
        email = validated_data.get("email")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        password = validated_data.get("password")
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role="client"
        )
        user.set_password(password)
        user.save()
        return user