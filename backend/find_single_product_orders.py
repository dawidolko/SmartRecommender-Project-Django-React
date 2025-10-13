#!/usr/bin/env python
"""
Skrypt do znalezienia zamówień z tylko 1 produktem
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from home.models import Order, OrderProduct
from django.db.models import Count

orders_by_product_count = Order.objects.annotate(
    product_count=Count('orderproduct')
).values('product_count').annotate(
    order_count=Count('id')
).order_by('product_count')

print("\n" + "="*70)
print("ROZKŁAD ZAMÓWIEŃ WEDŁUG LICZBY PRODUKTÓW")
print("="*70)
for item in orders_by_product_count:
    print(f"Zamówienia z {item['product_count']} produktami: {item['order_count']}")

single_product_orders = Order.objects.annotate(
    product_count=Count('orderproduct')
).filter(product_count=1)

print(f"\n{'='*70}")
print(f"ZAMÓWIENIA Z TYLKO 1 PRODUKTEM (Total: {single_product_orders.count()})")
print("="*70)

for order in single_product_orders[:20]: 
    product = order.orderproduct_set.first()
    print(f"Order #{order.id:3d} | User: {order.user.username:20s} | "
          f"Product: {product.product.name[:40]:40s} | Qty: {product.quantity}")

if single_product_orders.count() > 20:
    print(f"\n... i {single_product_orders.count() - 20} więcej zamówień z 1 produktem")

multi_product_orders = Order.objects.annotate(
    product_count=Count('orderproduct')
).filter(product_count__gte=2)

print(f"\n{'='*70}")
print(f"ZAMÓWIENIA Z 2+ PRODUKTAMI (używane w Apriori): {multi_product_orders.count()}")
print("="*70)

for order in multi_product_orders[:10]:
    products = order.orderproduct_set.all()
    product_names = ", ".join([f"{op.product.name} (x{op.quantity})" for op in products])
    print(f"Order #{order.id:3d} | User: {order.user.username:20s} | "
          f"Products ({len(products)}): {product_names[:80]}")

print(f"\n{'='*70}")
print("PODSUMOWANIE")
print("="*70)
total_orders = Order.objects.count()
single_count = single_product_orders.count()
multi_count = multi_product_orders.count()

print(f"Wszystkie zamówienia:              {total_orders}")
print(f"Zamówienia z 1 produktem:          {single_count} ({single_count/total_orders*100:.1f}%)")
print(f"Zamówienia z 2+ produktami:        {multi_count} ({multi_count/total_orders*100:.1f}%)")
print(f"\n✓ Algorytm Apriori używa {multi_count} transakcji (tylko 2+ produkty)")
print(f"✓ To dlatego Lift = 82.5 (używa {multi_count}), nie 50.0 (używałoby {total_orders})")
print("="*70 + "\n")
