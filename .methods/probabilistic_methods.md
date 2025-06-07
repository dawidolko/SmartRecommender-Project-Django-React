To be corrected: 06/06/2025

## 🧠 What Are "Probabilistic Methods" on Site?

Probabilistic methods in site are smart algorithms that:

- **Analyze customer behavior**
- **Predict product demand**
- **Estimate future sales**
- **Detect potential customer churn**
- **Recommend products based on likelihood of interest**

These features make shop smarter by personalizing user experience and helping admins make better business decisions.

---

## 📂 Project Structure Overview (Key Files & Roles)

### 1. `backend/home/analytics.py` – 🔮 **Core Probabilistic Logic**

This file contains all the main functions that do predictions and analytics:

| Function Name                                                 | What It Does                                               |
| ------------------------------------------------------------- | ---------------------------------------------------------- |
| `generate_purchase_probabilities_for_user(user)`              | Predicts how likely a user is to buy each product          |
| `generate_user_purchase_patterns_for_user(user)`              | Tracks how often and when a user buys products by category |
| `generate_risk_assessment_for_user(user)`                     | Checks if the user might stop buying soon (churn risk)     |
| `generate_sales_forecasts_for_products(product_ids)`          | Predicts how many units of each product will sell daily    |
| `generate_product_demand_forecasts_for_products(product_ids)` | Estimates demand over a week, month, and quarter           |

### 2. `backend/home/signals.py` – 🧠 **Auto-Trigger on New Order**

- This file **automatically triggers** all probabilistic functions when a client places a new order.
- It uses Django’s `@receiver(post_save, sender=Order)` signal to catch new orders and call the analytics.

### 3. `backend/home/serializers.py` – 🧾 **API Data Formatting**

- The `OrderSerializer` prepares data for sending to the frontend.
- It handles purchase data and links `OrderProduct` entries to the order.

### 4. `frontend/src/pages/Admin/AdminProbabilistic.jsx` – 📊 **Admin Dashboard for Insights**

This is the main admin page where all predictions and smart data are visualized. It fetches API data like:

- `/api/sales-forecast/` – 📈 Sales forecasts
- `/api/product-demand/` – 📦 Product demand levels
- `/api/risk-dashboard/` – ⚠️ Risk and churn predictions
- `/api/admin-purchase-patterns/` – 👤 Purchase patterns per user
- `/api/admin-product-recommendations/` – 💡 Suggested products

Here, the admin can:

- See daily/weekly/monthly trends
- React to demand (restock alerts)
- Spot users at risk of leaving
- Understand user behavior (patterns)
- View recommended products for each user

### 5. `frontend/src/components/Cart/CartContent.jsx` + `TotalAmount.jsx` – 🛒 **Client Triggers Analytics**

When a client checks out:

- `TotalAmount.jsx` posts the order via Axios (`POST /api/orders/`)
- This activates the backend signal from `signals.py`
- The analytics logic from `analytics.py` is run in the background
- Results are stored in the database (models like `RiskAssessment`, `SalesForecast`, etc.)

---

## 🤖 How It Works (Step by Step)

### 🔁 From Client Side:

1. User adds items to cart → `CartContent.jsx`
2. User clicks **Checkout** → `TotalAmount.jsx`
3. `axios.post('/api/orders/')` sends the order to Django
4. Django creates the order → triggers `signals.py`
5. `run_all_analytics_after_order()` is called
6. `analytics.py` runs:

   - Demand & sales predictions
   - Risk scoring
   - Product recommendations

### 📊 Admin Side:

1. Admin visits **Dashboard** (`AdminProbabilistic.jsx`)
2. Data is loaded via fetch from API endpoints
3. Charts, tables, and modals show:

   - Predicted sales
   - Products to reorder
   - At-risk customers
   - Recommended products
   - Purchase behavior insights

---

## 🛠️ Technologies Involved

| Area      | Tech                                                                                 |
| --------- | ------------------------------------------------------------------------------------ |
| Backend   | Django + Django REST Framework                                                       |
| Frontend  | React, Chart.js, Axios                                                               |
| Models    | Custom Django models: `PurchaseProbability`, `SalesForecast`, `RiskAssessment`, etc. |
| Data Flow | REST API endpoints (secured with JWT token)                                          |

---

## ✅ Summary of Key Files and Their Role

| File                                  | Role                                                 |
| ------------------------------------- | ---------------------------------------------------- |
| `analytics.py`                        | All smart logic (probabilities, forecasting, risk)   |
| `signals.py`                          | Triggers analytics when order is placed              |
| `serializers.py`                      | Formats order data for API                           |
| `AdminProbabilistic.jsx`              | Admin UI to view smart insights                      |
| `CartContent.jsx` / `TotalAmount.jsx` | Client side: handles checkout and triggers analytics |

---

### 🧠 **How it works now (based on randomness)**

Current analytics system uses **random number generation** to simulate intelligent behavior. This applies to several key methods in `analytics.py`:

1. **Purchase Probability (`generate_purchase_probabilities_for_user`)**

   - Uses `random.uniform(0, 0.2)` or similar to generate a base probability that a user will buy a product.
   - Confidence levels are also randomly generated.

2. **Risk Assessment (`generate_risk_assessment_for_user`)**

   - Churn risk scores are assigned randomly based on whether the user has placed a recent order.
   - Mitigation suggestions are static.

3. **Sales Forecasting (`generate_sales_forecasts_for_products`)**

   - Predicts sales based on averages + random seasonal/trend variation.
   - Confidence intervals are based on randomized margins.

4. **Product Demand Forecasting (`generate_product_demand_forecasts_for_products`)**

   - Uses product averages with random multipliers to simulate expected demand and stock recommendations.

In summary, system **mimics analytics** using randomness, which is useful for demonstration or testing purposes, but it does **not reflect real data patterns or customer behavior**.

---

### 🔧 **What needs to change to remove randomness and make it data-driven**

To eliminate random behavior and replace it with real intelligence, consider the following upgrades:

1. **Use actual user behavior data**

   - Track and store past purchases, frequencies, amounts, and categories.
   - Calculate probabilities and frequencies directly from the database instead of using random values.

2. **Integrate machine learning models**

   - Train models for:

     - Churn prediction
     - Product recommendation
     - Demand forecasting

   - You can use scikit-learn, TensorFlow, or external APIs.

3. **Apply statistical forecasting techniques**

   - Use time series models like ARIMA, Prophet, or exponential smoothing instead of randomized trends.

4. **Create meaningful features**

   - For example:

     - Recency, Frequency, Monetary (RFM) analysis for churn
     - Seasonality trends per product
     - Customer segmentation

5. **Automate training + update pipeline**

   - Store historical data and periodically retrain models.
   - Update forecasts and predictions based on new behavior.

---

### ✅ Example of a future change

**Now:**

```python
confidence = Decimal('0.6') + Decimal(random.uniform(0.0, 0.3))
```

**Later:**

```python
confidence = calculate_confidence_based_on_past_orders(user, product)
```

Where `calculate_confidence_based_on_past_orders` would analyze real data instead of using `random`.
