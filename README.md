# Product Recommendation Platform Using Machine Learning and Uncertainty Modeling

## Project Description

This project is a product recommendation platform that leverages advanced machine learning algorithms, uncertainty modeling, and user data analysis. The system aims to personalize recommendations based on purchase history, product attributes, and user reviews. The project integrates techniques such as:

- **Collaborative Filtering**
  - Identifying similarities between users (User-Based) and products (Item-Based).
- **Content-Based Filtering**
  - Analyzing product attributes and matching them to user preferences.
- **Fuzzy Logic**
  - Handling imprecise data, such as "low price" or "high quality."
- **Sentiment Analysis**
  - Evaluating product reviews using NLP techniques.

The platform consists of a Django-based backend and a React-based frontend application.

![Full Screen Screenshot](images/mobile_home.png)

---

## Features

- **Product Recommendations:**

  - Based on user purchase history.
  - Considering product attributes and sentiment analysis.
  - Dynamically adjusted recommendations in real-time.

- **Data Management:**
  - User login and registration.
  - Product and transaction management.
  - Data visualization using frontend libraries.

---

## Technologies

**Backend:**

- Python, Django, Django REST Framework
- PostgreSQL (database)
- scikit-learn (machine learning)
- fuzzywuzzy, scikit-fuzzy (fuzzy logic)
- spaCy, NLTK (natural language processing)

**Frontend:**

- React
- Redux (state management)
- Material-UI (UI framework)
- D3.js, Chart.js (data visualization)

---

## How to Run the Project

### Prerequisites

- Python 3.8+
- Node.js (version 16 or newer)
- PostgreSQL
- npm or yarn (for managing frontend packages)

### Step 1: Clone the Repository

```bash
# Clone the repository to your local machine
git clone https://github.com/dawidolko/Django-React-Project-SmartRecommender.git
cd Django-React-Project-SmartRecommender
```

---

### Running the Backend (Django)

1. **Set up a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure the database:**

   - Create a PostgreSQL database and update the access details in the `settings.py` file (DATABASES section).

3. **Apply migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create an admin account:**

   ```bash
   python manage.py createsuperuser
   ```

5. **Run the backend server:**
   ```bash
   python manage.py runserver
   ```

The backend will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

### Running the Frontend (React)

1. **Navigate to the `frontend` directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install  # or yarn install
   ```

3. **Start the frontend application:**
   ```bash
   npm start  # or yarn start
   ```

The frontend will be available at [http://localhost:3000/](http://localhost:3000/).

---

### Optional: Running Only the Frontend (React)

1. **Install dependencies and start the app:**
   ```bash
   cd frontend
   npm install
   npm start
   ```

You can configure a mock API or use local test data.

---

## Directory Structure

```plaintext
product-recommendation-platform/
├── backend/        # Backend code (Django)
├── frontend/       # Frontend code (React)
├── requirements.txt  # Python dependencies
├── README.md      # README file (this document)
└── .gitignore     # Git ignore file
```

---

## Authors

- Dawid Olko
- Piotr Smoła

This project was created as part of an engineering thesis under the supervision of Dr. Grochowalski.

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).

---

## Contact

For questions regarding this project, please contact us via GitHub or email.
