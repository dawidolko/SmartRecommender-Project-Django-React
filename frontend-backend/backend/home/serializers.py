from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    Product, PhotoProduct, Opinion, Category, Specification,
    Order, Complaint, User, CartItem, Tag
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
    photos = PhotoProductSerializer(source='photoproduct_set', many=True)
    tags = serializers.StringRelatedField(many=True)
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'old_price', 'description', 'categories', 'photos', 'tags']

# ---------------------------
#   NEW SERIALIZERS
# ---------------------------

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

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
    def get_token(self, user):
        token = super().get_token(user)
        token["role"] = user.role
        return token
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]