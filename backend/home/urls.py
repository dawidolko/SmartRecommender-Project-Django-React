from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    CategoriesAPIView,
    ProductImageUploadView,
    ProductReviewAPIView,
    ProductsAPIView,
    RandomProductsAPIView,
    ProductDetailAPIView,
    RecommendedProductsAPIView,
    ResetPhotoSequenceView,
    home_view,
    UserLoginView,
    UserRegisterView,
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    OrderListCreateAPIView,
    OrderUpdateDestroyAPIView,
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    ComplaintListCreateAPIView,
    ComplaintRetrieveUpdateDestroyAPIView,
    AdminStatsView,
    CurrentUserView,
    ProductSearchAPIView,
    ClientStatsView,
    CustomTokenObtainPairView,
    MyTokenObtainPairView,
    CartPreviewView,
    ProductSearchAPIView,
    TagsAPIView,
    ClientOrderDetailAPIView,
    CurrentUserUpdateAPIView,
    AdminDashboardStatsView,
)

from .recommendation_views import (
    CreateUserInteractionAPI,
    GenerateUserRecommendationsView,
    ProcessRecommendationsView,
    RecommendationPreviewView,
    RecommendationSettingsView,
    UpdateProductSimilarityView,
    RecommendationAlgorithmStatusView,
    CollaborativeFilteringDebugView,
    ContentBasedDebugView,
)

from .sentiment_views import (
    SentimentSearchAPIView,
    SentimentAnalysisDebugAPI,
    SentimentAnalysisDebugView,
    FuzzySearchAPIView,
    FuzzyLogicRecommendationsAPIView,
)

from .fuzzy_debug_view import FuzzyLogicDebugView

from .probabilistic_debug_view import ProbabilisticDebugView

from .association_views import (
    AssociationRulesListAPI,
    FrequentlyBoughtTogetherAPI,
    UpdateAssociationRulesAPI,
    AssociationRulesAnalysisAPI,
    ProductAssociationDebugAPI,
)

from .probabilistic_views import (
    MarkovRecommendationsAPI,
    BayesianInsightsAPI,
    ProbabilisticAnalysisAdminAPI,
)

from .analytics_views import (
    PurchasePredictionView,
    RiskDashboardView,
    SalesForecastView,
    ProductDemandView,
    UserPurchasePatternsView,
    AdminPurchasePatternsView,
    AdminProductRecommendationsView,
    AdminChurnPredictionView,
    MyShoppingInsightsView,
)

from .seasonal_views import SeasonalTrendsView

urlpatterns = [
    path("", home_view, name="home"),
    path("api/categories/", CategoriesAPIView.as_view(), name="categories"),
    path(
        "api/random-products/", RandomProductsAPIView.as_view(), name="random-products"
    ),
    path(
        "api/product/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"
    ),
    path("api/tags/", TagsAPIView.as_view(), name="tags"),
    path("api/products-old/", ProductsAPIView.as_view(), name="products"),
    path("api/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", UserRegisterView.as_view(), name="register"),
    path(
        "api/products/", ProductListCreateAPIView.as_view(), name="product-list-create"
    ),
    path(
        "api/products/<int:pk>/",
        ProductRetrieveUpdateDestroyAPIView.as_view(),
        name="product-rud",
    ),
    path("api/orders/", OrderListCreateAPIView.as_view(), name="orders-list-create"),
    path(
        "api/client/orders/<int:pk>/",
        ClientOrderDetailAPIView.as_view(),
        name="client-order-detail",
    ),
    path(
        "api/orders/<int:pk>/", OrderUpdateDestroyAPIView.as_view(), name="orders-rud"
    ),
    path("api/me/", CurrentUserUpdateAPIView.as_view(), name="current-user-update"),
    path("api/users/", UserListCreateAPIView.as_view(), name="users-list"),
    path(
        "api/users/<int:pk>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="users-destroy",
    ),
    path(
        "api/complaints/",
        ComplaintListCreateAPIView.as_view(),
        name="complaint-list-create",
    ),
    path(
        "api/products/<int:product_id>/reviews/",
        ProductReviewAPIView.as_view(),
        name="product-reviews",
    ),
    path(
        "api/complaints/<int:pk>/",
        ComplaintRetrieveUpdateDestroyAPIView.as_view(),
        name="complaint-rud",
    ),
    path("api/admin-stats/", AdminStatsView.as_view(), name="admin-stats"),
    path(
        "api/admin-dashboard-stats/",
        AdminDashboardStatsView.as_view(),
        name="admin-dashboard-stats",
    ),
    path("api/user/", CurrentUserView.as_view(), name="current_user"),
    path("api/products/search/", ProductSearchAPIView.as_view(), name="product_search"),
    path("cart/preview/", CartPreviewView.as_view(), name="cart_preview"),
    path("cart/update/<int:item_id>/", CartPreviewView.as_view(), name="cart_update"),
    path("cart/remove/<int:item_id>/", CartPreviewView.as_view(), name="cart_remove"),
    path("api/client-stats/", ClientStatsView.as_view(), name="client-stats"),
    path("api/purchase-prediction/", PurchasePredictionView.as_view(), name="purchase-prediction"),
    path(
        "api/recommended-products/",
        RecommendedProductsAPIView.as_view(),
        name="recommended-products",
    ),
    path(
        "api/products/<int:pk>/upload-images/",
        ProductImageUploadView.as_view(),
        name="upload-product-images",
    ),
    path(
        "api/reset-photo-sequence/",
        ResetPhotoSequenceView.as_view(),
        name="reset-photo-sequence",
    ),
    path(
        "api/sentiment-search/",
        SentimentSearchAPIView.as_view(),
        name="sentiment-search",
    ),
    path(
        "api/sentiment-analysis-debug/",
        SentimentAnalysisDebugView.as_view(),
        name="sentiment-analysis-debug",
    ),
    path(
        "api/sentiment-product-debug/",
        SentimentAnalysisDebugAPI.as_view(),
        name="sentiment-product-debug",
    ),
    path("api/fuzzy-search/", FuzzySearchAPIView.as_view(), name="fuzzy-search"),
    path(
        "api/fuzzy-logic-recommendations/",
        FuzzyLogicRecommendationsAPIView.as_view(),
        name="fuzzy-logic-recommendations",
    ),
    path(
        "api/recommendation-settings/",
        RecommendationSettingsView.as_view(),
        name="recommendation-settings",
    ),
    path(
        "api/process-recommendations/",
        ProcessRecommendationsView.as_view(),
        name="process-recommendations",
    ),
    path(
        "api/interaction/",
        CreateUserInteractionAPI.as_view(),
        name="create-interaction",
    ),
    path(
        "api/recommendation-preview/",
        RecommendationPreviewView.as_view(),
        name="recommendation-preview",
    ),
    path(
        "api/generate-user-recommendations/",
        GenerateUserRecommendationsView.as_view(),
        name="generate-user-recommendations",
    ),
    path(
        "api/admin/update-product-similarity/",
        UpdateProductSimilarityView.as_view(),
        name="update-product-similarity",
    ),
    path(
        "api/recommendation-algorithm-status/",
        RecommendationAlgorithmStatusView.as_view(),
        name="recommendation-algorithm-status",
    ),
    path(
        "api/collaborative-filtering-debug/",
        CollaborativeFilteringDebugView.as_view(),
        name="collaborative-filtering-debug",
    ),
    path(
        "api/content-based-debug/",
        ContentBasedDebugView.as_view(),
        name="content-based-debug",
    ),
    path(
        "api/fuzzy-logic-debug/",
        FuzzyLogicDebugView.as_view(),
        name="fuzzy-logic-debug",
    ),
    path(
        "api/probabilistic-debug/",
        ProbabilisticDebugView.as_view(),
        name="probabilistic-debug",
    ),
    path(
        "api/frequently-bought-together/",
        FrequentlyBoughtTogetherAPI.as_view(),
        name="frequently-bought-together",
    ),
    path(
        "api/update-association-rules/",
        UpdateAssociationRulesAPI.as_view(),
        name="update-association-rules",
    ),
    path(
        "api/association-rules/",
        AssociationRulesListAPI.as_view(),
        name="association-rules",
    ),
    path(
        "api/association-rules-analysis/",
        AssociationRulesAnalysisAPI.as_view(),
        name="association-rules-analysis",
    ),
    path(
        "api/product-association-debug/",
        ProductAssociationDebugAPI.as_view(),
        name="product-association-debug",
    ),
    path(
        "api/markov-recommendations/",
        MarkovRecommendationsAPI.as_view(),
        name="markov-recommendations",
    ),
    path(
        "api/bayesian-insights/",
        BayesianInsightsAPI.as_view(),
        name="bayesian-insights",
    ),
    path(
        "api/admin/probabilistic-analysis/",
        ProbabilisticAnalysisAdminAPI.as_view(),
        name="probabilistic-admin-analysis",
    ),
    path(
        "api/risk-dashboard/",
        RiskDashboardView.as_view(),
        name="risk-dashboard",
    ),
    path(
        "api/sales-forecast/",
        SalesForecastView.as_view(),
        name="sales-forecast",
    ),
    path(
        "api/product-demand/",
        ProductDemandView.as_view(),
        name="product-demand",
    ),
    path(
        "api/user-purchase-patterns/",
        UserPurchasePatternsView.as_view(),
        name="user-purchase-patterns",
    ),
    path(
        "api/admin-purchase-patterns/",
        AdminPurchasePatternsView.as_view(),
        name="admin-purchase-patterns",
    ),
    path(
        "api/admin-product-recommendations/",
        AdminProductRecommendationsView.as_view(),
        name="admin-product-recommendations",
    ),
    path(
        "api/admin-churn-prediction/",
        AdminChurnPredictionView.as_view(),
        name="admin-churn-prediction",
    ),
    path(
        "api/my-shopping-insights/",
        MyShoppingInsightsView.as_view(),
        name="my-shopping-insights",
    ),
    path(
        "api/personalized-recommendations/",
        RecommendedProductsAPIView.as_view(),
        name="personalized-recommendations",
    ),
    path(
        "api/seasonal-trends/",
        SeasonalTrendsView.as_view(),
        name="seasonal-trends",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
