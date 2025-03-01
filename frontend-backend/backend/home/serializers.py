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


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderProduct
        fields = ["id", "product", "quantity"]

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(required=False)
    order_products = OrderProductSerializer(many=True, read_only=True)
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

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        password = validated_data.get("password")
        if password:
            instance.set_password(password)
        instance.save()
        return instance
