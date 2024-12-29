# Product Recommendation Platform – Database

## Overview

The database layer for our product recommendation system is designed to store and manage user data, product information, transaction logs, and relevant ML metadata. By leveraging PostgreSQL, we ensure robust data integrity, high availability, and ease of integration with Django.

---

## Schema and Entities

1. **Users**

   - Stores account credentials, personal data (if required), and user-specific preferences.
   - References transactions, wishlists, and interactions with the recommendation engine.

2. **Products**

   - Contains core product details such as name, description, category, price, and stock.
   - May include additional metadata relevant to recommendation algorithms (e.g., TF-IDF vectors, fuzzy sets).

3. **Transactions**

   - Captures user purchase history, including product IDs, timestamps, quantities, and total cost.
   - Key to Collaborative Filtering and Naive Bayes training sets.

4. **Reviews** (Optional or Future Enhancements)

   - Holds user-generated text reviews or ratings, essential for Sentiment Analysis.
   - Linked to product ID and user ID.

5. **Recommendation Metadata**
   - Persists precomputed similarity matrices or model outputs for quick retrieval, reducing overhead when generating real-time suggestions.

---

## Key Features

1. **PostgreSQL as Primary Store**

   - Ensures ACID compliance, index-based optimization, and robust performance for data queries.

2. **Normalization & Performance**

   - Maintains a normalized schema where possible, ensuring efficient join operations while preventing data redundancy.

3. **Integration with Django**

   - Django ORM handles model definitions and migrations. Migrations ensure version control and consistent deployments across different environments.

4. **Scalability**

   - Optimized for high-volume read operations from the recommendation algorithms. May utilize caching layers (Redis, Memcached) for further speed.

5. **Backup and Migration Strategy**
   - Regular data backups and migrations keep the system up to date and resilient to unexpected failures or schema modifications.

---

## Setup and Configuration

1. **Database Creation**

   - Create a PostgreSQL database (e.g., `smartrecommender`) and user with proper privileges.
   - Update the Django `settings.py` with the correct credentials.

2. **Migrations**

   - In the backend root folder, run:
     ```bash
     python manage.py migrate
     ```
   - This step applies all initial migrations (Users, Products, Transactions, etc.).

3. **Seed Data (Optional)**

   - You can populate the database with sample products and user data for testing the recommendation workflows:
     ```bash
     python manage.py loaddata sample_data.json
     ```

4. **Maintenance**
   - Use `pg_dump` for backups and `vacuum` or `analyze` for performance optimizations.
