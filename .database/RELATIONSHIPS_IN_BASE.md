# Database Relationships in the Product Recommendation Platform

## Core Entity Relationships

### 1. **User Table (`db_user`)**

- Inherits from Django's `AbstractUser`
- Has one-to-many relationship with:
  - Orders (`db_order`)
  - Opinions (`db_opinion`)
  - CartItems (`db_cart_item`)
  - UserInteractions (`method_user_interactions`)
  - UserProductRecommendations (`method_user_product_recommendation`)
  - RecommendationSettings (`method_recommendation_settings`)
  - PurchaseProbability (`method_purchase_probability`)
  - UserPurchasePattern (`method_user_purchase_pattern`)

### 2. **Product Table (`db_product`)**

- Has foreign key to Sale (`db_sale`) with `SET_NULL` on deletion
- Many-to-many relationship with Category (`db_category`) via `db_product_category`
- Many-to-many relationship with Tag (`db_tag`)
- Has one-to-many relationship with:
  - PhotoProduct (`db_photo_product`)
  - Specification (`db_specification`)
  - Opinion (`db_opinion`)
- Connected to Orders via `db_order_product` junction table
- Referenced in multiple recommendation tables as described below

### 3. **Category Table (`db_category`)**

- Many-to-many relationship with Product (`db_product`) via `db_product_category`
- Has one-to-many relationship with UserPurchasePattern (`method_user_purchase_pattern`)

### 4. **Tag Table (`db_tag`)**

- Many-to-many relationship with Product (`db_product`)

### 5. **Sale Table (`db_sale`)**

- Has one-to-many relationship with Product (`db_product`)

## E-Commerce Functionality Relationships

### 6. **Order Table (`db_order`)**

- Foreign key to User (`db_user`) with `CASCADE` on deletion
- Has one-to-many relationship with:
  - OrderProduct (`db_order_product`)
  - Complaint (`db_complaint`)

### 7. **OrderProduct Table (`db_order_product`)**

- Junction table between Order and Product
- Foreign key to Order (`db_order`) with `CASCADE` on deletion
- Foreign key to Product (`db_product`) with `CASCADE` on deletion

### 8. **CartItem Table (`db_cart_item`)**

- Foreign key to User (`db_user`) with `CASCADE` on deletion
- Foreign key to Product (`db_product`) with `CASCADE` on deletion

### 9. **Complaint Table (`db_complaint`)**

- Foreign key to Order (`db_order`) with `CASCADE` on deletion

## Product Details Relationships

### 10. **PhotoProduct Table (`db_photo_product`)**

- Foreign key to Product (`db_product`) with `CASCADE` on deletion

### 11. **Specification Table (`db_specification`)**

- Foreign key to Product (`db_product`) with `CASCADE` on deletion

### 12. **Opinion Table (`db_opinion`)**

- Foreign key to Product (`db_product`) with `CASCADE` on deletion
- Foreign key to User (`db_user`) with `CASCADE` on deletion
- Has one-to-one relationship with SentimentAnalysis (`method_sentiment_analysis`)
- Includes a constraint ensuring rating is between 1 and 5
- Has unique constraint on (user, product) ensuring one opinion per product per user

## Recommendation Systems Relationships

### 13. **UserInteraction Table (`method_user_interactions`)**

- Foreign key to User (`db_user`) with `CASCADE` on deletion
- Foreign key to Product (`db_product`) with `CASCADE` on deletion
- Includes indexes on (user, product) and interaction_type for performance

### 14. **ProductSimilarity Table (`method_product_similarity`)**

- Foreign key to Product (`db_product`) as product1 with `CASCADE` on deletion
- Foreign key to Product (`db_product`) as product2 with `CASCADE` on deletion
- Unique together constraint on (product1, product2, similarity_type)

### 15. **UserProductRecommendation Table (`method_user_product_recommendation`)**

- Foreign key to User (`db_user`) with `CASCADE` on deletion
- Foreign key to Product (`db_product`) with `CASCADE` on deletion
- Unique together constraint on (user, product, recommendation_type)

### 16. **RecommendationSettings Table (`method_recommendation_settings`)**

- Foreign key to User (`db_user`) with `CASCADE` on deletion
- Unique together constraint on (user, active_algorithm)

### 17. **ProductAssociation Table (`method_productassociation`)**

- Foreign key to Product (`db_product`) as product_1 with `CASCADE` on deletion
- Foreign key to Product (`db_product`) as product_2 with `CASCADE` on deletion
- Unique together constraint on (product_1, product_2)

## Sentiment Analysis Relationships

### 18. **SentimentAnalysis Table (`method_sentiment_analysis`)**

- Foreign key to Product (`db_product`) with `CASCADE` on deletion
- One-to-one relationship with Opinion (`db_opinion`) with `CASCADE` on deletion
- Includes indexes on product and sentiment_category for efficient filtering

### 19. **ProductSentimentSummary Table (`method_product_sentiment_summary`)**

- One-to-one relationship with Product (`db_product`) with `CASCADE` on deletion
- Serves as aggregated cache of sentiment metrics per product

## Probabilistic Models Relationships

### 20. **PurchaseProbability Table (`method_purchase_probability`)**

- Foreign key to User (`db_user`) with `CASCADE` on deletion
- Foreign key to Product (`db_product`) with `CASCADE` on deletion
- Unique together constraint on (user, product)

### 21. **SalesForecast Table (`method_sales_forecast`)**

- Foreign key to Product (`db_product`) with `CASCADE` on deletion
- Unique together constraint on (product, forecast_date)

### 22. **UserPurchasePattern Table (`method_user_purchase_pattern`)**

- Foreign key to User (`db_user`) with `CASCADE` on deletion
- Foreign key to Category (`db_category`) with `CASCADE` on deletion
- Unique together constraint on (user, category)

### 23. **ProductDemandForecast Table (`method_product_demand_forecast`)**

- Foreign key to Product (`db_product`) with `CASCADE` on deletion
- Unique together constraint on (product, forecast_period, period_start)

### 24. **RiskAssessment Table (`method_risk_assessment`)**

- Doesn't have direct foreign key relationships but uses entity_type ('user' or 'product') and entity_id
- Has indexes on (entity_type, entity_id) and risk_type for efficient querying
