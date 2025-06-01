import re
from collections import defaultdict, Counter
from decimal import Decimal
from django.db.models import Count, Sum, Avg


class CustomContentBasedFilter:
    def __init__(self):
        self.similarity_threshold = 0.2
        self.max_products_for_similarity = 200
        self.batch_size = 50
        self.max_comparisons_per_product = 20

    def calculate_product_similarity(self, product1, product2):
        features1 = self._extract_features(product1)
        features2 = self._extract_features(product2)

        intersection = len(features1.intersection(features2))
        union = len(features1.union(features2))

        if union == 0:
            return 0.0

        return intersection / union

    def _extract_features(self, product):
        features = set()

        for category in product.categories.all():
            features.add(f"category_{category.name.lower()}")

        for tag in product.tags.all():
            features.add(f"tag_{tag.name.lower()}")

        if product.price < 100:
            features.add("price_low")
        elif product.price < 500:
            features.add("price_medium")
        else:
            features.add("price_high")

        return features

    def generate_similarities_for_all_products(self):
        from home.models import Product, ProductSimilarity

        products = list(
            Product.objects.prefetch_related("categories", "tags").all()[:self.max_products_for_similarity]
        )
        similarities_created = 0

        ProductSimilarity.objects.filter(similarity_type="content_based").delete()

        print(f"Processing {len(products)} products for content-based similarity (limited for performance)")

        for i, product1 in enumerate(products):
            if i % 10 == 0:
                print(f"Processed {i}/{len(products)} products")
                
            comparison_products = products[i + 1:i + 1 + self.max_comparisons_per_product]

            for product2 in comparison_products:
                similarity_score = self.calculate_product_similarity(product1, product2)

                if similarity_score > self.similarity_threshold:
                    ProductSimilarity.objects.create(
                        product1=product1,
                        product2=product2,
                        similarity_type="content_based",
                        similarity_score=similarity_score,
                    )
                    ProductSimilarity.objects.create(
                        product1=product2,
                        product2=product1,
                        similarity_type="content_based",
                        similarity_score=similarity_score,
                    )
                    similarities_created += 2

        print(f"Created {similarities_created} content-based similarities")
        return similarities_created


class CustomFuzzySearch:
    def __init__(self):
        self.default_threshold = 0.6
        self.max_distance_calc_length = 100

    def calculate_fuzzy_score(self, query, text):
        if not text or not query:
            return 0.0

        query = query.lower().strip()
        text = text.lower().strip()

        if query == text:
            return 1.0

        if query in text:
            return 0.9

        query_words = set(query.split())
        text_words = set(text.split())

        if query_words and text_words:
            word_intersection = len(query_words.intersection(text_words))
            word_score = word_intersection / len(query_words)
        else:
            word_score = 0.0

        if (
            len(query) <= self.max_distance_calc_length
            and len(text) <= self.max_distance_calc_length
        ):
            char_score = self._calculate_character_similarity(query, text)
        else:
            char_score = 0.0

        final_score = max(word_score * 0.7, char_score * 0.3)
        return final_score

    def _calculate_character_similarity(self, s1, s2):
        if not s1 or not s2:
            return 0.0

        s1 = s1[:self.max_distance_calc_length]
        s2 = s2[:self.max_distance_calc_length]

        len1, len2 = len(s1), len(s2)

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
        if threshold is None:
            threshold = self.default_threshold

        results = []

        for product in products:
            name_score = self.calculate_fuzzy_score(query, product.name)
            desc_score = self.calculate_fuzzy_score(query, product.description or "")

            category_scores = [
                self.calculate_fuzzy_score(query, cat.name)
                for cat in product.categories.all()
            ]
            category_score = max(category_scores) if category_scores else 0

            spec_scores = [
                self.calculate_fuzzy_score(query, spec.specification or "")
                for spec in product.specification_set.all()[:5]
            ]
            spec_score = max(spec_scores) if spec_scores else 0

            total_score = (
                name_score * 0.4
                + desc_score * 0.3
                + category_score * 0.2
                + spec_score * 0.1
            )

            if total_score >= threshold:
                results.append(
                    {
                        "product": product,
                        "score": total_score,
                        "name_score": name_score,
                        "desc_score": desc_score,
                        "category_score": category_score,
                        "spec_score": spec_score,
                    }
                )

        results.sort(key=lambda x: x["score"], reverse=True)
        return results


class CustomAssociationRules:
    def __init__(self, min_support=0.01, min_confidence=0.1):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.max_transactions = 2000
        self.max_items_per_transaction = 15

    def generate_association_rules(self, transactions):
        filtered_transactions = []
        for transaction in transactions[:self.max_transactions]:
            limited_transaction = transaction[:self.max_items_per_transaction]
            if len(limited_transaction) >= 2:
                filtered_transactions.append(limited_transaction)

        if len(filtered_transactions) < 2:
            return []

        print(f"Processing {len(filtered_transactions)} transactions for association rules")

        frequent_itemsets = self._find_frequent_itemsets(filtered_transactions)
        rules = self._generate_rules_from_itemsets(frequent_itemsets, filtered_transactions)

        return rules

    def _find_frequent_itemsets(self, transactions):
        total_transactions = len(transactions)

        item_counts = defaultdict(int)
        for transaction in transactions:
            for item in transaction:
                item_counts[item] += 1

        frequent_items = {}
        for item, count in item_counts.items():
            support = count / total_transactions
            if support >= self.min_support:
                frequent_items[frozenset([item])] = support

        print(f"Found {len(frequent_items)} frequent individual items")

        frequent_2_itemsets = self._generate_2_itemsets(
            transactions, frequent_items, total_transactions
        )

        print(f"Found {len(frequent_2_itemsets)} frequent 2-itemsets")

        all_frequent = {}
        all_frequent.update(frequent_items)
        all_frequent.update(frequent_2_itemsets)

        return all_frequent

    def _generate_2_itemsets(self, transactions, frequent_1_itemsets, total_transactions):
        frequent_items = [list(itemset)[0] for itemset in frequent_1_itemsets.keys()]
        pair_counts = defaultdict(int)

        for transaction in transactions:
            transaction_items = [item for item in transaction if item in frequent_items]
            for i in range(min(len(transaction_items), 10)):
                for j in range(i + 1, min(len(transaction_items), 10)):
                    pair = frozenset([transaction_items[i], transaction_items[j]])
                    pair_counts[pair] += 1

        frequent_2_itemsets = {}
        for pair, count in pair_counts.items():
            support = count / total_transactions
            if support >= self.min_support:
                frequent_2_itemsets[pair] = support

        return frequent_2_itemsets

    def _generate_rules_from_itemsets(self, frequent_itemsets, transactions):
        rules = []
        total_transactions = len(transactions)

        for itemset, support in frequent_itemsets.items():
            if len(itemset) == 2:
                items = list(itemset)
                item1, item2 = items[0], items[1]

                count_1 = sum(1 for t in transactions if item1 in t)
                count_2 = sum(1 for t in transactions if item2 in t)
                count_both = sum(1 for t in transactions if item1 in t and item2 in t)

                confidence_1_to_2 = count_both / count_1 if count_1 > 0 else 0
                confidence_2_to_1 = count_both / count_2 if count_2 > 0 else 0

                support_1 = count_1 / total_transactions
                support_2 = count_2 / total_transactions
                lift = (
                    support / (support_1 * support_2)
                    if (support_1 * support_2) > 0
                    else 0
                )

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

        return rules


class CustomSentimentAnalysis:
    def __init__(self):
        self.positive_words = {
            "excellent", "great", "amazing", "wonderful", "fantastic", "awesome",
            "good", "nice", "perfect", "outstanding", "brilliant", "superb",
            "love", "like", "enjoy", "recommend", "satisfied", "happy",
            "pleased", "delighted", "quality", "fast", "beautiful", "comfortable"
        }

        self.negative_words = {
            "terrible", "awful", "horrible", "bad", "worst", "disappointing",
            "poor", "useless", "hate", "dislike", "regret", "waste",
            "expensive", "slow", "broken", "defective", "uncomfortable",
            "ugly", "problem", "issue", "error", "fail", "complaint"
        }

        self.intensifiers = {"very", "extremely", "really", "quite", "totally"}
        self.negations = {"not", "no", "never", "nothing", "neither", "nor"}

    def analyze_sentiment(self, text):
        if not text:
            return 0.0, "neutral"

        text = text[:500]
        words = self._tokenize_text(text.lower())

        positive_score = 0
        negative_score = 0
        total_words = len(words)

        i = 0
        while i < len(words):
            word = words[i]

            is_negated = False
            if i > 0 and words[i - 1] in self.negations:
                is_negated = True

            intensity_multiplier = 1.0
            if i > 0 and words[i - 1] in self.intensifiers:
                intensity_multiplier = 1.5
            elif i < len(words) - 1 and words[i + 1] in self.intensifiers:
                intensity_multiplier = 1.5

            if word in self.positive_words:
                score = 1.0 * intensity_multiplier
                if is_negated:
                    negative_score += score
                else:
                    positive_score += score
            elif word in self.negative_words:
                score = 1.0 * intensity_multiplier
                if is_negated:
                    positive_score += score
                else:
                    negative_score += score

            i += 1

        if total_words == 0:
            sentiment_score = 0.0
        else:
            positive_ratio = positive_score / total_words
            negative_ratio = negative_score / total_words
            sentiment_score = positive_ratio - negative_ratio
            sentiment_score = max(-1.0, min(1.0, sentiment_score))

        if sentiment_score > 0.05:
            category = "positive"
        elif sentiment_score < -0.05:
            category = "negative"
        else:
            category = "neutral"

        return sentiment_score, category

    def _tokenize_text(self, text):
        text = re.sub(r"[^\w\s]", " ", text)
        words = text.split()
        return [word.strip() for word in words if word.strip()]

    def analyze_product_sentiment(self, product):
        from home.models import Opinion

        opinions = Opinion.objects.filter(product=product)

        if not opinions.exists():
            return {
                "average_sentiment_score": 0.0,
                "positive_count": 0,
                "neutral_count": 0,
                "negative_count": 0,
                "total_opinions": 0,
            }

        sentiment_scores = []
        positive_count = 0
        neutral_count = 0
        negative_count = 0

        for opinion in opinions:
            if opinion.content:
                score, category = self.analyze_sentiment(opinion.content)
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

        return {
            "average_sentiment_score": average_score,
            "positive_count": positive_count,
            "neutral_count": neutral_count,
            "negative_count": negative_count,
            "total_opinions": len(sentiment_scores),
        }


def calculate_association_rules(transactions, min_support=0.01, min_confidence=0.1):
    association_engine = CustomAssociationRules(min_support, min_confidence)
    return association_engine.generate_association_rules(transactions)