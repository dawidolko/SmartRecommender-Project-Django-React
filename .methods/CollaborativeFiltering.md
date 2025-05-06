## 🔄 What Is Collaborative Filtering on This Site?

The recommendation engine on this site supports two intelligent algorithms for product recommendations:

- **Collaborative Filtering (CF)** – Recommends products based on what _similar users_ have purchased.

These systems help personalize product discovery for users and allow admins to choose which method to apply.

---

## 📂 Project Structure Overview (Key Files & Roles)

### 1. `backend/home/views.py` – ⚙️ **Core Logic for CF Processing**

This file processes recommendations using both CF and CBF:

| Function Name                                     | What It Does                                                                                          |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `process_collaborative_filtering()`               | Builds user-product matrix and calculates cosine similarity between products based on user purchases. |
| `generate_user_recommendations_after_order(user)` | Generates final recommendations per user based on selected algorithm.                                 |

### 2. `backend/home/signals.py` – 🔁 **Triggers CF After Order**

- Automatically called when a new order is placed.
- Rebuilds association rules, calculates forecasts, and **triggers CF depending on user settings**.

### 3. `frontend/src/pages/Admin/AdminStatistics.jsx` – 🧪 **Admin Control Panel**

Admin can:

- Switch between CF and CBF via radio buttons.
- Apply chosen algorithm, which:

  - Triggers reprocessing of product similarities.
  - Updates database tables.

- See live preview of top recommended products under current algorithm.

### 4. `frontend/src/pages/Product/ProductPage.jsx` – 🛍️ **Interaction Logging**

When a user:

- Adds a product to cart
- Favorites a product

A log is created via API: `POST /api/log-interaction/` which updates:

- `user_interactions` table for future model training and insights.

### 5. `backend/home/models.py` – 🗃️ **Key Models**

| Model Name                  | Description                                                     |
| --------------------------- | --------------------------------------------------------------- |
| `ProductSimilarity`         | Stores similarity scores for each product pair (type: CF).      |
| `UserProductRecommendation` | Stores scored product recommendations for users.                |
| `RecommendationSettings`    | Saves which algorithm is currently active per user.             |
| `UserInteraction`           | Logs product views, clicks, adds to cart, favorites, purchases. |

---

## 🔁 How It Works (Step-by-Step)

### 🛒 From User Side

1. User adds product to cart → `ProductPage.jsx`
2. This logs `add_to_cart` event via API → stored in `UserInteraction`
3. On order completion:

   - Django `signals.py` triggers `run_all_analytics_after_order()`
   - Calls recommendation generation based on user’s selected algorithm
   - Updates `ProductSimilarity` and `UserProductRecommendation`

### 🧑‍💼 From Admin Side

1. Admin visits dashboard → `AdminStatistics.jsx`
2. Selects filtering method: CF
3. Clicks **Apply Algorithm**

   - Backend saves preference in `RecommendationSettings`
   - Triggers recomputation of similarities via API `/api/process-recommendations/`

4. Admin sees updated recommendation preview from `/api/recommendation-preview/`

---

## 🛠️ Technologies Involved

| Layer     | Techs Used                                                      |
| --------- | --------------------------------------------------------------- |
| Backend   | Django, Django REST Framework, NumPy, scikit-learn (cosine sim) |
| Frontend  | React, Axios, Toastify, Framer Motion                           |
| Storage   | PostgreSQL (or other DB), Django Models                         |
| Data Flow | REST APIs secured with JWT                                      |

---

## ✅ Summary of Key Tables

| Table Name                    | Purpose                                                |
| ----------------------------- | ------------------------------------------------------ |
| `user_interactions`           | Tracks all product actions (views, clicks, cart, etc.) |
| `product_similarity`          | Similarity scores between products for CF and CBF      |
| `user_product_recommendation` | Stores final recommendations per user                  |
| `recommendation_settings`     | Tracks which algorithm is active for each user         |

---
