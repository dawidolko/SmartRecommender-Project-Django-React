from django.db.models import Count
from random import sample
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Product
from .serializers import ProductSerializer

class RandomProductsAPIView(APIView):
    def get(self, request):
        all_products = Product.objects.annotate(photo_count=Count('photoproduct')).filter(photo_count__gt=0)
        random_products = sample(list(all_products), min(9, len(all_products)))
        serializer = ProductSerializer(random_products, many=True)
        return Response(serializer.data)

def home_view(request):
    return HttpResponse("Witamy w systemie rekomendacji produktów!")
