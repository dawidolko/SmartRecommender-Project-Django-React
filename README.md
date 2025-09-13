# 🛍️ SmartRecommender: Product Recommendation Platform

> **Project Description:** A comprehensive full-stack platform that delivers personalized product recommendations by combining machine learning, uncertainty modeling, and user behavior analysis. This system enhances user experience through dynamic, intelligent suggestions based on real-world data.

> **Tech Stack:** `Python`, `Django`, `PostgreSQL`, `React`, `scikit-learn`, `Docker`

---

## 🚀 Usage

### Option 1: Docker Setup (Recommended)

The easiest way to run the project is using Docker. This ensures consistent environment across all platforms.

#### Prerequisites

- **Docker Desktop** installed on your system
- **Hardware virtualization** enabled (Intel VT-x or AMD-V)

#### Quick Start with Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dawidolko/SmartRecommender-Project-Django-React
   cd SmartRecommender-Project-Django-React
   ```

2. **Create environment file:**

   ```bash
   # Create .env file in the root directory
   DB_NAME=product_recommendation
   DB_USER=postgres
   DB_PASSWORD=admin
   DB_HOST=db
   DB_PORT=5432
   SECRET_KEY=django-insecure-default-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

3. **Build and run with Docker:**

   ```bash
   docker compose -f .tools/docker/docker-compose.yml up --build
   ```

4. **Access the application:**
   - **Frontend (React)** → [http://localhost:3000](http://localhost:3000)
   - **Backend (Django)** → [http://localhost:8000](http://localhost:8000)
   - **Database (PostgreSQL)** → port `5432`

#### Docker Management Commands

```bash
# Run in background
docker compose -f .tools/docker/docker-compose.yml up -d --build

# Stop containers
docker compose -f .tools/docker/docker-compose.yml down

# View logs
docker compose -f .tools/docker/docker-compose.yml logs -f

# Enter backend container
docker exec -it SmartRecommender-Django bash

# Enter database
docker exec -it SmartRecommender-PostgreSQL psql -U postgres -d product_recommendation
```

### Option 2: Manual Setup

#### Running with Startup Scripts

We provide ready-to-use startup scripts for both Windows and Linux:

##### Windows

```bash
# Start backend
cd backend
start.bat

# Start frontend (in a new terminal)
cd frontend
start.bat
```

##### Linux/macOS

```bash
# Start backend
cd backend
chmod +x start.sh
./start.sh

# Start frontend (in a new terminal)
cd frontend
chmod +x start.sh
./start.sh
```

#### Manual Installation

##### Backend (Django)

1. Create and activate a virtual environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install backend dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your PostgreSQL database in `.env` (see `.env.example` for template)

4. Apply database migrations and seed data:

```bash
python manage.py migrate
python manage.py seed
```

5. Start the backend server:

```bash
python manage.py runserver
```

Backend will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

##### Frontend (React)

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install frontend dependencies:

```bash
npm install
```

3. Start the frontend server:

```bash
npm start
```

Frontend will be available at [http://localhost:3000/](http://localhost:3000/).

---

## 📈 Features

- **Advanced Product Recommendations:**

  - Collaborative Filtering (User-Based & Item-Based)
  - Content-Based Filtering
  - Association Rules (Frequently Bought Together)
  - Fuzzy Search Logic
  - Sentiment Analysis
  - Probabilistic Methods

- **Comprehensive Admin Dashboard:**

  - Sales forecasting
  - Demand prediction
  - Customer churn risk assessment
  - Purchase pattern analysis

- **User Experience:**
  - Personalized product recommendations
  - Smart search with typo tolerance
  - Sentiment-based product discovery

---

## 📂 Project Structure

```
SmartRecommender-Project-Django-React/
├── .database/                  # Database resources
│   ├── entity-relationship-diagram/  # ERD diagrams
│   ├── backup.sql              # Database backup
│   ├── clearAll.sql            # Reset script
│   ├── README.md               # Database documentation
│   ├── RELATIONSHIPS_IN_BASE.md  # Relationship documentation
│   └── tree_database.png       # Visual DB structure
│
├── .docs/                      # Documentation files
│
├── .github/                    # GitHub configuration
│
├── .methods/                   # Algorithm documentation
│   ├── association_rules.md    # Association rules implementation
│   ├── collaborative_filtering.md  # CF algorithm details
│   ├── content_based_filtering.md  # CBF algorithm details
│   ├── fuzzy_search.md         # Fuzzy search implementation
│   ├── probabilistic_methods.md  # Probabilistic methods
│   └── sentiment_analysis.md   # Sentiment analysis details
│
├── .tools/                     # Development tools
│   └── docker/                 # Docker configuration
│       ├── docker-compose.yml  # Docker Compose setup
│       ├── Dockerfile.backend  # Backend container
│       └── Dockerfile.frontend # Frontend container
│
├── backend/                    # Django backend
│   ├── core/                   # Core application
│   ├── home/                   # Main application
│   ├── media/                  # User uploaded files
│   ├── static/                 # Static files
│   ├── venv/                   # Python virtual environment
│   ├── .env                    # Environment variables
│   ├── .env.example            # Environment template
│   ├── check_media.py          # Media verification
│   ├── manage.py               # Django management
│   ├── package.json            # Node.js dependencies
│   ├── requirements.txt        # Python dependencies
│   ├── start.bat               # Windows startup script
│   └── start.sh                # Linux startup script
│
├── frontend/                   # React frontend
│   ├── node_modules/           # Node.js packages
│   ├── public/                 # Public assets
│   ├── src/                    # Source code
│   ├── .env                    # Environment variables
│   ├── .env.example            # Environment template
│   ├── .htaccess               # Apache configuration
│   ├── package-lock.json       # Dependency lock
│   ├── package.json            # Node.js dependencies
│   ├── README.md               # Frontend documentation
│   ├── start.bat               # Windows startup script
│   └── start.sh                # Linux startup script
│
├── images/                     # Project images
│   ├── team1.jpg               # Dawid Olko
│   ├── team2.jpg               # Piotr Smoła
│   └── team3.png               # Dr. Grochowalski
│
├── .gitignore                  # Git ignored files
├── CNAME                       # Custom domain
├── CNAME.md                    # Domain documentation
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # License information
└── README.md                   # Main documentation
```

---

## 🧠 Recommendation Algorithms

Our platform implements six distinct recommendation approaches:

1. **Collaborative Filtering**: Recommends products based on what similar users have purchased
2. **Content-Based Filtering**: Recommends products with similar attributes to those a user has liked
3. **Association Rules**: Identifies products frequently bought together using Apriori algorithm
4. **Fuzzy Search**: Intelligent search with typo tolerance and partial matching
5. **Sentiment Analysis**: Analyzes customer reviews to recommend positively reviewed products
6. **Probabilistic Methods**: Predicts user purchase probabilities and product demand

Detailed documentation for each algorithm can be found in the `.methods/` directory.

---

## 💾 Database Structure

The system uses PostgreSQL with a comprehensive schema of 24 interconnected tables, including:

- Core entities (Users, Products, Categories, Tags)
- E-Commerce functionality (Orders, Cart, Complaints)
- Recommendation tables (Similarities, Interactions, Associations)
- Analytics tables (Sentiment, Purchase Patterns, Risk Assessment)

See `.database/` directory for complete database documentation and entity relationship diagrams.

---

## 🖼️ Screenshots

[<img src="images/mobile_home.png" width="80%"/>](images/mobile_home.png)

---

## 🧑‍💻 Team

<table>
  <tr>
    <td align="center"><img src="images/team1.jpg" width="100px;" alt="Dawid Olko"/><br /><sub><b>Dawid Olko</b></sub></sub><br /><sub>Creator</sub></td>
    <td align="center"><img src="images/team3.png" width="100px;" alt="Dr. Grochowalski"/><br /><sub><b>Dr. Piotr Grochowalski</b></sub><br /><sub>Supervisor</sub></td>
    <td align="center"><img src="images/team2.jpg" width="100px;" alt="Piotr Smoła"/><br /><sub><b>Piotr Smoła</b></sub></sub><br /><sub>Creator</sub></td>
  </tr>
</table>

> This project was developed as part of an engineering thesis at TBD University.

---

## 📜 License

This project is licensed under the [Apache License 2.0](LICENSE).

---

## 📬 Contact

For any questions or suggestions, feel free to open an issue or contact us directly via GitHub.
