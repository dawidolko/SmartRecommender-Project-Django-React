from rest_framework import serializers
from .models import Product, PhotoProduct, Category

# Serializer for product images
class PhotoProductSerializer(serializers.ModelSerializer):
 classMeta:
 model = PhotoProduct
 fields = ['path']

# Serializer for products
class ProductSerializer(serializers.ModelSerializer):
 photos = PhotoProductSerializer(source='photoproduct_set', many=True)
 categories = serializers.SlugRelatedField(
 many=True,
 read_only=True,
 slug_field='name'
 )

 classMeta:
 model = Product
 fields = ['id', 'name', 'price', 'old_price', 'description', 'categories', 'photos']