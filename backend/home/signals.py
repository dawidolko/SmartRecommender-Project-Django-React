from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderProduct, ProductAssociation, Product
from collections import defaultdict
from django.db import transaction

@receiver(post_save, sender=Order)
def generate_association_rules(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: update_association_rules_after_order(instance))

def update_association_rules_after_order(order):
    orders = Order.objects.prefetch_related('orderproduct_set__product').all()
    
    transactions = []
    for order in orders:
        product_ids = []
        for item in order.orderproduct_set.all():
            product_ids.append(str(item.product_id))
        if product_ids:
            transactions.append(product_ids)
    
    rules = calculate_association_rules(transactions)
    
    ProductAssociation.objects.all().delete()
    for rule in rules:
        try:
            ProductAssociation.objects.get_or_create(
                product_1_id=int(rule['product_1']),
                product_2_id=int(rule['product_2']),
                support=rule['support'],
                confidence=rule['confidence'],
                lift=rule['lift']
            )
        except Exception as e:
            print(f"Error creating association rule: {e}")

def calculate_association_rules(transactions, min_support=0.01, min_confidence=0.1):
    item_counts = defaultdict(int)
    total_transactions = len(transactions)
    
    for transaction in transactions:
        for item in transaction:
            item_counts[item] += 1
    
    item_support = {item: count/total_transactions 
                   for item, count in item_counts.items()}
    
    frequent_items = {item for item, support in item_support.items() 
                     if support >= min_support}
    
    association_rules = []
    for transaction in transactions:
        transaction_items = [item for item in transaction 
                           if item in frequent_items]
        
        for i, item1 in enumerate(transaction_items):
            for item2 in transaction_items[i+1:]:
                count_1_to_2 = sum(1 for t in transactions 
                                 if item1 in t and item2 in t)
                count_2_to_1 = count_1_to_2  
                
                confidence_1_to_2 = count_1_to_2 / item_counts[item1]
                confidence_2_to_1 = count_2_to_1 / item_counts[item2]
                
                if confidence_1_to_2 >= min_confidence:
                    support = count_1_to_2 / total_transactions
                    lift = support / (item_support[item1] * item_support[item2])
                    
                    association_rules.append({
                        'product_1': item1,
                        'product_2': item2,
                        'support': support,
                        'confidence': confidence_1_to_2,
                        'lift': lift
                    })
                
                if confidence_2_to_1 >= min_confidence:
                    support = count_2_to_1 / total_transactions
                    lift = support / (item_support[item1] * item_support[item2])
                    
                    association_rules.append({
                        'product_1': item2,
                        'product_2': item1,
                        'support': support,
                        'confidence': confidence_2_to_1,
                        'lift': lift
                    })
    
    return association_rules