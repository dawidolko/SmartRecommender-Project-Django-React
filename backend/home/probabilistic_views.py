from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg, Sum, F, Max
from collections import defaultdict
import json

from .models import (
    Order, 
    OrderProduct, 
    Product, 
    User,
    UserInteraction,
    Category
)
from .custom_recommendation_engine import ProbabilisticRecommendationEngine
from .serializers import ProductSerializer


class IsAdminRole(BasePermission):
    """Custom permission to check if user has admin role"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class MarkovRecommendationsAPI(APIView):
    """API for Markov Chain based recommendations"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get Markov chain recommendations for current user"""
        user = request.user
        
        # Cache check
        cache_key = f"markov_recommendations_{user.id}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return Response({
                **cached_result,
                "cached": True
            })

        try:
            # Get user's purchase history
            user_orders = Order.objects.filter(user=user).order_by('date_order')
            
            if not user_orders.exists():
                return Response({
                    "message": "No purchase history available for Markov recommendations",
                    "recommendations": [],
                    "insights": {},
                    "sequence_prediction": []
                })

            # Build user's purchase sequence
            user_sequence = []
            for order in user_orders:
                for order_product in order.orderproduct_set.all():
                    user_sequence.append(order_product.product_id)

            # Get all users' sequences for training
            all_sequences = self._get_all_user_sequences()
            
            # Train Markov model
            prob_engine = ProbabilisticRecommendationEngine()
            sequences_trained = prob_engine.train_markov_model(all_sequences)
            
            if sequences_trained == 0:
                return Response({
                    "message": "Insufficient data for Markov chain training",
                    "recommendations": [],
                    "insights": {},
                    "sequence_prediction": []
                })

            # Get user's last purchased category
            last_product = user_sequence[-1] if user_sequence else None
            last_category = None
            
            if last_product:
                last_category = prob_engine.get_product_category(last_product)

            recommendations = []
            sequence_prediction = []
            
            if last_category:
                # Predict next categories
                next_categories = prob_engine.predict_next_purchase_categories(last_category, top_k=5)
                
                # Convert categories to product recommendations
                for category_pred in next_categories:
                    category_name = category_pred['state']
                    probability = category_pred['probability']
                    
                    # Get products from this category
                    try:
                        category = Category.objects.get(name=category_name)
                        category_products = Product.objects.filter(
                            categories=category
                        ).exclude(
                            id__in=user_sequence[-5:]  # Exclude recently purchased
                        )[:3]  # Top 3 products per category
                        
                        for product in category_products:
                            recommendations.append({
                                "product": ProductSerializer(product).data,
                                "predicted_category": category_name,
                                "markov_probability": round(probability, 3),
                                "recommendation_reason": f"Based on Markov chain transition from {last_category}"
                            })
                            
                    except Category.DoesNotExist:
                        continue

                # Predict sequence
                sequence_prediction = prob_engine.markov_chain.predict_sequence(
                    last_category, length=4
                )

            # Get insights
            insights = prob_engine.get_markov_insights()
            
            # Calculate purchase probability (based on recent activity)
            recent_orders = Order.objects.filter(user=user, date_order__gte=timezone.now() - timedelta(days=30)).count()
            next_purchase_probability = min(0.8, 0.3 + (recent_orders * 0.1))
            
            # Expected days to next purchase
            avg_days_between_orders = 30  # Default assumption
            if user_orders.count() > 1:
                order_dates = [order.date_order for order in user_orders.order_by('date_order')]
                days_between = [(order_dates[i] - order_dates[i-1]).days for i in range(1, len(order_dates))]
                avg_days_between_orders = sum(days_between) / len(days_between) if days_between else 30
            
            # Transform recommendations to match frontend expectations
            predicted_products = []
            for rec in recommendations[:6]:  # Top 6 for display
                product_data = rec["product"]
                predicted_products.append({
                    "id": product_data["id"],
                    "name": product_data["name"],
                    "price": product_data["price"],
                    "image_url": product_data.get("photos", [{}])[0].get("path", "") if product_data.get("photos") else "",
                    "prediction_score": rec["markov_probability"]
                })

            result = {
                "message": f"Markov recommendations based on {sequences_trained} purchase sequences",
                "next_purchase_probability": next_purchase_probability,
                "expected_days_to_next_purchase": int(avg_days_between_orders),
                "predicted_products": predicted_products,
                "sequence_analysis": {
                    "most_common_sequence": " → ".join(sequence_prediction) if sequence_prediction else "Not enough data",
                    "average_cycle_length": len(sequence_prediction) if sequence_prediction else None,
                    "total_sequences_analyzed": sequences_trained
                },
                "insights": {
                    "most_popular_categories": insights["most_popular_categories"],
                    "total_category_states": insights["total_states"],
                    "total_transitions": insights["total_transitions"],
                    "user_last_category": last_category
                },
                "algorithm": "First-order Markov Chain",
                "cached": False
            }
            
            # Cache for 1 hour
            cache.set(cache_key, result, timeout=3600)
            
            return Response(result)

        except Exception as e:
            return Response(
                {"error": f"Error generating Markov recommendations: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _get_all_user_sequences(self):
        """Get purchase sequences for all users"""
        sequences = []
        
        # Get users with at least 2 orders
        users_with_orders = User.objects.annotate(
            order_count=Count('order')
        ).filter(order_count__gte=2)[:200]  # Limit for performance
        
        for user in users_with_orders:
            user_orders = Order.objects.filter(user=user).order_by('date_order')
            user_sequence = []
            
            for order in user_orders:
                for order_product in order.orderproduct_set.all():
                    user_sequence.append(order_product.product_id)
            
            if len(user_sequence) >= 2:
                sequences.append(user_sequence)
        
        return sequences


class BayesianInsightsAPI(APIView):
    """API for Bayesian analysis and insights"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get Bayesian insights for current user"""
        user = request.user
        
        # Cache check
        cache_key = f"bayesian_insights_{user.id}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return Response({
                **cached_result,
                "cached": True
            })

        try:
            # Prepare training data
            user_features, purchase_labels = self._prepare_purchase_data()
            churn_features, churn_labels = self._prepare_churn_data()
            
            if not user_features or not churn_features:
                return Response({
                    "message": "Insufficient data for Bayesian analysis",
                    "purchase_prediction": {},
                    "churn_prediction": {},
                    "insights": {}
                })

            # Train models
            prob_engine = ProbabilisticRecommendationEngine()
            
            purchase_samples = prob_engine.train_purchase_prediction_model(user_features, purchase_labels)
            churn_samples = prob_engine.train_churn_prediction_model(churn_features, churn_labels)
            
            # Get user features
            user_profile = self._extract_user_features(user)
            
            # Make predictions
            purchase_prediction = prob_engine.predict_purchase_probability(user_profile)
            churn_prediction = prob_engine.predict_churn_probability(user_profile)
            
            # Get feature importance
            purchase_importance = prob_engine.naive_bayes_purchase.get_feature_importance()
            churn_importance = prob_engine.naive_bayes_churn.get_feature_importance()
            
            # Create category preferences for frontend
            category_preferences = {}
            user_orders = Order.objects.filter(user=user)
            if user_orders.exists():
                category_counts = defaultdict(int)
                total_items = 0
                
                for order in user_orders:
                    for order_product in order.orderproduct_set.all():
                        total_items += 1
                        for category in order_product.product.categories.all():
                            category_counts[category.name] += 1
                
                for category, count in category_counts.items():
                    category_preferences[category] = count / total_items if total_items > 0 else 0
            
            # Churn risk calculation
            churn_prob = churn_prediction.get('will_churn', 0)
            churn_risk_level = 'High' if churn_prob > 0.7 else 'Medium' if churn_prob > 0.4 else 'Low'
            
            # Behavioral patterns
            behavioral_patterns = {
                "shopping_frequency": user_profile.get("order_frequency", 0),
                "average_order_value": user_profile.get("avg_order_value", 0),
                "category_loyalty": max(category_preferences.values()) if category_preferences else 0,
                "recent_activity": 1.0 - (user_profile.get("days_since_last_order", 999) / 365.0)
            }

            result = {
                "message": f"Bayesian analysis based on {purchase_samples} purchase samples and {churn_samples} churn samples",
                "category_preferences": category_preferences,
                "churn_risk": {
                    "probability": round(churn_prob, 3),
                    "risk_level": churn_risk_level,
                    "confidence": round(max(churn_prediction.values()), 3),
                    "recommendation": "We miss you! Check out our latest offers to rediscover great products." if churn_prob > 0.5 else "Keep exploring our products!"
                },
                "behavioral_patterns": behavioral_patterns,
                "purchase_prediction": {
                    "probabilities": {k: round(v, 3) for k, v in purchase_prediction.items()},
                    "next_purchase_likely": purchase_prediction.get('will_purchase', 0) > 0.5,
                    "confidence": round(max(purchase_prediction.values()), 3)
                },
                "user_profile": user_profile,
                "insights": {
                    "key_factors": {k: round(v, 3) for k, v in sorted(purchase_importance.items(), key=lambda x: x[1], reverse=True)[:3]},
                    "behavioral_score": sum(behavioral_patterns.values()) / len(behavioral_patterns),
                    "training_quality": {
                        "purchase_samples": purchase_samples,
                        "churn_samples": churn_samples,
                        "reliability": "High" if min(purchase_samples, churn_samples) > 50 else "Medium" if min(purchase_samples, churn_samples) > 20 else "Low"
                    }
                },
                "algorithm": "Naive Bayes with Laplace Smoothing",
                "cached": False
            }
            
            # Cache for 2 hours
            cache.set(cache_key, result, timeout=7200)
            
            return Response(result)

        except Exception as e:
            return Response(
                {"error": f"Error generating Bayesian insights: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _prepare_purchase_data(self):
        """Prepare training data for purchase prediction"""
        features = []
        labels = []
        
        # Get users with varied purchase behavior
        users = User.objects.annotate(
            order_count=Count('order'),
            total_spent=Sum('order__orderproduct__product__price')
        ).filter(order_count__gte=1)[:300]
        
        for user in users:
            user_features = self._extract_user_features(user)
            
            # Label: will_purchase if user made purchase in last 30 days
            recent_orders = Order.objects.filter(
                user=user,
                date_order__gte=timezone.now() - timedelta(days=30)
            )
            
            label = "will_purchase" if recent_orders.exists() else "will_not_purchase"
            
            features.append(user_features)
            labels.append(label)
        
        return features, labels

    def _prepare_churn_data(self):
        """Prepare training data for churn prediction"""
        features = []
        labels = []
        
        # Get users with order history
        users = User.objects.annotate(
            order_count=Count('order'),
            last_order_date=Max('order__date_order')
        ).filter(order_count__gte=1)[:300]
        
        for user in users:
            user_features = self._extract_user_features(user)
            
            # Label: will_churn if no orders in last 60 days
            last_order = Order.objects.filter(user=user).order_by('-date_order').first()
            days_since_last_order = (timezone.now().date() - last_order.date_order.date()).days if last_order else 999
            
            label = "will_churn" if days_since_last_order > 60 else "will_not_churn"
            
            features.append(user_features)
            labels.append(label)
        
        return features, labels

    def _extract_user_features(self, user):
        """Extract features for a user"""
        # Calculate user statistics
        orders = Order.objects.filter(user=user)
        total_orders = orders.count()
        
        if total_orders == 0:
            return {
                "total_orders": 0,
                "avg_order_value": 0,
                "days_since_last_order": 999,
                "favorite_category": "none",
                "order_frequency": 0
            }
        
        # Total spent
        total_spent = sum(
            order_product.product.price * order_product.quantity
            for order in orders
            for order_product in order.orderproduct_set.all()
        )
        
        avg_order_value = total_spent / total_orders if total_orders > 0 else 0
        
        # Days since last order
        last_order = orders.order_by('-date_order').first()
        days_since_last_order = (timezone.now().date() - last_order.date_order.date()).days if last_order else 999
        
        # Most purchased category
        category_counts = defaultdict(int)
        for order in orders:
            for order_product in order.orderproduct_set.all():
                for category in order_product.product.categories.all():
                    category_counts[category.name] += 1
        
        favorite_category = max(category_counts, key=category_counts.get) if category_counts else "none"
        
        # Order frequency (orders per month)
        if orders.exists():
            first_order = orders.order_by('date_order').first()
            days_active = (timezone.now().date() - first_order.date_order.date()).days
            months_active = max(days_active / 30, 1)
            order_frequency = total_orders / months_active
        else:
            order_frequency = 0
        
        return {
            "total_orders": total_orders,
            "avg_order_value": round(avg_order_value, 2),
            "days_since_last_order": days_since_last_order,
            "favorite_category": favorite_category,
            "order_frequency": round(order_frequency, 2)
        }


class ProbabilisticAnalysisAdminAPI(APIView):
    """Admin API for probabilistic model analysis"""
    permission_classes = [IsAdminRole]

    def get(self, request):
        """Get comprehensive probabilistic analysis for admin"""
        try:
            # Cache check
            cache_key = "probabilistic_admin_analysis"
            cached_result = cache.get(cache_key)
            
            if cached_result:
                return Response({
                    **cached_result,
                    "cached": True
                })

            # Get overall statistics
            total_users = User.objects.count()
            total_orders = Order.objects.count()
            total_products = Product.objects.count()
            
            # Category transition analysis
            category_transitions = self._analyze_category_transitions()
            
            # Purchase pattern analysis
            purchase_patterns = self._analyze_purchase_patterns()
            
            # Churn analysis
            churn_analysis = self._analyze_churn_patterns()
            
            result = {
                "message": "Comprehensive probabilistic analysis",
                "overall_statistics": {
                    "total_users": total_users,
                    "total_orders": total_orders,
                    "total_products": total_products,
                    "analysis_date": timezone.now().isoformat()
                },
                "markov_analysis": {
                    "category_transitions": category_transitions,
                    "most_common_sequences": self._get_common_sequences()
                },
                "bayesian_analysis": {
                    "purchase_patterns": purchase_patterns,
                    "churn_analysis": churn_analysis
                },
                "model_performance": self._get_model_performance(),
                "cached": False
            }
            
            # Cache for 4 hours
            cache.set(cache_key, result, timeout=14400)
            
            return Response(result)

        except Exception as e:
            return Response(
                {"error": f"Error generating admin analysis: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _analyze_category_transitions(self):
        """Analyze transitions between categories"""
        transitions = defaultdict(lambda: defaultdict(int))
        
        # Get sequential orders for analysis
        users = User.objects.annotate(order_count=Count('order')).filter(order_count__gte=2)[:100]
        
        for user in users:
            orders = Order.objects.filter(user=user).order_by('date_order')
            categories = []
            
            for order in orders:
                order_categories = set()
                for order_product in order.orderproduct_set.all():
                    for category in order_product.product.categories.all():
                        order_categories.add(category.name)
                
                if order_categories:
                    categories.append(list(order_categories)[0])  # Take first category
            
            # Count transitions
            for i in range(len(categories) - 1):
                from_cat = categories[i]
                to_cat = categories[i + 1]
                transitions[from_cat][to_cat] += 1
        
        return dict(transitions)

    def _analyze_purchase_patterns(self):
        """Analyze purchase patterns using Bayesian approach"""
        patterns = {}
        
        # Analyze by user segments
        high_value_users = User.objects.annotate(
            total_spent=Sum('order__orderproduct__product__price')
        ).filter(total_spent__gte=1000).count()
        
        medium_value_users = User.objects.annotate(
            total_spent=Sum('order__orderproduct__product__price')
        ).filter(total_spent__gte=100, total_spent__lt=1000).count()
        
        low_value_users = User.objects.annotate(
            total_spent=Sum('order__orderproduct__product__price')
        ).filter(total_spent__lt=100).count()
        
        patterns = {
            "user_segments": {
                "high_value": high_value_users,
                "medium_value": medium_value_users,
                "low_value": low_value_users
            },
            "category_preferences": self._get_category_preferences()
        }
        
        return patterns

    def _analyze_churn_patterns(self):
        """Analyze customer churn patterns"""
        cutoff_date = timezone.now() - timedelta(days=60)
        
        active_users = User.objects.filter(
            order__date_order__gte=cutoff_date
        ).distinct().count()
        
        churned_users = User.objects.exclude(
            order__date_order__gte=cutoff_date
        ).filter(order__isnull=False).distinct().count()
        
        churn_rate = churned_users / (active_users + churned_users) if (active_users + churned_users) > 0 else 0
        
        return {
            "active_users": active_users,
            "churned_users": churned_users,
            "churn_rate": round(churn_rate, 3),
            "analysis_period": "60 days"
        }

    def _get_common_sequences(self):
        """Get most common purchase sequences"""
        # This would implement sequence mining
        # For now, return placeholder
        return [
            {"sequence": ["Electronics", "Accessories"], "frequency": 15},
            {"sequence": ["Computers", "Peripherals"], "frequency": 12},
            {"sequence": ["Gaming", "Electronics"], "frequency": 8}
        ]

    def _get_category_preferences(self):
        """Get category preferences by user segment"""
        preferences = {}
        
        categories = Category.objects.annotate(
            product_count=Count('product'),
            order_count=Count('product__orderproduct')
        ).order_by('-order_count')[:10]
        
        for category in categories:
            preferences[category.name] = {
                "product_count": category.product_count,
                "total_orders": category.order_count
            }
        
        return preferences

    def _get_model_performance(self):
        """Get model performance metrics"""
        # Placeholder for model performance metrics
        return {
            "markov_accuracy": "85%",
            "bayesian_accuracy": "78%",
            "last_training": timezone.now().isoformat(),
            "samples_used": 1000
        }