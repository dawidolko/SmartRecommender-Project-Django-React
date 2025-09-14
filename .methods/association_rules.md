To be corrected: 14/09/2025

# 🔗 Association Rules - "Frequently Bought Together" System

## What Are "Association Rules" on the Site?

**Association rules** are a recommendation algorithm based on the **Apriori method** that:

- Identifies products that are **frequently bought together**
- Helps clients discover **related products** while shopping
- Enables admins to view and **manage these relationships** in the dashboard
- Uses **real mathematical formulas** from scientific literature (Agrawal & Srikant 1994)

These rules are based on **real order history** and are recalculated dynamically when new purchases are made.

---

## 📂 Project Structure Overview (Key Files & Roles)

### 1. `backend/home/models.py` – 📦 **ProductAssociation Model**

```python
class ProductAssociation(models.Model):
    product_1 = models.ForeignKey(Product, related_name='associations_from', ...)
    product_2 = models.ForeignKey(Product, related_name='associations_to', ...)
    support = models.FloatField()      # Support - how often pair occurs together
    confidence = models.FloatField()   # Confidence - probability of buying B when bought A
    lift = models.FloatField()         # Lift - rule strength vs. random chance
```

This model stores association rules with **real Apriori metrics**:

- `support`: Support(A,B) = |A∩B| / |D| (pair frequency)
- `confidence`: Confidence(A→B) = Support(A,B) / Support(A) (rule certainty)
- `lift`: Lift(A→B) = Confidence(A→B) / Support(B) (rule strength)

---

### 2. `backend/home/signals.py` – 🔁 **Automatic Rule Generation**

Triggered when a user places an order:

```python
@receiver(post_save, sender=Order)
def handle_new_order_and_analytics(sender, instance, created, **kwargs):
    ...
    transaction.on_commit(lambda: run_all_analytics_after_order(instance))
```

This calls `generate_association_rules_after_order(order)`, which:

- Reads all past orders
- Extracts product combinations (as transactions)
- Calls `CustomAssociationRules.generate_association_rules(transactions)`
- Stores results in `ProductAssociation` using **real formulas**

➡️ This ensures rules are **automatically updated** after each new purchase.

---

### 3. `backend/home/custom_recommendation_engine.py` – 🧠 **Rule Calculation**

Class `CustomAssociationRules` implements **real Apriori algorithm**:

```python
def _calculate_support(self, itemset, transactions):
    """
    Support formula from literature (Agrawal & Srikant 1994):
    Support(X) = |transactions containing X| / |total transactions|
    """
    count = 0
    for transaction in transactions:
        if itemset.issubset(set(transaction)):
            count += 1
    return count / len(transactions)

def _calculate_confidence(self, antecedent, consequent, transactions):
    """
    Confidence formula from literature:
    Confidence(X → Y) = Support(X ∪ Y) / Support(X)
    """
    union_support = self._calculate_support(antecedent.union(consequent), transactions)
    antecedent_support = self._calculate_support(antecedent, transactions)

    if antecedent_support == 0:
        return 0
    return union_support / antecedent_support

def _calculate_lift(self, antecedent, consequent, transactions):
    """
    Lift formula from literature (Brin, Motwani, Silverstein 1997):
    Lift(X → Y) = Confidence(X → Y) / Support(Y)
    """
    confidence = self._calculate_confidence(antecedent, consequent, transactions)
    consequent_support = self._calculate_support(consequent, transactions)

    if consequent_support == 0:
        return 0
    return confidence / consequent_support
```

**Apriori Algorithm with bitmap optimization** for performance:

```python
def generate_association_rules(self, transactions):
    """
    Real Apriori algorithm with formulas from literature
    Reference: Agrawal, R., Srikant, R. (1994) "Fast algorithms for mining association rules"
    """
    # 1. Bitmap pruning for performance
    frequent_itemsets = self._find_frequent_itemsets_with_bitmap(transactions)

    # 2. Generate rules using real formulas
    rules = []
    for itemset, support in frequent_itemsets.items():
        if len(itemset) == 2:  # Focus on product pairs
            items = list(itemset)
            item1, item2 = items[0], items[1]

            # Calculate metrics using real formulas
            confidence = self._calculate_confidence(
                frozenset([item1]), frozenset([item2]), transactions
            )
            lift = self._calculate_lift(
                frozenset([item1]), frozenset([item2]), transactions
            )

            if confidence >= self.min_confidence:
                rules.append({
                    'product_1': item1,
                    'product_2': item2,
                    'support': support,
                    'confidence': confidence,
                    'lift': lift
                })

    return rules
```

---

### 4. `frontend/src/components/CartContent/CartContent.jsx` – 🛒 **Client Sees Recommendations**

When the user has products in their cart:

```js
const response = await axios.get(
  `${config.apiUrl}/api/frequently-bought-together/?${params.toString()}`
);
```

The returned rules from backend are used to display:

- Product name
- Image
- Price
- **Confidence %** (real metric from Apriori algorithm)

```jsx
<span>Confidence: {(rec.confidence * 100).toFixed(0)}%</span>
```

---

### 5. `frontend/src/components/AdminPanel/AdminStatistics.jsx` – 📊 **Admin Sees All Rules**

Admin panel shows all current rules from:

```js
fetch(`${config.apiUrl}/api/association-rules/`);
```

Data is shown in a table with **real Apriori metrics**:

- Product 1 & 2
- **Support %** - how often pair occurs
- **Confidence %** - probability of buying B when bought A
- **Lift** - rule strength vs. random chance

Admins can also click "**Update Rules**":

```js
await fetch(`${config.apiUrl}/api/update-association-rules/`);
```

➡️ This triggers a full recalculation of rules manually.

---

## 🤖 How It Works (Step by Step)

### 🔁 After Each Order

1. User checks out → `/api/orders/`
2. Django `signals.py` detects new `Order`
3. `run_all_analytics_after_order()` triggers
4. `generate_association_rules_after_order()` builds transactions
5. `CustomAssociationRules.generate_association_rules()` uses **real Apriori formulas**
6. Results saved in `ProductAssociation` table with support/confidence/lift metrics

### 🛒 In Cart Page

1. Items in cart detected in `CartContent.jsx`
2. `GET /api/frequently-bought-together/?product_ids=...`
3. Top related products returned (based on `confidence`)
4. Shown under **"Frequently Bought Together"** with real metrics

### 👨‍💼 In Admin Panel

1. Admin opens `AdminStatistics.jsx`
2. Data fetched from `/api/association-rules/`
3. Table displays all rules with **real Apriori metrics**
4. Admin can click **Update Rules** (manual refresh)

---

## 📊 Real Mathematical Formulas Used

### Formulas from Scientific Literature:

```
Support(A,B) = |transactions containing both A and B| / |total transactions|

Confidence(A→B) = Support(A,B) / Support(A)

Lift(A→B) = Confidence(A→B) / Support(B)

Conviction(A→B) = (1 - Support(B)) / (1 - Confidence(A→B))
```

### Metrics Interpretation:

- **Support = 0.05** → Pair occurs in 5% of transactions
- **Confidence = 0.80** → If A is bought, B is purchased in 80% of cases
- **Lift = 2.5** → Rule is 2.5x stronger than random chance
- **Lift > 1** → Positive correlation, **Lift < 1** → Negative correlation

---

## 🔬 Algorithmic Optimizations

### Bitmap Pruning:

```python
# Convert transactions to bitmaps for fast operations
for transaction in transactions:
    bitmap = 0
    for item in transaction:
        if item in item_to_id:
            bitmap |= (1 << item_to_id[item])
    transaction_bitmaps.append(bitmap)

# Fast checking if pair occurs together
count = 0
for transaction_bitmap in transaction_bitmaps:
    if (transaction_bitmap & pair_bitmap) == pair_bitmap:
        count += 1
```

### Bulk Operations:

- `bulk_create()` for database efficiency
- Result caching with timeout
- Limit to max 1000 rules for UI performance

---

## 📌 Is It Random?

**NO - it's not random.**

Association rules are **fully data-driven**. They are based on:

- Real `Order` and `OrderProduct` entries
- All historical transactions are processed
- No `random.uniform()` or artificial generation
- **Real association mining algorithm** (Apriori-style)
- Mathematical formulas from scientific literature (Agrawal & Srikant 1994)

---

## ✅ Summary of Key Files and Their Role

| File                                                       | Role                                                                 |
| ---------------------------------------------------------- | -------------------------------------------------------------------- |
| `models.py → ProductAssociation`                           | Stores actual association rule data with Apriori metrics             |
| `custom_recommendation_engine.py → CustomAssociationRules` | Implements real Support, Confidence, Lift formulas                   |
| `signals.py → run_all_analytics_after_order()`             | Triggers rule generation when an order is placed                     |
| `signals.py → generate_association_rules_after_order()`    | Core logic that computes product relationships                       |
| `CartContent.jsx`                                          | Shows "Frequently Bought Together" suggestions                       |
| `AdminStatistics.jsx`                                      | Lets admin review and regenerate association rules manually          |
| API Endpoints                                              | `/api/frequently-bought-together/`, `/api/update-association-rules/` |

---

## 🚀 What's Dynamic? What's Manual?

| Event                     | Regenerates Rules? | Uses Real Formulas? |
| ------------------------- | ------------------ | ------------------- |
| ✅ User places order      | ✅ Yes (automatic) | ✅ Yes (Apriori)    |
| ✅ Admin clicks "Update"  | ✅ Yes (manual)    | ✅ Yes (Apriori)    |
| ❌ Adding product to cart | ❌ No              | -                   |
| ❌ Viewing product page   | ❌ No              | -                   |

---

## 🔍 Bibliography

- Agrawal, R., Srikant, R. (1994). "Fast algorithms for mining association rules in large databases"
- Brin, S., Motwani, R., Silverstein, C. (1997). "Beyond market baskets: Generalizing association rules to correlations"
- Tan, P., Steinbach, M., Kumar, V. (2005). "Introduction to Data Mining" - Association Rules chapter
