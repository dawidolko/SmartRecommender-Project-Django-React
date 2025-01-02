from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),  # Endpoint do listy produktów
    path('products/<int:product_id>/', views.product_detail_extended, name='product_detail'),  # Endpoint do szczegółów produktu
]
