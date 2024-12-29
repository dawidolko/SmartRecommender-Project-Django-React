# Product Recommendation Platform

## Project Overview

This project, developed by Dawid Olko and Piotr Smoła under the supervision of Dr. Grochowalski, aims to create a product recommendation platform based on user data analysis using machine learning and uncertainty modeling. Below is a detailed description of the key aspects and stages of the project.

---

## I. Recommendation Algorithms Based on User History

### 1. Collaborative Filtering

- **Methodology:**
  - **User-Based Collaborative Filtering:**
    - Establishing similarities between users based on product ratings or purchase history.
    - Using similarity measures such as Pearson correlation or cosine similarity to calculate user similarities.
  - **Item-Based Collaborative Filtering:**
    - Analyzing similarities between products based on the purchase history of different users.
    - Recommending products with similar purchasing patterns to other users.
- **Implementation in the Project:**
  - Collecting user purchase data.
  - Calculating similarities using measures such as cosine similarity or Pearson correlation.
  - Generating recommendations based on historical purchase similarities.

### 2. Content-Based Filtering

- **Methodology:**
  - Recommending products similar to those already rated by the user, based on their attributes (e.g., categories, tags, descriptions).
  - Analyzing product attributes using algorithms such as TF-IDF to process product descriptions.
- **Implementation in the Project:**
  - Profiling users based on their purchase history.
  - Profiling products (e.g., "category," "description").
  - Calculating similarities between products and users based on textual attributes.

---

## II. Uncertainty Modeling in Data Using Machine Learning

### 1. Probabilistic Models (e.g., Naive Bayes Classifier)

- **Methodology:**
  - Using Naive Bayes Classifier to predict the probability of users being interested in products based on past actions and ratings.
- **Implementation in the Project:**
  - Feature extraction: Collecting data on user preferences and product attributes.
  - Training the model: Training the Naive Bayes classifier in Python using scikit-learn.
  - Prediction: Estimating the probability of user interest in a given product.

### 2. Fuzzy Decision Systems

- **Methodology:**
  - Using fuzzy decision rules to handle data imprecision, such as "low price" or "high quality."
- **Implementation in the Project:**
  - Defining membership functions for product attributes.
  - Creating fuzzy rules based on "expert" input and applying inference engines in Python (e.g., using fuzzywuzzy).

---

## III. Dynamic Recommendations and Offer Customization

### 1. Sentiment-Based Recommendations

- **Methodology:**
  - Using Natural Language Processing (NLP) and classification algorithms (e.g., SVM or Random Forest) to analyze sentiment in product reviews.
- **Implementation in the Project:**
  - Collecting data: Analyzing user reviews and opinions.
  - Processing natural language (NLP): Analyzing texts using libraries such as scikit-learn or spaCy.
  - Sentiment classification: Categorizing reviews as positive or negative.

---

## Recommended Tools and Technologies

### Backend:

- Django (backend and API)
- Python, scikit-learn (machine learning)
- PostgreSQL (database)
- fuzzywuzzy, scikit-fuzzy (fuzzy logic)

### Frontend:

- React (user interface)
- Redux (state management)
- Material-UI (UI framework)
- D3.js, Chart.js (data visualization)

### Data Analysis:

- NLP: Using spaCy, NLTK for text analysis and sentiment detection.

---

## Work Distribution

### Stage 1: Project Setup and Structure

- **Person 1:**
  - Backend: Initializing Django project, connecting to PostgreSQL, configuring Django REST Framework.
  - Frontend: Preparing a basic API integration template (e.g., setting up endpoints for the frontend to use once the API is functional).
  - Creating basic models (Users, Products, Transactions) – structure without recommendation logic.
  - Creating initial, simple backend endpoints (e.g., product list, user registration/login).
- **Person 2:**
  - Frontend: Initializing React project, preparing component structure (homepage, product list, product details).
  - Integration with a mocked backend (using fake API or static data) based on preliminary endpoint documentation from Person 1.
  - Backend: Assisting in refining the database schema and initial test migrations, consulting models with Person 1.

### Stage 2: Extending Backend and Frontend Integration

- **Person 1:**
  - Backend: Implementing migrations and seeders, populating with test data.
  - Adding endpoints for fetching/updating user and product data.
  - Frontend: Preparing a basic login form and connecting it to the backend authentication mechanism (e.g., JWT tokens).
- **Person 2:**
  - Frontend: Integrating the frontend authentication (login, displaying product lists) with real endpoints.
  - Adding filters, search functionality, basic component tests, and Material-UI styling.
  - Backend: Verifying and refining endpoints to meet frontend needs.

### Stage 3: Implementing Recommendation Algorithms – Part I (CF and CBF)

- **Person 1:**
  - Backend (ML): Implementing Collaborative Filtering (CF). Fetching transactional data, calculating similarities, and creating an endpoint for CF recommendations.
  - Frontend: Adding a placeholder "Recommended" component and basic logic to display recommendations from the CF endpoint.
- **Person 2:**
  - Backend (ML): Implementing Content-Based Filtering (CBF). Analyzing product attributes (e.g., TF-IDF), and creating an endpoint for recommendations based on attributes.
  - Frontend: Integrating the CBF recommendations view with existing components and adding integration tests.

### Stage 4: Implementing Recommendation Algorithms – Part II (Naive Bayes, Fuzzy Logic)

- **Person 1:**
  - Backend (ML): Implementing Naive Bayes. Training the model in Python and adding an endpoint for probabilistic recommendations.
  - Frontend: Integrating Naive Bayes results on the frontend (e.g., a section for probabilistic recommendations).
- **Person 2:**
  - Backend (ML): Implementing fuzzy logic. Defining fuzzy rules (e.g., low price, high quality) and integrating with the API to return fuzzy-based recommendations.
  - Frontend: Adding components (e.g., sliders or checkboxes) to allow users to adjust fuzzy rule parameters.

### Stage 5: Sentiment Analysis and Dynamic Recommendations (NLP)

- **Person 1:**
  - Backend (NLP): Implementing sentiment analysis (spaCy, NLTK), creating an endpoint that includes sentiment-based recommendations.
  - Frontend: Adding sentiment information to the interface (e.g., percentage of positive reviews).
- **Person 2:**
  - Backend (NLP): Configuring NLP pipelines, refining sentiment model parameters (e.g., tokenization, stopword removal).
  - Frontend: Adding a filter to display products with positive sentiment and performing basic A/B tests.

---

This README provides a comprehensive guide to the platform's development, methodology, and technical stack. The work distribution ensures efficient collaboration and modular implementation of key features. Further refinements and iterations will continue as the project progresses.
