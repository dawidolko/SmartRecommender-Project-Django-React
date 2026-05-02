# SmartRecommender — szczegółowy opis projektu i kontekst dla Claude

> Plik referencyjny dla agenta. Czytaj **przed** każdą zmianą kodu, aby unikać marnowania tokenów na powtórną eksplorację. Aktualizuj, jeśli zauważysz rozbieżność między tym opisem a faktycznym stanem kodu.

---

## 1. Streszczenie projektu (1 zdanie)

Pełnostackowa platforma e-commerce (Django REST + React 18 + PostgreSQL 16, konteneryzowana Dockerem) implementująca **6 metod rekomendacyjnych** napisanych od podstaw bez gotowych bibliotek rekomendacyjnych — projekt inżynierski 2-osobowy (Dawid Olko + Piotr Smoła, promotor: dr inż. Piotr Grochowalski, Uniwersytet Rzeszowski 2026).

**Podział metod między autorów:**
- **Olko**: Collaborative Filtering, Sentiment Analysis, Association Rules (Apriori)
- **Smoła**: Content-Based Filtering, Fuzzy Logic, Probabilistic Methods (Markov + Naive Bayes)

---

## 2. Struktura katalogów (root)

```
SmartRecommender-Project-Django-React/
├── .claude/                       # ← TEN katalog (konfiguracja Claude + skills.md)
├── .database/                     # ERD, backup.sql (~20 MB), README, RELATIONSHIPS_IN_BASE.md
├── .diagrams/                     # diagramy do prac inżynierskich (PNG)
├── .docs/                         # praca inżynierska + prezentacja
│   ├── description.md             # krótki opis 6 metod
│   ├── latex/olko/main.tex        # praca Olko (~116 KB, ok. 1700 linii)
│   ├── latex/smola/main.tex       # praca Smoła (~172 KB)
│   └── presentation/              # PPTX, PDF prac
├── .github/                       # konfig GitHub
├── .methods/                      # ← DOKUMENTACJA ALGORYTMÓW (czytaj przed zmianą metody!)
│   ├── association_rules.md       # Apriori (~47 KB)
│   ├── collaborative_filtering.md # Item-based CF + Adjusted Cosine (~36 KB)
│   ├── content_based_filtering.md # CBF (~5 KB) — niedokończona dokumentacja
│   ├── fuzzy_search.md            # Fuzzy search (~6 KB)
│   ├── probabilistic_methods.md   # Bayes, Markov (~8 KB)
│   └── sentiment_analysis.md      # Liu (2012) (~21 KB)
├── .tools/docker/                 # docker-compose.yml + Dockerfile.backend/frontend
├── backend/                       # Django REST Framework
├── frontend/                      # React 18 + craco
├── images/                        # zdjęcia członków zespołu
├── propozycje.md, README.md, ...
```

---

## 3. Stos technologiczny

| Warstwa  | Technologie                                                                 |
|----------|-----------------------------------------------------------------------------|
| Backend  | Python 3.12, Django 5.1.4, DRF 3.15.2, SimpleJWT, django-cors-headers, django-environ, psycopg2-binary, NumPy, scikit-learn, TextBlob (jest w obrazie, ale używana jest **własna** `CustomSentimentAnalysis`), pandas, NLTK, tqdm, colorama |
| Frontend | React 18, react-router-dom v6, axios, framer-motion, react-toastify, lucide-react, react-icons, jwt-decode, chart.js, recharts, react-slick, formik+yup, sass (.scss), craco |
| DB       | PostgreSQL 16 (Docker), 24+ tabel (12 core + opinii/sentymentu + 5 metod + 5 analitycznych) |
| Auth     | JWT (Bearer), `AUTH_USER_MODEL = home.User` (email = username field), role: `admin`/`client` |
| Cache    | Database cache `recommendation_cache_table` (max 5000 wpisów); stałe: `CACHE_TIMEOUT_SHORT=300`, `MEDIUM=1800`, `LONG=7200` |

---

## 4. Jak uruchomić projekt

### Docker (rekomendowane)

```bash
docker compose -f .tools/docker/docker-compose.yml up --build
```

- frontend: http://localhost:3000
- backend: http://localhost:8000
- postgres: port 5432 (user: `postgres`, pass: `admin`, db: `product_recommendation`)
- nazwy kontenerów: `SmartRecommender-PostgreSQL-DB`, `SmartRecommender-Django-BACKEND`, `SmartRecommender-React-FRONTEND`

**Entrypoint backendu (z `docker-compose.yml`):** czeka na `pg_isready`, przy pierwszym starcie wykonuje `makemigrations → migrate → createcachetable recommendation_cache_table → seed`, tworzy plik `/app/.db_initialized` (sentinel — przy kolejnym starcie pomija seed). `runserver 0.0.0.0:8000`.

### Lokalnie (bez Dockera)

```bash
# backend
cd backend
python -m venv venv && venv\Scripts\activate    # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver

# frontend (w osobnym terminalu)
cd frontend
npm install
npm start
```

Uwaga: `requirements.txt` w repo jest zapisany w UTF-16 (każda litera oddzielona spacją w Read tool — to artefakt kodowania). Nie edytować ręcznie bez konwersji na UTF-8.

### Skrypty pomocnicze

- `backend/start.bat` / `start.sh` — uruchamia migracje + serwer
- `frontend/start.bat` / `start.sh` — npm install + npm start

---

## 5. Jak działa Docker (`.tools/docker/`)

**`docker-compose.yml`** definiuje 3 usługi:

| Usługa     | Image / Build                          | Container                        | Port  | Volumes                          |
|------------|----------------------------------------|----------------------------------|-------|----------------------------------|
| `db`       | `postgres:16`                          | `SmartRecommender-PostgreSQL-DB` | 5432  | `postgres_data:/var/lib/postgresql/data` |
| `backend`  | build `Dockerfile.backend` (Python 3.12-slim) | `SmartRecommender-Django-BACKEND` | 8000 | bind mount `../../backend:/app` |
| `frontend` | build `Dockerfile.frontend` (Node 20)  | `SmartRecommender-React-FRONTEND`| 3000  | bind mount `../../frontend:/app` + named volume `/app/node_modules` |

**Healthcheck DB:** `pg_isready` co 30s, 5 retry. Backend ma `depends_on: condition: service_healthy`.
**Frontend:** `CHOKIDAR_USEPOLLING=true` (hot reload przez bind mount).

**Dockerfile.backend** instaluje także (poza requirements.txt): `psycopg2-binary`, `djangorestframework-simplejwt`, `Pillow`, `colorama`, `textblob`, `tqdm`, `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `nltk` oraz pobiera korpusy TextBlob.

---

## 6. Backend Django

### Struktura

```
backend/
├── core/                    # konfiguracja projektu
│   ├── settings.py          # DRF + JWT + CORS + DB cache + PostgreSQL
│   └── urls.py              # /admin/ + include('home.urls')
├── home/                    # JEDNA aplikacja Django ze wszystką logiką
│   ├── models.py            # 24+ modeli (User, Product, Order, Sim, Sentiment, ...)
│   ├── urls.py              # ~70 endpointów (zob. nagłówek pliku — pełna mapa API)
│   ├── views.py             # CRUD + auth + cart + admin stats
│   ├── serializers.py
│   ├── permissions.py
│   ├── signals.py           # post_save Order → run_all_analytics_after_order
│   ├── recommendation_views.py    # CF + CBF
│   ├── sentiment_views.py         # SentimentSearch, FuzzySearch, FuzzyLogicRec
│   ├── association_views.py       # Apriori (FrequentlyBoughtTogether, rules)
│   ├── probabilistic_views.py     # Markov + Bayesian
│   ├── analytics_views.py         # PurchasePrediction, RiskDashboard, SalesForecast, ChurnPrediction
│   ├── seasonal_views.py
│   ├── fuzzy_logic_engine.py      # Mamdani fuzzy logic engine
│   ├── fuzzy_debug_view.py
│   ├── probabilistic_debug_view.py
│   ├── analytics.py               # silnik probabilistyczny (zauważ: README mówi że używa losowości)
│   ├── custom_recommendation_engine.py  # CustomSentimentAnalysis + CustomAssociationRules
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/
│   │   ├── 0001_initial.py        # 25 KB — JEDNA migracja na całą strukturę
│   │   └── __init__.py
│   └── management/commands/
│       └── seed.py                # ⚠️ 1.4 MB — duży plik, NIE czytaj całego!
├── manage.py
├── requirements.txt               # UTF-16
├── check_media.py
└── .env / .env.example
```

### Wszystkie endpointy

Pełna mapa API jest w nagłówku `backend/home/urls.py` (linie 1-134). Dziesięć grup:

1. **Auth & Users** (`/api/login/`, `/api/register/`, `/api/me/`, `/api/users/`, `/api/token/refresh/`)
2. **Products** (`/api/products/`, `/api/random-products/`, `/api/products/search/`, `/api/products/<id>/upload-images/`, `/api/products/<id>/reviews/`, `/api/recommended-products/`, `/api/categories/`, `/api/tags/`)
3. **Cart & Orders** (`/cart/preview/`, `/cart/update/<id>/`, `/cart/remove/<id>/`, `/api/orders/`, `/api/client/orders/<id>/`)
4. **Complaints** (`/api/complaints/`)
5. **Recommendations** — CF/CBF debugging i przetwarzanie (`/api/process-recommendations/`, `/api/interaction/`, `/api/recommendation-preview/`, `/api/generate-user-recommendations/`, `/api/admin/update-product-similarity/`, `/api/recommendation-algorithm-status/`, `/api/collaborative-filtering-debug/`, `/api/all-collaborative-similarities/`, `/api/content-based-debug/`, `/api/fuzzy-logic-debug/`, `/api/probabilistic-debug/`)
6. **Association Rules** (`/api/frequently-bought-together/`, `/api/update-association-rules/`, `/api/association-rules/`, `/api/association-rules-analysis/`, `/api/product-association-debug/`)
7. **Probabilistic** (`/api/markov-recommendations/`, `/api/bayesian-insights/`, `/api/admin/probabilistic-analysis/`)
8. **Analytics** (`/api/purchase-prediction/`, `/api/risk-dashboard/`, `/api/sales-forecast/`, `/api/product-demand/`, `/api/user-purchase-patterns/`, `/api/admin-purchase-patterns/`, `/api/admin-product-recommendations/`, `/api/admin-churn-prediction/`, `/api/my-shopping-insights/`, `/api/seasonal-trends/`)
9. **Sentiment & Fuzzy Search** (`/api/sentiment-search/`, `/api/sentiment-analysis-debug/`, `/api/sentiment-product-debug/`, `/api/fuzzy-search/`, `/api/fuzzy-logic-recommendations/`)
10. **Admin Stats** (`/api/admin-stats/`, `/api/admin-dashboard-stats/`, `/api/client-stats/`)

### Modele (`home/models.py`) — 24 tabele

**Core (`db_*`):** `User` (extends AbstractUser, email = USERNAME_FIELD), `Category`, `Tag`, `Product`, `ProductCategory`, `PhotoProduct`, `Specification`, `Sale`, `Opinion` (rating 1-5, unique user+product), `Order`, `OrderProduct`, `CartItem`, `Complaint`.

**Metody (`method_*`):**
- `UserInteraction` (`method_user_interactions`) — 5 typów: view/click/add_to_cart/purchase/favorite
- `ProductSimilarity` (`method_product_similarity`) — 2 typy: `collaborative` / `content_based`, score [0..1]
- `UserProductRecommendation` (`method_user_product_recommendation`) — cache rekomendacji per user
- `RecommendationSettings` (`method_recommendation_settings`) — aktywny algorytm per user
- `ProductAssociation` (`method_productassociation`) — Apriori: support, confidence, lift
- `SentimentAnalysis` (`method_sentiment_analysis`) — 1:1 z Opinion, score [-1..1], category positive/neutral/negative
- `ProductSentimentSummary` (`method_product_sentiment_summary`) — agregat per produkt
- `PurchaseProbability` (`method_purchase_probability`) — Naive Bayes
- `SalesForecast` (`method_sales_forecast`) — predykcja dzienna 30 dni
- `UserPurchasePattern` (`method_user_purchase_pattern`) — RFM-like + seasonality JSON
- `ProductDemandForecast` (`method_product_demand_forecast`) — week/month/quarter
- `RiskAssessment` (`method_risk_assessment`) — generic entity_type + entity_id (churn/inventory/etc.)

### Seeder (`home/management/commands/seed.py`) — UWAGA: 1.4 MB

**NIE CZYTAĆ CAŁEGO PLIKU.** Funkcje (linie):
- `seed_categories()` (89) — 48 kategorii
- `seed_users()` (297) — 5 admin + 15 client
- `seed_sales()` (227)
- `seed_tags()` (334)
- `seed_products()` (356) — **~500 produktów, ogromny słownik** (zajmuje większość pliku)
- `seed_specifications()` (10579)
- `seed_product_photos()` (8461)
- `seed_product_categories()` (156)
- `seed_product_tags()` (10458)
- `seed_opinions()` (16606) — ~1750 opinii z gotowymi szablonami zbalansowanymi sentymentem (5/4/3/2/1 gwiazdek)
- `seed_orders()` (16783) — 10 zamówień / user, 1-5 produktów / zamówienie
- `seed_complaints()` (16825)
- `seed_sentiment_data()` (16872) — używa `CustomSentimentAnalysis`
- `generate_initial_association_rules()` (16943) — Apriori, `min_support=0.005`, `min_confidence=0.05`, fallback `0.001/0.01`
- `generate_purchase_probabilities()` (17006) — **bazuje na `random.uniform`**, nie na ML
- `generate_sales_forecasts()` (17041) — losowe + seasonal_factor
- `generate_user_purchase_patterns()` (17083)
- `generate_product_demand_forecasts()` (17131)
- `generate_risk_assessments()` (17181)
- `generate_product_similarities()` (17290)

**Sekwencja `Command.handle`:** categories → users → sales → tags → products → specifications → photos → product_categories → product_tags → opinions (+sentiment summaries) → orders → complaints → sentiment_data → association_rules → purchase_probs → sales_forecasts → purchase_patterns → demand_forecasts → risk → similarities.

`reset_sequences()` (63) — resetuje sekwencje ID w PostgreSQL po seedowaniu, żeby kolejne wstawki nie kolidowały.

### Migracje

- `0001_initial.py` (25 KB) — **wszystkie 24 modele w jednej migracji** (świeża baza). Zmiana w `models.py` → `python manage.py makemigrations` utworzy `0002_*`.

### Sygnały (`home/signals.py`)

`@receiver(post_save, sender=Order)` → `transaction.on_commit(lambda: run_all_analytics_after_order(instance))` → automatycznie po **każdym nowym zamówieniu**:
- regeneracja reguł asocjacyjnych
- przeliczenie similarity (CF/CBF zależnie od `RecommendationSettings`)
- prognozy / risk assessment
- aktualizacja sentymentów (jeśli dotyczy)

Również: `update_content_based_similarity` (sygnał używany w seederze).

---

## 7. Frontend React (`frontend/src/`)

### Struktura

```
src/
├── App.js                  # routing + AuthContext + ShopContext + FavoritesProvider
├── index.js
├── global.scss
├── config/config.js        # apiUrl + isProduction → useMockData
├── context/
│   ├── AuthContext.js      # JWT decode, localStorage 'access' + 'loggedUser', auto-logout on exp
│   └── CartContext.js
├── utils/
│   ├── axiosInstance.js    # axios baseURL = config.apiUrl
│   ├── demoUtils.js
│   ├── mockData.js         # fallback dane dla GitHub Pages preview
│   └── ScrollToTop.jsx
├── pages/                  # Home, Shop, Cart, Favorites, ProductSection, Blog, Faq, Contact, About, AdminPanel, ClientPanel
├── components/
│   ├── Navbar/             # + SearchModal (fuzzy + sentiment toggle)
│   ├── AdminPanel/         # ~25 komponentów: AdminProductsTab, AdminOrdersTab, AdminUsersTab, AdminComplaintsTab, AdminStatistics, AdminProbabilistic*, AdminDebug*, AdminSidebar, OverviewPanel, SalesOverview*, UserDemographics*, CustomersTab*, CategoryDistribution*, ConfirmationModal*, StatCard, ...
│   ├── ClientPanel/        # ClientDashboard, ClientOrders, ClientComplaints, ClientAccount, ClientProbabilistic, ClientFuzzy*, BayesianDashboard, MarkovVisualization, ReviewForm
│   ├── ShopContent/, CartContent/, FavoritesContent/
│   ├── ProductSection/     # ProductPage (logowanie interakcji POST /api/interaction/)
│   ├── Search/             # SearchResults
│   ├── panelLogin/         # LoginPanel + RegisterPanel
│   ├── PublicRoute/        # redirect uwierzytelnionych
│   ├── AccessibilityToolbar/, DemoNotice/, DemoFallback/
│   ├── Hero/, Footer/, Map/, Team/, Pricing/, Counter/, Testimonials/, Technology/, BlogContent/, ContactContent/, AboutContent/, LogoSlider/, Modal/, Accordion/, Message/, MainBackground/, FixedBg/, AnimatedPage/, AnimationVariants/, NewProducts/, NotFound/, CallBack/
│   └── ShopContext/        # provider koszyka
└── assets/
```

### Kluczowe konwencje frontendu

- **Routing:** React Router v6 (`<Routes>`, `<Route path="/admin/*" element={<PrivateRoute roles={['admin']}><AdminPanel/></PrivateRoute>}/>`).
- **Auth flow:** localStorage `access` (JWT) + `loggedUser` (decoded payload). `AuthContext.useEffect` weryfikuje `decoded.exp` — jeśli wygasł, automatyczny `logout()`. Po starcie odpala `fetchUserData()` → `GET /api/user/`.
- **PrivateRoute / PublicRoute:** plik `App.js` zawiera `PrivateRoute` inline; `PublicRoute` to osobny komponent (przekierowuje już zalogowanych z /login → /).
- **API calls:** `axiosInstance` z `baseURL=config.apiUrl` (env: `REACT_APP_API_URL`). Niektóre fetche używają natywnego `fetch` (np. `AuthContext`).
- **Mock data:** gdy `isProduction` (host = github.io / project.dawidolko.pl / https + nie localhost) **lub** `REACT_APP_USE_MOCK_DATA=true`, frontend używa danych z `mockData.js` (live demo nie ma backendu).
- **Stylowanie:** SCSS per-komponent, jeden plik `global.scss`. Tailwind dodany w devDependencies, ale nie wszędzie używany.
- **Animacje:** framer-motion (`AnimatePresence mode="sync"`).
- **Toast:** react-toastify (top-center, 3s, hideProgressBar).
- **Dev server:** craco (`craco start/build/test`).
- **Routing-specific UX:** Navbar/Footer **ukryte** dla `/admin/*` i `/client/*` (panele mają własny layout). AccessibilityToolbar też ukryty na panelach.

---

## 8. PostgreSQL — schemat i dane

24 tabele (zob. `.database/README.md` i `RELATIONSHIPS_IN_BASE.md`). Konwencja nazewnictwa:
- `db_*` = tabele e-commerce/core
- `method_*` = tabele algorytmów rekomendacyjnych
- ERD: `.docs/latex/olko/images/appErd.png` + `methodsErd.png`

**Backup pełny:** `.database/backup.sql` (~20 MB) — zawiera dane testowe.

**Restore:**
```bash
psql -U postgres -d product_recommendation < .database/backup.sql
```

Klucze relacji (wszystkie `CASCADE` chyba że zaznaczono):
- `Sale → Product` (`SET_NULL` przy usunięciu Sale)
- `Order → User`, `OrderProduct → Order, Product`, `Complaint → Order`
- `Opinion → User, Product` (unique user+product, rating 1-5 check)
- `SentimentAnalysis ↔ Opinion` (OneToOne)
- `ProductSimilarity` — 2× FK do Product (`product1`/`product2`), unique (product1, product2, similarity_type)
- `ProductAssociation` — 2× FK do Product (`product_1`/`product_2`)
- `RiskAssessment` używa **generic** `entity_type` + `entity_id` (brak FK)

---

## 9. Metody rekomendacyjne — jak działają

> Pełna dokumentacja: `.methods/*.md`. Poniżej streszczenie do szybkiego przypomnienia.

### 9.1 Collaborative Filtering — **Item-Based, Adjusted Cosine Similarity** (Sarwar 2001)

- Plik: `home/recommendation_views.py` → `process_collaborative_filtering()`
- Algorytm:
  1. Buduje macierz user×product z `OrderProduct.quantity`
  2. Mean-centering **tylko po zakupionych** produktach (val > 0); zera pozostają zerami
  3. Cosine similarity między **kolumnami** (product-product)
  4. Threshold pruning > 0.2 → zapis do `ProductSimilarity` z `similarity_type='collaborative'`
- Cache key: `collaborative_similarity_matrix`
- Reference w kodzie: Sarwar et al. 2001 — "Item-based collaborative filtering recommendation algorithms"

### 9.2 Content-Based Filtering

- Plik: `home/recommendation_views.py` → `process_content_based_filtering()`
- Cechy produktu: kategorie (40%), tagi (30%), cena (20%), słowa kluczowe TF-IDF z opisu (10%) — wagi z pracy Smoły
- Weighted Cosine Similarity → zapis do `ProductSimilarity` z `similarity_type='content_based'`
- Plus / minus: rozwiązuje cold-start, ale ma filter bubble

### 9.3 Association Rules — **własny Apriori z bitmap pruning** (Agrawal & Srikant 1994)

- Plik: `home/custom_recommendation_engine.py` → `CustomAssociationRules`
- Metryki: support, confidence, lift
- Próg: `min_support=0.005`, `min_confidence=0.05` (seeder); admin może zmienić
- Pipeline: `_find_frequent_itemsets_with_bitmap` → `_generate_optimized_rules_from_itemsets` → zapis do `ProductAssociation`
- Trigger: `post_save Order` (signals.py) → automatyczna regeneracja reguł
- Endpoint: `/api/frequently-bought-together/`, `/api/association-rules/`, `/api/update-association-rules/`

### 9.4 Sentiment Analysis — **wieloźródłowa, słownikowa** (Liu 2012)

- Plik: `home/custom_recommendation_engine.py` → `CustomSentimentAnalysis`
- 5 źródeł sentymentu z wagami: opinie 40%, opis 25%, nazwa 15%, specyfikacje 12%, kategorie 8%
- Final_score = ważony średni, range [-1..1]
- Kategoryzacja: positive / neutral / negative (na podstawie progów Liu 2012)
- Tabele: `SentimentAnalysis` (per opinia), `ProductSentimentSummary` (agregat per produkt)
- Endpoint: `/api/sentiment-search/?q=...` — sortuje wyniki po `final_score`
- **NIE używa TextBlob** mimo że jest w wymaganiach (TextBlob używany tylko w starym kodzie)

### 9.5 Fuzzy Search & Fuzzy Logic

- **Fuzzy Search** (`home/sentiment_views.py` → `FuzzySearchAPIView`): tolerancja literówek, weighted match
  - Wagi: name 40%, desc 30%, category 20%, spec 10%
  - Threshold: 0.3-1.0 (default 0.6)
  - Filtr cenowy: cheap (<$100) / medium ($100-$500) / expensive (>$500)
  - `calculate_fuzzy_score(query, text)`: containment check → word match → substring similarity
- **Fuzzy Logic Engine** (`home/fuzzy_logic_engine.py`): system Mamdani z regułami IF-THEN
  - 3 zmienne: cena, jakość, popularność
  - Funkcje przynależności: trójkątne i trapezoidalne
  - Wykresy w `.docs/latex/smola/images/fuzzy_*_membership.png`

### 9.6 Probabilistic Methods — Markov + Naive Bayes

- Plik: `home/probabilistic_views.py`, `home/analytics.py`
- **Markov 1-rzędu**: `/api/markov-recommendations/` — predykcja sekwencji zakupowej (next-basket)
- **Naive Bayes**: `/api/bayesian-insights/`, `/api/purchase-prediction/` — prawdopodobieństwo zakupu produktu
- **⚠️ UWAGA z `.methods/probabilistic_methods.md`:** w aktualnym `analytics.py` wiele metod używa `random.uniform()` zamiast prawdziwej statystyki — to TODO do dopracowania (patrz sekcja "What needs to change" w dokumencie)
- Modele DB: `PurchaseProbability`, `SalesForecast`, `UserPurchasePattern`, `ProductDemandForecast`, `RiskAssessment`

---

## 10. Praca inżynierska — kontekst akademicki

**Tytuły prac:**
- **Olko**: "System rekomendacji produktów oparty na filtracji współpracy, analizie sentymentu i regułach asocjacyjnych"
- **Smoła**: "System rekomendacji produktów wykorzystujący filtrację opartą na treści, logikę rozmytą i modele probabilistyczne"

**Promotor:** dr inż. Piotr Grochowalski (Uniwersytet Rzeszowski, WNST)
**Rok:** 2026
**Język pracy:** polski (LaTeX, czcionka Carlito, marginesy 3.5/2.5/2.5/2.5 cm, interlinia 1.5)

**Struktura pracy Olko (`.docs/latex/olko/main.tex`, ~1700 linii):**
1. Wstęp (cel, zakres)
2. Rozdział 1: Teoretyczne podstawy systemów rekomendacyjnych
3. Rozdział 2: Weryfikacja rozwiązań alternatywnych (Amazon Personalize, Google Vertex AI, Apache Mahout)
4. Rozdział 3: Opis projektu (cel, użytkownicy, wymagania funkcjonalne, use cases, architektura, **3.6 struktura bazy danych**)
5. Rozdział 4: Stos technologiczny (architektura, backend, frontend, PostgreSQL, **4.6 deployment Docker**, 4.7 architektura systemu rekomendacji)
6. Rozdział 5: **Implementacja algorytmów (5.1 podstawy matematyczne, 5.2 CF Item-Based + Adjusted Cosine, 5.3 Sentiment, 5.4 Apriori)**
7. Rozdział 6: Funkcjonowanie w praktyce (UI/UX dla każdej metody)
8. Rozdział 7: Porównanie i ewaluacja
9. Podsumowanie + Literatura + Streszczenie

**Praca Smoły (`.docs/latex/smola/main.tex`, ~3000 linii):** analogiczna struktura, ale o CBF, Fuzzy Logic, Markov+Bayes.

**Liczba danych testowych deklarowana w pracy:** 500 produktów, 20 użytkowników (5 admin + 15 client), 200 zamówień, ~600 OrderProduct, ~1750 opinii.

---

## 11. Konwencje kodu i zasady przy zmianach

### Nazewnictwo
- Tabele: `db_*` (core), `method_*` (algorytmy)
- Modele Python: `PascalCase`, np. `ProductSimilarity`
- Endpointy: kebab-case, prefix `/api/`
- Komponenty React: `PascalCase.jsx` + `PascalCase.scss` w jednym katalogu
- Pliki Pythona: `snake_case.py`

### Kodowanie
- **Polski w komentarzach pracy LaTeX** (`.tex`); kod Pythona / JS — angielski.
- W docstringach Pythona — angielski; często cytowane referencje akademickie (np. "Reference: Sarwar et al. 2001").

### Migrations
- Po zmianie modelu: `python manage.py makemigrations && python manage.py migrate`
- W Dockerze: backend wykonuje to przy pierwszym starcie (sentinel `/app/.db_initialized`).

### Cache
- Po zmianie danych wpływających na rekomendacje, **invalidate cache key** (`collaborative_similarity_matrix` itd.) — używaj `cache.delete()`.
- Tabela `recommendation_cache_table` — `python manage.py createcachetable` (już w entrypoint).

### Sygnały
- **Każdy nowy `Order` automatycznie triggeruje** przeliczenie wszystkich analiz. Jeśli dodajesz endpoint manualnego triggerowania, używaj tego samego `run_all_analytics_after_order`.

---

## 12. Najczęstsze pytania / pułapki

| Pytanie / problem                                            | Odpowiedź / rozwiązanie |
|---------------------------------------------------------------|--------------------------|
| Gdzie jest definiowane API?                                   | `backend/home/urls.py` (nagłówek dokumentuje wszystkie endpointy) |
| Gdzie jest logika konkretnej metody?                          | `home/recommendation_views.py` (CF/CBF), `home/sentiment_views.py` (sentiment + fuzzy search), `home/association_views.py` (Apriori), `home/probabilistic_views.py` (Markov, Bayes), `home/fuzzy_logic_engine.py` (Mamdani), `home/analytics.py` (forecasty, ryzyko) |
| Gdzie jest definiowany użytkownik?                            | `home/models.py` → `User(AbstractUser)` z `email` jako `USERNAME_FIELD` (login po emailu, nie username) |
| Frontend mówi "demo mode" / nie łączy z backendem             | Sprawdź `frontend/src/config/config.js` — `isProduction` jest `true` dla github.io / project.dawidolko.pl, wtedy `useMockData = true` |
| Seed nie wykonał się w Dockerze                               | Backend tworzy plik sentinel `/app/.db_initialized` po pierwszym seedowaniu. Aby zaseedować ponownie: `docker exec -it SmartRecommender-Django-BACKEND rm /app/.db_initialized` i restart |
| `requirements.txt` "wygląda dziwnie"                         | Plik jest w **UTF-16 LE z BOM**. Nie edytuj bezmyślnie — przekonwertuj na UTF-8 najpierw lub użyj `pip install` bezpośrednio (działa bo Python toleruje BOM) |
| Random w analytics                                            | `analytics.py` używa `random.uniform()` w kilku miejscach (purchase_probability, risk_assessment, sales_forecast). To znany TODO — zob. `.methods/probabilistic_methods.md` |
| `seed.py` jest ogromny (1.4 MB)                              | **Nie czytaj całego.** Używaj `Grep` na `^def\s+\w+` żeby znaleźć funkcję, potem `Read` z `offset+limit`. Większość pliku to słownik produktów |
| Nazwy kontenerów Dockera                                      | `SmartRecommender-PostgreSQL-DB`, `SmartRecommender-Django-BACKEND`, `SmartRecommender-React-FRONTEND` (compose name: `smartrecommender-project`) |
| Brak pakietu w `requirements.txt` ale działa                  | `Dockerfile.backend` instaluje dodatkowo: textblob, pandas, numpy, scikit-learn, matplotlib, seaborn, nltk, simplejwt, Pillow, colorama, tqdm. Lokalnie trzeba ręcznie. |

---

## 13. Wskazówki dla efektywnego pracowania z tym projektem

1. **Najpierw przeczytaj odpowiedni plik z `.methods/`** — to kompendium implementacji algorytmu.
2. **Nie czytaj `seed.py` w całości** — używaj `Grep` z funkcją lub czytaj z `offset`.
3. **Przed dodaniem nowego endpointu** sprawdź, czy podobny już nie istnieje (`backend/home/urls.py`).
4. **Zmiana modelu = nowa migracja** — nie edytuj `0001_initial.py`.
5. **Dla zmiany w UI panelu admina/klienta** szukaj w `frontend/src/components/AdminPanel/` lub `ClientPanel/`.
6. **Sprawdzanie zalogowanego usera w React:** `useContext(AuthContext)` → `user`, `user.role` (`'admin'`/`'client'`).
7. **Sprawdzanie roli na backendzie:** `home/permissions.py` (custom permissions), domyślne `IsAuthenticated`/`IsAdminUser`.
8. **Przy zmianach w algorytmie rekomendacji** — pamiętaj o cache (klucze typu `collaborative_similarity_matrix`).
9. **Język:** odpowiadaj użytkownikowi po polsku (rozmowa toczy się po polsku, projekt jest polski). Kod / commit messages — angielski.
10. **Praca inżynierska**: gdy zmiany dotyczą algorytmu opisanego w pracy, warto zerknąć do `.docs/latex/{olko,smola}/main.tex` (sekcja 5.x) żeby zachować spójność z tym co opisuje praca.

---

## 14. Aktualizacja tego pliku

Jeśli zauważysz, że ten dokument rozjeżdża się z rzeczywistością (przeniesione pliki, dodane endpointy, zmienione algorytmy) — **zaktualizuj go** zamiast pisać kolejny plik. Trzymanie kontekstu w jednym miejscu zmniejsza tokeny w przyszłych konwersacjach.

**Ostatnia aktualizacja:** 2026-05-02
**Autor wpisu:** Claude (Opus 4.7)
