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
    """
    API View for managing recommendation algorithm settings.
    
    This view handles GET and POST requests to retrieve and update the active
    recommendation algorithm configuration. Supports switching between different
    recommendation strategies (collaborative filtering, content-based, etc.).
    
    Attributes:
        permission_classes: Requires authenticated user access
        
    Methods:
        get: Retrieves current active algorithm setting
        post: Updates active algorithm setting for all users
    """
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the currently active recommendation algorithm.
        
        Returns:
            Response: JSON containing the active algorithm name
                Example: {"active_algorithm": "collaborative"}
        """
        settings = RecommendationSettings.objects.first()
        return Response(
            {"active_algorithm": (settings.active_algorithm if settings else None)}
        )

    def post(self, request):
        """
        Update the active recommendation algorithm system-wide.
        
        Args:
            request: HTTP request containing algorithm selection
                Expected data: {"algorithm": "collaborative"|"content_based"|"hybrid"}
        
        Returns:
            Response: Success confirmation with updated algorithm name
            
        Note:
            This updates the setting globally for all users and ensures
            only one active configuration exists in the database.
        """
        algorithm = request.data.get("algorithm", "collaborative")

        settings = RecommendationSettings.objects.first()

        if settings:
            settings.active_algorithm = algorithm
            settings.save()
        else:
            settings = RecommendationSettings.objects.create(
                user=request.user, active_algorithm=algorithm
            )

        # Ensure all other settings use the same algorithm
        RecommendationSettings.objects.exclude(id=settings.id).update(
            active_algorithm=algorithm
        )

        return Response(
            {
                "success": True,
                "message": f"Recommendation algorithm updated to {algorithm}",
                "active_algorithm": algorithm,
            }
        )


class ProcessRecommendationsView(APIView):
    """
    API View for processing and computing product recommendations.
    
    This view triggers the computation of product similarities and recommendations
    based on the selected algorithm. Supports both collaborative filtering and
    content-based filtering approaches.
    
    Collaborative Filtering:
        - Uses Adjusted Cosine Similarity (Sarwar et al., 2001)
        - Formula: sim(i,j) = Σ(R_u,i - R̄_u)(R_u,j - R̄_u) / √[Σ(R_u,i - R̄_u)² × Σ(R_u,j - R̄_u)²]
        - Based on user purchase patterns and item co-occurrence
    
    Content-Based Filtering:
        - Uses TF-IDF vectorization and Cosine Similarity
        - Formula: cos(θ) = (A · B) / (||A|| × ||B||)
        - Analyzes product features (name, description, category, tags)
    
    Attributes:
        permission_classes: Requires authenticated user access
        
    Methods:
        post: Triggers recommendation computation for selected algorithm
        process_collaborative_filtering: Implements CF using Adjusted Cosine
        process_content_based_filtering: Implements CBF using TF-IDF
    """
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Process recommendations using the specified algorithm.
        
        Args:
            request: HTTP request with algorithm selection
                Expected data: {"algorithm": "collaborative"|"content_based"}
        
        Returns:
            Response: Success/error message with algorithm details
            
        Raises:
            HTTP_500_INTERNAL_SERVER_ERROR: If computation fails
        """
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
        """
        Compute product similarities using Collaborative Filtering.
        
        Implementation Details:
            1. Builds user-product interaction matrix from purchase history
            2. Applies Adjusted Cosine Similarity algorithm (Sarwar et al., 2001)
            3. Mean-centers user ratings to account for rating bias
            4. Computes pairwise item similarities
            5. Filters similarities above threshold (0.3)
            6. Caches results for 2 hours
        
        Formula:
            sim(i,j) = Σ_u∈U(R_u,i - R̄_u)(R_u,j - R̄_u) / 
                      √[Σ_u∈U(R_u,i - R̄_u)² × Σ_u∈U(R_u,j - R̄_u)²]
        
        Where:
            - R_u,i: Rating (quantity) of user u for item i
            - R̄_u: Mean rating of user u across all items
            - U: Set of users who rated both items i and j
        
        Returns:
            Cached similarity matrix
            
        Note:
            Results are stored in ProductSimilarity model with type="collaborative"
        """
        cache_key = "collaborative_similarity_matrix"
        cached_result = cache.get(cache_key)

        if cached_result:
            print("Using cached collaborative filtering results")
            return cached_result
        users = User.objects.all()
        products = Product.objects.all()

        print(
            f"Processing collaborative filtering for {users.count()} users and {products.count()} products"
        )

        # Build user-product interaction matrix from purchase history
        user_product_matrix = defaultdict(dict)
        for order in OrderProduct.objects.select_related("order", "product").all():
            user_product_matrix[order.order.user_id][order.product_id] = order.quantity

        user_ids = list(user_product_matrix.keys())
        product_ids = list(products.values_list("id", flat=True))

        # Validate sufficient data for computation
        if len(user_ids) < 2 or len(product_ids) < 2:
            print("Insufficient data for collaborative filtering")
            return 0

        # Create dense matrix representation
        matrix = []
        for user_id in user_ids:
            row = []
            for product_id in product_ids:
                row.append(user_product_matrix[user_id].get(product_id, 0))
            matrix.append(row)

        matrix = np.array(matrix, dtype=np.float32)

        # Apply mean-centering for Adjusted Cosine Similarity (Sarwar et al., 2001)
        print(
            "Applying mean-centering (Adjusted Cosine Similarity - Sarwar et al. 2001)"
        )
        normalized_matrix = np.zeros_like(matrix, dtype=np.float32)

        # Mean-center each user's ratings to account for rating bias
        for i, user_row in enumerate(matrix):
            purchased_items = user_row[user_row > 0]

            if len(purchased_items) > 0:
                user_mean = np.mean(purchased_items)
                # Subtract user mean from all rated items
                for j, val in enumerate(user_row):
                    if val > 0:
                        normalized_matrix[i][j] = val - user_mean
                    else:
                        normalized_matrix[i][j] = 0
            else:
                normalized_matrix[i] = user_row

        # Compute item-item similarities using cosine similarity on transposed matrix
        if normalized_matrix.shape[0] > 1 and normalized_matrix.shape[1] > 1:
            product_similarity = cosine_similarity(normalized_matrix.T)

            # Clear old collaborative similarities
            ProductSimilarity.objects.filter(similarity_type="collaborative").delete()

            similarities_to_create = []
            similarity_count = 0

            # Threshold for storing similarities (reduces storage for sparse data)
            similarity_threshold = 0.5

            # Store only significant similarities above threshold
            for i, product1_id in enumerate(product_ids):
                for j, product2_id in enumerate(product_ids):
                    if i != j and product_similarity[i][j] > similarity_threshold:
                        similarities_to_create.append(
                            ProductSimilarity(
                                product1_id=product1_id,
                                product2_id=product2_id,
                                similarity_type="collaborative",
                                similarity_score=float(product_similarity[i][j]),
                            )
                        )
                        similarity_count += 1

                        # Batch insert for performance
                        if len(similarities_to_create) >= 1000:
                            ProductSimilarity.objects.bulk_create(
                                similarities_to_create
                            )
                            similarities_to_create = []

            # Insert remaining similarities
            if similarities_to_create:
                ProductSimilarity.objects.bulk_create(similarities_to_create)

            print(
                f"Created {similarity_count} collaborative similarities using Adjusted Cosine Similarity (Sarwar et al. 2001) with threshold {similarity_threshold}"
            )

            # Cache results for 2 hours
            cache.set(
                cache_key,
                similarity_count,
                timeout=getattr(settings, "CACHE_TIMEOUT_LONG", 7200),
            )

            return similarity_count

        return 0

    def process_content_based_filtering(self):
        """
        Compute product similarities using Content-Based Filtering.
        
        Implementation Details:
            1. Uses TF-IDF vectorization on product features
            2. Applies Cosine Similarity for feature vector comparison
            3. Analyzes: product name, description, category, tags
            4. Delegates to CustomContentBasedFilter class
        
        Formula (Cosine Similarity):
            cos(θ) = (A · B) / (||A|| × ||B||)
            
        Where:
            - A, B: TF-IDF feature vectors for products
            - A · B: Dot product of vectors
            - ||A||, ||B||: Euclidean norms of vectors
        
        Returns:
            int: Number of similarities generated
            
        Note:
            Results stored in ProductSimilarity model with type="content_based"
        """
        content_filter = CustomContentBasedFilter()
        similarity_count = content_filter.generate_similarities_for_all_products()
        print(
            f"Enhanced content-based filtering generated {similarity_count} similarities"
        )
        return similarity_count


class RecommendationPreviewView(APIView):
    """
    API View for generating personalized product recommendations.
    
    Supports multiple recommendation strategies:
        1. Fuzzy Logic: Uses fuzzy membership functions for user preferences
        2. Collaborative Filtering: Uses item-item similarities
        3. Content-Based: Uses TF-IDF and feature matching
        4. Hybrid: Combines multiple approaches
    
    Fuzzy Logic Implementation:
        - Membership functions: triangular, trapezoidal, gaussian
        - Input variables: price preference, rating sensitivity, category affinity
        - Output: fuzzy score for each product
        - Defuzzification: centroid method
    
    Attributes:
        permission_classes: Requires authenticated user access
        
    Methods:
        get: Generate and return top N recommendations for user
    """
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Generate personalized product recommendations for authenticated user.
        
        Args:
            request: HTTP request with query parameters
                - algorithm: str (default "collaborative")
                  Options: "fuzzy_logic", "collaborative", "content_based"
                - limit: int (default varies by algorithm)
        
        Returns:
            Response: JSON with recommended products
                {
                    "algorithm": str,
                    "count": int,
                    "products": [serialized product objects],
                    "fuzzy_scores": {...} (if fuzzy_logic)
                }
        
        Raises:
            HTTP_500: If fuzzy logic computation fails
        """
        algorithm = request.GET.get("algorithm", "collaborative")

        if algorithm == "fuzzy_logic":
            from home.fuzzy_logic_engine import (
                FuzzyMembershipFunctions,
                FuzzyUserProfile,
                SimpleFuzzyInference,
            )
            from home.models import Product
            from django.db.models import Count, Avg

            try:
                # Initialize fuzzy logic components
                membership_functions = FuzzyMembershipFunctions()
                user_profile = FuzzyUserProfile(user=request.user)
                fuzzy_engine = SimpleFuzzyInference(membership_functions, user_profile)

                # Fetch products with aggregated statistics
                products_query = Product.objects.all().annotate(
                    review_count=Count("opinion"),
                    avg_rating=Avg("opinion__rating"),
                    order_count=Count("orderproduct", distinct=True),
                )[:100]

                scored_products = []
                for product in products_query:
                    # Calculate category match using fuzzy logic
                    product_categories = [cat.name for cat in product.categories.all()]
                    category_match = max(
                        [
                            user_profile.fuzzy_category_match(cat)
                            for cat in product_categories
                        ]
                        or [0.0]
                    )

                    product_data = {
                        "price": float(product.price),
                        "rating": (
                            float(product.avg_rating) if product.avg_rating else 3.0
                        ),
                        "view_count": (
                            product.order_count
                            if hasattr(product, "order_count")
                            else 0
                        ),
                    }

                    fuzzy_result = fuzzy_engine.evaluate_product(
                        product_data, category_match
                    )
                    scored_products.append((product, fuzzy_result["fuzzy_score"]))

                scored_products.sort(key=lambda x: x[1], reverse=True)
                products = [p[0] for p in scored_products[:6]]

                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)

            except Exception as e:
                print(f"Error in fuzzy logic preview: {e}")
                import traceback

                traceback.print_exc()
                products = list(Product.objects.all()[:6])
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)

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
            return Response(
                {
                    "success": True,
                    "message": f"User recommendations loaded from cache for {algorithm} algorithm",
                    "recommendations_count": cached_result,
                    "implementation": (
                        "Custom Manual Implementation"
                        if algorithm == "content_based"
                        else "Collaborative Filtering"
                    ),
                    "cached": True,
                }
            )

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
                defaults={"score": score},
            )
            if not created and recommendation.score != score:
                recommendation.score = score
                recommendations_to_update.append(recommendation)

        if recommendations_to_update:
            UserProductRecommendation.objects.bulk_update(
                recommendations_to_update, ["score"]
            )

        cache.set(
            cache_key,
            len(recommendations),
            timeout=getattr(settings, "CACHE_TIMEOUT_MEDIUM", 1800),
        )

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
                "cached": False,
            }
        )


class CreateUserInteractionAPI(APIView):
    """
    API View for tracking user interactions with products.
    
    Records user behavioral data including:
        - Views: Product page visits
        - Clicks: Product detail interactions
        - Cart additions: Add to cart actions
        - Purchases: Order completions
        - Wishlist: Favorite product additions
    
    This data is used to enhance recommendation algorithms by
    incorporating implicit feedback signals.
    
    Attributes:
        permission_classes: Requires authenticated user access
        
    Methods:
        post: Create new user interaction record
    """
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Record a user interaction event.
        
        Args:
            request: HTTP request with interaction data
                Required fields:
                    - product_id: int
                    - interaction_type: str ("view"|"click"|"cart"|"purchase"|"wishlist")
        
        Returns:
            Response: Success confirmation or error message
            
        Raises:
            HTTP_400: If required fields are missing
        """
        product_id = request.data.get("product_id")
        interaction_type = request.data.get("interaction_type")

        if not product_id or not interaction_type:
            return Response({"error": "Invalid data."}, status=400)

        UserInteraction.objects.create(
            user=request.user, product_id=product_id, interaction_type=interaction_type
        )
        return Response({"success": True})


class UpdateProductSimilarityView(APIView):
    """
    API View for manually triggering product similarity computation.
    
    This endpoint allows administrators to refresh product similarities
    using the content-based filtering algorithm. Useful for:
        - Updating similarities after product catalog changes
        - Manual recomputation without waiting for scheduled tasks
        - Testing algorithm modifications
    
    Content-Based Algorithm:
        - TF-IDF vectorization of product features
        - Cosine similarity for feature comparison
        - Custom feature extraction (name, description, tags, category)
    
    Attributes:
        permission_classes: Requires authenticated admin user
        
    Methods:
        post: Trigger similarity computation
    """
    
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        """
        Trigger content-based similarity computation for all products.
        
        Returns:
            Response: Computation statistics
                {
                    "status": "success"|"error",
                    "message": str,
                    "similarity_records_created": int,
                    "implementation": str
                }
        
        Raises:
            HTTP_500: If computation fails with traceback
        """
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
    """
    API View for retrieving recommendation system status and statistics.
    
    Provides overview of:
        - Available recommendation algorithms
        - Similarity count for each algorithm type
        - Implementation details (manual vs library)
        - System health indicators
    
    Useful for:
        - Admin dashboard monitoring
        - Debugging recommendation system
        - Performance tracking
    
    Attributes:
        permission_classes: Requires authenticated user access
        
    Methods:
        get: Retrieve algorithm status and statistics
    """
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get status and statistics for all recommendation algorithms.
        
        Returns:
            Response: Algorithm statistics with implementation details
                - algorithms: Dict with content_based and collaborative stats
                - custom_implementations: List of custom algorithm names
        """
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


class CollaborativeFilteringDebugView(APIView):
    """
    Debug API endpoint for Collaborative Filtering diagnostics.
    
    Provides detailed debugging information for CF algorithm including:
        - User-product interaction matrix statistics
        - Similarity computation status
        - Cache performance metrics
        - Data quality indicators
        - System health checks
    
    Helps administrators diagnose issues with:
        - Insufficient training data
        - Matrix sparsity problems
        - Cache misses
        - Similarity computation failures
    
    Algorithm: Adjusted Cosine Similarity (Sarwar et al., 2001)
    
    Attributes:
        permission_classes: Public endpoint (no authentication required)
        
    Methods:
        get: Return comprehensive CF debug information
    """

    permission_classes = []

    def get(self, request):
        """
        Generate comprehensive debug report for Collaborative Filtering.
        
        Returns:
            Response: Debug report JSON containing:
                - database_stats: User, product, and order counts
                - matrix_info: Matrix dimensions and sparsity
                - similarity_matrix_info: Stored similarities count
                - cache_info: Cache status and configuration
                - top_10_similarities: Preview of best similarities
                - sample_user_vector: Example user purchase vector
                - computation_status: System readiness indicators
                - how_to_fix: Troubleshooting instructions
        
        Raises:
            HTTP_500: If debug data retrieval fails
        """
        try:
            users = User.objects.all()
            products = Product.objects.all()
            orders = OrderProduct.objects.all()

            users_count = users.count()
            products_count = products.count()
            orders_count = orders.count()

            # Check cache status for similarity matrix
            cache_key = "collaborative_similarity_matrix"
            cached_result = cache.get(cache_key)
            cache_status = (
                "HIT (data cached)" if cached_result else "MISS (no data)"
            )

            # Build user-product interaction matrix
            user_product_matrix = defaultdict(dict)
            for order in orders.select_related("order", "product"):
                user_product_matrix[order.order.user_id][
                    order.product_id
                ] = order.quantity

            users_with_purchases = len(user_product_matrix.keys())
            total_purchases = sum(
                len(products) for products in user_product_matrix.values()
            )

            # Calculate matrix statistics
            matrix_shape = f"({users_with_purchases}, {products_count})"
            total_cells = users_with_purchases * products_count
            sparsity = (
                ((total_cells - total_purchases) / total_cells * 100)
                if total_cells > 0
                else 0
            )

            cf_similarities = ProductSimilarity.objects.filter(
                similarity_type="collaborative"
            )
            cf_count = cf_similarities.count()

            total_possible_pairs = products_count * (products_count - 1)
            percentage_saved = (
                (cf_count / total_possible_pairs * 100)
                if total_possible_pairs > 0
                else 0
            )

            top_10 = cf_similarities.order_by("-similarity_score")[:10]
            top_similarities = [
                {
                    "product1_id": sim.product1_id,
                    "product1_name": sim.product1.name,
                    "product2_id": sim.product2_id,
                    "product2_name": sim.product2.name,
                    "score": float(sim.similarity_score),
                }
                for sim in top_10
            ]

            sample_user_vector = None
            if user_product_matrix:
                first_user_id = list(user_product_matrix.keys())[0]
                user_purchases = user_product_matrix[first_user_id]

                product_ids = list(products.values_list("id", flat=True))
                vector = [user_purchases.get(pid, 0) for pid in product_ids[:20]]

                sample_user_vector = {
                    "user_id": first_user_id,
                    "total_purchases": len(user_purchases),
                    "vector_sample": vector,
                    "vector_length": len(product_ids),
                }

            can_compute = users_with_purchases >= 2 and products_count >= 2

            issues = []
            if cf_count == 0:
                issues.append(
                    "⚠️ No collaborative similarities in database - run algorithm!"
                )
            if users_with_purchases < 2:
                issues.append(
                    f"⚠️ Insufficient users with purchases ({users_with_purchases} < 2)"
                )
            if total_purchases < 10:
                issues.append(f"⚠️ Insufficient purchases in system ({total_purchases} < 10)")
            if not can_compute:
                issues.append(
                    "❌ Insufficient data for collaborative filtering computation"
                )

            return Response(
                {
                    "status": "success",
                    "algorithm": "Collaborative Filtering (Item-Based, Sarwar et al. 2001)",
                    "formula": "Adjusted Cosine Similarity with Mean-Centering",
                    "database_stats": {
                        "total_users": users_count,
                        "total_products": products_count,
                        "total_order_items": orders_count,
                        "users_with_purchases": users_with_purchases,
                        "total_purchases": total_purchases,
                    },
                    "matrix_info": {
                        "shape": matrix_shape,
                        "total_cells": total_cells,
                        "non_zero_cells": total_purchases,
                        "sparsity_percentage": round(sparsity, 2),
                        "description": f"Matrix {matrix_shape} where each row = user, each column = product",
                    },
                    "similarity_matrix_info": {
                        "expected_shape": f"({products_count}, {products_count})",
                        "total_possible_pairs": total_possible_pairs,
                        "saved_similarities": cf_count,
                        "percentage_saved": round(percentage_saved, 2),
                        "threshold": 0.3,
                        "description": "Only similarities > 0.3 are saved to database",
                    },
                    "cache_info": {
                        "cache_key": cache_key,
                        "status": cache_status,
                        "cached_value": cached_result,
                        "timeout": "7200 seconds (2 hours)",
                    },
                    "top_10_similarities": top_similarities,
                    "sample_user_vector": sample_user_vector,
                    "computation_status": {
                        "can_compute": can_compute,
                        "issues": (
                            issues
                            if issues
                            else ["✅ All OK - can compute similarities"]
                        ),
                    },
                    "how_to_fix": {
                        "if_zero_similarities": [
                            "1. Go to Admin Panel → Statistics",
                            "2. Select 'Collaborative Filtering'",
                            "3. Click 'Apply Algorithm'",
                            "4. Wait ~30 seconds for computation",
                            "5. Refresh this page to see results",
                        ],
                        "manual_trigger": 'POST /api/process-recommendations/ with {"algorithm": "collaborative"}',
                    },
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


class AllCollaborativeSimilaritiesView(APIView):
    """
    API endpoint for retrieving all collaborative filtering similarities.
    
    Returns complete list of product-product similarities with pagination
    and filtering support. Useful for detailed analysis and modal displays
    in the admin debug interface.
    
    Features:
        - Pagination support (limit/offset)
        - Filter by similarity type
        - Ordered by similarity score (descending)
        - Includes product details (id, name)
    
    Query Parameters:
        - limit: int (default 100) - Maximum results per page
        - offset: int (default 0) - Starting position
        - similarity_type: str (default "collaborative") - Type of similarity
    
    Attributes:
        permission_classes: Public endpoint (no authentication required)
        
    Methods:
        get: Return paginated similarities list
    """

    permission_classes = []

    def get(self, request):
        """
        Retrieve paginated list of collaborative filtering similarities.
        
        Args:
            request: HTTP request with query parameters
                - limit: Maximum results (default 100)
                - offset: Starting position (default 0)
                - similarity_type: Similarity type filter (default "collaborative")
        
        Returns:
            Response: JSON with similarities
                {
                    "status": "success",
                    "count": int (total count),
                    "results": [
                        {
                            "product1": {"id": int, "name": str},
                            "product2": {"id": int, "name": str},
                            "similarity_score": float
                        }, ...
                    ],
                    "limit": int,
                    "offset": int
                }
        
        Raises:
            HTTP_500: If database query fails
        """
        try:
            # Parse query parameters
            limit = int(request.GET.get("limit", 100))
            offset = int(request.GET.get("offset", 0))
            similarity_type = request.GET.get("similarity_type", "collaborative")

            # Fetch similarities from database with related products
            similarities = (
                ProductSimilarity.objects.filter(similarity_type=similarity_type)
                .select_related("product1", "product2")
                .order_by("-similarity_score")
            )

            total_count = similarities.count()
            similarities_page = similarities[offset : offset + limit]

            # Format results for API response
            results = [
                {
                    "product1": {
                        "id": sim.product1_id,
                        "name": sim.product1.name,
                    },
                    "product2": {
                        "id": sim.product2_id,
                        "name": sim.product2.name,
                    },
                    "similarity_score": float(sim.similarity_score),
                }
                for sim in similarities_page
            ]

            return Response(
                {
                    "status": "success",
                    "count": total_count,
                    "results": results,
                    "limit": limit,
                    "offset": offset,
                }
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)}, status=500
            )


class ContentBasedDebugView(APIView):
    """
    Debug API endpoint for Content-Based Filtering diagnostics.
    
    Provides detailed debugging information for CBF algorithm including:
        - Feature vector analysis
        - TF-IDF weighting details
        - Cosine similarity computations
        - Feature extraction breakdown
        - Similarity score explanations
    
    Helps administrators understand:
        - How product features are weighted
        - Category, tag, price, and keyword contributions
        - Similarity calculation step-by-step
        - Common features between products
    
    Algorithm: TF-IDF + Cosine Similarity
    Formula: cos(θ) = (A · B) / (||A|| × ||B||)
    
    Attributes:
        permission_classes: Public endpoint (no authentication required)
        
    Methods:
        get: Return comprehensive CBF debug information
    """

    permission_classes = []

    def get(self, request):
        """
        Generate comprehensive debug report for Content-Based Filtering.
        
        Args:
            request: HTTP request with optional product_id
                - product_id: int (optional) - Specific product to analyze
        
        Returns:
            Response: Debug report JSON containing:
                - database_stats: Product count and similarities
                - cache_info: Cache status
                - feature_weights: Weighting scheme for features
                - selected_product: Product details (if product_id provided)
                - feature_vector: TF-IDF vector breakdown
                - similar_products: Top 10 with calculation details
        
        Raises:
            HTTP_404: If specified product_id not found
            HTTP_500: If debug data retrieval fails
        """
        try:
            from home.custom_recommendation_engine import CustomContentBasedFilter
            from home.models import ProductSimilarity
            import math

            product_id = request.GET.get("product_id")

            products = Product.objects.all()
            products_count = products.count()

            cb_similarities = ProductSimilarity.objects.filter(
                similarity_type="content_based"
            )
            cb_count = cb_similarities.count()

            cache_key = "content_based_similarity_matrix"
            cached_result = cache.get(cache_key)
            cache_status = (
                "HIT (data cached)" if cached_result else "MISS (no data)"
            )

            total_possible_pairs = products_count * (products_count - 1)
            percentage_saved = (
                (cb_count / total_possible_pairs * 100)
                if total_possible_pairs > 0
                else 0
            )

            response_data = {
                "status": "success",
                "algorithm": "Content-Based Filtering (Cosine Similarity)",
                "formula": "cos(θ) = (A·B) / (||A|| × ||B||)",
                "database_stats": {
                    "total_products": products_count,
                    "saved_similarities": cb_count,
                    "total_possible_pairs": total_possible_pairs,
                    "percentage_saved": round(percentage_saved, 2),
                    "threshold": 0.2,
                    "description": "Only similarities > 20% are saved to database",
                },
                "cache_info": {
                    "cache_key": cache_key,
                    "status": cache_status,
                    "cached_value": cached_result,
                    "timeout": "7200 seconds (2 hours)",
                },
                "feature_weights": {
                    "category": 0.40,
                    "tag": 0.30,
                    "price": 0.20,
                    "keywords": 0.10,
                    "description": "Weights used to build product feature vector",
                },
            }

            if product_id:
                try:
                    product = Product.objects.prefetch_related(
                        "categories", "tags", "specification_set"
                    ).get(id=product_id)
                except Product.DoesNotExist:
                    return Response(
                        {"error": f"Product {product_id} not found"}, status=404
                    )

                cb_filter = CustomContentBasedFilter()
                features = cb_filter._extract_weighted_features(product)

                price_category = cb_filter._get_price_category(product.price)

                keywords = cb_filter._extract_keywords(product.description or "")[:5]

                response_data["selected_product"] = {
                    "id": product.id,
                    "name": product.name,
                    "price": float(product.price),
                    "price_category": price_category,
                    "categories": [cat.name for cat in product.categories.all()],
                    "tags": [tag.name for tag in product.tags.all()],
                    "keywords": keywords,
                }

                response_data["feature_vector"] = {
                    "features": features,
                    "vector_length": len(features),
                    "example_explanation": {
                        "category_components": "40% wagi za kategorię 'Components'",
                        "tag_gaming": "30% wagi za tag 'Gaming'",
                        "price_high": "20% wagi za przedział cenowy 'high'",
                        "keyword_processor": "2% wagi za słowo kluczowe 'processor'",
                    },
                }

                similar_products = (
                    ProductSimilarity.objects.filter(
                        product1_id=product_id, similarity_type="content_based"
                    )
                    .select_related("product2")
                    .order_by("-similarity_score")[:10]
                )

                similarities_details = []
                for sim in similar_products:
                    product2 = sim.product2
                    features2 = cb_filter._extract_weighted_features(product2)

                    all_features = set(features.keys()) | set(features2.keys())
                    dot_product = sum(
                        features.get(f, 0.0) * features2.get(f, 0.0)
                        for f in all_features
                    )
                    norm1 = math.sqrt(
                        sum(features.get(f, 0.0) ** 2 for f in all_features)
                    )
                    norm2 = math.sqrt(
                        sum(features2.get(f, 0.0) ** 2 for f in all_features)
                    )

                    calculated_similarity = (
                        dot_product / (norm1 * norm2)
                        if (norm1 > 0 and norm2 > 0)
                        else 0.0
                    )

                    common_features = {
                        f: (features.get(f, 0.0), features2.get(f, 0.0))
                        for f in all_features
                        if features.get(f, 0.0) > 0 and features2.get(f, 0.0) > 0
                    }

                    similarities_details.append(
                        {
                            "product_2": {
                                "id": product2.id,
                                "name": product2.name,
                                "price": float(product2.price),
                                "categories": [
                                    cat.name for cat in product2.categories.all()
                                ],
                                "tags": [tag.name for tag in product2.tags.all()],
                            },
                            "similarity_score": round(float(sim.similarity_score), 4),
                            "calculation": {
                                "dot_product": round(dot_product, 4),
                                "norm_product1": round(norm1, 4),
                                "norm_product2": round(norm2, 4),
                                "formula": f"{round(dot_product, 4)} / ({round(norm1, 4)} × {round(norm2, 4)}) = {round(calculated_similarity, 4)}",
                                "stored_vs_calculated": {
                                    "stored": round(float(sim.similarity_score), 4),
                                    "calculated": round(calculated_similarity, 4),
                                    "match": abs(
                                        float(sim.similarity_score)
                                        - calculated_similarity
                                    )
                                    < 0.01,
                                },
                            },
                            "common_features": {
                                feature: {
                                    "product1_value": round(vals[0], 2),
                                    "product2_value": round(vals[1], 2),
                                }
                                for feature, vals in list(common_features.items())[:5]
                            },
                            "common_features_count": len(common_features),
                        }
                    )

                response_data["similar_products"] = {
                    "count": len(similarities_details),
                    "top_10": similarities_details,
                }
            else:
                top_10 = cb_similarities.order_by("-similarity_score")[:10]
                response_data["top_10_global_similarities"] = [
                    {
                        "product1_id": sim.product1_id,
                        "product1_name": sim.product1.name,
                        "product2_id": sim.product2_id,
                        "product2_name": sim.product2.name,
                        "score": round(float(sim.similarity_score), 4),
                    }
                    for sim in top_10
                ]

            issues = []
            if cb_count == 0:
                issues.append(
                    "⚠️ No content-based similarities in database - run algorithm!"
                )
            if products_count < 2:
                issues.append(f"⚠️ Insufficient products ({products_count} < 2)")

            response_data["computation_status"] = {
                "can_compute": products_count >= 2,
                "issues": (
                    issues
                    if issues
                    else ["✅ All OK - can compute similarities"]
                ),
            }

            response_data["how_to_fix"] = {
                "if_zero_similarities": [
                    "1. Go to Admin Panel → Statistics",
                    "2. Select 'Content-Based Filtering'",
                    "3. Click 'Apply Algorithm'",
                    "4. Wait ~1-2 minutes for computation",
                    "5. Refresh this page to see results",
                ]
            }

            return Response(response_data)

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
