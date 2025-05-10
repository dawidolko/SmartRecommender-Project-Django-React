## 🔗 What Are "Association Rules" on the Site?

**Association rules** are a type of recommendation logic that:

- Identify products that are **frequently bought together**.
- Help clients discover **related products** while shopping.
- Enable admins to view and **manage these relationships** in the dashboard.

These rules are based on **real order history** and are recalculated dynamically when new purchases are made.

---

## 📂 Project Structure Overview (Key Files & Roles)

### 1. `backend/home/models.py` – 📦 **ProductAssociation Model**

```python
class ProductAssociation(models.Model):
    product_1 = models.ForeignKey(Product, related_name='associations_from', ...)
    product_2 = models.ForeignKey(Product, related_name='associations_to', ...)
    support = models.FloatField()
    confidence = models.FloatField()
    lift = models.FloatField()
```

This model stores the association rules, including:

- `support`: how often the pair appears together.
- `confidence`: how likely product_2 is bought if product_1 is.
- `lift`: how much stronger the rule is compared to random chance.

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

- Reads all past orders.
- Extracts product combinations (as transactions).
- Calls `calculate_association_rules(transactions)`.
- Stores results in `ProductAssociation`.

➡️ This ensures rules are **automatically updated** after each new purchase.

---

### 3. `backend/home/api/association.py` – 🧠 **Rule Calculation**

Function: `calculate_association_rules(transactions)`

- Uses the **Apriori** method to find frequent product pairs.
- Returns rules with calculated `support`, `confidence`, `lift`.

```python
rules = calculate_association_rules(transactions)
```

These rules are saved via `get_or_create` into the DB.

---

### 4. `frontend/src/components/Cart/CartContent.jsx` – 🛒 **Client Sees Recommendations**

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
- Confidence %

```jsx
<span>Confidence: {(rec.confidence * 100).toFixed(0)}%</span>
```

---

### 5. `frontend/src/pages/Admin/AdminProbabilistic.jsx` – 📊 **Admin Sees All Rules**

Admin panel shows all current rules from:

```js
fetch(`${config.apiUrl}/api/association-rules/`);
```

Data is shown in a table with:

- Product 1 & 2
- Support %
- Confidence %
- Lift

Admins can also click “**Update Rules**”:

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
5. `calculate_association_rules()` finds frequent pairs
6. Results saved in `ProductAssociation` table

### 🛒 In Cart Page

1. Items in cart detected in `CartContent.jsx`
2. `GET /api/frequently-bought-together/?product_ids=...`
3. Top related products returned (based on `confidence`)
4. Shown under **"Frequently Bought Together"**

### 👨‍💼 In Admin Panel

1. Admin opens `AdminProbabilistic.jsx`
2. Data fetched from `/api/association-rules/`
3. Table displays all rules with support/confidence/lift
4. Admin can click **Update Rules** (manual refresh)

---

## 📌 Is It Random?

**No – it's not random.**

Association rules are **fully data-driven**. They are based on:

- Real `Order` and `OrderProduct` entries
- All historical transactions are processed
- No `random.uniform()` or artificial generation

This is a **real association mining algorithm** (Apriori-style).

---

## ✅ Summary of Key Files and Their Role

| File                                           | Role                                                                 |
| ---------------------------------------------- | -------------------------------------------------------------------- |
| `models.py → ProductAssociation`               | Stores the actual association rule data                              |
| `signals.py → run_all_analytics_after_order()` | Triggers rule generation when an order is placed                     |
| `signals.py → calculate_association_rules()`   | Core logic that computes product relationships                       |
| `CartContent.jsx`                              | Shows “Frequently Bought Together” suggestions                       |
| `AdminProbabilistic.jsx`                       | Lets admin review and regenerate association rules manually          |
| API Endpoints                                  | `/api/frequently-bought-together/`, `/api/update-association-rules/` |

---

## 🚀 What's Dynamic? What's Manual?

| Event                     | Regenerates Rules? |
| ------------------------- | ------------------ |
| ✅ User places order      | ✅ Yes (automatic) |
| ✅ Admin clicks “Update”  | ✅ Yes (manual)    |
| ❌ Adding product to cart | ❌ No              |
| ❌ Viewing product page   | ❌ No              |

---
