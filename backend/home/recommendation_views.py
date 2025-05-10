from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from .models import Product, User, Order, OrderProduct, RecommendationSettings, ProductSimilarity, UserProductRecommendation, CartItem, UserInteraction
from .serializers import ProductSerializer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .signals import update_content_based_similarity

class RecommendationSettingsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        settings = RecommendationSettings.objects.filter(user=request.user).first()
        return Response({
            'active_algorithm': settings.active_algorithm if settings else 'collaborative'
        })
    
    def post(self, request):
        algorithm = request.data.get('algorithm', 'collaborative')
        settings, created = RecommendationSettings.objects.get_or_create(
            user=request.user,
            defaults={'active_algorithm': algorithm}
        )
        if not created:
            settings.active_algorithm = algorithm
            settings.save()
        
        return Response({
            'success': True,
            'message': f'Recommendation algorithm updated to {algorithm}',
            'active_algorithm': algorithm
        })


class ProcessRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        algorithm = request.data.get('algorithm', 'collaborative')
        
        try:
            if algorithm == 'collaborative':
                self.process_collaborative_filtering()
            else:
                self.process_content_based_filtering()
            
            return Response({
                'success': True,
                'message': f'{algorithm} recommendations processed successfully'
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def process_collaborative_filtering(self):
        users = User.objects.all()
        products = Product.objects.all()
        
        user_product_matrix = defaultdict(dict)
        for order in OrderProduct.objects.select_related('order', 'product').all():
            user_product_matrix[order.order.user_id][order.product_id] = order.quantity
        
        user_ids = list(user_product_matrix.keys())
        product_ids = list(products.values_list('id', flat=True))
        
        matrix = []
        for user_id in user_ids:
            row = []
            for product_id in product_ids:
                row.append(user_product_matrix[user_id].get(product_id, 0))
            matrix.append(row)
        
        matrix = np.array(matrix)
        
        if matrix.shape[0] > 1 and matrix.shape[1] > 1:
            product_similarity = cosine_similarity(matrix.T)
            
            for i, product1_id in enumerate(product_ids):
                for j, product2_id in enumerate(product_ids):
                    if i != j and product_similarity[i][j] > 0.1:
                        ProductSimilarity.objects.update_or_create(
                            product1_id=product1_id,
                            product2_id=product2_id,
                            similarity_type='collaborative',
                            defaults={'similarity_score': float(product_similarity[i][j])}
                        )
    
    def process_content_based_filtering(self):
        products = Product.objects.prefetch_related('categories', 'tags').all()
        
        product_features = []
        product_ids = []
        
        for product in products:
            feature_vector = []
            for cat in product.categories.all():
                feature_vector.append(1)
            for tag in product.tags.all():
                feature_vector.append(1)
                
            product_features.append(feature_vector)
            product_ids.append(product.id)
        
        if product_features and len(product_features) > 1:
            max_length = max(len(f) for f in product_features)
            padded_features = []
            for feature in product_features:
                padded = feature + [0] * (max_length - len(feature))
                padded_features.append(padded)
            
            feature_matrix = np.array(padded_features)
            similarity_matrix = cosine_similarity(feature_matrix)

            for i, product1_id in enumerate(product_ids):
                for j, product2_id in enumerate(product_ids):
                    if i != j and similarity_matrix[i][j] > 0.1:
                        ProductSimilarity.objects.update_or_create(
                            product1_id=product1_id,
                            product2_id=product2_id,
                            similarity_type='content_based',
                            defaults={'similarity_score': float(similarity_matrix[i][j])}
                        )


class RecommendationPreviewView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        algorithm = request.GET.get('algorithm', 'collaborative')
        
        recommendations = UserProductRecommendation.objects.filter(
            user=request.user,
            recommendation_type=algorithm
        ).select_related('product').order_by('-score')[:6]
        
        if not recommendations.exists():
            similarities = ProductSimilarity.objects.filter(
                similarity_type=algorithm
            ).order_by('-similarity_score')[:10]
            
            products = [s.product2 for s in similarities]
        else:
            products = [r.product for r in recommendations]
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class GenerateUserRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        algorithm = request.data.get('algorithm', 'collaborative')
        
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
                product1_id=product_id,
                similarity_type=algorithm
            ).order_by('-similarity_score')[:5]
            
            for similarity in similarities:
                recommendations[similarity.product2_id] += float(similarity.similarity_score)
        
        for product_id, score in recommendations.items():
            UserProductRecommendation.objects.update_or_create(
                user=request.user,
                product_id=product_id,
                recommendation_type=algorithm,
                defaults={'score': score}
            )
        
        return Response({
            'success': True,
            'message': f'User recommendations generated for {algorithm} algorithm'
        })
    
class CreateUserInteractionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        interaction_type = request.data.get("interaction_type")

        if not product_id or not interaction_type:
            return Response({"error": "Invalid data."}, status=400)

        UserInteraction.objects.create(
            user=request.user,
            product_id=product_id,
            interaction_type=interaction_type
        )
        return Response({"success": True})

class UpdateProductSimilarityView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        try:
            product_count = Product.objects.count()
            update_content_based_similarity()
            similarity_count = ProductSimilarity.objects.count()
            
            return Response({
                'status': 'success',
                'message': f'Similarity updated for {product_count} products',
                'similarity_records_created': similarity_count
            })
        except Exception as e:
            import traceback
            return Response({
                'status': 'error',
                'message': str(e),
                'traceback': traceback.format_exc()
            }, status=500)