from django.urls import path
from .views import RandomProductsAPIView, home_view

urlpatterns = [
    path('', home_view, name='home'),
        path('api/random-products/', RandomProductsAPIView.as_view(), name='random-products'),
]
