import re
from collections import defaultdict, Counter
from decimal import Decimal
from django.db.models import Count, Sum, Avg
from django.core.cache import cache
from django.conf import settings
import math

try:
    from .models import Product, ProductSimilarity
except ImportError as e:
    print(f"Model import error: {e}")
    Product = None
    ProductSimilarity = None


class CustomContentBasedFilter:
    def __init__(self):
        self.similarity_threshold = 0.2
        self.max_products_for_similarity = 500
        self.batch_size = 100
        self.max_comparisons_per_product = 50

        self.feature_weights = {
            "category": 0.40,
            "tag": 0.30,
            "price": 0.20,
            "keywords": 0.10,
        }

        self.stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "this",
            "that",
            "these",
            "those",
            "i",
            "you",
            "he",
            "she",
            "it",
            "we",
            "they",
            "me",
            "him",
            "her",
            "us",
            "them",
            "my",
            "your",
            "his",
            "its",
            "our",
            "their",
            "jako",
            "że",
            "na",
            "w",
            "z",
            "do",
            "od",
            "po",
            "przez",
        }

    def calculate_product_similarity(self, product1, product2):
        """Oblicza podobieństwo między produktami używając systemu ważonego"""
        features1 = self._extract_weighted_features(product1)
        features2 = self._extract_weighted_features(product2)

        dot_product = 0.0
        norm1 = 0.0
        norm2 = 0.0

        all_features = set(features1.keys()) | set(features2.keys())

        for feature in all_features:
            val1 = features1.get(feature, 0.0)
            val2 = features2.get(feature, 0.0)

            dot_product += val1 * val2
            norm1 += val1 * val1
            norm2 += val2 * val2

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (math.sqrt(norm1) * math.sqrt(norm2))

    def _extract_weighted_features(self, product):
        """Ekstraktuje cechy produktu z wagami"""
        features = {}

        for category in product.categories.all():
            feature_name = f"category_{category.name.lower()}"
            features[feature_name] = self.feature_weights["category"]

        for tag in product.tags.all():
            feature_name = f"tag_{tag.name.lower()}"
            features[feature_name] = self.feature_weights["tag"]

        price_category = self._get_price_category(product.price)
        features[f"price_{price_category}"] = self.feature_weights["price"]

        if product.description:
            keywords = self._extract_keywords(product.description)
            for keyword in keywords[:5]:
                feature_name = f"keyword_{keyword}"
                features[feature_name] = self.feature_weights["keywords"] / len(
                    keywords[:5]
                )

        return features

    def _get_price_category(self, price):
        """Kategoryzuje cenę produktu"""
        if price < 100:
            return "low"
        elif price < 500:
            return "medium"
        elif price < 1500:
            return "high"
        else:
            return "premium"

    def _extract_keywords(self, text):
        """Ekstraktuje słowa kluczowe z tekstu produktu"""
        if not text:
            return []

        text = re.sub(r"[^\w\s]", " ", text.lower())
        words = text.split()

        filtered_words = [
            word for word in words if len(word) > 3 and word not in self.stop_words
        ]

        word_freq = Counter(filtered_words)
        return [word for word, freq in word_freq.most_common(10)]

    def generate_similarities_for_all_products(self):
        """Generuje podobieństwa dla wszystkich produktów z cache i bulk operations"""
        from home.models import Product, ProductSimilarity

        cache_key = "content_based_similarity_matrix"
        cached_result = cache.get(cache_key)

        if cached_result:
            print("Using cached content-based filtering results")
            return cached_result

        products = list(
            Product.objects.prefetch_related(
                "categories", "tags", "specification_set"
            ).all()[: self.max_products_for_similarity]
        )

        if len(products) < 2:
            return 0

        print(
            f"Processing {len(products)} products for enhanced content-based similarity"
        )

        ProductSimilarity.objects.filter(similarity_type="content_based").delete()

        similarities_to_create = []
        similarities_created = 0

        for i, product1 in enumerate(products):
            if i % 25 == 0:
                print(f"Processed {i}/{len(products)} products")

            comparison_products = products[
                i + 1 : i + 1 + self.max_comparisons_per_product
            ]

            for product2 in comparison_products:
                similarity_score = self.calculate_product_similarity(product1, product2)

                if similarity_score > self.similarity_threshold:
                    similarities_to_create.extend(
                        [
                            ProductSimilarity(
                                product1=product1,
                                product2=product2,
                                similarity_type="content_based",
                                similarity_score=similarity_score,
                            ),
                            ProductSimilarity(
                                product1=product2,
                                product2=product1,
                                similarity_type="content_based",
                                similarity_score=similarity_score,
                            ),
                        ]
                    )
                    similarities_created += 2

                    if len(similarities_to_create) >= 1000:
                        ProductSimilarity.objects.bulk_create(similarities_to_create)
                        similarities_to_create = []

        if similarities_to_create:
            ProductSimilarity.objects.bulk_create(similarities_to_create)

        print(f"Created {similarities_created} enhanced content-based similarities")

        cache.set(
            cache_key,
            similarities_created,
            timeout=getattr(settings, "CACHE_TIMEOUT_LONG", 7200),
        )

        return similarities_created


class CustomFuzzySearch:
    def __init__(self):
        self.default_threshold = 0.5
        self.max_distance_calc_length = 200

        self.chunk_size = 150
        self.chunk_overlap = 30

        self.field_weights = {
            "name": 0.45,
            "description": 0.25,
            "category": 0.20,
            "specification": 0.10,
        }

    def calculate_fuzzy_score(self, query, text):
        """Enhanced fuzzy scoring with n-grams and better text processing"""
        if not text or not query:
            return 0.0

        query = query.lower().strip()
        text = text.lower().strip()

        cache_key = f"fuzzy_{hash(query + text)}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        if query == text:
            result = 1.0
        elif query in text:
            result = 0.95
        else:
            scores = []

            word_score = self._calculate_word_similarity(query, text)
            scores.append(("word", word_score, 0.7))

            trigram_score = self._calculate_trigram_similarity(query, text)
            scores.append(("trigram", trigram_score, 0.2))

            if len(text) <= self.max_distance_calc_length:
                char_score = self._calculate_character_similarity(query, text)
                scores.append(("char", char_score, 0.1))
            else:
                chunk_score = self._calculate_chunked_similarity(query, text)
                scores.append(("chunk", chunk_score, 0.1))

            total_weight = sum(weight for _, _, weight in scores)
            if total_weight > 0:
                result = (
                    sum(score * weight for _, score, weight in scores) / total_weight
                )
            else:
                result = 0.0

        cache.set(cache_key, result, timeout=300)

        return min(1.0, max(0.0, result))

    def _calculate_word_similarity(self, query, text):
        """Enhanced word-based similarity"""
        query_words = set(query.split())
        text_words = set(text.split())

        if not query_words:
            return 0.0
        if not text_words:
            return 0.0

        intersection = query_words.intersection(text_words)
        exact_score = len(intersection) / len(query_words)

        partial_matches = 0
        for q_word in query_words:
            if q_word not in intersection:
                best_match = 0.0
                for t_word in text_words:
                    if len(q_word) > 3 and len(t_word) > 3:
                        similarity = self._calculate_character_similarity(
                            q_word, t_word
                        )
                        if similarity > 0.6:
                            best_match = max(best_match, similarity * 0.8)
                if best_match > 0:
                    partial_matches += best_match

        total_score = exact_score + (partial_matches / len(query_words))
        return min(1.0, total_score)

    def _calculate_trigram_similarity(self, query, text):
        """NOWE: Trigram-based similarity for better fuzzy matching"""
        if len(query) < 3 or len(text) < 3:
            return 0.0

        query_trigrams = self._generate_trigrams(query)
        text_trigrams = self._generate_trigrams(text)

        if not query_trigrams or not text_trigrams:
            return 0.0

        intersection = len(query_trigrams.intersection(text_trigrams))
        union = len(query_trigrams.union(text_trigrams))

        return intersection / union if union > 0 else 0.0

    def _generate_trigrams(self, text):
        """Generate character-level trigrams"""
        trigrams = set()
        text = f"###{text}###"
        for i in range(len(text) - 2):
            trigrams.add(text[i : i + 3])
        return trigrams

    def _calculate_chunked_similarity(self, query, text):
        """NOWE: Chunked processing for long texts"""
        if len(text) <= self.chunk_size:
            return self._calculate_character_similarity(query, text)

        chunks = []
        text_len = len(text)
        start = 0

        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            chunk = text[start:end]
            chunks.append(chunk)

            if end >= text_len:
                break

            start += self.chunk_size - self.chunk_overlap

        best_score = 0.0
        for chunk in chunks:
            chunk_score = self._calculate_character_similarity(query, chunk)
            best_score = max(best_score, chunk_score)

        return best_score

    def _calculate_character_similarity(self, s1, s2):
        """Optimized Levenshtein distance calculation"""
        if not s1 or not s2:
            return 0.0

        s1 = s1[: self.max_distance_calc_length]
        s2 = s2[: self.max_distance_calc_length]

        len1, len2 = len(s1), len(s2)

        if abs(len1 - len2) > max(len1, len2) * 0.5:
            return 0.0

        prev_row = list(range(len2 + 1))
        curr_row = [0] * (len2 + 1)

        for i in range(1, len1 + 1):
            curr_row[0] = i
            for j in range(1, len2 + 1):
                if s1[i - 1] == s2[j - 1]:
                    cost = 0
                else:
                    cost = 1

                curr_row[j] = min(
                    prev_row[j] + 1,
                    curr_row[j - 1] + 1,
                    prev_row[j - 1] + cost,
                )
            prev_row, curr_row = curr_row, prev_row

        max_len = max(len1, len2)
        if max_len == 0:
            return 1.0

        distance = prev_row[len2]
        similarity = 1 - (distance / max_len)

        return max(0.0, similarity)

    def search_products(self, query, products, threshold=None):
        """Enhanced product search with caching and better scoring"""
        if threshold is None:
            threshold = self.default_threshold

        cache_key = f"fuzzy_search_{hash(query)}_{threshold}_{len(products)}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        results = []

        for product in products:
            name_score = self.calculate_fuzzy_score(query, product.name)
            desc_score = self.calculate_fuzzy_score(query, product.description or "")

            category_scores = [
                self.calculate_fuzzy_score(query, cat.name)
                for cat in product.categories.all()
            ]
            category_score = max(category_scores) if category_scores else 0

            spec_scores = []
            for spec in product.specification_set.all()[:8]:
                if spec.specification:
                    spec_scores.append(
                        self.calculate_fuzzy_score(query, spec.specification)
                    )
                if spec.parameter_name:
                    spec_scores.append(
                        self.calculate_fuzzy_score(query, spec.parameter_name)
                    )

            spec_score = max(spec_scores) if spec_scores else 0

            tag_scores = [
                self.calculate_fuzzy_score(query, tag.name)
                for tag in product.tags.all()
            ]
            tag_score = max(tag_scores) if tag_scores else 0

            # Use MAX scoring instead of weighted average for better fuzzy matching
            # Rationale: If query matches name well (e.g., "laptpo" -> "laptop"),
            # don't penalize for not matching description/category
            # Apply slight penalties to non-name fields for better ranking
            total_score = max(
                name_score,  # Full weight for name
                desc_score * 0.9,  # 90% for description
                category_score * 0.8,  # 80% for category
                spec_score * 0.7,  # 70% for specs
                tag_score * 0.6,  # 60% for tags
            )

            if total_score >= threshold:
                results.append(
                    {
                        "product": product,
                        "score": round(total_score, 3),
                        "name_score": round(name_score, 3),
                        "desc_score": round(desc_score, 3),
                        "category_score": round(category_score, 3),
                        "spec_score": round(spec_score, 3),
                        "tag_score": round(tag_score, 3),
                    }
                )

        results.sort(key=lambda x: x["score"], reverse=True)

        cache.set(cache_key, results, timeout=600)

        return results


class CustomAssociationRules:
    """
    Custom implementation of Apriori algorithm for Market Basket Analysis.

    References:
    - Agrawal, R., Srikant, R. (1994). "Fast algorithms for mining association rules in large databases".
      Proceedings of the 20th International Conference on Very Large Data Bases (VLDB), pp. 487-499.
    - Brin, S., Motwani, R., Silverstein, C. (1997). "Beyond market baskets: Generalizing association rules to correlations".
      ACM SIGMOD Record, 26(2), pp. 265-276.

    Mathematical Formulas:

    1. Support(X):
       Support(X) = |{t ∈ T : X ⊆ t}| / |T|
       where:
       - T = set of all transactions
       - t = single transaction
       - X = itemset (set of products)
       - |T| = number of transactions

    2. Confidence(X→Y):
       Confidence(X→Y) = Support(X∪Y) / Support(X)
       where:
       - X = antecedent (source product)
       - Y = consequent (target product)
       - Support(X∪Y) = support for pair (X,Y)

    3. Lift(X→Y):
       Lift(X→Y) = Support(X∪Y) / (Support(X) × Support(Y))
                 = Confidence(X→Y) / Support(Y)
       Interpretation:
       - Lift > 1: Positive correlation (products bought together more than random)
       - Lift = 1: Independence (no relationship)
       - Lift < 1: Negative correlation (products bought together less than random)

    Optimizations:
    - Bitmap pruning: Using bitwise operations for efficient itemset counting (Zaki 2000)
    - Early pruning: Removing infrequent items before pair generation
    - Bulk operations: Batch database insertions
    - Caching: Storing computed results
    """

    def __init__(self, min_support=0.01, min_confidence=0.1):
        """
        Initialize Apriori algorithm parameters.

        Args:
            min_support (float): Minimum frequency threshold (default: 0.01 = 1%)
            min_confidence (float): Minimum certainty threshold (default: 0.1 = 10%)
        """
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.max_transactions = 3000
        self.max_items_per_transaction = 20

    def generate_association_rules(self, transactions):
        """Generates association rules with bitmap pruning optimization"""

        cache_key = f"association_rules_{len(transactions)}_{self.min_support}_{self.min_confidence}"
        cached_result = cache.get(cache_key)

        if cached_result:
            print("Using cached association rules")
            return cached_result

        filtered_transactions = []
        for transaction in transactions[: self.max_transactions]:
            limited_transaction = transaction[: self.max_items_per_transaction]
            if len(limited_transaction) >= 2:
                filtered_transactions.append(limited_transaction)

        if len(filtered_transactions) < 2:
            return []

        print(
            f"Processing {len(filtered_transactions)} transactions for enhanced association rules"
        )

        frequent_itemsets = self._find_frequent_itemsets_with_bitmap(
            filtered_transactions
        )
        rules = self._generate_optimized_rules_from_itemsets(
            frequent_itemsets, filtered_transactions
        )

        cache.set(
            cache_key, rules, timeout=getattr(settings, "CACHE_TIMEOUT_MEDIUM", 1800)
        )
        print(f"Cached {len(rules)} association rules for 30 minutes")

        return rules

    def _find_frequent_itemsets_with_bitmap(self, transactions):
        """Enhanced frequent itemset mining with bitmap pruning"""
        total_transactions = len(transactions)
        min_count_threshold = int(self.min_support * total_transactions)

        print(f"Minimum count threshold: {min_count_threshold}")

        item_counts = defaultdict(int)
        for transaction in transactions:
            for item in transaction:
                item_counts[item] += 1

        frequent_items = {}
        item_to_id = {}
        frequent_item_list = []

        item_id = 0
        for item, count in item_counts.items():
            if count >= min_count_threshold:
                support = count / total_transactions
                frequent_items[frozenset([item])] = support
                item_to_id[item] = item_id
                frequent_item_list.append(item)
                item_id += 1

        print(
            f"Found {len(frequent_items)} frequent individual items (after early pruning)"
        )

        if len(frequent_item_list) < 2:
            return frequent_items

        transaction_bitmaps = []
        for transaction in transactions:
            bitmap = 0
            for item in transaction:
                if item in item_to_id:
                    bitmap |= 1 << item_to_id[item]

            if bitmap:
                transaction_bitmaps.append(bitmap)

        print(f"Created {len(transaction_bitmaps)} transaction bitmaps")

        frequent_2_itemsets = self._generate_2_itemsets_with_bitmap(
            transaction_bitmaps,
            frequent_item_list,
            item_to_id,
            min_count_threshold,
            total_transactions,
        )

        print(
            f"Found {len(frequent_2_itemsets)} frequent 2-itemsets (with bitmap pruning)"
        )

        all_frequent = {}
        all_frequent.update(frequent_items)
        all_frequent.update(frequent_2_itemsets)

        return all_frequent

    def _generate_2_itemsets_with_bitmap(
        self,
        transaction_bitmaps,
        frequent_items,
        item_to_id,
        min_count_threshold,
        total_transactions,
    ):
        """Generate 2-itemsets using bitmap operations for efficiency"""
        frequent_2_itemsets = {}

        for i in range(len(frequent_items)):
            item1 = frequent_items[i]
            item1_bit = 1 << item_to_id[item1]

            for j in range(i + 1, len(frequent_items)):
                item2 = frequent_items[j]
                item2_bit = 1 << item_to_id[item2]

                pair_bitmap = item1_bit | item2_bit

                count = 0
                for transaction_bitmap in transaction_bitmaps:
                    if (transaction_bitmap & pair_bitmap) == pair_bitmap:
                        count += 1

                if count >= min_count_threshold:
                    support = count / total_transactions
                    pair = frozenset([item1, item2])
                    frequent_2_itemsets[pair] = support

        return frequent_2_itemsets

    def _generate_optimized_rules_from_itemsets(self, frequent_itemsets, transactions):
        """
        Generate association rules from frequent itemsets.

        Formula implementation (Agrawal & Srikant 1994):

        STEP 1: Cache individual item supports
            Support(A) = count(transactions containing A) / total_transactions

        STEP 2: For each 2-itemset (A,B):
            Support(A,B) = already computed in frequent_itemsets
            Support(A) = cached from step 1
            Support(B) = cached from step 1

        STEP 3: Calculate Confidence(A→B):
            Confidence(A→B) = Support(A,B) / Support(A)

            This answers: "If someone buys A, what's the probability they'll also buy B?"
            Formula from Agrawal & Srikant (1994), Section 4.2

        STEP 4: Calculate Lift(A→B):
            Lift(A→B) = Support(A,B) / (Support(A) × Support(B))

            This measures correlation strength:
            - Lift > 1: Products bought together MORE than random chance (positive correlation)
            - Lift = 1: No relationship (independence)
            - Lift < 1: Products bought together LESS than random chance (negative correlation)

            Formula from Brin, Motwani, Silverstein (1997), Section 3.1

        STEP 5: Filter by min_confidence threshold and create bidirectional rules

        Args:
            frequent_itemsets (dict): Dictionary of {frozenset: support_value}
            transactions (list): List of transaction lists

        Returns:
            list: List of rule dictionaries sorted by lift and confidence
        """
        rules = []
        total_transactions = len(transactions)

        item_support_cache = {}
        for itemset, support in frequent_itemsets.items():
            if len(itemset) == 1:
                item = list(itemset)[0]
                item_support_cache[item] = support

        print(f"Cached {len(item_support_cache)} individual item supports")

        for itemset, support in frequent_itemsets.items():
            if len(itemset) == 2:
                items = list(itemset)
                item1, item2 = items[0], items[1]

                support_1 = item_support_cache.get(item1, 0)
                support_2 = item_support_cache.get(item2, 0)

                if support_1 > 0:
                    confidence_1_to_2 = support / support_1
                else:
                    confidence_1_to_2 = 0

                if support_2 > 0:
                    confidence_2_to_1 = support / support_2
                else:
                    confidence_2_to_1 = 0

                if (support_1 * support_2) > 0:
                    lift = support / (support_1 * support_2)
                else:
                    lift = 0

                if confidence_1_to_2 >= self.min_confidence:
                    rules.append(
                        {
                            "product_1": item1,
                            "product_2": item2,
                            "support": support,
                            "confidence": confidence_1_to_2,
                            "lift": lift,
                        }
                    )

                if confidence_2_to_1 >= self.min_confidence:
                    rules.append(
                        {
                            "product_1": item2,
                            "product_2": item1,
                            "support": support,
                            "confidence": confidence_2_to_1,
                            "lift": lift,
                        }
                    )

        rules.sort(key=lambda x: (x["lift"], x["confidence"]), reverse=True)

        print(
            f"Generated {len(rules)} association rules (after filtering by min_confidence={self.min_confidence})"
        )

        return rules


class CustomSentimentAnalysis:
    def __init__(self):
        self.positive_words = {
            "excellent", "great", "amazing", "wonderful", "fantastic", "awesome", 
            "good", "nice", "perfect", "outstanding", "brilliant", "superb",
            "love", "like", "enjoy", "recommend", "satisfied", "happy", 
            "pleased", "delighted", "quality", "fast", "beautiful", "comfortable",
            
            "incredible", "marvelous", "spectacular", "impressive", "magnificent",
            "extraordinary", "remarkable", "phenomenal", "exceptional", "stellar",
            "flawless", "divine", "sublime", "gorgeous", "stunning", "breathtaking",
            "charming", "elegant", "graceful", "stylish", "trendy", "modern",
            "innovative", "creative", "unique", "original", "fresh", "exciting",
            "thrilling", "fun", "entertaining", "enjoyable", "pleasant", "delightful",
            "smooth", "efficient", "reliable", "durable", "sturdy", "solid",
            "premium", "luxury", "high-quality", "top-notch", "first-class", "superior",
            "affordable", "bargain", "value", "worthwhile", "reasonable", "economical",
            "helpful", "useful", "convenient", "practical", "functional", "effective",
            "user-friendly", "intuitive", "simple", "easy", "straightforward", "clear",
            "precise", "accurate", "detailed", "comprehensive", "complete", "thorough",
            "professional", "expert", "skilled", "competent", "capable", "talented",
            "friendly", "kind", "polite", "courteous", "respectful", "considerate",
            "quick", "speedy", "prompt", "instant", "immediate", "responsive"
        }

        self.negative_words = {
            "terrible",
            "awful",
            "horrible",
            "bad",
            "worst",
            "disappointing",
            "poor",
            "useless",
            "hate",
            "dislike",
            "regret",
            "waste",
            "expensive",
            "slow",
            "broken",
            "defective",
            "uncomfortable",
            "ugly",
            "problem",
            "issue",
            "error",
            "fail",
            "complaint",
            "disgusting",
            "revolting",
            "repulsive",
            "appalling",
            "dreadful",
            "ghastly",
            "atrocious",
            "abysmal",
            "pathetic",
            "miserable",
            "wretched",
            "deplorable",
            "inferior",
            "substandard",
            "mediocre",
            "inadequate",
            "insufficient",
            "lacking",
            "flawed",
            "damaged",
            "faulty",
            "malfunctioning",
            "unreliable",
            "unstable",
            "fragile",
            "weak",
            "cheap",
            "shoddy",
            "tacky",
            "gaudy",
            "tasteless",
            "outdated",
            "obsolete",
            "old-fashioned",
            "primitive",
            "backward",
            "clunky",
            "complicated",
            "confusing",
            "difficult",
            "hard",
            "frustrating",
            "annoying",
            "irritating",
            "aggravating",
            "bothersome",
            "troublesome",
            "problematic",
            "buggy",
            "overpriced",
            "costly",
            "pricey",
            "unaffordable",
            "unreasonable",
            "excessive",
            "worthless",
            "pointless",
            "meaningless",
            "irrelevant",
            "unnecessary",
            "redundant",
            "boring",
            "dull",
            "tedious",
            "monotonous",
            "uninteresting",
            "bland",
            "rude",
            "impolite",
            "disrespectful",
            "unprofessional",
            "incompetent",
            "lazy",
            "delayed",
            "late",
            "sluggish",
            "unresponsive",
            "frozen",
            "crashed",
            "limited",
            "restricted",
            "constrained",
            "cramped",
            "tight",
            "narrow",
        }

        self.intensifiers = {
            "very",
            "extremely",
            "really",
            "quite",
            "totally",
            "absolutely",
            "completely",
            "entirely",
            "thoroughly",
            "utterly",
            "highly",
            "incredibly",
            "amazingly",
            "exceptionally",
            "remarkably",
            "particularly",
            "especially",
            "super",
            "ultra",
            "mega",
            "tremendously",
            "enormously",
            "immensely",
        }

        self.negations = {
            "not",
            "no",
            "never",
            "nothing",
            "neither",
            "nor",
            "none",
            "nobody",
            "nowhere",
            "hardly",
            "barely",
            "scarcely",
            "seldom",
            "rarely",
            "without",
            "lacking",
            "missing",
            "absent",
            "void",
            "devoid",
        }

        self.positive_bigrams = {
            "highly recommend",
            "love it",
            "great quality",
            "excellent service",
            "perfect condition",
            "amazing product",
            "outstanding performance",
            "works perfectly",
            "very satisfied",
            "extremely happy",
            "absolutely love",
            "top quality",
            "best ever",
            "incredible value",
            "fantastic experience",
            "smooth operation",
            "user friendly",
            "great design",
            "perfect size",
            "excellent condition",
            "fast delivery",
            "good price",
            "nice quality",
        }

        self.negative_bigrams = {
            "terrible quality",
            "waste money",
            "worst product",
            "complete disaster",
            "total failure",
            "absolutely terrible",
            "extremely disappointed",
            "poor quality",
            "bad experience",
            "horrible service",
            "never again",
            "money wasted",
            "completely useless",
            "terrible condition",
            "awful experience",
            "very disappointed",
            "extremely poor",
            "totally broken",
            "completely wrong",
            "serious problems",
            "major issues",
            "absolutely horrible",
            "worst ever",
        }

        self.window_size = 300
        self.window_overlap = 50

    def analyze_sentiment(self, text):
        positive_score = 0.0
        negative_score = 0.0
        neutral_score = 0.0
        total_words = 0

        words = self._tokenize_text(text.lower())

        for word in words:
            if word in self.positive_words:
                positive_score += 1.0
            elif word in self.negative_words:
                negative_score += 1.0
            else:
                neutral_score += 1.0
            total_words += 1

        if total_words == 0:
            return 0.0, "neutral"

        sentiment_score = (positive_score - negative_score) / total_words

        sentiment_score = max(-1.0, min(1.0, sentiment_score))

        if sentiment_score > 0.1:
            category = "positive"
        elif sentiment_score < -0.1:
            category = "negative"
        else:
            category = "neutral"

        return sentiment_score, category

    def _analyze_long_text_with_sliding_window(self, text, cache_key):
        """Analyze long texts using sliding window approach"""
        segments = []
        text_len = len(text)

        start = 0
        while start < text_len:
            end = min(start + self.window_size, text_len)
            segment = text[start:end]
            segments.append(segment)

            if end >= text_len:
                break

            start += self.window_size - self.window_overlap

        segment_scores = []
        segment_categories = []

        for segment in segments:
            score, category = self._analyze_text_segment(segment)
            segment_scores.append(score)
            segment_categories.append(category)

        if segment_scores:
            weights = [len(seg) for seg in segments]
            total_weight = sum(weights)

            weighted_score = (
                sum(score * weight for score, weight in zip(segment_scores, weights))
                / total_weight
            )

            if weighted_score > 0.05:
                final_category = "positive"
            elif weighted_score < -0.05:
                final_category = "negative"
            else:
                final_category = "neutral"

            result = (weighted_score, final_category)
        else:
            result = (0.0, "neutral")

        if cache_key:
            cache.set(
                cache_key,
                result,
                timeout=getattr(settings, "CACHE_TIMEOUT_MEDIUM", 3600),
            )

        return result

    def _analyze_text_segment(self, text):
        """Analyze single text segment with enhanced context awareness"""
        text = text.lower().strip()
        words = self._tokenize_text(text)

        if not words:
            return 0.0, "neutral"

        positive_score = 0.0
        negative_score = 0.0
        total_words = len(words)

        bigram_score = self._analyze_bigrams(words)
        positive_score += bigram_score["positive"]
        negative_score += bigram_score["negative"]

        i = 0
        while i < len(words):
            word = words[i]

            negation_context = self._check_negation_context(words, i)

            intensity_multiplier = self._calculate_intensity_multiplier(words, i)

            if word in self.positive_words:
                score = 1.0 * intensity_multiplier
                if negation_context:
                    negative_score += score * 0.8
                else:
                    positive_score += score

            elif word in self.negative_words:
                score = 1.0 * intensity_multiplier
                if negation_context:
                    positive_score += score * 0.8
                else:
                    negative_score += score

            i += 1

        if total_words == 0:
            sentiment_score = 0.0
        else:
            positive_ratio = positive_score / (total_words * 0.5)
            negative_ratio = negative_score / (total_words * 0.5)
            sentiment_score = positive_ratio - negative_ratio
            sentiment_score = max(-1.0, min(1.0, sentiment_score))

        if sentiment_score > 0.08:
            category = "positive"
        elif sentiment_score < -0.08:
            category = "negative"
        else:
            category = "neutral"

        return sentiment_score, category

    def _calculate_polarity_score(self, words):
        """
        Implementacja wzoru z pracy: Liu, Bing. "Sentiment Analysis and Opinion Mining" (2012)
        Polarity Score = Σ(positive_words) - Σ(negative_words) / |total_words|
        """
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)

        if len(words) == 0:
            return 0.0

        polarity = (positive_count - negative_count) / len(words)
        return polarity

    def _calculate_subjectivity_score(self, words):
        """
        Wzór z TextBlob: Subjectivity = (subjective_words) / (total_words)
        """
        subjective_words = sum(
            1
            for word in words
            if word in self.positive_words or word in self.negative_words
        )

        if len(words) == 0:
            return 0.0

        return subjective_words / len(words)

    def _check_negation_context(self, words, current_index):
        """Check for negation in 2-3 words context"""
        for i in range(max(0, current_index - 3), current_index):
            if words[i] in self.negations:
                return True
        return False

    def _calculate_intensity_multiplier(self, words, current_index):
        """Calculate intensity multiplier from broader context"""
        multiplier = 1.0

        for i in range(max(0, current_index - 2), min(len(words), current_index + 3)):
            if i != current_index and words[i] in self.intensifiers:
                multiplier = max(multiplier, 1.8)

        return multiplier

    def _analyze_bigrams(self, words):
        """Analyze sentiment using bigrams for better context"""
        bigram_scores = {"positive": 0.0, "negative": 0.0}

        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i + 1]}"

            if bigram in self.positive_bigrams:
                bigram_scores["positive"] += 2.0
            elif bigram in self.negative_bigrams:
                bigram_scores["negative"] += 2.0

        return bigram_scores

    def _tokenize_text(self, text):
        text = re.sub(r"[^\w\s]", " ", text)
        words = text.split()
        return [word.strip() for word in words if word.strip()]

    def analyze_product_sentiment(self, product):
        """Enhanced product sentiment analysis with caching"""
        from home.models import Opinion

        cache_key = f"product_sentiment_{product.id}_{product.updated_at if hasattr(product, 'updated_at') else 'static'}"
        cached_result = cache.get(cache_key)

        if cached_result:
            return cached_result

        opinions = Opinion.objects.filter(product=product)

        if not opinions.exists():
            result = {
                "average_sentiment_score": 0.0,
                "positive_count": 0,
                "neutral_count": 0,
                "negative_count": 0,
                "total_opinions": 0,
            }
            cache.set(
                cache_key, result, timeout=getattr(settings, "CACHE_TIMEOUT_SHORT", 900)
            )
            return result

        sentiment_scores = []
        positive_count = 0
        neutral_count = 0
        negative_count = 0

        opinion_contents = [opinion.content for opinion in opinions if opinion.content]

        for content in opinion_contents:
            score, category = self.analyze_sentiment(content)
            sentiment_scores.append(score)

            if category == "positive":
                positive_count += 1
            elif category == "negative":
                negative_count += 1
            else:
                neutral_count += 1

        average_score = (
            sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
        )

        sentiment_variance = 0.0
        if len(sentiment_scores) > 1:
            mean = average_score
            sentiment_variance = sum(
                (score - mean) ** 2 for score in sentiment_scores
            ) / len(sentiment_scores)

        result = {
            "average_sentiment_score": round(average_score, 3),
            "positive_count": positive_count,
            "neutral_count": neutral_count,
            "negative_count": negative_count,
            "total_opinions": len(sentiment_scores),
        }

        cache.set(
            cache_key, result, timeout=getattr(settings, "CACHE_TIMEOUT_LONG", 7200)
        )

        return result


def calculate_association_rules(transactions, min_support=0.01, min_confidence=0.1):
    association_engine = CustomAssociationRules(min_support, min_confidence)
    return association_engine.generate_association_rules(transactions)


class CustomMarkovChain:
    """Implementation of Markov Chain for purchase sequence prediction"""

    def __init__(self, order=1):
        self.order = order
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.states = set()
        self.total_sequences = 0

    def train(self, sequences):
        """Train Markov chain on purchase sequences"""
        self.total_sequences = len(sequences)

        for sequence in sequences:
            if len(sequence) < 2:
                continue

            for state in sequence:
                self.states.add(state)

            for i in range(len(sequence) - 1):
                current_state = sequence[i]
                next_state = sequence[i + 1]

                self.transitions[current_state][next_state] += 1

        for current_state in self.transitions:
            total_transitions = sum(self.transitions[current_state].values())
            if total_transitions > 0:
                for next_state in self.transitions[current_state]:
                    self.transitions[current_state][next_state] /= total_transitions

        print(
            f"Trained Markov chain on {self.total_sequences} sequences with {len(self.states)} unique states"
        )

    def predict_next(self, current_state, top_k=5):
        """Predict next most likely states given current state"""
        if current_state not in self.transitions:
            return []

        predictions = []
        for next_state, probability in self.transitions[current_state].items():
            predictions.append({"state": next_state, "probability": probability})

        predictions.sort(key=lambda x: x["probability"], reverse=True)
        return predictions[:top_k]

    def predict_sequence(self, initial_state, length=3):
        """Generate a sequence of predicted states"""
        if initial_state not in self.transitions:
            return [initial_state]

        sequence = [initial_state]
        current_state = initial_state

        for _ in range(length - 1):
            predictions = self.predict_next(current_state, top_k=1)
            if not predictions:
                break

            next_state = predictions[0]["state"]
            sequence.append(next_state)
            current_state = next_state

            if sequence.count(current_state) > 2:
                break

        return sequence

    def get_transition_probability(self, from_state, to_state):
        """Get probability of transitioning from one state to another"""
        if from_state in self.transitions and to_state in self.transitions[from_state]:
            return self.transitions[from_state][to_state]
        return 0.0

    def get_stationary_distribution(self):
        """Calculate stationary distribution of the Markov chain"""
        state_counts = defaultdict(int)

        for current_state in self.transitions:
            for next_state, count in self.transitions[current_state].items():
                state_counts[next_state] += count

        total = sum(state_counts.values())
        if total == 0:
            return {}

        return {state: count / total for state, count in state_counts.items()}


class CustomNaiveBayes:
    """Custom Naive Bayes implementation for purchase prediction and churn analysis"""

    def __init__(self):
        self.class_priors = {}
        self.feature_likelihoods = defaultdict(
            lambda: defaultdict(lambda: defaultdict(int))
        )
        self.feature_counts = defaultdict(lambda: defaultdict(int))
        self.classes = set()
        self.trained = False

    def train(self, features_list, labels):
        """Train Naive Bayes classifier

        Args:
            features_list: List of feature dictionaries
            labels: List of corresponding labels
        """
        if len(features_list) != len(labels):
            raise ValueError("Features and labels must have same length")

        n_samples = len(labels)

        class_counts = defaultdict(int)
        for label in labels:
            self.classes.add(label)
            class_counts[label] += 1

        for class_label in self.classes:
            self.class_priors[class_label] = class_counts[class_label] / n_samples

        for features, label in zip(features_list, labels):
            for feature, value in features.items():
                self.feature_likelihoods[feature][label][value] += 1
                self.feature_counts[feature][label] += 1

        for feature in self.feature_likelihoods:
            for class_label in self.classes:
                total_count = self.feature_counts[feature][class_label]
                unique_values = len(self.feature_likelihoods[feature][class_label])

                for value in self.feature_likelihoods[feature][class_label]:
                    self.feature_likelihoods[feature][class_label][value] = (
                        self.feature_likelihoods[feature][class_label][value] + 1
                    ) / (total_count + unique_values)

        self.trained = True
        print(
            f"Trained Naive Bayes on {n_samples} samples with {len(self.classes)} classes"
        )

    def predict_proba(self, features):
        """Predict class probabilities for given features"""
        if not self.trained:
            raise ValueError("Model must be trained before prediction")

        probabilities = {}

        for class_label in self.classes:
            prob = math.log(self.class_priors[class_label])

            for feature, value in features.items():
                if feature in self.feature_likelihoods:
                    if value in self.feature_likelihoods[feature][class_label]:
                        likelihood = self.feature_likelihoods[feature][class_label][
                            value
                        ]
                    else:
                        total_count = self.feature_counts[feature][class_label]
                        unique_values = len(
                            self.feature_likelihoods[feature][class_label]
                        )
                        likelihood = 1 / (total_count + unique_values + 1)

                    prob += math.log(likelihood)

            probabilities[class_label] = prob

        max_log_prob = max(probabilities.values())
        for class_label in probabilities:
            probabilities[class_label] = math.exp(
                probabilities[class_label] - max_log_prob
            )

        total_prob = sum(probabilities.values())
        if total_prob > 0:
            for class_label in probabilities:
                probabilities[class_label] /= total_prob

        return probabilities

    def predict(self, features):
        """Predict class label for given features"""
        probabilities = self.predict_proba(features)
        return max(probabilities, key=probabilities.get)

    def get_feature_importance(self):
        """Calculate feature importance based on information gain"""
        feature_importance = {}

        for feature in self.feature_likelihoods:
            total_entropy = 0
            total_samples = sum(self.feature_counts[feature].values())

            if total_samples == 0:
                continue

            for class_label in self.classes:
                class_count = self.feature_counts[feature][class_label]
                if class_count > 0:
                    class_prob = class_count / total_samples
                    total_entropy -= class_prob * math.log2(class_prob + 1e-10)

            feature_importance[feature] = total_entropy

        return feature_importance


class ProbabilisticRecommendationEngine:
    """Combined engine using both Markov Chains and Naive Bayes"""

    def __init__(self):
        self.markov_chain = CustomMarkovChain(order=1)
        self.naive_bayes_purchase = CustomNaiveBayes()
        self.naive_bayes_churn = CustomNaiveBayes()
        self.category_mapping = {}
        self.trained = False

    def train_markov_model(self, user_purchase_sequences):
        """Train Markov chain on user purchase sequences"""
        category_sequences = []

        for sequence in user_purchase_sequences:
            if len(sequence) >= 2:
                category_sequence = []
                for product_id in sequence:
                    category = self.get_product_category(product_id)
                    if category:
                        category_sequence.append(category)

                if len(category_sequence) >= 2:
                    category_sequences.append(category_sequence)

        if category_sequences:
            self.markov_chain.train(category_sequences)
            return len(category_sequences)
        return 0

    def train_purchase_prediction_model(self, user_features, purchase_labels):
        """Train Naive Bayes for purchase prediction"""
        if user_features and purchase_labels:
            self.naive_bayes_purchase.train(user_features, purchase_labels)
            return len(user_features)
        return 0

    def train_churn_prediction_model(self, user_features, churn_labels):
        """Train Naive Bayes for churn prediction"""
        if user_features and churn_labels:
            self.naive_bayes_churn.train(user_features, churn_labels)
            return len(user_features)
        return 0

    def get_product_category(self, product_id):
        """Get main category for a product"""
        if product_id in self.category_mapping:
            return self.category_mapping[product_id]

        try:
            from home.models import Product

            product = Product.objects.get(id=product_id)
            main_category = product.categories.first()
            if main_category:
                category_name = main_category.name
                self.category_mapping[product_id] = category_name
                return category_name
        except:
            pass

        return None

    def predict_next_purchase_categories(self, last_category, top_k=5):
        """Predict next purchase categories using Markov chain"""
        return self.markov_chain.predict_next(last_category, top_k)

    def predict_purchase_probability(self, user_features):
        """Predict purchase probability using Naive Bayes"""
        if not self.naive_bayes_purchase.trained:
            return {"will_purchase": 0.5, "will_not_purchase": 0.5}

        probabilities = self.naive_bayes_purchase.predict_proba(user_features)
        return probabilities

    def predict_churn_probability(self, user_features):
        """Predict churn probability using Naive Bayes"""
        if not self.naive_bayes_churn.trained:
            return {"will_churn": 0.5, "will_not_churn": 0.5}

        probabilities = self.naive_bayes_churn.predict_proba(user_features)
        return probabilities

    def get_markov_insights(self):
        """Get insights from Markov chain analysis"""
        stationary_dist = self.markov_chain.get_stationary_distribution()

        insights = {
            "most_popular_categories": sorted(
                stationary_dist.items(), key=lambda x: x[1], reverse=True
            )[:5],
            "total_states": len(self.markov_chain.states),
            "total_transitions": sum(
                len(transitions)
                for transitions in self.markov_chain.transitions.values()
            ),
        }

        return insights
