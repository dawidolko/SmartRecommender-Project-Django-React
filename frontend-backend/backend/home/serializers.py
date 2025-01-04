from rest_framework import serializers
from .models import Product, PhotoProduct, Opinion, Category, Specification

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
            'photos', 'opinions', 'specifications'
        ]

class ProductSerializer(serializers.ModelSerializer):
    photos = PhotoProductSerializer(source='photoproduct_set', many=True)
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'old_price', 'description', 'categories', 'photos']
