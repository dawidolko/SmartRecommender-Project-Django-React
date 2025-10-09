"""
Fuzzy Logic Engine for Product Recommendations

Implementation of fuzzy logic system for modeling uncertainty in user preferences.
Based on:
- Zadeh, L. A. (1965). "Fuzzy sets". Information and Control.
- Mamdani, E. H. (1975). "Application of fuzzy algorithms for control of simple dynamic plant"

This module provides:
1. Fuzzy Membership Functions
2. Fuzzy User Profiling
3. Simplified Fuzzy Inference Engine
"""

from collections import defaultdict
from django.core.cache import cache


class FuzzyMembershipFunctions:
    """
    Fuzzy membership functions for product attributes.

    Implements triangular and trapezoidal membership functions
    for modeling uncertainty in product characteristics.
    """

    def __init__(self):
        # Price thresholds (in PLN)
        self.price_low = 100
        self.price_mid_low = 500
        self.price_mid = 700
        self.price_mid_high = 1200
        self.price_high = 2000

        # Rating thresholds (0-5 scale)
        self.rating_low = 2.5
        self.rating_mid = 3.5
        self.rating_high = 4.5

        # Popularity thresholds (view count)
        self.pop_low = 50
        self.pop_mid = 200
        self.pop_high = 1000

    # ===== PRICE MEMBERSHIP FUNCTIONS =====

    def mu_price_cheap(self, price):
        """
        Triangular membership function for 'cheap' price.

        μ(price) = {
            1.0                         if price <= 100
            (500 - price) / 400         if 100 < price < 500
            0.0                         if price >= 500
        }

        Args:
            price: Product price in PLN

        Returns:
            Membership degree [0.0, 1.0]
        """
        if price <= self.price_low:
            return 1.0
        elif price < self.price_mid_low:
            return (self.price_mid_low - price) / (self.price_mid_low - self.price_low)
        else:
            return 0.0

    def mu_price_medium(self, price):
        """
        Trapezoidal membership function for 'medium' price.

        μ(price) = {
            0.0                         if price < 300
            (price - 300) / 200         if 300 <= price < 500
            1.0                         if 500 <= price <= 1000
            (1500 - price) / 500        if 1000 < price < 1500
            0.0                         if price >= 1500
        }
        """
        if price < 300:
            return 0.0
        elif price < self.price_mid_low:
            return (price - 300) / (self.price_mid_low - 300)
        elif price <= self.price_mid_high:
            return 1.0
        elif price < 1500:
            return (1500 - price) / (1500 - self.price_mid_high)
        else:
            return 0.0

    def mu_price_expensive(self, price):
        """
        Triangular membership function for 'expensive' price.

        μ(price) = {
            0.0                         if price <= 1000
            (price - 1000) / 1000       if 1000 < price < 2000
            1.0                         if price >= 2000
        }
        """
        if price <= 1000:
            return 0.0
        elif price < self.price_high:
            return (price - 1000) / (self.price_high - 1000)
        else:
            return 1.0

    # ===== RATING/QUALITY MEMBERSHIP FUNCTIONS =====

    def mu_quality_low(self, rating):
        """
        Membership function for 'low quality' (poor ratings).

        μ(rating) = {
            1.0                         if rating <= 2.5
            (3.5 - rating) / 1.0        if 2.5 < rating < 3.5
            0.0                         if rating >= 3.5
        }
        """
        if rating <= self.rating_low:
            return 1.0
        elif rating < self.rating_mid:
            return (self.rating_mid - rating) / (self.rating_mid - self.rating_low)
        else:
            return 0.0

    def mu_quality_medium(self, rating):
        """
        Membership function for 'medium quality'.

        Triangular function centered at 3.5
        """
        if rating < self.rating_low:
            return 0.0
        elif rating < self.rating_mid:
            return (rating - self.rating_low) / (self.rating_mid - self.rating_low)
        elif rating <= self.rating_mid:
            return 1.0
        elif rating < self.rating_high:
            return (self.rating_high - rating) / (self.rating_high - self.rating_mid)
        else:
            return 0.0

    def mu_quality_high(self, rating):
        """
        Membership function for 'high quality' (excellent ratings).

        μ(rating) = {
            0.0                         if rating < 3.5
            (rating - 3.5) / 1.0        if 3.5 <= rating < 4.5
            1.0                         if rating >= 4.5
        }

        This models uncertainty: rating 4.0 is "somewhat" high quality (μ=0.5)
        """
        if rating < self.rating_mid:
            return 0.0
        elif rating < self.rating_high:
            return (rating - self.rating_mid) / (self.rating_high - self.rating_mid)
        else:
            return 1.0

    # ===== POPULARITY MEMBERSHIP FUNCTIONS =====

    def mu_popularity_low(self, view_count):
        """Low popularity (few views)"""
        if view_count <= self.pop_low:
            return 1.0
        elif view_count < self.pop_mid:
            return (self.pop_mid - view_count) / (self.pop_mid - self.pop_low)
        else:
            return 0.0

    def mu_popularity_medium(self, view_count):
        """Medium popularity"""
        if view_count < self.pop_low:
            return 0.0
        elif view_count < self.pop_mid:
            return (view_count - self.pop_low) / (self.pop_mid - self.pop_low)
        elif view_count <= self.pop_mid:
            return 1.0
        elif view_count < self.pop_high:
            return (self.pop_high - view_count) / (self.pop_high - self.pop_mid)
        else:
            return 0.0

    def mu_popularity_high(self, view_count):
        """High popularity (viral)"""
        if view_count < self.pop_mid:
            return 0.0
        elif view_count < self.pop_high:
            return (view_count - self.pop_mid) / (self.pop_high - self.pop_mid)
        else:
            return 1.0

    # ===== HELPER METHODS =====

    def get_price_fuzzy_set(self, price):
        """
        Returns all membership degrees for price.

        Returns:
            dict: {'cheap': μ, 'medium': μ, 'expensive': μ}
        """
        return {
            "cheap": self.mu_price_cheap(price),
            "medium": self.mu_price_medium(price),
            "expensive": self.mu_price_expensive(price),
        }

    def get_quality_fuzzy_set(self, rating):
        """Returns all membership degrees for quality"""
        return {
            "low": self.mu_quality_low(rating),
            "medium": self.mu_quality_medium(rating),
            "high": self.mu_quality_high(rating),
        }

    def get_popularity_fuzzy_set(self, view_count):
        """Returns all membership degrees for popularity"""
        return {
            "low": self.mu_popularity_low(view_count),
            "medium": self.mu_popularity_medium(view_count),
            "high": self.mu_popularity_high(view_count),
        }


class FuzzyUserProfile:
    """
    Fuzzy user profile builder - models uncertainty in user preferences.

    Builds fuzzy sets representing user's category interests and shopping behavior
    from purchase history (authenticated users) or session data (guests).
    """

    def __init__(self, user=None, session_data=None):
        """
        Args:
            user: Django User object (for authenticated users)
            session_data: dict with session info (for guests)
        """
        self.user = user
        self.session_data = session_data or {}
        self.category_interests = {}
        self.price_sensitivity = 0.5  # Default: medium sensitivity

        # Build profile
        if user and user.is_authenticated:
            self._build_from_user_history()
        elif session_data:
            self._build_from_session()
        else:
            self._build_default_profile()

    def _build_from_user_history(self):
        """
        Build fuzzy profile from authenticated user's purchase history.

        Uses frequency of category purchases to determine fuzzy membership degrees.
        """
        from home.models import Order

        # Get user's orders
        orders = Order.objects.filter(user=self.user).prefetch_related(
            "orderproduct_set__product__categories"
        )

        if not orders.exists():
            self._build_default_profile()
            return

        # Count category purchases
        category_counts = defaultdict(int)
        total_items = 0
        total_spending = 0

        for order in orders:
            for order_product in order.orderproduct_set.all():
                product = order_product.product
                quantity = order_product.quantity

                # Count categories
                for category in product.categories.all():
                    category_counts[category.name] += quantity

                total_items += quantity
                total_spending += float(product.price) * quantity

        # Normalize to [0, 1] - fuzzy membership degrees
        if total_items > 0:
            self.category_interests = {
                cat: count / total_items for cat, count in category_counts.items()
            }

        # Calculate price sensitivity
        if orders.count() > 0:
            avg_price = total_spending / total_items if total_items > 0 else 500
            # Low avg price → high sensitivity (1.0)
            # High avg price → low sensitivity (0.0)
            if avg_price < 300:
                self.price_sensitivity = 0.9
            elif avg_price < 700:
                self.price_sensitivity = 0.6
            elif avg_price < 1500:
                self.price_sensitivity = 0.4
            else:
                self.price_sensitivity = 0.2

    def _build_from_session(self):
        """
        Build fuzzy profile from guest's session data (viewed products, time spent).

        Uses viewing time to infer fuzzy interest degrees.
        """
        viewed = self.session_data.get("viewed_products", [])

        if not viewed:
            self._build_default_profile()
            return

        category_time = defaultdict(float)
        total_time = 0

        for view in viewed:
            category = view.get("category", "Unknown")
            time_spent = view.get("time_spent", 0)  # seconds

            # Fuzzy interest from time: more time = more interest
            interest_degree = self._fuzzy_interest_from_time(time_spent)

            # Accumulate with T-conorma (max)
            category_time[category] = max(category_time[category], interest_degree)
            total_time += time_spent

        self.category_interests = dict(category_time)

        # Infer price sensitivity from viewed products' prices
        avg_viewed_price = self.session_data.get("avg_viewed_price", 500)
        self.price_sensitivity = 0.8 if avg_viewed_price < 500 else 0.5

    def _build_default_profile(self):
        """Default profile for users without history"""
        # Popular categories with moderate interest
        self.category_interests = {"Electronics": 0.5, "Home": 0.4, "Gaming": 0.3}
        self.price_sensitivity = 0.6

    def _fuzzy_interest_from_time(self, seconds):
        """
        Fuzzy membership function: viewing time → interest degree

        μ_interest(time) = {
            0.1                         if time < 5s
            0.3 + (time-5)/10 * 0.3     if 5s <= time < 15s
            0.6 + (time-15)/30 * 0.3    if 15s <= time < 45s
            0.9                         if time >= 45s
        }

        Interpretation:
        - < 5s: barely interested (0.1)
        - 15s: moderately interested (0.5)
        - 45s+: highly interested (0.9)
        """
        if seconds < 5:
            return 0.1
        elif seconds < 15:
            return 0.3 + (seconds - 5) / 10 * 0.3  # 0.3 to 0.6
        elif seconds < 45:
            return 0.6 + (seconds - 15) / 30 * 0.3  # 0.6 to 0.9
        else:
            return 0.9

    def fuzzy_category_match(self, product_category):
        """
        Fuzzy matching between user's interests and product category.

        Uses fuzzy category similarity matrix and T-norm/T-conorm aggregation.

        Args:
            product_category: str, category name

        Returns:
            Membership degree [0.0, 1.0] representing how well the category matches
        """
        # Fuzzy similarity matrix - models relationships between categories
        # E.g., Gaming is "somewhat" related to Electronics (0.7)
        category_similarity = {
            "Gaming": {
                "Gaming": 1.0,
                "Electronics": 0.7,
                "Computers": 0.8,
                "Tech": 0.6,
                "Accessories": 0.5,
            },
            "Electronics": {
                "Electronics": 1.0,
                "Gaming": 0.7,
                "Computers": 0.8,
                "Photography": 0.6,
                "Tech": 0.9,
            },
            "Photography": {
                "Photography": 1.0,
                "Cameras": 0.9,
                "Electronics": 0.6,
                "Accessories": 0.7,
            },
            "Computers": {
                "Computers": 1.0,
                "Electronics": 0.8,
                "Gaming": 0.8,
                "Tech": 0.9,
                "Office": 0.6,
            },
            "Home": {"Home": 1.0, "Kitchen": 0.8, "Garden": 0.6, "Furniture": 0.7},
        }

        max_match = 0.0

        for user_cat, user_interest in self.category_interests.items():
            # Get similarity between user's category and product's category
            similarity = category_similarity.get(user_cat, {}).get(
                product_category, 0.0
            )

            # T-norm (min) for AND: user has interest AND categories are similar
            match = min(user_interest, similarity)

            # T-conorm (max) for OR: accumulate best match
            max_match = max(max_match, match)

        return max_match

    def get_profile_summary(self):
        """Returns human-readable profile summary"""
        sorted_interests = sorted(
            self.category_interests.items(), key=lambda x: x[1], reverse=True
        )

        return {
            "top_interests": sorted_interests[:5],
            "price_sensitivity": self.price_sensitivity,
            "profile_type": "authenticated" if self.user else "session-based",
        }


class SimpleFuzzyInference:
    """
    Simplified Fuzzy Inference Engine (OPTION 4-lite)

    Implements Mamdani-style inference with simplified defuzzification.
    Based on:
    - Mamdani, E. H. (1975). "Application of fuzzy algorithms for control of simple dynamic plant"
    - Zadeh, L. A. (1973). "Outline of a new approach to the analysis of complex systems"

    Uses:
    - T-norm (min) for AND in rule antecedents
    - T-conorm (max) for OR aggregation
    - Weighted average for simplified defuzzification
    """

    def __init__(self, membership_functions, user_profile):
        """
        Args:
            membership_functions: FuzzyMembershipFunctions instance
            user_profile: FuzzyUserProfile instance
        """
        self.mf = membership_functions
        self.user_profile = user_profile

        # Define fuzzy rules (Mamdani-style IF-THEN rules)
        self.rules = self._define_rules()

    def _define_rules(self):
        """
        Define simplified fuzzy rule base.

        Rules follow format:
        IF (antecedent conditions) THEN (recommendation degree)

        Returns:
            list of rule functions
        """
        rules = [
            # Rule 1: High quality + reasonable price → high recommendation
            {
                "name": "R1: High Quality Bargain",
                "eval": lambda p, cat_match: min(
                    self.mf.mu_quality_high(p.get("rating", 0)),
                    max(
                        self.mf.mu_price_cheap(p.get("price", 0)),
                        self.mf.mu_price_medium(p.get("price", 0)),
                    ),
                ),
                "weight": 0.9,
            },
            # Rule 2: Category match + high popularity → medium recommendation
            {
                "name": "R2: Popular in Category",
                "eval": lambda p, cat_match: min(
                    cat_match, self.mf.mu_popularity_high(p.get("view_count", 0))
                ),
                "weight": 0.7,
            },
            # Rule 3: Price sensitive user + cheap product → boost recommendation
            {
                "name": "R3: Price Sensitive Match",
                "eval": lambda p, cat_match: (
                    min(
                        self.user_profile.price_sensitivity,
                        self.mf.mu_price_cheap(p.get("price", 0)),
                    )
                    if self.user_profile.price_sensitivity > 0.6
                    else 0.0
                ),
                "weight": 0.6,
            },
            # Rule 4: High category match + good quality → high recommendation
            {
                "name": "R4: Category Quality Match",
                "eval": lambda p, cat_match: min(
                    cat_match,
                    max(
                        self.mf.mu_quality_medium(p.get("rating", 0)),
                        self.mf.mu_quality_high(p.get("rating", 0)),
                    ),
                ),
                "weight": 0.85,
            },
            # Rule 5: Low price insensitive user + expensive + high quality → boost
            {
                "name": "R5: Premium Match",
                "eval": lambda p, cat_match: (
                    min(
                        1.0 - self.user_profile.price_sensitivity,  # Low sensitivity
                        self.mf.mu_price_expensive(p.get("price", 0)),
                        self.mf.mu_quality_high(p.get("rating", 0)),
                    )
                    if self.user_profile.price_sensitivity < 0.4
                    else 0.0
                ),
                "weight": 0.8,
            },
        ]

        return rules

    def evaluate_product(self, product_data, category_match=0.0):
        """
        Evaluate a product using fuzzy inference.

        Args:
            product_data: dict with keys: 'price', 'rating', 'view_count', etc.
            category_match: fuzzy degree of category match [0.0, 1.0]

        Returns:
            dict: {
                'fuzzy_score': final recommendation degree [0.0, 1.0],
                'rule_activations': dict of rule activations for explainability
            }
        """
        rule_activations = {}
        weighted_sum = 0.0
        weight_sum = 0.0

        for rule in self.rules:
            # Evaluate rule antecedent (T-norm applied inside rule eval)
            activation = rule["eval"](product_data, category_match)

            rule_activations[rule["name"]] = round(activation, 3)

            # Accumulate for defuzzification (weighted average)
            weighted_sum += activation * rule["weight"]
            weight_sum += rule["weight"]

        # Simplified defuzzification: weighted average
        fuzzy_score = weighted_sum / weight_sum if weight_sum > 0 else 0.0

        return {
            "fuzzy_score": round(fuzzy_score, 3),
            "rule_activations": rule_activations,
            "category_match": round(category_match, 3),
        }

    def get_rule_explanations(self):
        """
        Returns human-readable explanations of all fuzzy rules.

        Useful for debugging and thesis documentation.
        """
        explanations = []

        explanations.append(
            {
                "rule": "R1: High Quality Bargain",
                "condition": "IF quality is HIGH AND (price is CHEAP OR MEDIUM)",
                "consequence": "THEN recommendation degree is HIGH (weight: 0.9)",
                "interpretation": "Products with excellent ratings at reasonable prices get high recommendations",
            }
        )

        explanations.append(
            {
                "rule": "R2: Popular in Category",
                "condition": "IF category matches user interest AND product is HIGHLY POPULAR",
                "consequence": "THEN recommendation degree is MEDIUM-HIGH (weight: 0.7)",
                "interpretation": "Trending products in categories the user likes",
            }
        )

        explanations.append(
            {
                "rule": "R3: Price Sensitive Match",
                "condition": "IF user is PRICE SENSITIVE AND product is CHEAP",
                "consequence": "THEN boost recommendation (weight: 0.6)",
                "interpretation": "Budget-conscious users get cheap product recommendations boosted",
            }
        )

        explanations.append(
            {
                "rule": "R4: Category Quality Match",
                "condition": "IF category matches strongly AND quality is MEDIUM-HIGH",
                "consequence": "THEN recommendation degree is HIGH (weight: 0.85)",
                "interpretation": "Good quality products in preferred categories",
            }
        )

        explanations.append(
            {
                "rule": "R5: Premium Match",
                "condition": "IF user is NOT price sensitive AND product is EXPENSIVE AND quality is HIGH",
                "consequence": "THEN boost recommendation (weight: 0.8)",
                "interpretation": "Premium users get expensive high-quality products boosted",
            }
        )

        return explanations
