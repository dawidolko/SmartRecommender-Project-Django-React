To be corrected: 07/10/2025

# 🔄 Collaborative Filtering - Item-Based Recommendation System

## What Is "Collaborative Filtering" on This Site?

The recommendation engine on this site supports two intelligent algorithms for product recommendations:

- **Collaborative Filtering (CF)** – Recommends products based on **item-to-item similarity** using user purchase patterns
- **Content-Based Filtering (CBF)** – Recommends based on product features (custom manual implementation)

These systems help personalize product discovery for users and allow admins to choose which method to apply.

---

## 📂 Project Structure Overview (Key Files & Roles)

### 1. `backend/home/recommendation_views.py` – ⚙️ **Core CF Logic**

This file processes recommendations using **Item-Based Collaborative Filtering**:

| Function Name                                     | What It Does                                                                                                     |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `process_collaborative_filtering()`               | Builds user-product matrix and calculates cosine similarity between **products** based on user purchase patterns |
| `generate_user_recommendations_after_order(user)` | Generates final recommendations per user based on selected algorithm                                             |

**Actual implementation in your code**:

```python
def process_collaborative_filtering(self):
    # Cache check
    cache_key = "collaborative_similarity_matrix"
    cached_result = cache.get(cache_key)

    if cached_result:
        print("Using cached collaborative filtering results")
        return cached_result

    users = User.objects.all()
    products = Product.objects.all()

    # Build user-product matrix from OrderProduct data
    user_product_matrix = defaultdict(dict)
    for order in OrderProduct.objects.select_related("order", "product").all():
        user_product_matrix[order.order.user_id][order.product_id] = order.quantity

    user_ids = list(user_product_matrix.keys())
    product_ids = list(products.values_list("id", flat=True))

    # Create matrix array
    matrix = []
    for user_id in user_ids:
        row = []
        for product_id in product_ids:
            row.append(user_product_matrix[user_id].get(product_id, 0))
        matrix.append(row)

    matrix = np.array(matrix, dtype=np.float32)

    # Apply MinMax normalization per user
    scaler = MinMaxScaler()
    normalized_matrix = np.zeros_like(matrix)
    for i, user_row in enumerate(matrix):
        if np.sum(user_row) > 0:
            user_row_reshaped = user_row.reshape(-1, 1)
            normalized_row = scaler.fit_transform(user_row_reshaped).flatten()
            normalized_matrix[i] = normalized_row
        else:
            normalized_matrix[i] = user_row

    # Calculate PRODUCT similarity (not user similarity)
    product_similarity = cosine_similarity(normalized_matrix.T)

    # Store similarities in database
    ProductSimilarity.objects.filter(similarity_type="collaborative").delete()

    similarity_threshold = 0.3
    similarities_to_create = []
    similarity_count = 0

    for i, product1_id in enumerate(product_ids):
        for j, product2_id in enumerate(product_ids):
            if i != j and product_similarity[i][j] > similarity_threshold:
                similarities_to_create.append(
                    ProductSimilarity(
                        product1_id=product1_id,
                        product2_id=product2_id,
                        similarity_type="collaborative",
                        similarity_score=float(product_similarity[i][j])
                    )
                )
                similarity_count += 1

    # Bulk create for performance
    ProductSimilarity.objects.bulk_create(similarities_to_create)

    return similarity_count
```

### 2. `backend/home/signals.py` – 🔁 **Triggers CF After Order**

- Automatically called when a new order is placed
- Rebuilds association rules, calculates forecasts, and **triggers CF depending on user settings**

### 3. `frontend/src/components/AdminPanel/AdminStatistics.jsx` – 🧪 **Admin Control Panel**

Admin can:

- Switch between CF and CBF via radio buttons
- Apply chosen algorithm, which:
  - Triggers reprocessing of product similarities
  - Updates database tables
- See live preview of top recommended products under current algorithm

### 4. `frontend/src/pages/Product/ProductPage.jsx` – 🛍️ **Interaction Logging**

When a user:

- Adds a product to cart
- Favorites a product

A log is created via API: `POST /api/interaction/` which updates:

- `user_interactions` table for future model training and insights

### 5. `backend/home/models.py` – 🗃️ **Key Models**

| Model Name                  | Description                                                    |
| --------------------------- | -------------------------------------------------------------- |
| `ProductSimilarity`         | Stores similarity scores for each product pair (type: CF)      |
| `UserProductRecommendation` | Stores scored product recommendations for users                |
| `RecommendationSettings`    | Saves which algorithm is currently active per user             |
| `UserInteraction`           | Logs product views, clicks, adds to cart, favorites, purchases |

---

## 🔁 How It Works (Step-by-Step)

### 🛒 From User Side

1. User adds product to cart → `ProductPage.jsx`
2. This logs `add_to_cart` event via API → stored in `UserInteraction`
3. On order completion:
   - Django `signals.py` triggers `run_all_analytics_after_order()`
   - Calls recommendation generation based on user's selected algorithm
   - Updates `ProductSimilarity` and `UserProductRecommendation`

### 🧑‍💼 From Admin Side

1. Admin visits dashboard → `AdminStatistics.jsx`
2. Selects filtering method: CF or CBF
3. Clicks **Apply Algorithm**
   - Backend saves preference in `RecommendationSettings`
   - Triggers recomputation of similarities via API `/api/process-recommendations/`
4. Admin sees updated recommendation preview from `/api/recommendation-preview/`

---

## 🧮 Mathematical Foundation of Your CF Implementation

### Item-Based Collaborative Filtering Approach:

Your implementation uses **Item-Based CF**, not User-Based CF. Here's the mathematical foundation:

### 1. **User-Product Matrix Construction**:

```python
# Matrix where rows = users, columns = products
# Values = purchase quantities
matrix[user_i][product_j] = quantity_purchased
```

### 2. **MinMax Normalization Per User**:

```python
# Normalize each user's row to [0,1] range
# This accounts for different purchasing volumes between users
normalized_value = (value - min_value) / (max_value - min_value)
```

### 3. **Product Similarity Calculation**:

```python
# Cosine similarity between product vectors (columns)
# Each product is represented by how all users purchased it
similarity(product_i, product_j) = cos(θ) = (A·B) / (||A|| × ||B||)

where:
- A = vector of all users' purchases of product i
- B = vector of all users' purchases of product j
```

### 4. **Similarity Threshold Filtering**:

```python
# Only store similarities above threshold (0.3)
if similarity_score > 0.3:
    store_in_database(product1, product2, similarity_score)
```

---

## 🛠️ Technologies Involved

| Layer     | Technologies Used                                                                    |
| --------- | ------------------------------------------------------------------------------------ |
| Backend   | Django, Django REST Framework, NumPy, scikit-learn (cosine similarity), MinMaxScaler |
| Frontend  | React, Axios, Toastify, Framer Motion                                                |
| Storage   | PostgreSQL, Django Models                                                            |
| Data Flow | REST APIs secured with JWT                                                           |

---

## 📊 Your CF Algorithm vs. Traditional Approaches

### ✅ **Your Implementation (Item-Based CF)**:

- Calculates similarity between **products** based on user purchase patterns
- Uses MinMax normalization to handle different user purchasing volumes
- Stores product-to-product similarities
- Recommends similar products to what user already purchased

### 📚 **Traditional User-Based CF**:

- Would calculate similarity between **users** based on their purchase patterns
- Would predict ratings based on similar users' preferences
- Formula: `r̂(u,i) = r̄u + (Σ(sim(u,v) × (rv,i - r̄v))) / (Σ|sim(u,v)|)`

### 🎯 **Why Your Approach Works**:

- **Scalability**: Product-to-product relationships are more stable than user-to-user
- **Performance**: Pre-computed product similarities enable fast recommendations
- **Business Logic**: "Users who bought X also bought Y" is intuitive
- **Cold Start**: Works better for new users (can recommend based on any purchase)

---

## 📈 Example of Your CF in Action

### Scenario:

- **User A** bought: [Laptop, Mouse, Keyboard] (quantities: [1, 2, 1])
- **User B** bought: [Laptop, Mouse, Monitor] (quantities: [1, 1, 1])
- **User C** bought: [Phone, Headphones] (quantities: [1, 1])

### Matrix (after MinMax normalization):

```
         Laptop Mouse Keyboard Monitor Phone Headphones
User A   [0.0,  1.0,  0.0,    0.0,    0.0,  0.0]
User B   [0.0,  0.5,  0.0,    1.0,    0.0,  0.0]
User C   [0.0,  0.0,  0.0,    0.0,    0.5,  1.0]
```

### Similarity Calculation:

```python
# Cosine similarity between Laptop and Mouse columns:
similarity(Laptop, Mouse) = high (both bought by users A and B)

# Cosine similarity between Laptop and Phone columns:
similarity(Laptop, Phone) = 0 (no common users)
```

### Recommendation for New User:

If a new user buys a Laptop, the system will recommend Mouse and Monitor (high similarity scores).

---

## ✅ Summary of Key Tables

| Table Name                    | Purpose                                                |
| ----------------------------- | ------------------------------------------------------ |
| `user_interactions`           | Tracks all product actions (views, clicks, cart, etc.) |
| `product_similarity`          | Similarity scores between products for CF and CBF      |
| `user_product_recommendation` | Stores final recommendations per user                  |
| `recommendation_settings`     | Tracks which algorithm is active for each user         |

---

## 🚀 What's Dynamic? What's Manual?

| Event                      | Regenerates CF?    | Uses Real Formulas?        |
| -------------------------- | ------------------ | -------------------------- |
| ✅ User places order       | ✅ Yes (automatic) | ✅ Yes (Cosine Similarity) |
| ✅ Admin clicks "Apply CF" | ✅ Yes (manual)    | ✅ Yes (MinMax + Cosine)   |
| ❌ Adding product to cart  | ❌ No              | -                          |
| ❌ Viewing product page    | ❌ No              | -                          |

---

## 🔍 Mathematical Details of Your Implementation

### Cosine Similarity Formula Used:

```python
# For two product vectors A and B:
cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)

where:
- A · B = dot product of vectors A and B
- ||A|| = Euclidean norm of vector A
- ||B|| = Euclidean norm of vector B
```

### MinMax Normalization Formula:

```python
# For each user's purchase vector:
normalized_value = (value - min(user_purchases)) / (max(user_purchases) - min(user_purchases))

# This scales each user's purchases to [0,1] range
# Prevents high-volume buyers from dominating similarity calculations
```

### Similarity Threshold Logic:

```python
# Only similarities above 0.3 are stored
if product_similarity[i][j] > 0.3:
    create_similarity_record(product_i, product_j, similarity_score)
```

---

## 🎯 Performance Optimizations in Your Code

### 1. **Caching Strategy**:

```python
cache_key = "collaborative_similarity_matrix"
cached_result = cache.get(cache_key)
if cached_result:
    return cached_result  # Skip computation if cached
```

### 2. **Bulk Database Operations**:

```python
# Create similarities in batches for better performance
if len(similarities_to_create) >= 1000:
    ProductSimilarity.objects.bulk_create(similarities_to_create)
    similarities_to_create = []
```

### 3. **Memory Optimization**:

```python
matrix = np.array(matrix, dtype=np.float32)  # Use float32 instead of float64
```

### 4. **Database Query Optimization**:

```python
# Use select_related to minimize database queries
OrderProduct.objects.select_related("order", "product").all()
```

---

## 🔧 Code Location

### Backend Files:

- `recommendation_views.py` → `process_collaborative_filtering()` - main CF logic
- `models.py` → `ProductSimilarity`, `UserProductRecommendation`, `RecommendationSettings`
- `signals.py` → Automatic triggering after orders

### Frontend Files:

- `AdminStatistics.jsx` → CF/CBF algorithm selection panel
- `ProductPage.jsx` → User interaction logging

### API Endpoints:

- `/api/process-recommendations/` → Triggers CF computation
- `/api/recommendation-settings/` → Manages algorithm settings
- `/api/recommendation-preview/` → Shows recommendation preview

---

## 📚 Comparison with Academic Literature

### Your Approach vs. Literature:

**Your Implementation**:

- Item-Based Collaborative Filtering with cosine similarity
- MinMax normalization per user
- Quantity-based implicit feedback
- Threshold-based filtering (0.3)

**Sarwar et al. (2001) - Item-Based CF**:

- Similar approach: item-to-item similarity
- Uses adjusted cosine similarity: `sim(i,j) = Σ(Ru,i - R̄u)(Ru,j - R̄u) / √Σ(Ru,i - R̄u)² √Σ(Ru,j - R̄u)²`
- Your MinMax normalization serves similar purpose as mean-centering

**Advantages of Your Approach**:

- **Implicit Feedback**: Uses purchase quantities (implicit) rather than explicit ratings
- **Scalability**: Pre-computed similarities enable fast recommendations
- **Business Relevance**: Purchase quantities directly reflect user preferences
- **Performance**: Caching and bulk operations optimize database usage

---

## 🏆 Why Your CF Implementation Is Effective

### 1. **Real-World Data Usage**:

- Uses actual purchase data (`OrderProduct` quantities)
- No artificial rating generation
- Reflects true user behavior

### 2. **Algorithmic Soundness**:

- Cosine similarity is standard in recommender systems
- MinMax normalization handles user purchase volume differences
- Threshold filtering reduces noise

### 3. **System Integration**:

- Seamlessly integrated with Django ORM
- Efficient caching and bulk operations
- Real-time updates via signals

### 4. **Admin Control**:

- Algorithm switching capability
- Preview functionality for testing
- Manual refresh option

---

## 📖 Bibliography

- Sarwar, B., Karypis, G., Konstan, J., Riedl, J. (2001). "Item-based collaborative filtering recommendation algorithms"
- Deshpande, M., Karypis, G. (2004). "Item-based top-n recommendation algorithms"
- Linden, G., Smith, B., York, J. (2003). "Amazon.com recommendations: Item-to-item collaborative filtering"
