from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Category, Opinion, PhotoProduct

# Widok listowania produktów
def product_list(request):
    products = Product.objects.all()
    data = [
        {
            "id": p.id,
            "name": p.name,
            "price": str(p.price),
            "categories": [c.name for c in p.categories.all()],
        }
        for p in products
    ]
    return JsonResponse({"products": data})

# Widok szczegółów produktu
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Pobieranie pierwszego zdjęcia produktu
    photo = PhotoProduct.objects.filter(product=product).first()
    
    data = {
        "id": product.id,
        "name": product.name,
        "price": str(product.price),
        "old_price": str(product.old_price) if product.old_price else None,
        "description": product.description,
        "categories": [c.name for c in product.categories.all()],
        "photo": photo.path if photo else None,  # Dodanie ścieżki do zdjęcia
    }
    return JsonResponse(data)

# Widok opinii o produkcie
def product_opinions(request, product_id):
    opinions = Opinion.objects.filter(product_id=product_id)
    data = [
        {
            "user": o.user.username,
            "content": o.content,
            "rating": o.rating,
        }
        for o in opinions
    ]
    return JsonResponse({"opinions": data})

# Widok szczegółów z pełnym wyświetlaniem danych o produkcie (rozszerzony)
def product_detail_extended(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    photo = PhotoProduct.objects.filter(product=product).first()

    data = {
        "id": product.id,
        "name": product.name,
        "price": str(product.price),
        "old_price": str(product.old_price) if product.old_price else None,
        "description": product.description,
        "categories": [c.name for c in product.categories.all()],
        "photo": photo.path if photo else None,
        "specifications": [
            {
                "parameter_name": spec.parameter_name,
                "specification": spec.specification,
            }
            for spec in product.specification_set.all()
        ],
        "opinions": [
            {
                "user": opinion.user.username,
                "content": opinion.content,
                "rating": opinion.rating,
            }
            for opinion in product.opinion_set.all()
        ],
    }
    return JsonResponse(data)