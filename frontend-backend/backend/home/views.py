from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from random import sample
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    CartItem,
    Product,
    Category,
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
)
from django.http import HttpResponse
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
)  # Custom permission checking for administrator rights
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

# ----------------------------------
# TOKEN HANDLING
# ----------------------------------


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


# ----------------------------------
# CATEGORIES - Public Access
# ----------------------------------


class CategoriesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.values("name")
        return Response(categories)


# ----------------------------------
# PRODUCTS
# Public product list view; creation/modification is allowed only for admin users.
# ----------------------------------


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


# ----------------------------------
# HOME PAGE - Public Access
# ----------------------------------


def home_view(request):
    return HttpResponse("Welcome to the Product Recommendation System!")


# ----------------------------------
# LOGIN - Public Access
# ----------------------------------


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


# ----------------------------------
# REGISTRATION - Public Access
# ----------------------------------


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


# ----------------------------------
# CRUD ENDPOINTS - Authentication Required
# ----------------------------------


# Products - creation, modification, and deletion allowed only for admin users
class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        # For GET requests, public access is allowed; only POST (creation) requires admin privileges
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        ids = self.request.query_params.get("ids")
        if ids:
            try:
                id_list = [int(x) for x in ids.split(",") if x.isdigit()]
                queryset = queryset.filter(id__in=id_list)
            except Exception as e:
                pass
        return queryset


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# Orders - A user can view and modify only their own orders; admin can access all orders.
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
        # Save order with status "Pending"
        order = serializer.save(user=self.request.user, status="Pending")
        for product_id, quantity in items.items():
            try:
                product = Product.objects.get(id=product_id)
                OrderProduct.objects.create(
                    order=order, product=product, quantity=quantity
                )
            except Product.DoesNotExist:
                continue


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


# Users - Only admin can manage users.
class UserListAPIView(ListAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class UserDestroyAPIView(DestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# Complaints - A user can see only their own complaints; admin can see all.
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


# Admin statistics - accessible only by administrators.
class AdminStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        data = {
            "products": Product.objects.count(),
            "clients": User.objects.filter(role="client").count(),
            "orders": Order.objects.count(),
            "complaints": Complaint.objects.count(),
        }
        return Response(data)

class AdminDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        orders = Order.objects.all()
        total_sales = OrderProduct.objects.aggregate(total=Sum("product__price", field="product__price * quantity"))["total"] or 0
        new_users = User.objects.filter(date_joined__gte=timezone.now() - timedelta(days=30)).count()
        total_products = Product.objects.count()

        clients = User.objects.filter(role="client").count()
        conversion_rate = round((orders.count() / clients * 100), 1) if clients else 0

        orders_by_month = orders.annotate(month=TruncMonth("date_order")).values("month").annotate(
            total_quantity=Sum("orderproduct__quantity")
        ).order_by("month")
        trend_labels = [order["month"].strftime("%b %Y") for order in orders_by_month]
        trend_data = [order["total_quantity"] for order in orders_by_month]
        max_trend = max(trend_data, default=0)

        category_qs = OrderProduct.objects.values("product__categories__name").annotate(
            total=Sum("quantity")
        ).order_by("-total")
        top5 = list(category_qs)[:5]
        cat_labels = [item["product__categories__name"] for item in top5 if item["product__categories__name"]]
        cat_data = [item["total"] for item in top5]

        sales_channels = [
            {"name": "Website", "value": orders.filter(status__iexact="website").count()},
            {"name": "Mobile App", "value": orders.filter(status__iexact="mobile").count()},
            {"name": "Marketplace", "value": orders.filter(status__iexact="marketplace").count()},
            {"name": "Social Media", "value": orders.filter(status__iexact="social").count()},
        ]

        return Response({
            "totalSales": total_sales,
            "newUsers": new_users,
            "totalProducts": total_products,
            "conversionRate": f"{conversion_rate}%",
            "trend": {
                "labels": trend_labels,
                "data": trend_data,
                "y_axis_max": max_trend + 2,
            },
            "category_distribution": {
                "labels": cat_labels,
                "data": cat_data,
            },
            "sales_channels": sales_channels,
        })

# Current user - accessible only for authenticated users.
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


# Product search - public access.
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


# Client statistics - accessible only for authenticated users (pertaining to their own data).
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

        from django.db.models.functions import TruncMonth

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


# Tags - public access.
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
