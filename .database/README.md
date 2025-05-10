# Product Recommendation Platform – Database

## Overview

The database layer for our product recommendation system is designed to store and manage user data, product information, transaction logs, and relevant ML metadata. By leveraging PostgreSQL, we ensure robust data integrity, high availability, and ease of integration with Django.

---

## Schema and Entities

### Core Entities

1. **Users**

   - Table: `db_user`
   - Stores account credentials, personal data, and role information (admin/client)
   - Fields include username, email, password, first/last name, and role
   - Forms the foundation for personalization and recommendation systems

2. **Products**

   - Table: `db_product`
   - Contains core product details such as name, description, price, and old_price
   - Connects to categories and tags through many-to-many relationships
   - Includes relations to photos, specifications, and sale information

3. **Categories**

   - Table: `db_category`
   - Hierarchical classification of products
   - Stores category name and description
   - Used for filtering and organizing products

4. **Tags**
   - Table: `db_tag`
   - Additional metadata labels for products
   - Enables more specific product categorization and filtering
   - Used in content-based recommendation algorithms

### E-Commerce Functionality

5. **Orders**

   - Table: `db_order`
   - Captures purchase transactions with date and status
   - Links to the user who placed the order
   - Connected to products through OrderProduct junction table

6. **OrderProduct**

   - Table: `db_order_product`
   - Junction table connecting orders to products
   - Stores quantity of each product in an order
   - Critical for transactional analysis and collaborative filtering

7. **CartItem**

   - Table: `db_cart_item`
   - Stores user's shopping cart contents
   - Tracks products and quantities for each user
   - Used for cart abandonment analysis and recommendations

8. **Complaint**

   - Table: `db_complaint`
   - Customer complaints related to specific orders
   - Includes cause, status, and submission date
   - Valuable for customer satisfaction analysis

9. **Sale**
   - Table: `db_sale`
   - Tracks promotional discounts and sales events
   - Includes discount amount, start date, and end date
   - Products can reference active sales

### Product Details

10. **PhotoProduct**

    - Table: `db_photo_product`
    - Stores paths to product images
    - Multiple photos can be linked to a single product
    - Essential for visual presentation

11. **Specification**

    - Table: `db_specification`
    - Technical specifications for products
    - Includes parameter name and specification details
    - Enhances product search and filtering

12. **Opinion**
    - Table: `db_opinion`
    - User reviews and ratings for products
    - 1-5 rating scale with optional text content
    - Source data for sentiment analysis

### Recommendation Systems

13. **UserInteraction**

    - Table: `method_user_interactions`
    - Tracks all user engagements with products
    - Types include view, click, add_to_cart, purchase, favorite
    - Forms the basis for behavioral recommendation algorithms

14. **ProductSimilarity**

    - Table: `method_product_similarity`
    - Precomputed similarity scores between product pairs
    - Supports two similarity types: collaborative and content-based
    - Powers "similar products" recommendations

15. **UserProductRecommendation**

    - Table: `method_user_product_recommendation`
    - Personalized product recommendations for each user
    - Includes recommendation type and confidence score
    - Precalculated for efficient retrieval

16. **RecommendationSettings**

    - Table: `method_recommendation_settings`
    - User-specific preferences for recommendation algorithms
    - Controls which algorithm is active for each user
    - Enables personalization of recommendation strategy

17. **ProductAssociation**
    - Table: `method_productassociation`
    - Frequently bought together relationships
    - Includes support, confidence, and lift metrics
    - Used for market basket analysis and "frequently bought together" features

### Sentiment Analysis

18. **SentimentAnalysis**

    - Table: `method_sentiment_analysis`
    - Natural language processing results from product opinions
    - Includes sentiment score and category (positive/neutral/negative)
    - Linked to both opinions and products

19. **ProductSentimentSummary**
    - Table: `method_product_sentiment_summary`
    - Aggregated sentiment metrics for each product
    - Includes counts of positive, neutral, and negative opinions
    - Used in search ranking and product scoring

### Probabilistic Models

20. **PurchaseProbability**

    - Table: `method_purchase_probability`
    - Prediction of user's likelihood to buy specific products
    - Includes probability score and confidence level
    - Powers targeted product recommendations

21. **SalesForecast**

    - Table: `method_sales_forecast`
    - Time-series predictions of product sales
    - Includes forecast date, quantities, and confidence intervals
    - Critical for inventory management

22. **UserPurchasePattern**

    - Table: `method_user_purchase_pattern`
    - Analysis of user buying behavior by category
    - Tracks frequency, value, preferred time, and seasonality
    - Used for predictive recommendations and marketing

23. **ProductDemandForecast**

    - Table: `method_product_demand_forecast`
    - Medium-term demand projections (weekly/monthly/quarterly)
    - Includes expected demand, variance, and suggested stock levels
    - Supports inventory optimization

24. **RiskAssessment**
    - Table: `method_risk_assessment`
    - Predictive indicators for business risks
    - Types include customer churn, inventory excess, price sensitivity
    - Provides actionable insights for risk mitigation

---

## Key Features

1. **PostgreSQL as Primary Store**

   - Ensures ACID compliance, index-based optimization, and robust performance for data queries
   - Supports complex JSON fields for storing algorithm-specific data

2. **Normalization & Performance**

   - Maintains a normalized schema with appropriate foreign key relationships
   - Strategic indexes on frequently queried columns for optimal performance
   - Unique constraints where appropriate to maintain data integrity

3. **Integration with Django**

   - Django ORM handles model definitions and migrations
   - Automatic creation of tables, indexes, and constraints
   - Built-in serializers for REST API endpoints

4. **Multi-Algorithm Support**

   - Database structure supports multiple recommendation approaches:
     - Content-based filtering (tags, categories)
     - Collaborative filtering (user interactions, purchases)
     - Association rules (product associations)
     - Sentiment analysis (opinion processing)
     - Probabilistic models (forecasting, purchase patterns)

5. **Real-Time and Batch Processing**
   - Signal-based triggers for real-time recommendation updates
   - Support for scheduled batch processing of recommendation data
   - Efficient storage of precomputed recommendations for quick retrieval

---

## Setup and Configuration

1. **Database Creation**

   - Create a PostgreSQL database and user with proper privileges
   - Update the Django `settings.py` with the correct credentials

2. **Migrations**

   - In the backend root folder, run:
     ```bash
     python manage.py migrate
     ```
   - This step applies all initial migrations for all 24 database tables

3. **Seed Data**

   - Alternatively, use included data generators for realistic test data:
     ```bash
     python manage.py seed
     ```

4. **Maintenance**
   - Regularly run PostgreSQL VACUUM ANALYZE for query optimization
   - Schedule periodic updates of recommendation tables
   - Monitor table growth and performance, particularly for interaction logs

---

## Schema Diagram

The database consists of interconnected tables with the following key relationships:

- Users → Orders → OrderProducts → Products
- Products → Categories/Tags (many-to-many)
- Products → Specifications/Photos (one-to-many)
- Products → Opinions → SentimentAnalysis
- Products ↔ Products (via ProductSimilarity and ProductAssociation)
- Users → UserInteractions → Products
- Users → UserProductRecommendation → Products
