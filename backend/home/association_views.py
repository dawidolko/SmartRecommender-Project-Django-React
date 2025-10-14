from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from collections import defaultdict
from django.core.cache import cache
from django.conf import settings
from .models import Order, OrderProduct, ProductAssociation, Product
from .serializers import ProductSerializer
from django.db.models import Prefetch, Count
from rest_framework.permissions import IsAuthenticated
from .custom_recommendation_engine import CustomAssociationRules


class FrequentlyBoughtTogetherAPI(APIView):
    def get(self, request):
        cart_product_ids = request.GET.getlist("product_ids[]")
        if not cart_product_ids:
            return Response([], status=status.HTTP_200_OK)

        print(f"Received cart product IDs: {cart_product_ids}")

        recommendations = []
        seen_product_ids = set()

        for product_id in cart_product_ids:
            try:
                product_id_int = int(product_id)
            except ValueError:
                continue

            associations = (
                ProductAssociation.objects.filter(product_1_id=product_id_int)
                .select_related("product_2")
                .order_by("-lift", "-confidence")[:5]
            )

            print(f"Found {associations.count()} associations for product {product_id}")

            for assoc in associations:
                if (
                    str(assoc.product_2_id) not in cart_product_ids
                    and assoc.product_2_id not in seen_product_ids
                ):
                    try:
                        product_data = ProductSerializer(assoc.product_2).data
                        recommendations.append(
                            {
                                "product": product_data,
                                "confidence": round(float(assoc.confidence), 2),
                                "lift": round(float(assoc.lift), 2),
                                "support": round(float(assoc.support), 3),
                            }
                        )
                        seen_product_ids.add(assoc.product_2_id)
                    except Exception as e:
                        print(f"Error serializing product {assoc.product_2_id}: {e}")
                        continue

        recommendations = sorted(
            recommendations, key=lambda x: (x["lift"], x["confidence"]), reverse=True
        )

        unique_recommendations = []
        seen_ids = set()

        for rec in recommendations:
            if rec["product"]["id"] not in seen_ids:
                unique_recommendations.append(rec)
                seen_ids.add(rec["product"]["id"])

        max_recommendations = int(request.GET.get('max_recommendations', 5))
        
        print(f"Returning {len(unique_recommendations[:max_recommendations])} unique recommendations (max: {max_recommendations})")
        return Response(unique_recommendations[:max_recommendations])


class UpdateAssociationRulesAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            min_support = float(request.data.get('min_support', 0.005))
            min_confidence = float(request.data.get('min_confidence', 0.05))  
            min_lift = float(request.data.get('min_lift', 1.0))
            
            print(f"Starting association rules update with thresholds: support={min_support}, confidence={min_confidence}, lift={min_lift}")
            
            cache_key = "association_rules_processing"
            if cache.get(cache_key):
                return Response(
                    {
                        "message": "Association rules update already in progress",
                        "cached": True
                    }
                )
            
            cache.set(cache_key, True, timeout=300)
            
            try:
                ProductAssociation.objects.all().delete()

                orders = Order.objects.prefetch_related(
                    Prefetch(
                        "orderproduct_set",
                        queryset=OrderProduct.objects.select_related("product"),
                    )
                ).all()[:2000]

                transactions = []
                for order in orders:
                    product_ids = [
                        str(item.product_id) for item in order.orderproduct_set.all()
                    ]
                    if len(product_ids) >= 2:
                        transactions.append(product_ids)

                if len(transactions) < 2:
                    print(f"⚠️ Not enough transactions: {len(transactions)} (need at least 2)")
                    return Response(
                        {
                            "message": "Not enough transactions to generate association rules.",
                            "rules_created": 0,
                            "total_transactions": len(transactions),
                        }
                    )

                print(f"✅ Processing {len(transactions)} transactions with Apriori algorithm")
                print(f"📊 Thresholds: support={min_support}, confidence={min_confidence}, lift={min_lift}")

                association_engine = CustomAssociationRules(
                    min_support=min_support, 
                    min_confidence=min_confidence
                )
                rules = association_engine.generate_association_rules(transactions)

                associations_to_create = []
                created_pairs = set()
                rules_processed = 0

                for rule in rules[:1000]:
                    try:
                        product_1_id = int(rule["product_1"])
                        product_2_id = int(rule["product_2"])

                        pair_key = (product_1_id, product_2_id)
                        if pair_key in created_pairs:
                            continue

                        if rule["lift"] < min_lift:
                            continue

                        associations_to_create.append(
                            ProductAssociation(
                                product_1_id=product_1_id,
                                product_2_id=product_2_id,
                                support=rule["support"],
                                confidence=rule["confidence"],
                                lift=rule["lift"],
                            )
                        )

                        created_pairs.add(pair_key)
                        rules_processed += 1

                        if len(associations_to_create) >= 200:
                            ProductAssociation.objects.bulk_create(associations_to_create)
                            associations_to_create = []

                    except (ValueError, KeyError) as e:
                        print(f"Error processing rule: {e}")
                        continue

                if associations_to_create:
                    ProductAssociation.objects.bulk_create(associations_to_create)

                print(f"✅ Created {rules_processed} association rules using Apriori algorithm")
                print(f"📊 Rules stats: {rules_processed} rules from {len(transactions)} transactions")
                
                if rules_processed == 0:
                    print(f"⚠️ No rules created! Check thresholds: support={min_support}, confidence={min_confidence}, lift={min_lift}")
                    print(f"💡 Try lowering thresholds or checking if transactions have enough product pairs")
                
                cache.delete("association_rules_list")
                
                return Response(
                    {
                        "message": f"Association rules updated successfully",
                        "rules_created": rules_processed,
                        "total_transactions": len(transactions),
                        "thresholds": {
                            "min_support": min_support,
                            "min_confidence": min_confidence,
                            "min_lift": min_lift
                        },
                        "algorithm": "Apriori Algorithm (Agrawal & Srikant 1994)",
                        "optimization": "Bitmap Pruning + Bulk Operations",
                    }
                )
                
            finally:
                cache.delete(cache_key)

        except Exception as e:
            print(f"Error in association rules update: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AssociationRulesListAPI(APIView):
    def get(self, request):
        # Check if user wants all rules
        fetch_all = request.GET.get("all", "").lower() == "true"
        
        if fetch_all:
            cache_key = "association_rules_all"
        else:
            cache_key = "association_rules_list"
        
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return Response({
                **cached_result,
                "cached": True
            })

        rules_query = (
            ProductAssociation.objects.all()
            .select_related("product_1", "product_2")
            .order_by("-lift")
        )
        
        # If not fetching all, limit to top 20
        if not fetch_all:
            rules_query = rules_query[:20]

        serialized_rules = []
        for rule in rules_query:
            serialized_rules.append(
                {
                    "id": rule.id,
                    "product_1": {"id": rule.product_1.id, "name": rule.product_1.name},
                    "product_2": {"id": rule.product_2.id, "name": rule.product_2.name},
                    "support": round(rule.support, 4),
                    "confidence": round(rule.confidence, 4),
                    "lift": round(rule.lift, 4),
                    "created_at": rule.created_at,
                }
            )

        result = {
            "rules": serialized_rules,
            "total_rules": len(serialized_rules),
            "implementation": "Enhanced Apriori Algorithm with Bitmap Pruning",
            "cached": False
        }
        
        cache.set(cache_key, result, timeout=getattr(settings, 'CACHE_TIMEOUT_MEDIUM', 1800))
        
        return Response(result)


class AssociationRulesAnalysisAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        top_support = ProductAssociation.objects.select_related(
            "product_1", "product_2"
        ).order_by("-support")[:5]

        top_confidence = ProductAssociation.objects.select_related(
            "product_1", "product_2"
        ).order_by("-confidence")[:5]

        top_lift = ProductAssociation.objects.select_related(
            "product_1", "product_2"
        ).order_by("-lift")[:5]

        def serialize_rule_list(rules):
            return [
                {
                    "product_1": rule.product_1.name,
                    "product_2": rule.product_2.name,
                    "support": round(rule.support, 4),
                    "confidence": round(rule.confidence, 4),
                    "lift": round(rule.lift, 4),
                }
                for rule in rules
            ]

        return Response(
            {
                "analysis": {
                    "top_support_rules": serialize_rule_list(top_support),
                    "top_confidence_rules": serialize_rule_list(top_confidence),
                    "top_lift_rules": serialize_rule_list(top_lift),
                    "total_rules": ProductAssociation.objects.count(),
                    "implementation": "Custom Manual Apriori Algorithm",
                }
            }
        )


class ProductAssociationDebugAPI(APIView):
    """
    Debug endpoint to analyze association rules for a specific product.
    Shows which products are recommended and why (with formulas).
    """

    def get(self, request):
        product_id = request.GET.get('product_id')
        if not product_id:
            return Response(
                {"error": "product_id parameter required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": f"Product {product_id} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        associations = ProductAssociation.objects.filter(
            product_1_id=product_id
        ).select_related('product_2').order_by('-lift', '-confidence')[:10]
        
        total_rules = ProductAssociation.objects.count()
        product_rules_count = ProductAssociation.objects.filter(product_1_id=product_id).count()
        
        transactions_with_product = OrderProduct.objects.filter(
            product_id=product_id
        ).values('order_id').distinct().count()
        
        multi_product_orders = Order.objects.annotate(
            product_count=Count('orderproduct')
        ).filter(product_count__gte=2)
        
        total_transactions = multi_product_orders.count()
        all_orders_count = Order.objects.count()
        single_product_orders_count = all_orders_count - total_transactions
        
        product_support = transactions_with_product / total_transactions if total_transactions > 0 else 0
        
        orders_with_product = Order.objects.filter(
            orderproduct__product_id=product_id
        ).select_related('user').prefetch_related('orderproduct_set__product').distinct()
        
        orders_details = []
        for order in orders_with_product:
            products_in_order = [
                {
                    "id": op.product.id,
                    "name": op.product.name,
                    "quantity": op.quantity
                }
                for op in order.orderproduct_set.all()
            ]
            orders_details.append({
                "order_id": order.id,
                "user": {
                    "id": order.user.id,
                    "email": order.user.email,
                    "first_name": order.user.first_name,
                    "last_name": order.user.last_name,
                    "username": order.user.username
                },
                "date_order": order.date_order.strftime("%Y-%m-%d %H:%M:%S"),
                "products": products_in_order,
                "total_items": len(products_in_order)
            })
        
        rules_details = []
        for assoc in associations:
            transactions_with_both = OrderProduct.objects.filter(
                product_id=product_id
            ).values('order_id').distinct().filter(
                order_id__in=OrderProduct.objects.filter(
                    product_id=assoc.product_2_id
                ).values('order_id')
            ).count()
            
            transactions_with_product2 = OrderProduct.objects.filter(
                product_id=assoc.product_2_id
            ).values('order_id').distinct().count()
            
            product2_support = transactions_with_product2 / total_transactions if total_transactions > 0 else 0
            
            rules_details.append({
                "product_2": {
                    "id": assoc.product_2.id,
                    "name": assoc.product_2.name
                },
                "metrics": {
                    "support": round(assoc.support, 4),
                    "confidence": round(assoc.confidence, 4),
                    "lift": round(assoc.lift, 4)
                },
                "formula_verification": {
                    "support_formula": f"Support(A,B) = {transactions_with_both}/{total_transactions} = {round(assoc.support, 4)}",
                    "confidence_formula": f"Confidence(A→B) = Support(A,B)/Support(A) = {round(assoc.support, 4)}/{round(product_support, 4)} = {round(assoc.confidence, 4)}",
                    "lift_formula": f"Lift(A→B) = Support(A,B)/(Support(A)×Support(B)) = {round(assoc.support, 4)}/({round(product_support, 4)}×{round(product2_support, 4)}) = {round(assoc.lift, 4)}"
                },
                "interpretation": {
                    "support": f"{round(assoc.support * 100, 2)}% of transactions contain both products",
                    "confidence": f"If customer buys {product.name}, there's {round(assoc.confidence * 100, 1)}% chance they'll buy {assoc.product_2.name}",
                    "lift": f"Products are bought together {round(assoc.lift, 2)}x more than random chance" if assoc.lift > 1 else f"Products are bought together {round(assoc.lift, 2)}x less than random chance"
                }
            })
        
        return Response({
            "product": {
                "id": product.id,
                "name": product.name
            },
            "statistics": {
                "all_orders_in_db": all_orders_count,
                "single_product_orders": single_product_orders_count,
                "multi_product_orders": total_transactions,
                "total_transactions_used_in_algorithm": total_transactions,
                "transactions_with_product": transactions_with_product,
                "product_support": round(product_support, 4),
                "total_rules_in_system": total_rules,
                "rules_for_this_product": product_rules_count,
                "note": f"Algorithm uses only {total_transactions} orders with 2+ products (excludes {single_product_orders_count} single-product orders)"
            },
            "orders_with_this_product": orders_details,
            "top_associations": rules_details,
            "formulas_used": {
                "support": "Support(A,B) = count(transactions with A and B) / total_transactions (only 2+ product orders)",
                "confidence": "Confidence(A→B) = Support(A,B) / Support(A)",
                "lift": "Lift(A→B) = Support(A,B) / (Support(A) × Support(B))"
            },
            "algorithm_behavior": {
                "filtering": "Association rules ONLY use orders with 2+ products",
                "reason": "Single-product orders cannot show 'bought together' patterns",
                "impact": f"Using {total_transactions} transactions instead of {all_orders_count} total orders"
            },
            "references": [
                "Agrawal, R., Srikant, R. (1994). Fast algorithms for mining association rules. VLDB.",
                "Brin, S., Motwani, R., Silverstein, C. (1997). Beyond market baskets. ACM SIGMOD."
            ]
        })
