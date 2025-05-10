from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from collections import defaultdict
from .models import Order, OrderProduct, ProductAssociation, Product
from .serializers import ProductSerializer
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated

class FrequentlyBoughtTogetherAPI(APIView):
    def get(self, request):
        cart_product_ids = request.GET.getlist('product_ids[]')
        if not cart_product_ids:
            return Response([], status=status.HTTP_200_OK)
        
        recommendations = []
        
        for product_id in cart_product_ids:
            associations = ProductAssociation.objects.filter(
                product_1_id=product_id
            ).select_related('product_2').order_by('-lift')[:3]
            
            for assoc in associations:
                if str(assoc.product_2_id) not in cart_product_ids:
                    recommendations.append({
                        'product': ProductSerializer(assoc.product_2).data,
                        'confidence': round(assoc.confidence, 2),
                        'lift': round(assoc.lift, 2)
                    })
        
        recommendations = sorted(recommendations, key=lambda x: x['lift'], reverse=True)
        
        unique_recommendations = []
        seen_ids = set()
        
        for rec in recommendations:
            if rec['product']['id'] not in seen_ids:
                unique_recommendations.append(rec)
                seen_ids.add(rec['product']['id'])
        
        return Response(unique_recommendations[:5])

class UpdateAssociationRulesAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            ProductAssociation.objects.all().delete()
            
            orders = Order.objects.prefetch_related(
                Prefetch('orderproduct_set', queryset=OrderProduct.objects.select_related('product'))
            ).all()
            
            transactions = []
            for order in orders:
                product_ids = [str(item.product_id) for item in order.orderproduct_set.all()]
                if product_ids:
                    transactions.append(product_ids)
            
            if len(transactions) < 2:
                return Response({
                    "message": "Not enough transactions to generate association rules.",
                    "rules_created": 0
                })
            
            rules = self.calculate_association_rules(transactions)
            rules_created = 0
            
            created_pairs = set()
            
            for rule in rules:
                try:
                    product_1_id = int(rule['product_1'])
                    product_2_id = int(rule['product_2'])
                    
                    pair_key = (product_1_id, product_2_id)
                    if pair_key in created_pairs:
                        continue
                    
                    ProductAssociation.objects.create(
                        product_1_id=product_1_id,
                        product_2_id=product_2_id,
                        support=rule['support'],
                        confidence=rule['confidence'],
                        lift=rule['lift']
                    )
                    
                    created_pairs.add(pair_key)
                    rules_created += 1
                    
                except Exception as e:
                    print(f"Error creating rule: {e}")
                    continue
            
            return Response({
                "message": "Association rules updated successfully",
                "rules_created": rules_created
            })
            
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def calculate_association_rules(self, transactions, min_support=0.01, min_confidence=0.1):
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
                    count_both = sum(1 for t in transactions 
                                   if item1 in t and item2 in t)
                    confidence = count_both / item_counts[item1]
                    
                    if confidence >= min_confidence:
                        support = count_both / total_transactions
                        lift = support / (item_support[item1] * item_support[item2])
                        
                        association_rules.append({
                            'product_1': item1,
                            'product_2': item2,
                            'support': support,
                            'confidence': confidence,
                            'lift': lift
                        })
        
        return association_rules

class AssociationRulesListAPI(APIView):
    def get(self, request):
        rules = ProductAssociation.objects.all().select_related(
            'product_1',
            'product_2'
        ).order_by('-lift')[:20] 
        
        serialized_rules = []
        for rule in rules:
            serialized_rules.append({
                'product_1': {
                    'id': rule.product_1.id,
                    'name': rule.product_1.name
                },
                'product_2': {
                    'id': rule.product_2.id,
                    'name': rule.product_2.name
                },
                'support': rule.support,
                'confidence': rule.confidence,
                'lift': rule.lift
            })
        
        return Response(serialized_rules)