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
    path = serializers.SerializerMethodField()

    class Meta:
        model = PhotoProduct
        fields = ['path']

    def get_path(self, obj):
        return f"{obj.path}"

class OpinionSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email")

    class Meta:
        model = Opinion
        fields = ['user_email', 'content', 'rating']

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['parameter_name', 'specification']

class ProductDetailSerializer(serializers.ModelSerializer):
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
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    categories = serializers.SlugRelatedField(queryset=Category.objects.all(), many=True, slug_field='name', required=False)
    photos = PhotoProductSerializer(source='photoproduct_set', many=True, required=False)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.old_price = validated_data.get('old_price', instance.old_price)
        instance.description = validated_data.get('description', instance.description)

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

# ---------------------------
#   NEW SERIALIZERS
# ---------------------------


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderProduct
        fields = ["id", "product", "quantity"]

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(required=False)
    order_products = OrderProductSerializer(many=True, read_only=True, source='orderproduct_set')
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "user", "date_order", "status", "order_products", "total"]
        read_only_fields = ["date_order"]

    def get_total(self, obj):
        total_value = 0
        for op in obj.orderproduct_set.all():
            total_value += op.product.price * op.quantity
        return total_value


# Item in cart
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "user", "product", "quantity"]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    class Meta:
        model = Order
        fields = ["id", "user", "user_email", "date_order", "status"]

class ComplaintSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source="order.id", read_only=True)

    class Meta:
        model = Complaint
        fields = ["id", "order", "order_id", "cause", "status", "submission_date"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "role", "first_name", "last_name"]

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"
    
    def get_token(self, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        return token
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

    def validate_first_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("First name cannot be empty.")
        if len(value) > 50:
            raise serializers.ValidationError("First name must not exceed 50 characters.")
        if not re.match(r'^[A-Za-z]+$', value):
            raise serializers.ValidationError("First name can contain only letters.")
        return value

    def validate_last_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Last name cannot be empty.")
        if len(value) > 50:
            raise serializers.ValidationError("Last name must not exceed 50 characters.")
        if not re.match(r'^[A-Za-z]+$', value):
            raise serializers.ValidationError("Last name can contain only letters.")
        return value

    def validate_email(self, value):
        validator = EmailValidator()
        try:
            validator(value)
        except Exception:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_password(self, value):
        if value == "":
            return value  # If field is empty, we don't update
        if len(value) < 8:
            raise serializers.ValidationError("Password must have at least 8 characters.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        password = validated_data.get("password")
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
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
    nickname = serializers.CharField(source="username", required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["nickname", "email", "first_name", "last_name", "password"]

    def validate_first_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("First name cannot be empty.")
        if len(value) > 50:
            raise serializers.ValidationError("First name must not exceed 50 characters.")
        if not re.match(r'^[A-Za-z]+$', value):
            raise serializers.ValidationError("First name can contain only letters.")
        return value

    def validate_last_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Last name cannot be empty.")
        if len(value) > 50:
            raise serializers.ValidationError("Last name must not exceed 50 characters.")
        if not re.match(r'^[A-Za-z]+$', value):
            raise serializers.ValidationError("Last name can contain only letters.")
        return value

    def validate_email(self, value):
        validator = EmailValidator()
        try:
            validator(value)
        except Exception:
            raise serializers.ValidationError("Enter a valid email address.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value

    def create(self, validated_data):
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