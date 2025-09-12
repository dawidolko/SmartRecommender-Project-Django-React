from django.db.models import Count, Q, Sum, F, FloatField
from django.db.models.functions import TruncMonth
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import os
from home.signals import run_all_analytics_after_order
from random import sample
from rest_framework.views import APIView
from rest_framework.response import Response
import os
import time
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product, PhotoProduct
from .permissions import IsAdminUser
from django.db import connection
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import AllowAny
from .models import Product, Opinion, Category
from .serializers import OpinionSerializer, ProductSerializer
from django.db.models import Q, Avg, F
from .models import Product, ProductSentimentSummary
from .serializers import ProductSerializer
import re
from textblob import TextBlob
from .models import SentimentAnalysis, ProductSentimentSummary
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    CartItem,
    PhotoProduct,
    Product,
    Category,
    Opinion,
    Order,
    Complaint,
    OrderProduct,
    Tag,
    User as MyUser,
)
from .serializers import (
    CartItemSerializer,
    ProductSerializer,
    ProductDetailSerializer,
    OrderSerializer,
    ComplaintSerializer,
    UserSerializer,
    MyTokenObtainPairSerializer,
    TagSerializer,
    UserUpdateSerializer,
    UserRegisterSerializer,
    AdminUserSerializer,
)
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model, authenticate
from rest_framework.generics import (
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework import status
from .permissions import (
    IsAdminUser,
) 
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import IntegrityError
from django.db.models import Avg

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["user"] = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CategoriesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.values("name")
        return Response(categories)

class ProductsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.prefetch_related(
            "categories", "photoproduct_set"
        ).all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class RandomProductsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        all_products = Product.objects.annotate(
            photo_count=Count("photoproduct")
        ).filter(photo_count__gt=0)
        random_products = sample(list(all_products), min(9, len(all_products)))
        serializer = ProductSerializer(random_products, many=True)
        return Response(serializer.data)


class ProductDetailAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.prefetch_related(
        "categories", "photoproduct_set", "opinion_set", "specification_set"
    )
    serializer_class = ProductDetailSerializer

class ProductImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        images = request.FILES.getlist('images')
        result = []
        
        if not os.path.exists('media'):
            os.makedirs('media')
        
        for image in images:
            original_filename = image.name
            base_name, extension = os.path.splitext(original_filename)
            timestamp = int(time.time() * 1000)
            filename = f"{base_name}_{timestamp}{extension}"
            
            filepath = os.path.join('media', filename)
            with open(filepath, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            max_attempts = 3
            attempt = 0
            success = False
            
            while attempt < max_attempts and not success:
                try:
                    photo = PhotoProduct.objects.create(product=product, path=filename)
                    result.append({"id": photo.id, "path": filename})
                    success = True
                except IntegrityError:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT MAX(id) FROM db_photo_product")
                        max_id = cursor.fetchone()[0] or 0
                        cursor.execute(f"ALTER SEQUENCE db_photo_product_id_seq RESTART WITH {max_id + 1}")
                    attempt += 1
            
            if not success:
                return Response({
                    "error": "Failed to add image due to database constraints after multiple attempts"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            "message": f"{len(images)} images uploaded successfully",
            "uploaded_images": result
        }, status=status.HTTP_201_CREATED)

def home_view(request):
    html_content = """
    <html>
        <head>
            <title>Product Recommendation System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    color: #333;
                }
                .container {
                    text-align: center;
                    padding: 20px;
                    background-color: #fff;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    border-radius: 10px;
                    width: 80%;
                    max-width: 600px;
                }
                h1 {
                    font-size: 2.5rem;
                    color: black;
                }
                p {
                    font-size: 1.2rem;
                    color: #555;
                }
                .btn {
                    padding: 10px 20px;
                    font-size: 1rem;
                    color: #fff;
                    background-color: black;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    text-decoration: none;
                }
                .btn:hover {
                    background-color: #333;
                }

                .logo {
                    margin-bottom: 20px;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }

                .logo:hover {
                    transform: scale(1.1);
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <img src="./media/logo_of_name.png" alt="Product Recommendation System Logo" class="logo" width="350" />
                <h1>Welcome to the Product Recommendation System!</h1>
                <p>We provide personalized product recommendations based on your preferences. Start exploring now!</p>
                <a href="http://localhost:3000" class="btn">Get Started</a>
            </div>
        </body>
    </html>
    """
    return HttpResponse(html_content)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "nickname": user.username,
                        "role": user.role,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST
        )

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "user": {
                        "email": user.email,
                        "nickname": user.username,
                        "role": user.role,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]

def perform_create(self, serializer):
    tags = self.request.data.get("tags", [])
    categories = self.request.data.get("categories", [])
    photos = self.request.data.get("photos", [])

    if not tags:
        raise ValidationError("Tags are required.")
    if not categories:
        raise ValidationError("Categories are required.")

    try:
        product = serializer.save()

        if tags:
            tags_objects = Tag.objects.filter(id__in=tags)
            product.tags.set(tags_objects)

        if categories:
            categories_objects = Category.objects.filter(name__in=categories)
            product.categories.set(categories_objects)

        if photos:
            for photo_path in photos:
                photo_product = PhotoProduct.objects.create(product=product, path=photo_path)
    except Exception as e:
        raise ValidationError(f"Error occurred during product creation: {str(e)}")
        
class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_update(self, serializer):
        serializer.save()


class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin" or user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        items = self.request.data.get("items", {})
        order = serializer.save(user=self.request.user, status="Pending")
        for product_id, quantity in items.items():
            try:
                product = Product.objects.get(id=product_id)
                OrderProduct.objects.create(
                    order=order, product=product, quantity=quantity
                )
            except Product.DoesNotExist:
                continue

        run_all_analytics_after_order(order)


class ClientOrderDetailAPIView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin" or user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

class UserListCreateAPIView(ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ComplaintListCreateAPIView(ListCreateAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin" or user.is_staff:
            return Complaint.objects.all()
        return Complaint.objects.filter(order__user=user)

    def perform_create(self, serializer):
        serializer.save()


class ComplaintRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin" or user.is_staff:
            return Complaint.objects.all()
        return Complaint.objects.filter(order__user=user)

class AdminStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            total_users = User.objects.count()
            client_users = User.objects.filter(role="client").count()
            admin_users = User.objects.filter(role="admin").count()
            
            all_roles = list(User.objects.values_list('role', flat=True).distinct())
            
            data = {
                "products": Product.objects.count(),
                "clients": client_users,
                "orders": Order.objects.count(),
                "complaints": Complaint.objects.count(),
                "debug_info": {
                    "total_users": total_users,
                    "client_users": client_users,
                    "admin_users": admin_users,
                    "all_roles": all_roles
                }
            }
            return Response(data)
        except Exception as e:
            return Response({
                "error": str(e),
                "products": 0,
                "clients": 0,
                "orders": 0,
                "complaints": 0
            }, status=500)

class AdminDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_sales = OrderProduct.objects.aggregate(
            total=Sum(F('product__price') * F('quantity'), output_field=FloatField())
        )['total'] or 0

        new_users = User.objects.filter(
            date_joined__gte=timezone.now() - timedelta(days=30)
        ).count()

        total_products = Product.objects.count()

        clients = User.objects.filter(role="client").count()

        conversion_rate = round((Order.objects.count() / clients * 100), 1) if clients else 0

        orders_by_month = OrderProduct.objects.annotate(
            month=TruncMonth("order__date_order")
        ).values("month").annotate(
            total_sales=Sum(F('product__price') * F('quantity'), output_field=FloatField())
        ).order_by("month")

        trend_labels = [order["month"].strftime("%b %Y") for order in orders_by_month]
        trend_data = [float(order["total_sales"]) for order in orders_by_month]
        max_trend = max(trend_data, default=0) if trend_data else 0

        category_distribution_qs = OrderProduct.objects.values(
            'product__categories__name'
        ).annotate(
            total_quantity=Sum('quantity')
        )

        cat_summary = {}
        for item in category_distribution_qs:
            full_name = item['product__categories__name']
            if full_name:
                main_cat = full_name.split('.')[0]
                cat_summary[main_cat] = cat_summary.get(main_cat, 0) + item['total_quantity']

        cat_labels = list(cat_summary.keys())
        cat_data = list(cat_summary.values())

        top_selling_data = OrderProduct.objects.values('product').annotate(
            total_sold=Sum('quantity')
        ).order_by('-total_sold').first()
        top_selling = top_selling_data['total_sold'] if top_selling_data else 0

        churned_users = User.objects.filter(
            last_login__lte=timezone.now() - timedelta(days=30)
        ).count()
        churn_rate = round((churned_users / clients * 100), 1) if clients else 0

        total_opinions = Opinion.objects.count()

        avg_rating_dict = Opinion.objects.aggregate(avg_rating=Avg('rating'))
        average_rating = avg_rating_dict['avg_rating'] or 0

        top_category_name = None
        if cat_summary:
            sorted_cats = sorted(cat_summary.items(), key=lambda x: x[1], reverse=True)
            top_category_name = sorted_cats[0][0]

        product_sales_qs = (
            OrderProduct.objects
            .values('product')
            .annotate(total_sold=Sum('quantity'))
        )
        product_sales_dict = {x['product']: x['total_sold'] for x in product_sales_qs}

        tag_summary = {}
        for tag in Tag.objects.prefetch_related('product_set'):
            sum_sold_for_tag = 0
            for prod in tag.product_set.all():
                sum_sold_for_tag += product_sales_dict.get(prod.id, 0)
            tag_summary[tag.name] = sum_sold_for_tag

        top_tag_name = None
        if tag_summary:
            sorted_tags = sorted(tag_summary.items(), key=lambda x: x[1], reverse=True)
            top_tag_name = sorted_tags[0][0]

        return Response({
            "totalSales": float(total_sales),
            "newUsers": new_users,
            "totalProducts": total_products,
            "conversionRate": f"{conversion_rate}%",
            "trend": {
                "labels": trend_labels,
                "data": trend_data,
                "y_axis_max": max_trend + (max_trend * 0.1) if max_trend > 0 else 10
            },
            "category_distribution": {
                "labels": cat_labels,
                "data": cat_data
            },
            "topSelling": top_selling,
            "churnRate": f"{churn_rate}%", 

            "totalOpinions": total_opinions,
            "averageRating": round(average_rating, 2),
            "topCategoryName": top_category_name or "",
            "topTagName": top_tag_name or "",
        })

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_anonymous:
            return Response({"error": "Not authenticated"}, status=401)
        user = request.user
        return Response(
            {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            status=status.HTTP_200_OK,
        )

class ClientStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)

        purchased_items = (
            OrderProduct.objects.filter(order__in=orders).aggregate(
                total=Sum("quantity")
            )["total"]
            or 0
        )

        complaints_count = Complaint.objects.filter(order__user=request.user).count()

        orders_by_month = (
            orders.annotate(month=TruncMonth("date_order"))
            .values("month")
            .annotate(total_quantity=Sum("orderproduct__quantity"))
            .order_by("month")
        )
        trend_labels = [order["month"].strftime("%b %Y") for order in orders_by_month]
        trend_data = [order["total_quantity"] for order in orders_by_month]
        max_trend = max(trend_data, default=0)
        order_trends = {
            "labels": trend_labels,
            "data": trend_data,
            "y_axis_max": max_trend + 2,
        }

        category_distribution_qs = (
            OrderProduct.objects.filter(order__in=orders)
            .values("product__categories__name")
            .annotate(total=Sum("quantity"))
            .order_by("-total")
        )
        categories = list(category_distribution_qs)
        top5 = categories[:5]
        others = categories[5:]
        others_sum = sum(item["total"] for item in others)
        cat_labels = [
            item["product__categories__name"]
            for item in top5
            if item["product__categories__name"]
        ]
        cat_data = [item["total"] for item in top5]
        if others_sum > 0:
            cat_labels.append("Others")
            cat_data.append(others_sum)
        category_distribution = {
            "labels": cat_labels,
            "data": cat_data,
        }

        data = {
            "purchased_items": purchased_items,
            "complaints": complaints_count,
            "order_trends": order_trends,
            "category_distribution": category_distribution,
        }
        return Response(data, status=200)


class CartPreviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)[:3]
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def patch(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        action = request.data.get("action")
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            return Response(
                {"error": "Invalid action or quantity"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cart_item.save()
        return Response(
            {"message": "Quantity updated", "new_quantity": cart_item.quantity}
        )

    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        cart_item.delete()
        return Response({"message": "Item removed"})

class TagsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    

class CurrentUserUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class RecommendedProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            from .models import UserProductRecommendation, RecommendationSettings
            
            settings = RecommendationSettings.objects.filter(user=user).first()
            algorithm = settings.active_algorithm if settings else "collaborative"
            
            user_recommendations = UserProductRecommendation.objects.filter(
                user=user,
                recommendation_type=algorithm
            ).select_related('product').order_by('-score')[:12]
            
            if user_recommendations.exists():
                recommended_products = [rec.product for rec in user_recommendations]
            else:
                recommended_products = self.get_fallback_recommendations(user)
            
            serializer = ProductSerializer(recommended_products, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            recommended_products = Product.objects.annotate(
                order_count=Count('orderproduct')
            ).order_by('-order_count')[:12]
            
            serializer = ProductSerializer(recommended_products, many=True)
            return Response(serializer.data)
    
    def get_fallback_recommendations(self, user):
        """Get fallback recommendations when no personalized data exists"""
        try:
            user_orders = Order.objects.filter(user=user)
            if user_orders.exists():
                purchased_categories = Product.objects.filter(
                    orderproduct__order__user=user
                ).values_list('categories__id', flat=True).distinct()
                
                if purchased_categories:
                    return Product.objects.filter(
                        categories__id__in=purchased_categories
                    ).annotate(
                        order_count=Count('orderproduct')
                    ).order_by('-order_count')[:12]
            
            return Product.objects.annotate(
                order_count=Count('orderproduct')
            ).order_by('-order_count')[:12]
            
        except Exception:
            return Product.objects.all()[:12]

class ResetPhotoSequenceView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(id) FROM db_photo_product")
            max_id = cursor.fetchone()[0] or 0
            
            cursor.execute(f"ALTER SEQUENCE db_photo_product_id_seq RESTART WITH {max_id + 1}")
            
            return Response({
                "message": f"Sequence reset to {max_id + 1}",
                "max_id": max_id
            })
    
class ProductSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get("q", "")
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(categories__name__icontains=query)
            ).distinct()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        return Response({"error": "No query provided"}, status=400)
    
class ProductReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        user = request.user

        purchased = OrderProduct.objects.filter(
            order__user=user, product=product
        ).exists()
        if not purchased:
            return Response(
                {"detail": "You can only review products you have purchased."},
                status=status.HTTP_403_FORBIDDEN,
            )
            
        existing_review = Opinion.objects.filter(user=user, product=product).exists()
        if existing_review:
            return Response(
                {"detail": "A review has already been added for this product."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = OpinionSerializer(
            data=request.data,
            context={"request": request, "product": product},
        )
        serializer.is_valid(raise_exception=True)

        opinion = serializer.save(user=user, product=product)

        return Response(OpinionSerializer(opinion).data,
                        status=status.HTTP_201_CREATED)
    