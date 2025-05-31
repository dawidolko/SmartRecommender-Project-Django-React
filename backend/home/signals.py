from colorama import Fore
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from collections import defaultdict
from django.db.models import Avg
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
    if created and instance.user.role == "client":
        transaction.on_commit(lambda: run_all_analytics_after_order(instance))


@receiver(post_save, sender=OrderProduct)
def log_interaction_on_purchase(sender, instance, created, **kwargs):
    if created:
        UserInteraction.objects.create(
            user=instance.order.user,
            product=instance.product,
            interaction_type="purchase",
        )


@receiver(post_save, sender=CartItem)
def log_interaction_on_cart_add(sender, instance, created, **kwargs):
    if created:
        UserInteraction.objects.create(
            user=instance.user, product=instance.product, interaction_type="add_to_cart"
        )
        update_content_based_similarity()
        update_user_cb_recommendations(instance.user)


@receiver(post_save, sender=Opinion)
def handle_sentiment_analysis(sender, instance, created, **kwargs):
    if instance.content:
        sentiment_analyzer = CustomSentimentAnalysis()
        sentiment_score, sentiment_category = sentiment_analyzer.analyze_sentiment(
            instance.content
        )

        SentimentAnalysis.objects.update_or_create(
            opinion=instance,
            defaults={
                "product": instance.product,
                "sentiment_score": sentiment_score,
                "sentiment_category": sentiment_category,
            },
        )

        sentiment_data = sentiment_analyzer.analyze_product_sentiment(instance.product)

        ProductSentimentSummary.objects.update_or_create(
            product=instance.product, defaults=sentiment_data
        )


def run_all_analytics_after_order(order):
    generate_association_rules_after_order(order)
    generate_purchase_probabilities_for_user(order.user)
    generate_user_purchase_patterns_for_user(order.user)
    generate_risk_assessment_for_user(order.user)
    product_ids = OrderProduct.objects.filter(order=order).values_list(
        "product_id", flat=True
    )
    generate_sales_forecasts_for_products(product_ids)
    generate_product_demand_forecasts_for_products(product_ids)

    similarity_count = update_content_based_similarity()
    generate_user_recommendations_after_order(order.user)


def generate_user_recommendations_after_order(user):
    settings = RecommendationSettings.objects.filter(user=user).first()
    algorithm = settings.active_algorithm if settings else "collaborative"

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
            product1_id=product_id, similarity_type=algorithm
        ).order_by("-similarity_score")[:5]
        for similarity in similarities:
            recommendations[similarity.product2_id] += float(
                similarity.similarity_score
            )

    for product_id, score in recommendations.items():
        UserProductRecommendation.objects.update_or_create(
            user=user,
            product_id=product_id,
            recommendation_type=algorithm,
            defaults={"score": score},
        )


def generate_association_rules_after_order(order):
    orders = Order.objects.prefetch_related("orderproduct_set__product").all()
    transactions = []
    for order in orders:
        product_ids = [str(item.product_id) for item in order.orderproduct_set.all()]
        if product_ids:
            transactions.append(product_ids)

    association_engine = CustomAssociationRules(min_support=0.01, min_confidence=0.1)
    rules = association_engine.generate_association_rules(transactions)

    ProductAssociation.objects.all().delete()
    for rule in rules:
        try:
            ProductAssociation.objects.get_or_create(
                product_1_id=int(rule["product_1"]),
                product_2_id=int(rule["product_2"]),
                support=rule["support"],
                confidence=rule["confidence"],
                lift=rule["lift"],
            )
        except Exception:
            continue


def update_user_cb_recommendations(user):
    user_interactions = UserInteraction.objects.filter(user=user).values_list(
        "product_id", flat=True
    )
    recommendations = defaultdict(float)
    for product_id in set(user_interactions):
        similarities = ProductSimilarity.objects.filter(
            product1_id=product_id, similarity_type="content_based"
        ).order_by("-similarity_score")[:5]
        for similarity in similarities:
            recommendations[similarity.product2_id] += float(
                similarity.similarity_score
            )

    for product_id, score in recommendations.items():
        UserProductRecommendation.objects.update_or_create(
            user=user,
            product_id=product_id,
            recommendation_type="content_based",
            defaults={"score": score},
        )


def update_content_based_similarity():
    try:
        content_filter = CustomContentBasedFilter()
        similarity_count = content_filter.generate_similarities_for_all_products()
        print(
            Fore.GREEN
            + f"Generated {similarity_count} content-based similarities using custom implementation"
        )
        return similarity_count
    except Exception as e:
        print(Fore.RED + f"Error in custom content-based similarity: {e}")
        return 0
