# 🛍️ Product Recommendation Platform Using Machine Learning and Uncertainty Modeling

> **Case:** Build a full-stack platform that delivers personalized product recommendations by combining machine learning, uncertainty modeling, and user behavior analysis. The system enhances user experience through dynamic, intelligent suggestions based on real-world data.

> **Tech Stack:** `Python`, `Django`, `PostgreSQL`, `React`, `Redux`, `Material-UI`, `D3.js`, `scikit-learn`, `fuzzywuzzy`, `spaCy`, `NLTK`.

---

## 🚀 Usage

### Running the Application Locally

- Clone the repository:

```bash
git clone https://github.com/dawidolko/Django-React-Project-SmartRecommender.git
cd Django-React-Project-SmartRecommender
```

- Ensure you have installed:
  - Python 3.8+
  - Node.js (v16+)
  - PostgreSQL
  - npm or yarn

---

### Backend (Django)

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install backend dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your PostgreSQL database in `settings.py`.

4. Apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a Django admin user:

```bash
python manage.py createsuperuser
```

6. Start the backend server:

```bash
python manage.py runserver
```

Backend will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

### Frontend (React)

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install frontend dependencies:

```bash
npm install  # or yarn install
```

3. Start the frontend server:

```bash
npm start  # or yarn start
```

Frontend will be available at [http://localhost:3000/](http://localhost:3000/).

---

## 📈 Features

- **Advanced Product Recommendations:**
  - Collaborative Filtering (User-Based & Item-Based)
  - Content-Based Filtering
  - Real-time dynamic adjustment
  - Sentiment analysis based on user reviews

- **Uncertainty Modeling:**
  - Fuzzy Logic applied to product attributes ("low price", "high quality", etc.)

- **Full Data Management:**
  - User authentication (login/register)
  - Product and transaction database management
  - Visual dashboards for data representation

- **Intuitive UI/UX:**
  - Responsive and user-friendly interface built with Material-UI and D3.js.

---

## 🧠 Technologies

**Backend:**
- Django & Django REST Framework
- PostgreSQL
- scikit-learn
- fuzzywuzzy, scikit-fuzzy
- spaCy, NLTK

**Frontend:**
- React
- Redux
- Material-UI
- D3.js, Chart.js

---

## 📂 Project Structure

```plaintext
product-recommendation-platform/
├── backend/           # Django backend
├── frontend/          # React frontend
├── requirements.txt   # Backend dependencies
├── README.md          # Documentation
└── .gitignore         # Git ignored files
```

---

## 🖼️ Screenshots

[<img src="images/mobile_home.png" width="80%"/>](images/mobile_home.png)

---

## 🧑‍💻 Authors

- Dawid Olko
- Piotr Smoła

> This project was developed as part of an engineering thesis under the supervision of Dr. Grochowalski.

---

## 📜 License

The **Product Recommendation Platform** project is licensed under the [Apache License 2.0](LICENSE).

---

## 📬 Contact

For any questions or suggestions, feel free to open an issue or contact us directly via GitHub.

---
