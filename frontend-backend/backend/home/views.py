from django.db.models import Count
from random import sample
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse
from .models import Product, Category
from .serializers import ProductSerializer, ProductDetailSerializer

class CategoriesAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all().values("name")
        return Response(categories)

class ProductsAPIView(APIView):
    def get(self, request):
        products = Product.objects.prefetch_related("categories", "photoproduct_set").all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class RandomProductsAPIView(APIView):
    def get(self, request):
        all_products = Product.objects.annotate(photo_count=Count('photoproduct')).filter(photo_count__gt=0)
        random_products = sample(list(all_products), min(9, len(all_products)))
        serializer = ProductSerializer(random_products, many=True)
        return Response(serializer.data)

class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.prefetch_related(
        "categories", "photoproduct_set", "opinion_set", "specification_set"
    )
    serializer_class = ProductDetailSerializer

def home_view(request):
    return HttpResponse("Welcome to the Product Recommendation System!")
