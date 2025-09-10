from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from collections import defaultdict
from django.core.cache import cache
from django.conf import settings
from .models import Order, OrderProduct, ProductAssociation, Product
from .serializers import ProductSerializer
from django.db.models import Prefetch
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

        print(f"Returning {len(unique_recommendations)} unique recommendations")
        return Response(unique_recommendations[:5])


class UpdateAssociationRulesAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            print("Starting enhanced association rules update...")
            
            # Sprawdź cache
            cache_key = "association_rules_processing"
            if cache.get(cache_key):
                return Response(
                    {
                        "message": "Association rules update already in progress",
                        "cached": True
                    }
                )
            
            # Ustaw cache że przetwarzanie trwa
            cache.set(cache_key, True, timeout=300)  # 5 minut
            
            try:
                # Usuwanie starych reguł
                ProductAssociation.objects.all().delete()

                # ZWIĘKSZONE: z 1000 do 2000 zamówień
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
                    return Response(
                        {
                            "message": "Not enough transactions to generate association rules.",
                            "rules_created": 0,
                        }
                    )

                print(f"Processing {len(transactions)} transactions with enhanced algorithm")

                # NOWA: Ulepszona wersja z bitmap pruning
                association_engine = CustomAssociationRules(
                    min_support=0.008, min_confidence=0.08  # Nieco niższe progi dla większej ilości reguł
                )
                rules = association_engine.generate_association_rules(transactions)

                # BULK OPERATIONS: Tworzenie reguł w batch'ach
                associations_to_create = []
                created_pairs = set()
                rules_processed = 0

                # ZWIĘKSZONE: z 500 do 1000 reguł
                for rule in rules[:1000]:
                    try:
                        product_1_id = int(rule["product_1"])
                        product_2_id = int(rule["product_2"])

                        pair_key = (product_1_id, product_2_id)
                        if pair_key in created_pairs:
                            continue

                        # Dodanie do listy bulk create
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

                        # BULK CREATE co 200 reguł
                        if len(associations_to_create) >= 200:
                            ProductAssociation.objects.bulk_create(associations_to_create)
                            associations_to_create = []

                    except (ValueError, KeyError) as e:
                        print(f"Error processing rule: {e}")
                        continue

                # Utworzenie pozostałych reguł
                if associations_to_create:
                    ProductAssociation.objects.bulk_create(associations_to_create)

                print(f"Created {rules_processed} enhanced association rules using bitmap pruning")
                
                # Invalidate related caches
                cache.delete("association_rules_list")
                
                return Response(
                    {
                        "message": f"Enhanced association rules updated successfully",
                        "rules_created": rules_processed,
                        "total_transactions": len(transactions),
                        "algorithm": "Enhanced Apriori with Bitmap Pruning",
                        "optimization": "Bulk operations + Caching",
                    }
                )
                
            finally:
                # Usuń cache przetwarzania
                cache.delete(cache_key)

        except Exception as e:
            print(f"Error in association rules update: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AssociationRulesListAPI(APIView):
    def get(self, request):
        # Sprawdź cache
        cache_key = "association_rules_list"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return Response({
                **cached_result,
                "cached": True
            })

        rules = (
            ProductAssociation.objects.all()
            .select_related("product_1", "product_2")
            .order_by("-lift")[:20]
        )

        serialized_rules = []
        for rule in rules:
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
        
        # Cache wyników na 30 minut
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
