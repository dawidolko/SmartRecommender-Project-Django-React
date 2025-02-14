from django.db.models import Count
from random import sample
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer
from rest_framework.generics import (
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    DestroyAPIView,
)
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .permissions import IsAdminUser

from .models import Product, Category, Order, Complaint, User as MyUser
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    OrderSerializer,
    ComplaintSerializer,
    UserSerializer,
    MyTokenObtainPairSerializer,
)

from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
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

# ---------------------------
# KATEGORIE
# ---------------------------
class CategoriesAPIView(APIView):
    def get(self, request):
        categories = Category.objects.values("name")
        return Response(categories)


# ---------------------------
# PRODUKTY
# ---------------------------
class ProductsAPIView(APIView):
    def get(self, request):
        products = Product.objects.prefetch_related("categories", "photoproduct_set").all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class RandomProductsAPIView(APIView):
    def get(self, request):
        all_products = Product.objects.annotate(photo_count=Count('photoproduct')).filter(photo_count__gt=0)
        random_products = sample(list(all_products), min(9, len(all_products)))
        serializer = ProductSerializer(random_products, many=True)
        return Response(serializer.data)


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.prefetch_related(
        "categories", "photoproduct_set", "opinion_set", "specification_set"
    )
    serializer_class = ProductDetailSerializer


# ---------------------------
# STRONA GŁÓWNA
# ---------------------------
def home_view(request):
    return HttpResponse("Welcome to the Product Recommendation System!")


# ---------------------------
# LOGOWANIE
# ---------------------------
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
        return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------
# REJESTRACJA
# ---------------------------
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        nickname = request.data.get("nickname")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        role = request.data.get("role", "client")

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email is already registered"}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({"error": "Password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create(
                username=nickname,
                email=email,
                password=make_password(password),
                role=role,
                first_name=first_name,
                last_name=last_name,
            )
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
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------------------
# CRUD ENDPOINTY
# ---------------------------
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.select_related("user").all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


class OrderUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.select_related("user").all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


class UserListAPIView(ListAPIView):
    """Lista użytkowników (np. do panelu admina)."""
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserDestroyAPIView(DestroyAPIView):
    """Usuwanie użytkownika (np. przez admina)."""
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ComplaintListCreateAPIView(ListCreateAPIView):
    queryset = Complaint.objects.select_related("order").all()
    serializer_class = ComplaintSerializer
    permission_classes = [AllowAny]


class ComplaintRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Complaint.objects.select_related("order").all()
    serializer_class = ComplaintSerializer
    permission_classes = [AllowAny]

class AdminStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            "products": Product.objects.count(),
            "clients": MyUser.objects.filter(role="client").count(),
            "orders": Order.objects.count(),
            "complaints": Complaint.objects.count(),
        }
        return Response(data)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(f"Received request from: {request.user}")
        print(f"🔹 Headers: {request.headers}") 
        if request.user.is_anonymous:
            return Response({"error": "Not authenticated"}, status=401)
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }, status=status.HTTP_200_OK)

class ProductSearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get("q", "")
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(specification_set__parameter_name__icontains=query) |
                Q(specification_set__specification__icontains=query) |
                Q(opinion_set__content__icontains=query)
            ).distinct()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        return Response({"error": "No query provided"}, status=400)

class ClientStatsView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        purchased_items_count = Order.objects.count()  
        complaints_count = Complaint.objects.count() 

        data = {
            "purchased_items": purchased_items_count,
            "complaints": complaints_count,
        }
        return Response(data, status=status.HTTP_200_OK)


# class ProductAdminViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]  # Tylko dla admina

class CartPreviewView(APIView):

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)[:3]  # Max 3 products
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def patch(self, request, item_id):
        """Products quantity update"""
        cart_item = CartItem.objects.get(id=item_id, user=request.user)
        action = request.data.get("action")

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

        return Response({"message": "Quantity updated", "new_quantity": cart_item.quantity})

    def delete(self, request, item_id):
        """Product removal from cart"""
        cart_item = CartItem.objects.get(id=item_id, user=request.user)
        cart_item.delete()
        return Response({"message": "Item removed"})