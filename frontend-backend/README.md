# Product Recommendation Platform

## Overview

The Product Recommendation Platform is a full-stack web application designed to provide personalized product recommendations using machine learning and advanced data analysis techniques. It combines a React-based frontend, a Django-powered backend, and PostgreSQL for data storage to deliver a robust, scalable solution.

This project was developed by Dawid Olko and Piotr Smoła under the supervision of Dr. Grochowalski. It explores various recommendation algorithms such as Collaborative Filtering, Content-Based Filtering, Naive Bayes, Fuzzy Logic, and Sentiment Analysis, making it a versatile and data-driven platform.

---

## Features

### Frontend (React)

1. **Interactive User Interface**:

   - Built with React for a dynamic and responsive experience.
   - Utilizes Material-UI for consistent styling and intuitive navigation.

2. **Product Listings and Recommendations**:

   - Displays product lists with filtering, searching, and sorting functionalities.
   - Dynamically shows personalized recommendations based on user interactions.

3. **User Authentication**:

   - Implements user registration, login, and session management using token-based authentication (JWT).

4. **Data Visualization**:
   - Incorporates libraries like D3.js and Chart.js for visual representation of user analytics and recommendation performance.

---

### Backend (Django)

1. **RESTful API**:

   - Developed using Django REST Framework to handle user, product, and transaction data.
   - Provides endpoints for personalized recommendations and sentiment analysis.

2. **Machine Learning Integration**:

   - Implements recommendation algorithms using Python libraries like scikit-learn, scikit-fuzzy, and spaCy.
   - Offers probabilistic and sentiment-based recommendations via dedicated endpoints.

3. **Data Security**:

   - Ensures secure data handling with authentication, authorization, and robust database management.

4. **Flexible Logic**:
   - Incorporates fuzzy logic to model user preferences like "affordable price" or "premium quality."

---

### Database (PostgreSQL)

1. **Scalable Data Storage**:

   - Uses PostgreSQL 17 for efficient data storage and management.
   - Supports complex queries for user behaviors, product attributes, and recommendation results.

2. **Optimized Data Relationships**:
   - Stores normalized tables for users, products, categories, and transactions.
   - Handles Many-to-Many relationships using intermediate tables.

---

## Recommendation Techniques

1. **Collaborative Filtering (CF)**:

   - Suggests products based on user or item similarities.
   - Utilizes historical purchase data and similarity metrics (e.g., cosine similarity).

2. **Content-Based Filtering (CBF)**:

   - Recommends products with similar attributes (e.g., categories, tags).
   - Employs algorithms like TF-IDF for text processing.

3. **Naive Bayes**:

   - Uses probabilistic models to predict user preferences.
   - Based on user actions, ratings, and product features.

4. **Fuzzy Logic**:

   - Applies fuzzy decision-making rules for intuitive recommendations.
   - Allows flexible criteria like "low cost" or "high quality."

5. **Sentiment Analysis**:
   - Analyzes product reviews to gauge user sentiment.
   - Utilizes NLP libraries (spaCy, NLTK) for classification.

---

## Tech Stack

### Frontend:

- **React**: Main framework for building the user interface.
- **Redux**: State management for application-wide consistency.
- **Material-UI**: Component library for responsive design.
- **Chart.js/D3.js**: Data visualization libraries.

### Backend:

- **Django**: Framework for handling API logic and data processing.
- **Django REST Framework**: For creating RESTful APIs.
- **Python Libraries**: scikit-learn, spaCy, scikit-fuzzy, fuzzywuzzy.

### Database:

- **PostgreSQL**: Relational database for scalable data storage.

---

## Getting Started

### Prerequisites

1. **Install Python and Node.js**:

   - Python >= 3.8
   - Node.js >= 16.x

2. **Install PostgreSQL**:
   - Ensure PostgreSQL 17 is installed and running.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-repo/product-recommendation-platform.git
   cd product-recommendation-platform
   ```

2. **Backend Setup**:

   - Create a virtual environment:
     ```bash
     python -m venv .venv
     ```
   - Activate the virtual environment:
     ```bash
     source .venv/bin/activate # On Linux/Mac
     .venv\Scripts\activate    # On Windows
     ```
   - Install backend dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Configure database settings in `settings.py`:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'product_recommendation',
             'USER': 'postgres',
             'PASSWORD': 'admin',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```
   - Apply migrations and seed data:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     python manage.py seed
     ```

3. **Frontend Setup**:

   - Navigate to the frontend directory:
     ```bash
     cd frontend
     ```
   - Install frontend dependencies:
     ```bash
     npm install
     ```
   - Start the development server:
     ```bash
     npm start
     ```

4. **Run the Backend**:

   - WINDOWS:

   ```bash
   start.bat
   ```

   - MACOS/LINUX:

   ```bash
   start.sh
   ```

---

## How It Works

- The frontend interacts with the backend via RESTful APIs to fetch and display data.
- The backend processes data, applies machine learning algorithms, and serves personalized recommendations.
- PostgreSQL manages the data, ensuring efficient and secure storage.

---

## Contributors

- Dawid Olko
- Piotr Smoła

Under the supervision of Dr. Grochowalski.
