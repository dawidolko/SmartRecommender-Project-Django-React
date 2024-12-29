# Product Recommendation Platform – Backend

## Overview

This Django-based backend serves as the core of our product recommendation system. It manages user data, product information, and multiple recommendation algorithms (Collaborative Filtering, Content-Based Filtering, Naive Bayes, Fuzzy Logic, and Sentiment Analysis). The backend provides RESTful APIs to the React frontend, enabling seamless data exchange and real-time recommendation generation.

---

## Key Features

1. **RESTful API Endpoints**

   - Built with Django REST Framework to expose user, product, and transaction data.
   - Provides dedicated endpoints for multiple recommendation methods (CF, CBF, Naive Bayes, etc.).

2. **Machine Learning Integration**

   - Utilizes Python libraries like **scikit-learn**, **scikit-fuzzy**, and **spaCy** to run recommendation algorithms and sentiment analysis.
   - Offers endpoints returning recommendations and probability scores for personalized product suggestions.

3. **Authentication and Security**

   - Implements user registration/login, token-based authentication (JWT), and essential security measures to protect data integrity.

4. **Fuzzy Logic & Uncertainty Modeling**

   - Leverages fuzzy decision systems (e.g., fuzzywuzzy, scikit-fuzzy) to handle vague criteria like “low price” or “high quality” for more intuitive user recommendations.

5. **Sentiment Analysis**
   - Processes user reviews using NLP libraries (spaCy, NLTK), scoring products based on positive or negative sentiment to refine recommendations further.

---

## Tech Stack

- **Django & Django REST Framework**
- **PostgreSQL** for data storage (connection details configured in `settings.py`).
- **scikit-learn**, **spaCy**, **NLTK**, **scikit-fuzzy** for ML tasks.
- **fuzzywuzzy** for fuzzy rule management.

---

## How It Works

1. **Data Pipeline**: Collects user interactions (purchases, ratings) to train and update models in real-time or via scheduled background tasks.
2. **Recommendation Services**:

   - **Collaborative Filtering**: Exploits purchase patterns among similar users or products.
   - **Content-Based Filtering**: Analyzes product attributes to suggest similar items.
   - **Naive Bayes**: Assigns probability scores based on user behavior and product features.
   - **Fuzzy Logic**: Incorporates expert rules with flexible membership functions.
   - **Sentiment Analysis**: Rates products via user reviews and boosts relevant suggestions.

3. **Exposing Endpoints**: The backend provides JSON responses containing recommended items, which the frontend can display in real time.

---

## Getting Started

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Database Migrations**
   ```bash
   python manage.py migrate
   ```
3. **Start Development Server**
   ```bash
   python manage.py runserver
   ```
4. **Configure Environment**
   - Update `DATABASES` in `settings.py` for PostgreSQL.
   - Adjust environment variables for secret keys, debug mode, etc.
