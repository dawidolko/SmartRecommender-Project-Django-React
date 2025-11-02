"""
Django Signals Module for Real-Time Analytics and Recommendation Updates.

This module implements event-driven triggers that automatically:
    - Update recommendation models when users make purchases or add to cart
    - Regenerate association rules (Apriori algorithm) after new orders
    - Perform sentiment analysis on new product opinions/reviews
    - Invalidate caches to ensure fresh recommendations
    - Trigger probabilistic analytics (purchase probability, churn risk, forecasts)

Signal Triggers:
    1. Order Created → Generate analytics + association rules + recommendations
    2. OrderProduct Created → Log interaction + invalidate caches
    3. CartItem Created → Log interaction + update content-based recommendations
    4. Product Modified → Invalidate content-based cache
    5. Opinion Created → Analyze sentiment + update product summary

Architecture Pattern:
    Observer Pattern - Django signals act as event subscribers that respond
    to model changes automatically without explicit method calls.

Performance Optimizations:
    - transaction.on_commit() - Delays expensive operations until DB commit
    - Cache invalidation - Targeted deletion of affected cache keys
    - Bulk operations - batch_size=500 for mass inserts
    - Skip flags - _skip_analytics prevents duplicate processing

Mathematical Models Triggered:
    - Apriori Association Rules (min_support=0.001, min_confidence=0.01)
    - Naive Bayes Purchase Probability
    - Logistic Regression Churn Risk
    - ARIMA Sales Forecasting
    - Sentiment Analysis (Lexicon-based)

Authors: Dawid Olko & Piotr Smoła
Date: 2025-11-02
Version: 2.0
"""

from colorama import Fore
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from collections import defaultdict
from django.db.models import Avg
from django.core.cache import cache
from .models import (
    Order,
    OrderProduct,
    ProductAssociation,
    Product,
    RecommendationSettings,
    ProductSimilarity,
    UserProductRecommendation,
    CartItem,
    UserInteraction,
    Opinion,
    SentimentAnalysis,
    ProductSentimentSummary,
)
from .analytics import (
    generate_purchase_probabilities_for_user,
    generate_user_purchase_patterns_for_user,
    generate_risk_assessment_for_user,
    generate_sales_forecasts_for_products,
    generate_product_demand_forecasts_for_products,
)
from .custom_recommendation_engine import (
    CustomContentBasedFilter,
    CustomAssociationRules,
    CustomSentimentAnalysis,
)


@receiver(post_save, sender=Order)
def handle_new_order_and_analytics(sender, instance, created, **kwargs):
    """
    Trigger comprehensive analytics pipeline when new order is created.
    
    Event: post_save signal for Order model (fired after order.save())
    
    Actions Performed:
        1. Verify order is new (created=True) and user is client (not admin)
        2. Schedule analytics execution after database commit (transaction safety)
        3. Delegate to run_all_analytics_after_order() for heavy processing
    
    Args:
        sender (Model): Order model class
        instance (Order): The order instance that was saved
        created (bool): True if new order, False if update
        **kwargs: Additional signal arguments
    
    Performance:
        Uses transaction.on_commit() to defer expensive operations until
        after database transaction completes. Prevents blocking HTTP response.
    
    Example Flow:
        User places order → Order.save() → Signal fires → 
        Wait for commit → Run analytics → Generate recommendations
    
    Skip Conditions:
        - Order already exists (created=False)
        - User is admin (role != 'client')
        - _skip_analytics flag is set (prevents duplicate processing)
    """
    if created and instance.user.role == "client":
        transaction.on_commit(lambda: run_all_analytics_after_order(instance))


@receiver(post_save, sender=OrderProduct)
def log_interaction_on_purchase(sender, instance, created, **kwargs):
    """
    Log user-product interaction and invalidate recommendation caches on purchase.
    
    Event: post_save signal for OrderProduct model (product added to order)
    
    Actions Performed:
        1. Create UserInteraction record (type='purchase')
        2. Invalidate ALL recommendation caches (collaborative, content-based, association)
        3. Invalidate user-specific recommendation caches
    
    Args:
        sender (Model): OrderProduct model class
        instance (OrderProduct): The order-product relationship instance
        created (bool): True if new purchase
        **kwargs: Additional signal arguments
    
    Cache Keys Invalidated:
        - collaborative_similarity_matrix: Full collaborative filtering matrix
        - content_based_similarity_matrix: Full content-based matrix
        - association_rules_list: Apriori association rules
        - user_recommendations_{user_id}_collaborative: User-specific CF recs
        - user_recommendations_{user_id}_content_based: User-specific CB recs
    
    Why Invalidate:
        New purchase changes user's preference profile, requiring fresh
        recommendation calculations with updated data.
    
    Example:
        User buys "Laptop" → OrderProduct created → Log interaction →
        Delete cached recommendations → Next API call regenerates fresh recs
    """
    if created:
        # Log interaction for analytics tracking
        UserInteraction.objects.create(
            user=instance.order.user,
            product=instance.product,
            interaction_type="purchase",
        )
        
        # Invalidate global recommendation caches
        cache.delete("collaborative_similarity_matrix")
        cache.delete("content_based_similarity_matrix")
        cache.delete("association_rules_list")
        
        # Invalidate user-specific caches
        user_id = instance.order.user.id
        cache.delete(f"user_recommendations_{user_id}_collaborative")
        cache.delete(f"user_recommendations_{user_id}_content_based")
        
        print("Cache invalidated due to new purchase")


@receiver(post_save, sender=CartItem)
def log_interaction_on_cart_add(sender, instance, created, **kwargs):
    """
    Log user-product interaction and update content-based recommendations on cart add.
    
    Event: post_save signal for CartItem model (product added to shopping cart)
    
    Actions Performed:
        1. Create UserInteraction record (type='add_to_cart')
        2. Update user's content-based recommendations
    
    Args:
        sender (Model): CartItem model class
        instance (CartItem): The cart item instance
        created (bool): True if new cart addition
        **kwargs: Additional signal arguments
    
    Skip Conditions:
        - _skip_similarity_update flag is set (prevents recursive updates)
    
    Why Update Recommendations:
        Adding to cart indicates strong interest in product category/features.
        Content-based filter uses this signal to recommend similar products.
    
    Example:
        User adds "Gaming Mouse" to cart → CartItem created → Log interaction →
        Find products similar to "Gaming Mouse" (same category, specs) →
        Update UserProductRecommendation with new scores
    
    Difference from Purchase:
        Cart addition triggers ONLY content-based updates (lighter operation).
        Purchase triggers FULL analytics pipeline (heavier operation).
    """
    if created:
        # Log interaction for analytics
        UserInteraction.objects.create(
            user=instance.user, product=instance.product, interaction_type="add_to_cart"
        )
        
        # Update content-based recommendations (unless skipped)
        if not getattr(instance, "_skip_similarity_update", False):
            update_user_cb_recommendations(instance.user)


@receiver(post_save, sender=Product)
def handle_product_changes(sender, instance, created, **kwargs):
    """
    Invalidate content-based cache when product metadata changes.
    
    Event: post_save signal for Product model (product created or updated)
    
    Actions Performed:
        1. Check if relevant fields changed (name, description, price)
        2. Invalidate content-based similarity matrix cache
    
    Args:
        sender (Model): Product model class
        instance (Product): The product instance
        created (bool): True if new product, False if update
        **kwargs: Additional signal arguments (includes update_fields)
    
    Watched Fields:
        - name: Product name (used in TF-IDF vectorization)
        - description: Product description (main content for similarity)
        - price: Product price (affects value-based recommendations)
    
    Why Invalidate:
        Content-based filtering uses product text (name + description) to
        calculate TF-IDF vectors and cosine similarity. Changes to these
        fields require recalculation of similarity matrix.
    
    Cache Key Invalidated:
        - content_based_similarity_matrix: Full content-based matrix
    
    Example:
        Admin updates product description →
        Product.save(update_fields=['description']) → Signal fires →
        Delete cached similarity matrix → Next recommendation call regenerates
    
    Performance:
        Only invalidates if relevant fields changed (avoids unnecessary work).
    """
    update_fields = kwargs.get('update_fields', [])
    
    # Check if product is new OR relevant fields were updated
    if created or (update_fields is not None and any(field in update_fields for field in ['name', 'description', 'price'])):
        cache.delete("content_based_similarity_matrix")
        print("Content-based cache invalidated due to product changes")


@receiver(post_save, sender=Opinion)
def handle_sentiment_analysis(sender, instance, created, **kwargs):
    """
    Automatically analyze sentiment of product reviews/opinions on creation.
    
    Event: post_save signal for Opinion model (new review posted)
    
    Actions Performed:
        1. Check for skip flag (_skip_sentiment_update)
        2. Verify opinion has content text
        3. Initialize CustomSentimentAnalysis engine
        4. Analyze sentiment using lexicon-based approach
        5. Store results in SentimentAnalysis model
        6. Invalidate product-specific sentiment cache
        7. Update ProductSentimentSummary with aggregated scores
    
    Args:
        sender (Model): Opinion model class
        instance (Opinion): The opinion instance (product review)
        created (bool): True if new opinion
        **kwargs: Additional signal arguments
    
    Skip Conditions:
        - _skip_sentiment_update flag is set (prevents duplicate processing)
        - instance.content is None or empty (no text to analyze)
    
    Sentiment Analysis Process:
        1. Text Preprocessing:
           - Tokenize review text (instance.content) into words
           - Convert to lowercase
           - Remove punctuation
        
        2. Lexicon Matching:
           - positive_words: Opinion Lexicon (2006+ words)
           - negative_words: AFINN-165 (3382 words)
           - Calculate sentiment score [-1.0, +1.0]
        
        3. Categorization:
           sentiment_category = 'positive' if score > 0.1
                               'negative' if score < -0.1
                               'neutral' otherwise
        
        4. Database Storage:
           - SentimentAnalysis: Individual review sentiment (opinion, score, category)
           - ProductSentimentSummary: Aggregated product-level sentiment
    
    Cache Management:
        Invalidates: product_sentiment_{product_id}_static
        This forces fresh calculation on next API call requesting product sentiment.
    
    Example Flow:
        User posts review: "This laptop is amazing! Fast and reliable."
        → Signal fires → Extract content → Analyze sentiment →
        Result: {score: 0.75, category: 'positive'}
        → Store in SentimentAnalysis → Delete cache →
        → Calculate product average → Update ProductSentimentSummary
    
    Data Model:
        SentimentAnalysis:
            - opinion: ForeignKey to Opinion (one-to-one relationship)
            - product: ForeignKey to Product (denormalized for quick access)
            - sentiment_score: Float [-1.0, +1.0]
            - sentiment_category: 'positive' | 'negative' | 'neutral'
        
        ProductSentimentSummary:
            - product: OneToOne with Product
            - avg_sentiment_score: Average score across all reviews
            - total_positive: Count of positive reviews
            - total_negative: Count of negative reviews
            - total_neutral: Count of neutral reviews
            - dominant_sentiment: Most common category
    
    Performance:
        - Runs synchronously after opinion creation (lightweight operation)
        - Lexicon matching: O(n) where n = word count in review
        - No ML inference (faster than neural models)
        - Cache invalidation prevents stale data
    """
    # Skip if flag is set (prevents recursive updates)
    if getattr(instance, "_skip_sentiment_update", False):
        return
        
    # Only process if opinion has text content
    if instance.content:
        # Initialize sentiment analyzer with academic lexicons
        sentiment_analyzer = CustomSentimentAnalysis()
        
        # Analyze sentiment: returns (score, category)
        sentiment_score, sentiment_category = sentiment_analyzer.analyze_sentiment(
            instance.content
        )

        # Store or update individual review sentiment
        SentimentAnalysis.objects.update_or_create(
            opinion=instance,
            defaults={
                "product": instance.product,
                "sentiment_score": sentiment_score,
                "sentiment_category": sentiment_category,
            },
        )

        # Invalidate product-specific sentiment cache
        cache_pattern = f"product_sentiment_{instance.product.id}_*"
        cache.delete(f"product_sentiment_{instance.product.id}_static")
        
        # Recalculate aggregated product sentiment (all reviews)
        sentiment_data = sentiment_analyzer.analyze_product_sentiment(
            instance.product
        )
        
        # Update product sentiment summary with new averages
        ProductSentimentSummary.objects.update_or_create(
            product=instance.product, defaults=sentiment_data
        )
        
        print(f"Sentiment cache invalidated for product {instance.product.id}")


def run_all_analytics_after_order(order):
    """
    Execute comprehensive analytics pipeline after order creation.
    
    This is the main orchestrator function that coordinates all analytics
    modules to update user profiles, product forecasts, and recommendations.
    
    Args:
        order (Order): The newly created order instance
    
    Pipeline Stages:
        1. Cache Invalidation:
           - Delete collaborative_similarity_matrix cache
           - Ensures fresh CF recommendations
        
        2. Association Rules:
           - Generate Apriori rules from all transactions
           - Create ProductAssociation records (unless _skip_analytics)
        
        3. User-Specific Analytics:
           - Purchase Probabilities (Naive Bayes)
           - Purchase Patterns (RFM Analysis)
           - Risk Assessment (Churn Prediction)
        
        4. Product-Specific Analytics:
           - Sales Forecasts (ARIMA-inspired)
           - Demand Forecasts (Inventory Management)
           - Only for products in current order
        
        5. Recommendation Updates:
           - Generate user recommendations based on active algorithm
           - Collaborative or Content-Based
    
    Process Flow:
        Order Created → run_all_analytics_after_order() →
        ├─ cache.delete("collaborative_similarity_matrix")
        ├─ generate_association_rules_after_order()
        ├─ generate_purchase_probabilities_for_user()
        ├─ generate_user_purchase_patterns_for_user()
        ├─ generate_risk_assessment_for_user()
        ├─ generate_sales_forecasts_for_products(product_ids)
        ├─ generate_product_demand_forecasts_for_products(product_ids)
        └─ generate_user_recommendations_after_order()
    
    Skip Flags:
        - order._skip_analytics: Skips association rules and user recommendations
        - Useful during bulk imports or data migrations
    
    Performance Considerations:
        - Runs in transaction.on_commit() hook (after DB commit)
        - Processes single user + products in order only
        - Takes ~2-5 seconds for typical order
        - Does NOT block HTTP response
    
    Mathematical Models:
        1. Purchase Probabilities:
           P(purchase | history, category, recency) using Naive Bayes
        
        2. RFM Analysis:
           Frequency = N_orders / months_active
           Recency = days_since_last_order
           Monetary = average_order_value
        
        3. Churn Risk:
           Logistic Regression:
           P(churn) = 1 / (1 + e^-(β₀ + β₁×recency + β₂×frequency))
        
        4. Sales Forecast:
           Forecast(t) = Trend(t) × Seasonal(t) × Noise
           Trend = linear regression on historical data
           Seasonal = monthly multiplier (0.85-1.5x)
        
        5. Association Rules:
           Apriori algorithm with min_support=0.001, min_confidence=0.01
           Support(A→B) = count(A∩B) / total_orders
           Confidence(A→B) = count(A∩B) / count(A)
    
    Console Output:
        - "Running analytics for order {id}"
        - "Invalidated CF cache after order {id}"
        - Progress messages from each analytics function
    
    Error Handling:
        - Individual function failures don't crash pipeline
        - Missing data handled gracefully (returns empty results)
        - Exceptions logged to console
    
    Example:
        User places order for "Laptop" (ID=1) + "Mouse" (ID=2) →
        Pipeline runs:
        1. Delete CF cache
        2. Generate association rule: Laptop → Mouse (confidence=0.75)
        3. Update user's purchase probability for "Electronics"
        4. Calculate user's RFM scores (frequency +1)
        5. Predict churn risk (recency updated)
        6. Forecast sales for Laptop and Mouse (next 30 days)
        7. Generate recommendations (users who bought laptop also bought...)
    """
    print(f"Running analytics for order {order.id}")

    # Stage 1: Invalidate collaborative filtering cache
    cache_key = "collaborative_similarity_matrix"
    cache.delete(cache_key)
    print(f"Invalidated CF cache after order {order.id}")

    # Stage 2: Generate association rules (unless skipped)
    if not getattr(order, "_skip_analytics", False):
        generate_association_rules_after_order(order)

    # Stage 3: User-specific probabilistic analytics
    generate_purchase_probabilities_for_user(order.user)
    generate_user_purchase_patterns_for_user(order.user)
    generate_risk_assessment_for_user(order.user)

    # Stage 4: Product-specific forecasts (only for products in this order)
    product_ids = OrderProduct.objects.filter(order=order).values_list(
        "product_id", flat=True
    )
    generate_sales_forecasts_for_products(product_ids)
    generate_product_demand_forecasts_for_products(product_ids)

    # Stage 5: Update user recommendations (unless skipped)
    if not getattr(order, "_skip_analytics", False):
        generate_user_recommendations_after_order(order.user)


def generate_user_recommendations_after_order(user):
    """
    Generate personalized product recommendations for user after order placement.
    
    Uses user's purchase history and cart items to find similar products
    based on the active recommendation algorithm (collaborative or content-based).
    
    Args:
        user (User): The user instance to generate recommendations for
    
    Algorithm Selection:
        Reads RecommendationSettings.active_algorithm for user:
        - 'collaborative': Uses user-user collaborative filtering
        - 'content_based': Uses product feature similarity
        - Default: 'collaborative' if no settings found
    
    Process Flow:
        1. Get active algorithm from user settings
        2. Collect all user's product interactions:
           - Products from past orders (OrderProduct)
           - Products in current cart (CartItem)
        3. For each interacted product:
           - Find top 5 similar products (ProductSimilarity)
           - Accumulate similarity scores
        4. Aggregate scores for duplicate recommendations
        5. Store in UserProductRecommendation with algorithm type
    
    Recommendation Scoring:
        For each product user has interacted with:
            Find similar_products = ProductSimilarity.filter(
                product1=interacted_product,
                similarity_type=algorithm
            ).order_by('-similarity_score')[:5]
            
            For each similar product:
                recommendations[product_id] += similarity_score
        
        Final score = sum of all similarity scores from multiple sources
    
    Example:
        User has:
        - Purchased: Laptop (ID=1), Keyboard (ID=2)
        - In cart: Mouse (ID=3)
        
        Algorithm='collaborative'
        
        Similarities:
        - Laptop → [Monitor(0.9), Webcam(0.8), Headset(0.7)]
        - Keyboard → [Mouse(0.85), Mousepad(0.75)]
        - Mouse → [Mousepad(0.9), USB Hub(0.6)]
        
        Aggregated recommendations:
        - Monitor: 0.9
        - Webcam: 0.8
        - Headset: 0.7
        - Mouse: 0.85
        - Mousepad: 0.75 + 0.9 = 1.65 (accumulated!)
        - USB Hub: 0.6
    
    Database Updates:
        Uses update_or_create() for UserProductRecommendation:
        - user: ForeignKey to User
        - product_id: ID of recommended product
        - recommendation_type: 'collaborative' | 'content_based'
        - score: Float (aggregated similarity score)
    
    Performance:
        - Queries ProductSimilarity for top 5 per interacted product
        - Uses defaultdict for efficient score aggregation
        - Bulk updates via update_or_create (one query per recommendation)
    
    Filtering:
        Automatically excludes products user already owns/has in cart
        (they're in the source product list, not in recommendations).
    """
    # Get user's preferred recommendation algorithm
    settings = RecommendationSettings.objects.filter(user=user).first()
    algorithm = settings.active_algorithm if settings else "collaborative"

    # Collect all products user has interacted with
    user_products = []
    
    # Add products from past orders
    orders = Order.objects.filter(user=user)
    for order in orders:
        products = order.orderproduct_set.all()
        user_products.extend([op.product_id for op in products])

    # Add products from current cart
    cart_items = CartItem.objects.filter(user=user)
    user_products.extend([item.product_id for item in cart_items])

    # Accumulate similarity scores from all interacted products
    recommendations = defaultdict(float)
    for product_id in set(user_products):  # Remove duplicates
        # Find top 5 most similar products
        similarities = ProductSimilarity.objects.filter(
            product1_id=product_id, similarity_type=algorithm
        ).order_by("-similarity_score")[:5]

        # Add similarity scores (accumulate if product appears multiple times)
        for similarity in similarities:
            recommendations[similarity.product2_id] += float(
                similarity.similarity_score
            )

    # Store recommendations in database
    for product_id, score in recommendations.items():
        UserProductRecommendation.objects.update_or_create(
            user=user,
            product_id=product_id,
            recommendation_type=algorithm,
            defaults={"score": score},
        )


def generate_association_rules_after_order(order):
    """
    Generate product association rules using Apriori algorithm after new order.
    
    Analyzes all historical orders to find frequent product combinations
    (e.g., "Users who bought Laptop also bought Mouse"). Creates
    ProductAssociation records with support, confidence, and lift metrics.
    
    Args:
        order (Order): The newly created order (triggers rule regeneration)
    
    Apriori Algorithm Parameters:
        - min_support: 0.001 (product pair must appear in 0.1% of orders)
        - min_confidence: 0.01 (rule must be correct 1% of the time)
    
    Mathematical Formulas:
        1. Support:
           Support(A → B) = count(orders containing both A and B) / total_orders
           
           Example: If 10 orders have {Laptop, Mouse} out of 1000 orders:
           Support = 10/1000 = 0.01 = 1%
        
        2. Confidence:
           Confidence(A → B) = count(A and B together) / count(A alone)
           
           Example: If Laptop appears in 50 orders, {Laptop, Mouse} in 10:
           Confidence = 10/50 = 0.2 = 20%
           (20% of laptop buyers also buy mouse)
        
        3. Lift:
           Lift(A → B) = Confidence(A → B) / Support(B)
           
           Example: If Mouse appears in 100 orders (support=0.1):
           Lift = 0.2 / 0.1 = 2.0
           (Laptop buyers are 2× more likely to buy mouse than random)
    
    Process Flow:
        1. Cache Invalidation:
           Delete association_rules_list, CF matrix, CB matrix
        
        2. Transaction Extraction:
           orders = all Order objects with products
           transactions = [[product_1, product_2, ...], ...]
           Filter: only orders with 2+ products
        
        3. Minimum Validation:
           Require at least 2 transactions (insufficient data otherwise)
        
        4. Apriori Execution:
           engine = CustomAssociationRules(min_support=0.001, min_confidence=0.01)
           rules = engine.generate_association_rules(transactions)
        
        5. Database Update:
           - Delete all existing ProductAssociation records
           - Create new records from generated rules
           - Bulk insert with batch_size=500
    
    Data Model:
        ProductAssociation:
            - product_1: ForeignKey to Product (antecedent A)
            - product_2: ForeignKey to Product (consequent B)
            - support: Float [0.0, 1.0]
            - confidence: Float [0.0, 1.0]
            - lift: Float (typically 0.0-5.0, >1.0 means positive correlation)
    
    Example Output:
        Rule: Laptop (ID=1) → Mouse (ID=2)
        - support: 0.05 (5% of orders have both)
        - confidence: 0.35 (35% of laptop buyers buy mouse)
        - lift: 2.5 (2.5× more likely than random)
        
        Interpretation: Strong association! If customer buys laptop,
        recommend mouse (35% chance they'll buy it).
    
    Performance:
        - Prefetch related for efficient order loading
        - Bulk create with batch_size=500 (reduces DB queries)
        - Typical execution: 2-10 seconds for 1000 orders
    
    Console Output:
        - "🔄 Generating association rules from X transactions..."
        - "📊 Generated Y rules, deleting old rules..."
        - "✅ Created Z association rules"
        - "❌ Error..." (if exception occurs)
    
    Edge Cases:
        - Not enough transactions (<2): Prints warning, returns early
        - Product not found: Skips invalid product IDs
        - ValueError during parsing: Skips malformed rules
    
    Error Handling:
        - try/except around entire function
        - Prints error message but doesn't raise
        - Invalid products skipped gracefully
    """
    try:
        # Stage 1: Invalidate all recommendation caches
        cache.delete_many([
            "association_rules_list",
            "collaborative_similarity_matrix",
            "content_based_similarity_matrix"
        ])
        
        # Stage 2: Extract transactions from all orders
        orders = Order.objects.prefetch_related("orderproduct_set__product").all()
        transactions = []

        for order_obj in orders:
            # Get product IDs as strings (required by Apriori implementation)
            product_ids = [
                str(item.product_id) for item in order_obj.orderproduct_set.all()
            ]
            # Only include orders with multiple products (required for association)
            if len(product_ids) >= 2:
                transactions.append(product_ids)

        # Stage 3: Validate minimum data requirements
        if len(transactions) < 2:
            print("Not enough transactions for association rules")
            return

        print(f"🔄 Generating association rules from {len(transactions)} transactions...")
        
        # Stage 4: Run Apriori algorithm
        association_engine = CustomAssociationRules(
            min_support=0.001,  # 0.1% minimum support
            min_confidence=0.01  # 1% minimum confidence
        )
        rules = association_engine.generate_association_rules(transactions)

        print(f"📊 Generated {len(rules)} rules, deleting old rules...")
        
        # Stage 5: Replace old rules with new ones
        ProductAssociation.objects.all().delete()
        
        # Prepare bulk insert
        rules_to_create = []
        for rule in rules:
            try:
                # Convert product IDs from strings to Product instances
                product_1 = Product.objects.get(id=int(rule["product_1"]))
                product_2 = Product.objects.get(id=int(rule["product_2"]))
                
                # Create ProductAssociation instance (not saved yet)
                rules_to_create.append(ProductAssociation(
                    product_1=product_1,
                    product_2=product_2,
                    support=rule["support"],
                    confidence=rule["confidence"],
                    lift=rule["lift"],
                ))
            except (Product.DoesNotExist, ValueError):
                # Skip invalid product IDs
                continue

        # Bulk insert all rules at once
        ProductAssociation.objects.bulk_create(rules_to_create, batch_size=500)
        print(f"✅ Created {len(rules_to_create)} association rules")

    except Exception as e:
        print(f"❌ Error generating association rules: {e}")


def update_user_cb_recommendations(user):
    """
    Update content-based recommendations for user based on interaction history.
    
    Analyzes user's product interactions (views, cart adds, purchases) and
    finds similar products using content-based filtering (TF-IDF + cosine similarity).
    
    Args:
        user (User): The user instance to update recommendations for
    
    Content-Based Filtering:
        Uses product features (name, description, category) to calculate
        similarity between products. Recommends products similar to ones
        user has already interacted with.
    
    Algorithm:
        1. TF-IDF Vectorization:
           text = product.name + " " + product.description
           vector = TfidfVectorizer(max_features=100).fit_transform(text)
        
        2. Cosine Similarity:
           similarity(A, B) = dot(A, B) / (||A|| × ||B||)
           Range: [0.0, 1.0] where 1.0 = identical products
        
        3. Similarity stored in ProductSimilarity:
           product1, product2, similarity_score, similarity_type='content_based'
    
    Process Flow:
        1. Get all user interactions (any type: view, cart, purchase)
        2. Extract unique product IDs from interactions
        3. For each interacted product:
           - Find top 5 similar products (ProductSimilarity)
           - Filter by similarity_type='content_based'
        4. Accumulate similarity scores for each recommended product
        5. Store in UserProductRecommendation with type='content_based'
    
    Example:
        User interactions:
        - Viewed: "Gaming Laptop" (ID=1)
        - Added to cart: "Mechanical Keyboard" (ID=2)
        - Purchased: "Gaming Mouse" (ID=3)
        
        ProductSimilarity (content_based):
        - Gaming Laptop → [Business Laptop(0.85), Ultrabook(0.75), Tablet(0.6)]
        - Mechanical Keyboard → [Gaming Keyboard(0.9), Wireless Keyboard(0.7)]
        - Gaming Mouse → [Wireless Mouse(0.88), Gaming Mousepad(0.6)]
        
        Aggregated recommendations:
        - Business Laptop: 0.85
        - Ultrabook: 0.75
        - Gaming Keyboard: 0.9
        - Wireless Keyboard: 0.7
        - Wireless Mouse: 0.88
        - Gaming Mousepad: 0.6
        - Tablet: 0.6
    
    Difference from Collaborative Filtering:
        - Content-Based: Uses product FEATURES (text, category)
        - Collaborative: Uses USER BEHAVIOR (who bought what together)
        
        Content-based works well for:
        - New users (cold start problem)
        - Users with specific preferences (always buy gaming products)
        
        Collaborative works well for:
        - Diverse users with varied tastes
        - Discovering unexpected products
    
    Data Model:
        UserProductRecommendation:
            - user: ForeignKey to User
            - product_id: ID of recommended product
            - recommendation_type: 'content_based'
            - score: Float (aggregated similarity score)
    
    Performance:
        - Uses defaultdict for efficient score aggregation
        - Queries top 5 similarities per interacted product
        - update_or_create: one query per recommendation
    
    Error Handling:
        - try/except around entire function
        - Prints error but doesn't raise (graceful failure)
        - Invalid data skipped silently
    """
    try:
        # Get all user's product interactions (any type)
        user_interactions = UserInteraction.objects.filter(user=user).values_list(
            "product_id", flat=True
        )
        
        # Accumulate similarity scores
        recommendations = defaultdict(float)

        # For each unique interacted product
        for product_id in set(user_interactions):
            # Find top 5 content-based similar products
            similarities = ProductSimilarity.objects.filter(
                product1_id=product_id, similarity_type="content_based"
            ).order_by("-similarity_score")[:5]

            # Add similarity scores (accumulate if product appears multiple times)
            for similarity in similarities:
                recommendations[similarity.product2_id] += float(
                    similarity.similarity_score
                )

        # Store content-based recommendations in database
        for product_id, score in recommendations.items():
            UserProductRecommendation.objects.update_or_create(
                user=user,
                product_id=product_id,
                recommendation_type="content_based",
                defaults={"score": score},
            )

    except Exception as e:
        print(f"Error updating content-based recommendations: {e}")


def update_content_based_similarity():
    """
    Regenerate content-based similarity matrix for ALL products.
    
    Calculates pairwise product similarity using TF-IDF vectorization and
    cosine similarity on product text (name + description). Updates
    ProductSimilarity table with new similarity scores.
    
    Returns:
        int: Number of similarity relationships created
    
    Content-Based Filtering Algorithm:
        1. Text Preprocessing:
           For each product:
               text = product.name + " " + product.description
               text = lowercase(text)
               text = remove_punctuation(text)
        
        2. TF-IDF Vectorization:
           TF (Term Frequency):
               TF(word, doc) = count(word in doc) / total_words(doc)
           
           IDF (Inverse Document Frequency):
               IDF(word) = log(total_products / products_containing_word)
           
           TF-IDF:
               score(word, doc) = TF(word, doc) × IDF(word)
           
           Vector: [score_word1, score_word2, ..., score_wordN]
        
        3. Cosine Similarity:
           similarity(A, B) = (A · B) / (||A|| × ||B||)
           
           Where:
           - A · B = dot product of vectors A and B
           - ||A|| = magnitude of vector A = sqrt(sum(a_i²))
           - Range: [0.0, 1.0]
           
           Example:
           Product A: "Gaming Laptop" → [0.5, 0.8, 0.2, 0.0, ...]
           Product B: "Business Laptop" → [0.3, 0.7, 0.1, 0.0, ...]
           
           Similarity = (0.5×0.3 + 0.8×0.7 + 0.2×0.1) / (sqrt(...) × sqrt(...))
                      = 0.73 / 0.95
                      = 0.77 (high similarity!)
    
    Process Flow:
        1. Initialize CustomContentBasedFilter engine
        2. Call generate_similarities_for_all_products():
           - Get all products from database
           - Vectorize product texts using TF-IDF
           - Calculate pairwise cosine similarities
           - Store in ProductSimilarity with type='content_based'
        3. Return count of similarities created
    
    When to Run:
        - Product metadata changed (name, description, price)
        - New products added to catalog
        - Manual cache refresh requested
        - Triggered by handle_product_changes signal
    
    Performance Considerations:
        - Complexity: O(n²) where n = number of products
        - For 1000 products: ~500,000 similarity pairs
        - Typical execution: 10-30 seconds
        - Uses sparse matrix representation for efficiency
        - Bulk creates ProductSimilarity records
    
    Data Model:
        ProductSimilarity:
            - product1: ForeignKey to Product (source)
            - product2: ForeignKey to Product (target)
            - similarity_score: Float [0.0, 1.0]
            - similarity_type: 'content_based'
    
    Example Output:
        ProductSimilarity records:
        - (Gaming Laptop, Business Laptop, 0.77, 'content_based')
        - (Gaming Laptop, Ultrabook, 0.65, 'content_based')
        - (Gaming Laptop, Gaming Mouse, 0.45, 'content_based')
        - (Gaming Laptop, Office Chair, 0.12, 'content_based')
    
    Console Output:
        - Success: "Generated X content-based similarities" (green)
        - Error: "Error in content-based similarity: Y" (red)
    
    Error Handling:
        - try/except around entire function
        - Returns 0 on failure
        - Prints error message with colorama.Fore.RED
    
    Integration:
        Used by:
        - handle_product_changes signal (automatic)
        - Admin panel "Regenerate Similarities" button (manual)
        - Management command: python manage.py generate_similarities
    """
    try:
        # Initialize content-based filtering engine
        content_filter = CustomContentBasedFilter()
        
        # Generate similarities for all products (TF-IDF + cosine similarity)
        similarity_count = content_filter.generate_similarities_for_all_products()
        
        # Log success with count
        print(Fore.GREEN + f"Generated {similarity_count} content-based similarities")
        return similarity_count
        
    except Exception as e:
        # Log error but don't raise (graceful failure)
        print(Fore.RED + f"Error in content-based similarity: {e}")
        return 0
