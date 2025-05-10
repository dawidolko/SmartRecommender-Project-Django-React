from colorama import Fore
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from collections import defaultdict
from textblob import TextBlob
from django.db.models import Avg
from .models import (
    Order, OrderProduct, ProductAssociation, Product,
    RecommendationSettings, ProductSimilarity, UserProductRecommendation,
    CartItem, UserInteraction, Opinion, SentimentAnalysis, ProductSentimentSummary
)
from .analytics import (
    generate_purchase_probabilities_for_user,
    generate_user_purchase_patterns_for_user,
    generate_risk_assessment_for_user,
    generate_sales_forecasts_for_products,
    generate_product_demand_forecasts_for_products
)
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


@receiver(post_save, sender=Order)
def handle_new_order_and_analytics(sender, instance, created, **kwargs):
    if created and instance.user.role == 'client':
        transaction.on_commit(lambda: run_all_analytics_after_order(instance))


@receiver(post_save, sender=OrderProduct)
def log_interaction_on_purchase(sender, instance, created, **kwargs):
    if created:
        UserInteraction.objects.create(
            user=instance.order.user,
            product=instance.product,
            interaction_type='purchase'
        )


@receiver(post_save, sender=CartItem)
def log_interaction_on_cart_add(sender, instance, created, **kwargs):
    if created:
        UserInteraction.objects.create(
            user=instance.user,
            product=instance.product,
            interaction_type='add_to_cart'
        )
        update_content_based_similarity()
        update_user_cb_recommendations(instance.user)


@receiver(post_save, sender=Opinion)
def handle_sentiment_analysis(sender, instance, created, **kwargs):
    if instance.content:
        blob = TextBlob(instance.content)
        sentiment_score = blob.sentiment.polarity
        if sentiment_score > 0.05:
            sentiment_category = 'positive'
        elif sentiment_score < -0.05:
            sentiment_category = 'negative'
        else:
            sentiment_category = 'neutral'

        SentimentAnalysis.objects.update_or_create(
            opinion=instance,
            defaults={
                'product': instance.product,
                'sentiment_score': sentiment_score,
                'sentiment_category': sentiment_category
            }
        )

        summary_values = SentimentAnalysis.objects.filter(product=instance.product)
        total = summary_values.count()
        pos = summary_values.filter(sentiment_category='positive').count()
        neu = summary_values.filter(sentiment_category='neutral').count()
        neg = summary_values.filter(sentiment_category='negative').count()
        avg_score = summary_values.aggregate(avg=Avg('sentiment_score'))['avg'] or 0

        ProductSentimentSummary.objects.update_or_create(
            product=instance.product,
            defaults={
                'average_sentiment_score': avg_score,
                'positive_count': pos,
                'neutral_count': neu,
                'negative_count': neg,
                'total_opinions': total
            }
        )


def run_all_analytics_after_order(order):
    generate_association_rules_after_order(order)
    generate_purchase_probabilities_for_user(order.user)
    generate_user_purchase_patterns_for_user(order.user)
    generate_risk_assessment_for_user(order.user)
    product_ids = OrderProduct.objects.filter(order=order).values_list('product_id', flat=True)
    generate_sales_forecasts_for_products(product_ids)
    generate_product_demand_forecasts_for_products(product_ids)

    similarity_count = update_content_based_similarity()
    generate_user_recommendations_after_order(order.user)


def generate_user_recommendations_after_order(user):
    settings = RecommendationSettings.objects.filter(user=user).first()
    algorithm = settings.active_algorithm if settings else 'collaborative'
    user_products = []
    orders = Order.objects.filter(user=user)
    for order in orders:
        products = order.orderproduct_set.all()
        user_products.extend([op.product_id for op in products])
    cart_items = CartItem.objects.filter(user=user)
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
            user=user,
            product_id=product_id,
            recommendation_type=algorithm,
            defaults={'score': score}
        )


def generate_association_rules_after_order(order):
    orders = Order.objects.prefetch_related('orderproduct_set__product').all()
    transactions = []
    for order in orders:
        product_ids = [str(item.product_id) for item in order.orderproduct_set.all()]
        if product_ids:
            transactions.append(product_ids)
    rules = calculate_association_rules(transactions)
    ProductAssociation.objects.all().delete()
    for rule in rules:
        try:
            ProductAssociation.objects.get_or_create(
                product_1_id=int(rule['product_1']),
                product_2_id=int(rule['product_2']),
                support=rule['support'],
                confidence=rule['confidence'],
                lift=rule['lift']
            )
        except Exception:
            continue


def calculate_association_rules(transactions, min_support=0.01, min_confidence=0.1):
    item_counts = defaultdict(int)
    total_transactions = len(transactions)
    for transaction in transactions:
        for item in transaction:
            item_counts[item] += 1
    item_support = {item: count / total_transactions for item, count in item_counts.items()}
    frequent_items = {item for item, support in item_support.items() if support >= min_support}
    association_rules = []
    for transaction in transactions:
        items = [item for item in transaction if item in frequent_items]
        for i, item1 in enumerate(items):
            for item2 in items[i + 1:]:
                count_1_2 = sum(1 for t in transactions if item1 in t and item2 in t)
                confidence_1_2 = count_1_2 / item_counts[item1]
                confidence_2_1 = count_1_2 / item_counts[item2]
                support = count_1_2 / total_transactions
                lift = support / (item_support[item1] * item_support[item2])
                if confidence_1_2 >= min_confidence:
                    association_rules.append({
                        'product_1': item1,
                        'product_2': item2,
                        'support': support,
                        'confidence': confidence_1_2,
                        'lift': lift
                    })
                if confidence_2_1 >= min_confidence:
                    association_rules.append({
                        'product_1': item2,
                        'product_2': item1,
                        'support': support,
                        'confidence': confidence_2_1,
                        'lift': lift
                    })
    return association_rules

def update_user_cb_recommendations(user):
    user_interactions = UserInteraction.objects.filter(user=user).values_list('product_id', flat=True)
    recommendations = defaultdict(float)
    for product_id in set(user_interactions):
        similarities = ProductSimilarity.objects.filter(
            product1_id=product_id,
            similarity_type='content_based'
        ).order_by('-similarity_score')[:5]
        for similarity in similarities:
            recommendations[similarity.product2_id] += float(similarity.similarity_score)
    for product_id, score in recommendations.items():
        UserProductRecommendation.objects.update_or_create(
            user=user,
            product_id=product_id,
            recommendation_type='content_based',
            defaults={'score': score}
        )

def update_content_based_similarity():
    products = Product.objects.prefetch_related('categories', 'tags').all()
    product_features = []
    product_ids = []
    
    print(Fore.GREEN + f"Starting similarity calculation for {len(products)} products")
    
    products_with_no_features = []
    for product in products:
        categories = list(product.categories.all())
        tags = list(product.tags.all())
        
        if len(categories) == 0 and len(tags) == 0:
            products_with_no_features.append(product.id)
    
    if products_with_no_features:
        print(Fore.YELLOW + f"WARNING: Following products have no categories or tags: {products_with_no_features}")
        print(Fore.GREEN + "Adding default features to ensure similarity calculation works")
    
    for product in products:
        feature_vector = [1] 
        
        for cat in product.categories.all():
            feature_vector.append(1)
        for tag in product.tags.all():
            feature_vector.append(1)
        
        product_features.append(feature_vector)
        product_ids.append(product.id)
    
    print(Fore.GREEN + f"Collected features for {len(product_features)} products")
    
    if len(product_features) < 2:
        print(Fore.GREEN + "Not enough products to calculate similarity")
        return
    
    max_length = max(len(f) for f in product_features)
    padded_features = []
    for feature in product_features:
        padded = feature + [0] * (max_length - len(feature))
        padded_features.append(padded)
        
    print(Fore.GREEN + f"Features padded to length {max_length}")
    
    feature_matrix = np.array(padded_features)
    similarity_matrix = cosine_similarity(feature_matrix)
    
    print(Fore.GREEN + f"Similarity matrix shape: {similarity_matrix.shape}")
    similarity_count = 0
    
    print(Fore.BLUE + f"Created/updated {similarity_count} similarity relationships")
    return similarity_count