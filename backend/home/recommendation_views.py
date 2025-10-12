from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.core.cache import cache
from django.conf import settings
from .models import (
    Product,
    User,
    Order,
    OrderProduct,
    RecommendationSettings,
    ProductSimilarity,
    UserProductRecommendation,
    CartItem,
    UserInteraction,
)
from .serializers import ProductSerializer
from collections import defaultdict
from rest_framework.permissions import IsAdminUser
from .custom_recommendation_engine import CustomContentBasedFilter
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        settings = RecommendationSettings.objects.filter(user=request.user).first()
        return Response(
            {
                "active_algorithm": (
                    settings.active_algorithm if settings else "collaborative"
                )
            }
        )

    def post(self, request):
        algorithm = request.data.get("algorithm", "collaborative")
        settings, created = RecommendationSettings.objects.get_or_create(
            user=request.user, defaults={"active_algorithm": algorithm}
        )
        if not created:
            settings.active_algorithm = algorithm
            settings.save()

        return Response(
            {
                "success": True,
                "message": f"Recommendation algorithm updated to {algorithm}",
                "active_algorithm": algorithm,
            }
        )


class ProcessRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        algorithm = request.data.get("algorithm", "collaborative")

        try:
            if algorithm == "collaborative":
                self.process_collaborative_filtering()
            else:
                self.process_content_based_filtering()

            return Response(
                {
                    "success": True,
                    "message": f"{algorithm} recommendations processed successfully",
                    "implementation": (
                        "Custom Manual Implementation"
                        if algorithm == "content_based"
                        else "Collaborative Filtering"
                    ),
                }
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def process_collaborative_filtering(self):
        cache_key = "collaborative_similarity_matrix"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            print("Using cached collaborative filtering results")
            return cached_result
        
        users = User.objects.all()
        products = Product.objects.all()
        
        print(f"Processing collaborative filtering for {users.count()} users and {products.count()} products")

        user_product_matrix = defaultdict(dict)
        for order in OrderProduct.objects.select_related("order", "product").all():
            user_product_matrix[order.order.user_id][order.product_id] = order.quantity

        user_ids = list(user_product_matrix.keys())
        product_ids = list(products.values_list("id", flat=True))

        if len(user_ids) < 2 or len(product_ids) < 2:
            print("Insufficient data for collaborative filtering")
            return 0

        matrix = []
        for user_id in user_ids:
            row = []
            for product_id in product_ids:
                row.append(user_product_matrix[user_id].get(product_id, 0))
            matrix.append(row)

        matrix = np.array(matrix, dtype=np.float32)
        
        print("Applying mean-centering (Adjusted Cosine Similarity - Sarwar et al. 2001)")
        normalized_matrix = np.zeros_like(matrix, dtype=np.float32)
        
        for i, user_row in enumerate(matrix):
            purchased_items = user_row[user_row > 0]
            
            if len(purchased_items) > 0:
                user_mean = np.mean(purchased_items)
                normalized_matrix[i] = user_row - user_mean
            else:
                normalized_matrix[i] = user_row

        if normalized_matrix.shape[0] > 1 and normalized_matrix.shape[1] > 1:
            product_similarity = cosine_similarity(normalized_matrix.T)
            
            ProductSimilarity.objects.filter(similarity_type="collaborative").delete()
            
            similarities_to_create = []
            similarity_count = 0
            
            similarity_threshold = 0.3
            
            for i, product1_id in enumerate(product_ids):
                for j, product2_id in enumerate(product_ids):
                    if i != j and product_similarity[i][j] > similarity_threshold:
                        similarities_to_create.append(
                            ProductSimilarity(
                                product1_id=product1_id,
                                product2_id=product2_id,
                                similarity_type="collaborative",
                                similarity_score=float(product_similarity[i][j])
                            )
                        )
                        similarity_count += 1
                        
                        if len(similarities_to_create) >= 1000:
                            ProductSimilarity.objects.bulk_create(similarities_to_create)
                            similarities_to_create = []
                            
            if similarities_to_create:
                ProductSimilarity.objects.bulk_create(similarities_to_create)
            
            print(f"Created {similarity_count} collaborative similarities using Adjusted Cosine Similarity (Sarwar et al. 2001) with threshold {similarity_threshold}")
            
            cache.set(cache_key, similarity_count, timeout=getattr(settings, 'CACHE_TIMEOUT_LONG', 7200))
            
            return similarity_count
        
        return 0

    def process_content_based_filtering(self):
        content_filter = CustomContentBasedFilter()
        similarity_count = content_filter.generate_similarities_for_all_products()
        print(
            f"Enhanced content-based filtering generated {similarity_count} similarities"
        )
        return similarity_count


class RecommendationPreviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        algorithm = request.GET.get("algorithm", "collaborative")

        # Handle fuzzy logic separately - it uses real-time computation
        if algorithm == "fuzzy_logic":
            from home.fuzzy_logic_engine import (
                FuzzyMembershipFunctions,
                FuzzyUserProfile,
                SimpleFuzzyInference
            )
            from home.models import Product
            from django.db.models import Count, Avg

            try:
                # Initialize fuzzy system
                membership_functions = FuzzyMembershipFunctions()
                user_profile = FuzzyUserProfile(user=request.user)
                fuzzy_engine = SimpleFuzzyInference(membership_functions, user_profile)

                # Get products with necessary annotations
                products_query = Product.objects.all().annotate(
                    review_count=Count('opinion'),
                    avg_rating=Avg('opinion__rating'),
                    order_count=Count('orderproduct', distinct=True)
                )[:100]

                # Score products
                scored_products = []
                for product in products_query:
                    product_categories = [cat.name for cat in product.categories.all()]
                    category_match = max([user_profile.fuzzy_category_match(cat) for cat in product_categories] or [0.0])

                    product_data = {
                        'price': float(product.price),
                        'rating': float(product.avg_rating) if product.avg_rating else 3.0,
                        'view_count': product.order_count if hasattr(product, 'order_count') else 0
                    }

                    fuzzy_result = fuzzy_engine.evaluate_product(product_data, category_match)
                    scored_products.append((product, fuzzy_result['fuzzy_score']))

                # Sort and take top 6
                scored_products.sort(key=lambda x: x[1], reverse=True)
                products = [p[0] for p in scored_products[:6]]

                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)

            except Exception as e:
                print(f"Error in fuzzy logic preview: {e}")
                import traceback
                traceback.print_exc()
                # Fallback to random products
                products = list(Product.objects.all()[:6])
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)

        # Handle collaborative and content_based normally
        recommendations = (
            UserProductRecommendation.objects.filter(
                user=request.user, recommendation_type=algorithm
            )
            .select_related("product")
            .order_by("-score")[:6]
        )

        if not recommendations.exists():
            similarities = ProductSimilarity.objects.filter(
                similarity_type=algorithm
            ).order_by("-similarity_score")[:10]

            products = [s.product2 for s in similarities]
        else:
            products = [r.product for r in recommendations]

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class GenerateUserRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        algorithm = request.data.get("algorithm", "collaborative")
        
        cache_key = f"user_recommendations_{request.user.id}_{algorithm}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return Response({
                "success": True,
                "message": f"User recommendations loaded from cache for {algorithm} algorithm",
                "recommendations_count": cached_result,
                "implementation": (
                    "Custom Manual Implementation"
                    if algorithm == "content_based"
                    else "Collaborative Filtering"
                ),
                "cached": True
            })

        user_products = []

        orders = Order.objects.filter(user=request.user)
        for order in orders:
            products = order.orderproduct_set.all()
            user_products.extend([op.product_id for op in products])

        cart_items = CartItem.objects.filter(user=request.user)
        user_products.extend([item.product_id for item in cart_items])

        recommendations = defaultdict(float)

        for product_id in set(user_products):
            similarities = ProductSimilarity.objects.filter(
                product1_id=product_id, similarity_type=algorithm
            ).order_by("-similarity_score")[:5]

            for similarity in similarities:
                recommendations[similarity.product2_id] += float(
                    similarity.similarity_score
                )

        recommendations_to_update = []
        for product_id, score in recommendations.items():
            recommendation, created = UserProductRecommendation.objects.get_or_create(
                user=request.user,
                product_id=product_id,
                recommendation_type=algorithm,
                defaults={"score": score}
            )
            if not created and recommendation.score != score:
                recommendation.score = score
                recommendations_to_update.append(recommendation)
                
        if recommendations_to_update:
            UserProductRecommendation.objects.bulk_update(recommendations_to_update, ['score'])

        cache.set(cache_key, len(recommendations), timeout=getattr(settings, 'CACHE_TIMEOUT_MEDIUM', 1800))

        return Response(
            {
                "success": True,
                "message": f"User recommendations generated for {algorithm} algorithm",
                "recommendations_count": len(recommendations),
                "implementation": (
                    "Custom Manual Implementation"
                    if algorithm == "content_based"
                    else "Collaborative Filtering"
                ),
                "cached": False
            }
        )


class CreateUserInteractionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        interaction_type = request.data.get("interaction_type")

        if not product_id or not interaction_type:
            return Response({"error": "Invalid data."}, status=400)

        UserInteraction.objects.create(
            user=request.user, product_id=product_id, interaction_type=interaction_type
        )
        return Response({"success": True})


class UpdateProductSimilarityView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        try:
            content_filter = CustomContentBasedFilter()
            similarity_count = content_filter.generate_similarities_for_all_products()

            product_count = Product.objects.count()

            return Response(
                {
                    "status": "success",
                    "message": f"Custom content-based similarity updated for {product_count} products",
                    "similarity_records_created": similarity_count,
                    "implementation": "Custom Manual Content-Based Filter",
                }
            )
        except Exception as e:
            import traceback

            return Response(
                {
                    "status": "error",
                    "message": str(e),
                    "traceback": traceback.format_exc(),
                },
                status=500,
            )


class RecommendationAlgorithmStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content_based_count = ProductSimilarity.objects.filter(
            similarity_type="content_based"
        ).count()

        collaborative_count = ProductSimilarity.objects.filter(
            similarity_type="collaborative"
        ).count()

        return Response(
            {
                "algorithms": {
                    "content_based": {
                        "implementation": "Custom Manual Implementation",
                        "similarity_count": content_based_count,
                        "description": "Jaccard similarity with manual feature extraction",
                    },
                    "collaborative": {
                        "implementation": "Scikit-learn Cosine Similarity",
                        "similarity_count": collaborative_count,
                        "description": "User-item matrix with cosine similarity",
                    },
                },
                "custom_implementations": [
                    "content_based",
                    "fuzzy_search",
                    "association_rules",
                    "sentiment_analysis",
                ],
            }
        )
