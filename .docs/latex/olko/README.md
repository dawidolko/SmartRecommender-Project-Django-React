# Dokumentacja Metod Rekomendacyjnych - SmartRecommender

## Autorzy: Dawid Olko & Piotr Smoła

## Data: 2025-11-02

## Wersja: 2.0

---

# Spis treści

1. [System Cache w Aplikacji](#1-system-cache-w-aplikacji)
2. [Collaborative Filtering (CF)](#2-collaborative-filtering-cf)
3. [Analiza Sentymentu](#3-analiza-sentymentu)
4. [Reguły Asocjacyjne (Apriori)](#4-reguły-asocjacyjne-apriori)
5. [Integracja z Frontend](#5-integracja-z-frontend)

---

# 1. System Cache w Aplikacji

## 1.1 Konfiguracja Cache

Aplikacja używa **Database Cache** - cache oparty na bazie danych PostgreSQL. Konfiguracja znajduje się w pliku `backend/core/settings.py`:

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "recommendation_cache_table",
        "OPTIONS": {
            "MAX_ENTRIES": 5000,
            "CULL_FREQUENCY": 4,
        },
    }
}
```

### Gdzie przechowywany jest cache?

**Cache jest przechowywany w tabeli bazy danych PostgreSQL** o nazwie `recommendation_cache_table`.

- **NIE tworzy się osobny katalog** z plikami cache
- **NIE używa Redis ani Memcached**
- Dane cache są zapisywane bezpośrednio w bazie danych PostgreSQL

### Parametry cache:

| Parametr         | Wartość | Opis                                                  |
| ---------------- | ------- | ----------------------------------------------------- |
| `MAX_ENTRIES`    | 5000    | Maksymalna liczba wpisów w cache                      |
| `CULL_FREQUENCY` | 4       | Przy osiągnięciu limitu usuwa 1/4 najstarszych wpisów |

### Timeouty cache (stałe zdefiniowane w settings.py):

```python
CACHE_TIMEOUT_SHORT = 300      # 5 minut - dla często zmieniających się danych
CACHE_TIMEOUT_MEDIUM = 1800    # 30 minut - dla umiarkowanie stabilnych danych
CACHE_TIMEOUT_LONG = 7200      # 2 godziny - dla rzadko zmieniających się danych
```

## 1.2 Użycie Cache w Metodach Rekomendacyjnych

### Collaborative Filtering:

- **Klucz cache:** `collaborative_similarity_matrix`
- **Timeout:** 2 godziny (CACHE_TIMEOUT_LONG = 7200s)
- **Zawartość:** Liczba utworzonych podobieństw

### Analiza Sentymentu:

- **Klucz cache:** `product_sentiment_{product_id}_{updated_at}`
- **Timeout:** 15 minut (CACHE_TIMEOUT_SHORT = 900s)
- **Zawartość:** Wyniki analizy sentymentu produktu

### Reguły Asocjacyjne:

- **Klucz cache:** `association_rules_{transactions}_{support}_{confidence}`
- **Timeout:** 30 minut (CACHE_TIMEOUT_MEDIUM = 1800s)
- **Zawartość:** Lista reguł asocjacyjnych

## 1.3 Inwalidacja Cache (Django Signals)

Cache jest automatycznie unieważniany przez sygnały Django w pliku `backend/home/signals.py`:

```python
@receiver(post_save, sender=OrderProduct)
def log_interaction_on_purchase(sender, instance, created, **kwargs):
    if created:
        # Inwalidacja globalnych cache rekomendacji
        cache.delete("collaborative_similarity_matrix")
        cache.delete("content_based_similarity_matrix")
        cache.delete("association_rules_list")

        # Inwalidacja cache specyficznego dla użytkownika
        user_id = instance.order.user.id
        cache.delete(f"user_recommendations_{user_id}_collaborative")
        cache.delete(f"user_recommendations_{user_id}_content_based")
```

---

# 2. Collaborative Filtering (CF)

## 2.1 Opis Algorytmu

**Nazwa:** Item-Based Collaborative Filtering z metryką Adjusted Cosine Similarity

**Źródło naukowe:** Sarwar et al. (2001) - "Item-based Collaborative Filtering Recommendation Algorithms"

## 2.2 Wzór Matematyczny

Wzór **Adjusted Cosine Similarity** (Sarwar et al., 2001):

$$sim(i,j) = \frac{\sum_{u \in U}(R_{u,i} - \bar{R}_u)(R_{u,j} - \bar{R}_u)}{\sqrt{\sum_{u \in U}(R_{u,i} - \bar{R}_u)^2} \cdot \sqrt{\sum_{u \in U}(R_{u,j} - \bar{R}_u)^2}}$$

Gdzie:

- $R_{u,i}$ - ilość zakupu użytkownika $u$ dla produktu $i$ (quantity z OrderProduct)
- $\bar{R}_u$ - średnia ilość zakupów użytkownika $u$ dla wszystkich produktów
- $U$ - zbiór użytkowników, którzy kupili oba produkty $i$ i $j$

### Dlaczego ten wzór?

**Mean-centering** (odejmowanie średniej użytkownika $\bar{R}_u$) eliminuje **bias** (wartość progową) wynikającą z różnych skal zakupowych użytkowników:

- Hurtownik kupujący po 100 sztuk
- Klient indywidualny kupujący po 1 sztuce

Po normalizacji obaj mają porównywalne wagi przy obliczaniu podobieństwa.

## 2.3 Implementacja w Backend

### Plik: `backend/home/recommendation_views.py`

#### Klasa: `ProcessRecommendationsView`

**Krok 1: Budowa macierzy użytkownik-produkt**

```python
def process_collaborative_filtering(self):
    # Budowa macierzy interakcji z historii zakupów
    user_product_matrix = defaultdict(dict)
    for order in OrderProduct.objects.select_related("order", "product").all():
        user_product_matrix[order.order.user_id][order.product_id] = order.quantity
```

**Krok 2: Konwersja do macierzy NumPy**

```python
    matrix = []
    for user_id in user_ids:
        row = []
        for product_id in product_ids:
            row.append(user_product_matrix[user_id].get(product_id, 0))
        matrix.append(row)

    matrix = np.array(matrix, dtype=np.float32)
```

**Krok 3: Normalizacja Mean-Centering (Adjusted Cosine)**

```python
    # Normalizacja - odejmowanie średniej użytkownika
    normalized_matrix = np.zeros_like(matrix, dtype=np.float32)

    for i, user_row in enumerate(matrix):
        purchased_items = user_row[user_row > 0]

        if len(purchased_items) > 0:
            user_mean = np.mean(purchased_items)
            # Odejmij średnią użytkownika od wszystkich zakupionych produktów
            for j, val in enumerate(user_row):
                if val > 0:
                    normalized_matrix[i][j] = val - user_mean
                else:
                    normalized_matrix[i][j] = 0
```

**Krok 4: Obliczenie podobieństw cosinusowych**

```python
    # Transpozycja i obliczenie podobieństw item-item
    product_similarity = cosine_similarity(normalized_matrix.T)
```

**Krok 5: Filtrowanie i zapis do bazy**

```python
    similarity_threshold = 0.5  # Próg podobieństwa

    for i, product1_id in enumerate(product_ids):
        for j, product2_id in enumerate(product_ids):
            if i != j and product_similarity[i][j] > similarity_threshold:
                similarities_to_create.append(
                    ProductSimilarity(
                        product1_id=product1_id,
                        product2_id=product2_id,
                        similarity_type="collaborative",
                        similarity_score=float(product_similarity[i][j]),
                    )
                )

    # Bulk insert dla wydajności (1000 rekordów na raz)
    ProductSimilarity.objects.bulk_create(similarities_to_create)
```

## 2.4 Tabele w Bazie Danych

### Tabela: `method_product_similarity`

| Kolumna          | Typ        | Opis                                |
| ---------------- | ---------- | ----------------------------------- |
| id               | BigInt     | Klucz główny                        |
| product1_id      | ForeignKey | ID pierwszego produktu              |
| product2_id      | ForeignKey | ID drugiego produktu                |
| similarity_type  | CharField  | "collaborative" lub "content_based" |
| similarity_score | Float      | Wynik podobieństwa [0.0, 1.0]       |

## 2.5 Integracja z Frontend

### Panel Administratora - Debug CF

**Plik:** `frontend/src/components/AdminPanel/AdminDebug.jsx`

**Endpoint API:** `GET /api/collaborative-filtering-debug/`

```jsx
const fetchCFDebug = async () => {
  const res = await axios.get(
    `${config.apiUrl}/api/collaborative-filtering-debug/`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
  setCfDebugData(res.data);
};
```

**Wyświetlane informacje:**

- Nazwa algorytmu i wzór
- Statystyki bazy danych (użytkownicy, produkty, zamówienia)
- Informacje o macierzy User-Product (shape, sparsity)
- Informacje o macierzy podobieństw (saved similarities, threshold)
- Status cache

### Strona Główna - Sekcje Rekomendacji

**Plik:** `frontend/src/components/NewProducts/NewProducts.jsx`

```jsx
useEffect(() => {
  const fetchData = async () => {
    const token = localStorage.getItem("access");
    if (token) {
      // Pobierz aktywny algorytm użytkownika
      const settingsResponse = await axios.get(
        `${config.apiUrl}/api/recommendation-settings/`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      const algorithm =
        settingsResponse.data.active_algorithm || "collaborative";

      // Pobierz rekomendacje dla algorytmu
      const response = await axios.get(
        `${config.apiUrl}/api/recommendation-preview/?algorithm=${algorithm}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
    }
  };
  fetchData();
}, []);
```

### Panel Klienta - Dashboard

**Plik:** `frontend/src/components/ClientPanel/ClientDashboard.jsx`

```jsx
const fetchingAlgorithm = algorithmRequest.then((response) => {
  const algorithm = response.data.active_algorithm || "collaborative";

  // Ustaw tytuł sekcji rekomendacji
  if (algorithm === "collaborative") {
    setRecommendationTitle("Recommended For You (Collaborative Filtering)");
  }

  // Pobierz rekomendacje
  return axios.get(
    `${config.apiUrl}/api/recommendation-preview/?algorithm=${algorithm}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
});
```

## 2.6 Przepływ Danych - Collaborative Filtering

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COLLABORATIVE FILTERING - PRZEPŁYW                    │
└─────────────────────────────────────────────────────────────────────────┘

1. GENEROWANIE PODOBIEŃSTW (Backend)
   ┌──────────────────┐
   │  OrderProduct    │ ──► Pobierz historię zakupów
   │  (user, product, │
   │   quantity)      │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Macierz         │ ──► user_product_matrix[user_id][product_id] = quantity
   │  User-Product    │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Mean-Centering  │ ──► normalized[i][j] = matrix[i][j] - user_mean
   │  (Normalizacja)  │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Cosine          │ ──► similarity = cosine_similarity(matrix.T)
   │  Similarity      │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  ProductSimilarity│ ──► Zapisz podobieństwa > 0.5 do bazy
   │  (tabela DB)     │
   └──────────────────┘

2. POBIERANIE REKOMENDACJI (Frontend)
   ┌──────────────────┐
   │  Frontend        │ ──► GET /api/recommendation-preview/?algorithm=collaborative
   │  (React)         │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Backend API     │ ──► Pobierz ProductSimilarity dla produktów użytkownika
   │                  │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Response        │ ──► Lista rekomendowanych produktów z wynikami podobieństwa
   │  (JSON)          │
   └──────────────────┘
```

---

# 3. Analiza Sentymentu

## 3.1 Opis Algorytmu

**Nazwa:** Lexicon-based Sentiment Analysis (Analiza sentymentu oparta na słowniku)

**Źródła naukowe:**

- Liu, Bing (2012) - "Sentiment Analysis and Opinion Mining"
- Opinion Lexicon (Hu & Liu 2004) - ~6800 słów opiniotwórczych
- AFINN-165 (Nielsen 2011) - słowa z ocenami [-5, +5]

## 3.2 Wzór Matematyczny

### Wzór podstawowy (Liu, 2012):

$$Sentiment\_Score = \frac{N_{positive} - N_{negative}}{N_{total}}$$

Gdzie:

- $N_{positive}$ - liczba słów pozytywnych w tekście
- $N_{negative}$ - liczba słów negatywnych w tekście
- $N_{total}$ - całkowita liczba słów w tekście

**Zakres wyniku:** [-1.0, +1.0]

### Klasyfikacja sentymentu:

- **Pozytywny:** Score > 0.1
- **Negatywny:** Score < -0.1
- **Neutralny:** -0.1 ≤ Score ≤ 0.1

### Wzór wieloźródłowej agregacji (per produkt):

$$Final\_Score = (Opinion\_Score \times 0.40) + (Description\_Score \times 0.25) + (Name\_Score \times 0.15) + (Spec\_Score \times 0.12) + (Category\_Score \times 0.08)$$

### Wagi źródeł:

| Źródło                  | Waga | Uzasadnienie                                           |
| ----------------------- | ---- | ------------------------------------------------------ |
| Opinie klientów         | 40%  | Najbardziej wiarygodne źródło                          |
| Opis produktu           | 25%  | Profesjonalny opis z kluczowymi cechami                |
| Nazwa produktu          | 15%  | Często zawiera wskazówki jakościowe ("Premium", "Pro") |
| Specyfikacje techniczne | 12%  | Obiektywne parametry                                   |
| Kategorie produktu      | 8%   | Ogólny kontekst                                        |

**Dlaczego takie wagi?** Rozwiązują problem **cold start** - produkty bez opinii klientów nadal otrzymują wynik sentymentu na podstawie pozostałych 4 źródeł tekstowych.

## 3.3 Implementacja w Backend

### Plik: `backend/home/custom_recommendation_engine.py`

#### Klasa: `CustomSentimentAnalysis`

**Słowniki sentymenty (fragmenty):**

```python
class CustomSentimentAnalysis:
    def __init__(self):
        # Słowa pozytywne (Opinion Lexicon + AFINN-165)
        self.positive_words = {
            # Core positive (AFINN +4, +5)
            "excellent", "exceptional", "outstanding", "superb", "wonderful", "fantastic",
            "amazing", "brilliant", "perfect", "awesome", "magnificent", "spectacular",

            # Strong positive (AFINN +3)
            "great", "good", "love", "best", "beautiful", "incredible", "gorgeous",
            "happy", "delighted", "pleased", "satisfied", "fabulous", "marvelous",

            # Quality descriptors (Opinion Lexicon)
            "quality", "premium", "superior", "first-class", "top-notch", "high-quality",
            "professional", "reliable", "durable", "sturdy", "solid", "robust",
            # ... (~200 słów)
        }

        # Słowa negatywne (Opinion Lexicon + AFINN-165)
        self.negative_words = {
            # Core negative (AFINN -4, -5)
            "terrible", "horrible", "awful", "worst", "disgusting", "appalling",
            "atrocious", "abysmal", "dreadful", "pathetic", "miserable", "deplorable",

            # Strong negative (AFINN -3)
            "bad", "poor", "disappointing", "hate", "dislike",
            "regret", "unfortunate", "unacceptable", "unsatisfactory", "subpar",
            # ... (~200 słów)
        }

        # Intensyfikatory (zwiększają wagę × 1.8)
        self.intensifiers = {
            "very", "extremely", "really", "quite", "totally", "absolutely",
            "completely", "entirely", "thoroughly", "utterly", "highly", "incredibly",
        }

        # Negacje (odwracają polaryzację)
        self.negations = {
            "not", "no", "never", "nothing", "neither", "nor", "none", "nobody",
            "nowhere", "hardly", "barely", "scarcely", "seldom", "rarely",
        }
```

**Funkcja analizy sentymentu:**

```python
def analyze_sentiment(self, text):
    """
    Implementacja wzoru Liu (2012):
    polarity = (positive_count - negative_count) / total_words
    """
    positive_score = 0.0
    negative_score = 0.0
    total_words = 0

    words = self._tokenize_text(text.lower())

    for word in words:
        if word in self.positive_words:
            positive_score += 1.0
        elif word in self.negative_words:
            negative_score += 1.0
        total_words += 1

    if total_words == 0:
        return 0.0, "neutral"

    # Wzór: (positive - negative) / total
    sentiment_score = (positive_score - negative_score) / total_words

    # Ograniczenie do zakresu [-1.0, 1.0]
    sentiment_score = max(-1.0, min(1.0, sentiment_score))

    # Klasyfikacja
    if sentiment_score > 0.1:
        category = "positive"
    elif sentiment_score < -0.1:
        category = "negative"
    else:
        category = "neutral"

    return sentiment_score, category
```

### Plik: `backend/home/sentiment_views.py`

#### Klasa: `SentimentSearchAPIView`

**Wieloźródłowa agregacja sentymentu:**

```python
def get(self, request):
    from .custom_recommendation_engine import CustomSentimentAnalysis

    query = request.GET.get("q", "").strip()

    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).prefetch_related("categories", "opinion_set", "specification_set")

    analyzer = CustomSentimentAnalysis()
    products_with_scores = []

    for product in products:
        # 1. Analiza opinii (waga 40%)
        opinion_scores = []
        for opinion in product.opinion_set.all()[:20]:
            score, _ = analyzer.analyze_sentiment(opinion.content)
            opinion_scores.append(score)
        opinion_sentiment = sum(opinion_scores) / len(opinion_scores) if opinion_scores else 0.0

        # 2. Analiza opisu (waga 25%)
        desc_score, _ = analyzer.analyze_sentiment(product.description or "")

        # 3. Analiza nazwy (waga 15%)
        name_score, _ = analyzer.analyze_sentiment(product.name)

        # 4. Analiza specyfikacji (waga 12%)
        spec_texts = [f"{s.parameter_name} {s.specification}" for s in product.specification_set.all()[:10]]
        spec_combined = " ".join(spec_texts)
        spec_score, _ = analyzer.analyze_sentiment(spec_combined) if spec_combined else (0.0, "neutral")

        # 5. Analiza kategorii (waga 8%)
        category_names = " ".join([cat.name for cat in product.categories.all()])
        category_score, _ = analyzer.analyze_sentiment(category_names) if category_names else (0.0, "neutral")

        # Wzór wieloźródłowej agregacji
        final_score = (
            opinion_sentiment * 0.40 +
            desc_score * 0.25 +
            name_score * 0.15 +
            spec_score * 0.12 +
            category_score * 0.08
        )

        products_with_scores.append({
            "product": product,
            "final_score": final_score,
            "opinion_score": opinion_sentiment,
            "desc_score": desc_score,
            "name_score": name_score,
            "spec_score": spec_score,
            "category_score": category_score,
        })

    # Sortowanie po wyniku sentymentu (malejąco)
    products_with_scores.sort(key=lambda x: x["final_score"], reverse=True)
```

## 3.4 Tabele w Bazie Danych

### Tabela: `method_sentiment_analysis`

| Kolumna            | Typ        | Opis                              |
| ------------------ | ---------- | --------------------------------- |
| id                 | BigInt     | Klucz główny                      |
| opinion_id         | ForeignKey | Powiązana opinia                  |
| sentiment_score    | Float      | Wynik sentymentu [-1.0, 1.0]      |
| sentiment_category | CharField  | "positive", "negative", "neutral" |

### Tabela: `method_product_sentiment_summary`

| Kolumna           | Typ        | Opis                      |
| ----------------- | ---------- | ------------------------- |
| id                | BigInt     | Klucz główny              |
| product_id        | ForeignKey | Powiązany produkt         |
| average_sentiment | Float      | Średni sentyment          |
| positive_count    | Integer    | Liczba pozytywnych opinii |
| negative_count    | Integer    | Liczba negatywnych opinii |
| neutral_count     | Integer    | Liczba neutralnych opinii |

## 3.5 Integracja z Frontend

### Wyszukiwarka z sortowaniem po sentymencie

**Plik:** `frontend/src/components/Search/SearchResults.jsx`

Wyszukiwarka używa endpointu `GET /api/sentiment-search/?q={query}` który zwraca produkty posortowane według zagregowanego sentymentu.

### Panel Administratora - Debug Sentiment

**Plik:** `frontend/src/components/AdminPanel/AdminDebug.jsx`

```jsx
const fetchSentimentDetailDebug = async (productId) => {
  const res = await axios.get(
    `${config.apiUrl}/api/sentiment-product-debug/?product_id=${productId}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
  setSentimentDetailData(res.data);
};
```

**Wyświetlane informacje dla wybranego produktu:**

- Wynik sentymentu z każdego źródła (opinie, opis, nazwa, specyfikacje, kategorie)
- Wzór obliczeniowy z konkretnymi wartościami
- Słowa pozytywne/negatywne znalezione w tekście
- Finalny wynik agregowany

## 3.6 Przepływ Danych - Analiza Sentymentu

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ANALIZA SENTYMENTU - PRZEPŁYW                         │
└─────────────────────────────────────────────────────────────────────────┘

1. WYSZUKIWANIE (Frontend → Backend)
   ┌──────────────────┐
   │  SearchBar       │ ──► GET /api/sentiment-search/?q=laptop
   │  (React)         │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  SentimentSearch │ ──► Filtruj produkty po nazwie/opisie/kategorii
   │  APIView         │
   └──────────────────┘
            │
            ▼
2. ANALIZA KAŻDEGO PRODUKTU
   ┌──────────────────┐
   │  Dla każdego     │
   │  produktu:       │
   └──────────────────┘
            │
   ┌────────┼────────┬────────┬────────┬────────┐
   │        │        │        │        │        │
   ▼        ▼        ▼        ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│Opinie│ │ Opis │ │Nazwa │ │Spec. │ │Kateg.│
│ 40%  │ │ 25%  │ │ 15%  │ │ 12%  │ │  8%  │
└──────┘ └──────┘ └──────┘ └──────┘ └──────┘
   │        │        │        │        │
   └────────┴────────┴────────┴────────┘
            │
            ▼
   ┌──────────────────┐
   │  Wzór:           │
   │  (pos - neg)     │ ──► sentiment_score dla każdego źródła
   │  / total_words   │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Agregacja:      │
   │  0.40*op + 0.25* │ ──► final_score
   │  desc + 0.15*    │
   │  name + ...      │
   └──────────────────┘
            │
            ▼
3. SORTOWANIE I RESPONSE
   ┌──────────────────┐
   │  Sort by         │ ──► Produkty posortowane po final_score (malejąco)
   │  final_score     │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Response JSON   │ ──► {product, sentiment_score, sentiment_breakdown, ...}
   │                  │
   └──────────────────┘
```

---

# 4. Reguły Asocjacyjne (Apriori)

## 4.1 Opis Algorytmu

**Nazwa:** Algorytm Apriori dla Market Basket Analysis

**Źródła naukowe:**

- Agrawal, R., Srikant, R. (1994) - "Fast algorithms for mining association rules in large databases"
- Brin, S., Motwani, R., Silverstein, C. (1997) - "Beyond market baskets: Generalizing association rules to correlations"
- Zaki, M.J. (2000) - "Scalable Algorithms for Association Mining" (optymalizacja bitmap pruning)

## 4.2 Wzory Matematyczne

### 1. Support (Wsparcie)

$$Support(X, Y) = \frac{|{t \in T : X \cup Y \subseteq t}|}{|T|}$$

Gdzie:

- $T$ - zbiór wszystkich transakcji (zamówień)
- $t$ - pojedyncza transakcja
- $X, Y$ - produkty

**Interpretacja:** Jaka część wszystkich transakcji zawiera zarówno produkt X jak i Y?

### 2. Confidence (Pewność)

$$Confidence(X \rightarrow Y) = \frac{Support(X, Y)}{Support(X)}$$

**Interpretacja:** Jeśli klient kupił X, jakie jest prawdopodobieństwo że kupi również Y?

### 3. Lift (Wzmocnienie)

$$Lift(X \rightarrow Y) = \frac{Support(X, Y)}{Support(X) \times Support(Y)} = \frac{Confidence(X \rightarrow Y)}{Support(Y)}$$

**Interpretacja:**

- **Lift > 1:** Pozytywna korelacja - produkty kupowane razem częściej niż losowo
- **Lift = 1:** Niezależność - brak związku
- **Lift < 1:** Negatywna korelacja - produkty kupowane razem rzadziej niż losowo

## 4.3 Implementacja w Backend

### Plik: `backend/home/custom_recommendation_engine.py`

#### Klasa: `CustomAssociationRules`

**Inicjalizacja z progami:**

```python
class CustomAssociationRules:
    def __init__(self, min_support=0.01, min_confidence=0.1):
        self.min_support = min_support      # Domyślnie 1%
        self.min_confidence = min_confidence # Domyślnie 10%
        self.max_transactions = 3000
        self.max_items_per_transaction = 20
```

**Funkcja główna - generowanie reguł:**

```python
def generate_association_rules(self, transactions):
    """
    Generuje reguły asocjacyjne algorytmem Apriori z cache'owaniem.
    """
    cache_key = f"association_rules_{len(transactions)}_{self.min_support}_{self.min_confidence}"
    cached_result = cache.get(cache_key)

    if cached_result:
        return cached_result

    # Filtruj transakcje (min. 2 produkty)
    filtered_transactions = []
    for transaction in transactions[:self.max_transactions]:
        limited_transaction = transaction[:self.max_items_per_transaction]
        if len(limited_transaction) >= 2:
            filtered_transactions.append(limited_transaction)

    # Znajdź częste itemsety (z optymalizacją bitmap)
    frequent_itemsets = self._find_frequent_itemsets_with_bitmap(filtered_transactions)

    # Generuj reguły z frequent itemsets
    rules = self._generate_optimized_rules_from_itemsets(frequent_itemsets, filtered_transactions)

    # Cache na 30 minut
    cache.set(cache_key, rules, timeout=1800)

    return rules
```

**Optymalizacja Bitmap Pruning (Zaki 2000):**

```python
def _find_frequent_itemsets_with_bitmap(self, transactions):
    """
    Optymalizacja: używa operacji bitowych zamiast iteracji po listach.
    """
    total_transactions = len(transactions)
    min_count_threshold = int(self.min_support * total_transactions)

    # Krok 1: Zlicz częstość pojedynczych produktów
    item_counts = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_counts[item] += 1

    # Krok 2: Filtruj produkty spełniające min_support (early pruning)
    frequent_items = {}
    item_to_id = {}
    frequent_item_list = []

    item_id = 0
    for item, count in item_counts.items():
        if count >= min_count_threshold:
            support = count / total_transactions
            frequent_items[frozenset([item])] = support
            item_to_id[item] = item_id
            frequent_item_list.append(item)
            item_id += 1

    # Krok 3: Konwertuj transakcje do bitmap
    transaction_bitmaps = []
    for transaction in transactions:
        bitmap = 0
        for item in transaction:
            if item in item_to_id:
                bitmap |= (1 << item_to_id[item])  # Ustaw bit
        if bitmap:
            transaction_bitmaps.append(bitmap)

    # Krok 4: Generuj 2-itemsety z operacjami bitowymi
    frequent_2_itemsets = self._generate_2_itemsets_with_bitmap(
        transaction_bitmaps, frequent_item_list, item_to_id,
        min_count_threshold, total_transactions
    )

    return {**frequent_items, **frequent_2_itemsets}
```

**Generowanie 2-itemsetów z bitmap:**

```python
def _generate_2_itemsets_with_bitmap(self, transaction_bitmaps, frequent_items,
                                      item_to_id, min_count_threshold, total_transactions):
    """
    Używa operacji bitowych AND dla szybkiego sprawdzania par.
    """
    frequent_2_itemsets = {}

    for i in range(len(frequent_items)):
        item1 = frequent_items[i]
        item1_bit = 1 << item_to_id[item1]

        for j in range(i + 1, len(frequent_items)):
            item2 = frequent_items[j]
            item2_bit = 1 << item_to_id[item2]

            pair_bitmap = item1_bit | item2_bit  # OR - maska dla pary

            # Zlicz transakcje zawierające oba produkty (operacja AND)
            count = 0
            for transaction_bitmap in transaction_bitmaps:
                if (transaction_bitmap & pair_bitmap) == pair_bitmap:
                    count += 1

            if count >= min_count_threshold:
                support = count / total_transactions
                pair = frozenset([item1, item2])
                frequent_2_itemsets[pair] = support

    return frequent_2_itemsets
```

**Generowanie reguł z metrykami:**

```python
def _generate_optimized_rules_from_itemsets(self, frequent_itemsets, transactions):
    """
    Implementacja wzorów Agrawal & Srikant (1994) oraz Brin et al. (1997).
    """
    rules = []
    total_transactions = len(transactions)

    # Cache wsparcia pojedynczych produktów
    item_support_cache = {}
    for itemset, support in frequent_itemsets.items():
        if len(itemset) == 1:
            item = list(itemset)[0]
            item_support_cache[item] = support

    # Dla każdego 2-itemsetu generuj reguły
    for itemset, support in frequent_itemsets.items():
        if len(itemset) == 2:
            items = list(itemset)
            item1, item2 = items[0], items[1]

            support_1 = item_support_cache.get(item1, 0)
            support_2 = item_support_cache.get(item2, 0)

            # Wzór Confidence (Agrawal & Srikant 1994)
            # Confidence(A→B) = Support(A,B) / Support(A)
            confidence_1_to_2 = support / support_1 if support_1 > 0 else 0
            confidence_2_to_1 = support / support_2 if support_2 > 0 else 0

            # Wzór Lift (Brin et al. 1997)
            # Lift(A→B) = Support(A,B) / (Support(A) × Support(B))
            lift = support / (support_1 * support_2) if (support_1 * support_2) > 0 else 0

            # Dodaj reguły spełniające min_confidence
            if confidence_1_to_2 >= self.min_confidence:
                rules.append({
                    "product_1": item1,
                    "product_2": item2,
                    "support": support,
                    "confidence": confidence_1_to_2,
                    "lift": lift,
                })

            if confidence_2_to_1 >= self.min_confidence:
                rules.append({
                    "product_1": item2,
                    "product_2": item1,
                    "support": support,
                    "confidence": confidence_2_to_1,
                    "lift": lift,
                })

    # Sortuj po lift, potem confidence
    rules.sort(key=lambda x: (x["lift"], x["confidence"]), reverse=True)

    return rules
```

### Plik: `backend/home/association_views.py`

#### Klasa: `UpdateAssociationRulesAPI`

**Endpoint do aktualizacji reguł:**

```python
def post(self, request):
    min_support = float(request.data.get('min_support', 0.005))    # 0.5%
    min_confidence = float(request.data.get('min_confidence', 0.05)) # 5%
    min_lift = float(request.data.get('min_lift', 1.0))             # > 1.0

    # Pobierz transakcje z zamówień
    orders = Order.objects.prefetch_related("orderproduct_set")[:2000]

    transactions = []
    for order in orders:
        product_ids = [str(item.product_id) for item in order.orderproduct_set.all()]
        if len(product_ids) >= 2:
            transactions.append(product_ids)

    # Uruchom algorytm Apriori
    association_engine = CustomAssociationRules(
        min_support=min_support,
        min_confidence=min_confidence
    )
    rules = association_engine.generate_association_rules(transactions)

    # Zapisz do bazy (bulk insert po 200 rekordów)
    for rule in rules[:1000]:
        if rule["lift"] >= min_lift:
            ProductAssociation.objects.create(
                product_1_id=int(rule["product_1"]),
                product_2_id=int(rule["product_2"]),
                support=rule["support"],
                confidence=rule["confidence"],
                lift=rule["lift"],
            )
```

#### Klasa: `FrequentlyBoughtTogetherAPI`

**Endpoint dla koszyka:**

```python
def get(self, request):
    cart_product_ids = request.GET.getlist("product_ids[]")

    recommendations = []
    seen_product_ids = set()

    for product_id in cart_product_ids:
        # Pobierz reguły asocjacyjne dla produktu
        associations = (
            ProductAssociation.objects
            .filter(product_1_id=int(product_id))
            .select_related("product_2")
            .order_by("-lift", "-confidence")[:5]  # Top 5 po lift
        )

        for assoc in associations:
            if str(assoc.product_2_id) not in cart_product_ids:
                recommendations.append({
                    "product": ProductSerializer(assoc.product_2).data,
                    "confidence": round(float(assoc.confidence), 2),
                    "lift": round(float(assoc.lift), 2),
                    "support": round(float(assoc.support), 3),
                })

    # Sortuj finalnie po lift i confidence
    recommendations = sorted(
        recommendations,
        key=lambda x: (x["lift"], x["confidence"]),
        reverse=True
    )

    return Response(recommendations[:5])  # Zwróć max 5
```

## 4.4 Tabela w Bazie Danych

### Tabela: `method_productassociation`

| Kolumna      | Typ        | Opis                          |
| ------------ | ---------- | ----------------------------- |
| id           | BigInt     | Klucz główny                  |
| product_1_id | ForeignKey | Produkt źródłowy (antecedent) |
| product_2_id | ForeignKey | Produkt docelowy (consequent) |
| support      | Float      | Wsparcie reguły               |
| confidence   | Float      | Pewność reguły                |
| lift         | Float      | Wzmocnienie reguły            |
| created_at   | DateTime   | Data utworzenia               |

## 4.5 Integracja z Frontend

### Koszyk - "Frequently Bought Together"

**Plik:** `frontend/src/components/CartContent/CartContent.jsx`

```jsx
const fetchRecommendations = async () => {
  setRecommendationsLoading(true);
  try {
    // Zbierz ID produktów z koszyka
    const productIds = Object.keys(items).filter((id) => items[id] > 0);

    // Zbuduj query params
    const params = new URLSearchParams();
    productIds.forEach((id) => params.append("product_ids[]", id));

    // Pobierz rekomendacje Apriori
    const response = await axios.get(
      `${config.apiUrl}/api/frequently-bought-together/?${params.toString()}`
    );

    setRecommendations(response.data);
  } catch (error) {
    console.error("Error fetching cart recommendations:", error);
  } finally {
    setRecommendationsLoading(false);
  }
};

// Wywoływane przy każdej zmianie koszyka
useEffect(() => {
  if (Object.keys(items).length > 0) {
    fetchRecommendations();
  }
}, [items]);
```

**Wyświetlanie rekomendacji z metrykami:**

```jsx
{
  recommendations.map((rec, index) => (
    <div key={index} className="cart__recommendation-item">
      <img src={`${config.apiUrl}/media/${rec.product.photos[0]?.path}`} />
      <div className="cart__recommendation-info">
        <h4>{rec.product.name}</h4>
        <p>${rec.product.price}</p>
        <div className="cart__recommendation-stats">
          <span className="stat-confidence">
            Confidence: {(rec.confidence * 100).toFixed(0)}%
          </span>
          <span className="stat-lift">Lift: {rec.lift.toFixed(2)}x</span>
          <span className="stat-support">
            Support: {(rec.support * 100).toFixed(1)}%
          </span>
        </div>
        <button onClick={() => handleAddToCart(rec.product.id)}>
          Add to Cart
        </button>
      </div>
    </div>
  ));
}
```

### Panel Administratora - Debug Association Rules

**Plik:** `frontend/src/components/AdminPanel/AdminDebug.jsx`

```jsx
const fetchAssociationDebug = async (productId) => {
  const res = await axios.get(
    `${config.apiUrl}/api/product-association-debug/?product_id=${productId}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
  setAssociationDebugData(res.data);
};
```

**Wyświetlane informacje:**

- Wszystkie reguły asocjacyjne dla wybranego produktu
- Metryki: Support, Confidence, Lift
- Top 10 reguł posortowanych po Lift
- Statystyki (średni lift, liczba reguł)

## 4.6 Przepływ Danych - Reguły Asocjacyjne

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    APRIORI - PRZEPŁYW                                    │
└─────────────────────────────────────────────────────────────────────────┘

1. GENEROWANIE REGUŁ (Admin Panel → Backend)
   ┌──────────────────┐
   │  Admin Panel     │ ──► POST /api/update-association-rules/
   │  (React)         │     {min_support: 0.005, min_confidence: 0.05, min_lift: 1.0}
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Order +         │ ──► Pobierz zamówienia z 2+ produktami
   │  OrderProduct    │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Transactions    │ ──► [[prod1, prod2, prod3], [prod2, prod4], ...]
   │  (listy ID)      │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Early Pruning   │ ──► Usuń produkty z support < min_support
   │                  │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Bitmap          │ ──► Konwertuj transakcje do bitmap
   │  Conversion      │     Transaction [1,3,5] → 0b100101
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  2-Itemsets      │ ──► Użyj operacji bitowych AND
   │  (bitmap AND)    │     (transaction & pair_mask) == pair_mask
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Oblicz metryki  │ ──► Support = count / total
   │  Support,        │     Confidence = Support(A,B) / Support(A)
   │  Confidence,     │     Lift = Support(A,B) / (Support(A) × Support(B))
   │  Lift            │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  ProductAssoc.   │ ──► Zapisz reguły do bazy (bulk insert)
   │  (tabela DB)     │
   └──────────────────┘

2. POBIERANIE REKOMENDACJI (Cart → Backend)
   ┌──────────────────┐
   │  CartContent     │ ──► GET /api/frequently-bought-together/?product_ids[]=1&product_ids[]=2
   │  (React)         │
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  FrequentlyBought│ ──► SELECT * FROM ProductAssociation
   │  TogetherAPI     │     WHERE product_1_id IN (1,2)
   │                  │     ORDER BY lift DESC, confidence DESC
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │  Response JSON   │ ──► [{product: {...}, confidence: 0.85, lift: 2.3, support: 0.02}, ...]
   │                  │
   └──────────────────┘
```

---

# 5. Integracja z Frontend

## 5.1 Miejsca Użycia Metod

### 5.1.1 Strona Główna (NewProducts.jsx)

**Lokalizacja:** `frontend/src/components/NewProducts/NewProducts.jsx`

**Używana metoda:** Ta którą wybierze admin w panelu (collaborative, content_based, fuzzy_logic)

**Endpoint:** `GET /api/recommendation-preview/?algorithm={algorithm}`

```jsx
// Pobierz aktywny algorytm
const settingsResponse = await axios.get(
  `${config.apiUrl}/api/recommendation-settings/`
);
const algorithm = settingsResponse.data.active_algorithm || "collaborative";

// Pobierz rekomendacje
const response = await axios.get(
  `${config.apiUrl}/api/recommendation-preview/?algorithm=${algorithm}`
);
```

### 5.1.2 Panel Klienta - Dashboard (ClientDashboard.jsx)

**Lokalizacja:** `frontend/src/components/ClientPanel/ClientDashboard.jsx`

**Używana metoda:** Ta którą wybierze admin w panelu

**Sekcja:** "Recommended For You"

```jsx
// Tytuł zmienia się zależnie od algorytmu
if (algorithm === "collaborative") {
  setRecommendationTitle("Recommended For You (Collaborative Filtering)");
} else if (algorithm === "content_based") {
  setRecommendationTitle("Recommended For You (Content-Based)");
} else if (algorithm === "fuzzy_logic") {
  setRecommendationTitle("Recommended For You (Fuzzy Logic)");
}
```

### 5.1.3 Koszyk (CartContent.jsx)

**Lokalizacja:** `frontend/src/components/CartContent/CartContent.jsx`

**Używana metoda:** Reguły Asocjacyjne (Apriori)

**Sekcja:** "Frequently Bought Together"

**Endpoint:** `GET /api/frequently-bought-together/?product_ids[]={ids}`

```jsx
// Wyświetlanie metryk
<span className="stat-confidence">
    Confidence: {(rec.confidence * 100).toFixed(0)}%
</span>
<span className="stat-lift">
    Lift: {rec.lift.toFixed(2)}x
</span>
<span className="stat-support">
    Support: {(rec.support * 100).toFixed(1)}%
</span>
```

### 5.1.4 Wyszukiwarka (SentimentSearchAPIView)

**Lokalizacja:** Backend `sentiment_views.py`

**Używana metoda:** Analiza Sentymentu

**Endpoint:** `GET /api/sentiment-search/?q={query}`

**Sortowanie:** Produkty posortowane według zagregowanego sentymentu (malejąco)

### 5.1.5 Panel Administratora - Debug (AdminDebug.jsx)

**Lokalizacja:** `frontend/src/components/AdminPanel/AdminDebug.jsx`

**Dostępne zakładki:**

1. **Collaborative Filtering** - `/api/collaborative-filtering-debug/`
2. **Sentiment Analysis** - `/api/sentiment-analysis-debug/`, `/api/sentiment-product-debug/`
3. **Association Rules** - `/api/product-association-debug/`
4. Content-Based (inna praca)
5. Fuzzy Logic (inna praca)
6. Probabilistic (inna praca)

## 5.2 Endpointy API

| Endpoint                              | Metoda   | Opis                                  | Używana przez                |
| ------------------------------------- | -------- | ------------------------------------- | ---------------------------- |
| `/api/recommendation-settings/`       | GET/POST | Pobierz/ustaw aktywny algorytm        | Admin Panel, NewProducts     |
| `/api/recommendation-preview/`        | GET      | Rekomendacje dla użytkownika          | NewProducts, ClientDashboard |
| `/api/frequently-bought-together/`    | GET      | Reguły asocjacyjne dla koszyka        | CartContent                  |
| `/api/sentiment-search/`              | GET      | Wyszukiwanie z sortowaniem sentymentu | SearchBar                    |
| `/api/update-association-rules/`      | POST     | Regeneracja reguł Apriori             | Admin Panel                  |
| `/api/collaborative-filtering-debug/` | GET      | Debug CF                              | Admin Panel                  |
| `/api/sentiment-product-debug/`       | GET      | Debug sentymentu produktu             | Admin Panel                  |
| `/api/product-association-debug/`     | GET      | Debug reguł asocjacyjnych             | Admin Panel                  |

---

# Podsumowanie

## Metody i ich zastosowanie w aplikacji

| Metoda                      | Backend                                                   | Frontend                                 | Wzór                                              |
| --------------------------- | --------------------------------------------------------- | ---------------------------------------- | ------------------------------------------------- |
| **Collaborative Filtering** | `recommendation_views.py`                                 | NewProducts, ClientDashboard, AdminDebug | Adjusted Cosine Similarity (Sarwar 2001)          |
| **Analiza Sentymentu**      | `sentiment_views.py`, `custom_recommendation_engine.py`   | Wyszukiwarka, AdminDebug                 | (pos - neg) / total (Liu 2012)                    |
| **Reguły Asocjacyjne**      | `association_views.py`, `custom_recommendation_engine.py` | CartContent, AdminDebug                  | Apriori: Support, Confidence, Lift (Agrawal 1994) |

## Cache

- **Typ:** Database Cache (PostgreSQL)
- **Tabela:** `recommendation_cache_table`
- **Timeouty:** 5 min (short), 30 min (medium), 2h (long)
- **Inwalidacja:** Automatyczna przez Django Signals przy nowych zakupach/opiniach
