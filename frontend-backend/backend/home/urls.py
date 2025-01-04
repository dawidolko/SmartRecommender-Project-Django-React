from django.urls import path
from .views import CategoriesAPIView, ProductsAPIView, RandomProductsAPIView, ProductDetailAPIView, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('api/categories/', CategoriesAPIView.as_view(), name='categories'),
    path('api/random-products/', RandomProductsAPIView.as_view(), name='random-products'),
    path('api/product/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('api/products/', ProductsAPIView.as_view(), name='products'),
]
