# Propozycje tematów pracy magisterskiej — wersja finalna

**Rozszerzenie pracy inżynierskiej SmartRecommender o warstwę badawczo-eksperymentalną**

| | |
|---|---|
| **Autorzy** | Dawid Olko, Piotr Smoła |
| **Promotor** | dr inż. Piotr Grochowalski |
| **Jednostka** | Uniwersytet Rzeszowski, Wydział Nauk Ścisłych i Technicznych |
| **Repozytorium** | github.com/dawidolko/SmartRecommender-Project-Django-React |
| **Data** | 2026-05-02 |

---

## Streszczenie

Niniejszy dokument finalizuje wybór tematów dwóch równoległych prac magisterskich, stanowiących rozszerzenie wcześniejszej pracy inżynierskiej. Zachowujemy w całości istniejącą architekturę aplikacji (Django + React + PostgreSQL) oraz sześć zaimplementowanych metod rekomendacyjnych jako bazę odniesienia. Dokładamy warstwę badawczą: powtarzalny zbiór danych testowych z personami, wspólny moduł oceny offline, oraz dwa rozdzielne kierunki badawcze.

**Olko**: hybrydowe łączenie metod (CF + Sentyment + Apriori) z udziałem modeli LLM.
**Smoła**: segmentacja użytkowników metodami klasteryzacji oraz wnioskowanie rozmyte typu drugiego (IT2-FLS) jako zamiennik logiki Mamdani T1.

Oba tematy zostały bezpośrednio zaakceptowane lub zasugerowane przez promotora i są zgodne z bieżącymi trendami w literaturze (LLM4Rec, IT2-FLS, segmentowane systemy hybrydowe).

---

## Spis treści

1. Punkt wyjścia — stan obecny po pracy inżynierskiej
2. Co należy poprawić w istniejącym projekcie zanim zaczniemy badania
3. Ostateczny podział tematów
4. Wspólna infrastruktura badawcza (rdzeń projektu)
5. Tabelaryczne porównanie tematów
6. Harmonogram realizacji
7. Ryzyka i plany awaryjne
8. Pytania do uzgodnienia z promotorem

---

## 1. Punkt wyjścia — stan obecny po pracy inżynierskiej

W ramach pracy inżynierskiej zrealizowanej wspólnie przez autorów powstał działający system rekomendacji produktów `SmartRecommender` w architekturze:

- **Backend**: Django 5.1 + Django REST Framework + PostgreSQL 16
- **Frontend**: React 18 (SPA) z uwierzytelnianiem JWT
- **Konteneryzacja**: Docker Compose (3 usługi: db, backend, frontend)
- **Baza**: 24 tabele, ok. 70 endpointów REST, panel admina i klienta

Zaimplementowano 6 metod rekomendacyjnych (oraz kilka podmodułów, które dla potrzeb badań traktujemy jako 9 niezależnych kanałów rankingowych):

| Lp. | Metoda / Kanał | Autor | Lokalizacja w kodzie |
|-----|----------------|-------|----------------------|
| 1 | Collaborative Filtering (Item-Based, Adjusted Cosine) | Olko | `home/recommendation_views.py` |
| 2 | Content-Based Filtering (Cosine + TF-IDF) | Smoła | `home/recommendation_views.py` |
| 3 | Reguły asocjacyjne — Apriori z bitmap pruning | Olko | `home/custom_recommendation_engine.py` |
| 4 | Logika rozmyta Mamdani typu pierwszego | Smoła | `home/fuzzy_logic_engine.py` |
| 5 | Wyszukiwanie rozmyte (fuzzy search z literówkami) | Smoła (poboczne) | `home/sentiment_views.py::FuzzySearchAPIView` |
| 6 | Analiza sentymentu (słownikowa, Liu 2012) | Olko | `home/custom_recommendation_engine.py::CustomSentimentAnalysis` |
| 7 | Łańcuchy Markowa pierwszego rzędu | Smoła | `home/probabilistic_views.py::MarkovRecommendationsAPI` |
| 8 | Naiwny klasyfikator Bayesa | Smoła | `home/probabilistic_views.py::BayesianInsightsAPI` |
| 9 | Analiza sezonowości (komponent temporalny) | Smoła | `home/seasonal_views.py` |

Każda metoda ma osobny endpoint debugujący (np. `/api/collaborative-filtering-debug/`), co zostało docenione w pracy inżynierskiej i ułatwia walidację w pracy magisterskiej.

---

## 2. Co należy poprawić w istniejącym projekcie zanim zaczniemy badania

Istniejący seeder (`backend/home/management/commands/seed.py`, ~1.4 MB, ~17 300 linii) generuje dane w sposób, który nie wystarcza do rzetelnej oceny metod rekomendacyjnych. Wszystkie poniższe problemy zostały zweryfikowane w kodzie:

| Problem | Aktualny stan w kodzie | Konsekwencja dla badań |
|---------|------------------------|------------------------|
| Mało użytkowników | `seed_users()` tworzy 5 admin + 15 client (linia 297) | Za mało, by liczyć wiarygodne metryki Precision@K |
| Losowe interakcje | `UserInteraction` jest seedowany tylko dorywczo, bez korelacji z zakupem | Brak realistycznego sygnału ukrytego (implicit feedback) |
| Losowe opinie | `seed_opinions()` losuje treść z 60 szablonów bez związku z produktem (linia 16606) | Sentyment per-produkt jest niewiarygodny |
| Losowe daty zamówień | `random.randint(1, 365)` dni wstecz (linia 16803) | Nie da się zrobić temporalnego split (test = ostatnie X% czasu) |
| Losowe wagi probabilistyki | `analytics.py` używa `random.uniform()` w wielu miejscach | Modele probabilistyczne są atrapą, nie ML — co znów potwierdza dokument `.methods/probabilistic_methods.md` |
| Brak persony | Wszyscy klienci kupują wszystko z jednakowym prawdopodobieństwem | Brak struktury, której metody mogłyby się "uczyć" |
| Brak czasu na karcie | `UserInteraction` ma `timestamp`, ale brak `duration_ms` | Nie da się zbadać "dane jawne vs ukryte" w sensie dwell time |
| Brak metadanych eksperymentów | Brak tabeli wyników | Trzeba szukać metryk po logach konsoli zamiast porównywać systematycznie |

### 2.1 Plan naprawczy — nowa komenda `seed_research`

Rozwiązanie: **nowa komenda** `python manage.py seed_research` w pliku `backend/home/management/commands/seed_research.py`. Istniejący `seed.py` zostaje **bez zmian** jako kompatybilność wsteczna z aplikacją produkcyjną i panelem demo.

#### 2.1.1 Persony użytkowników

Definiujemy 5 person zachowaniowych z parametrami liczbowymi:

```python
PERSONAS = {
    "gamer": {
        "preferred_categories": [
            "computers.gaming", "components.graphics",
            "peripherals.mice", "peripherals.headphones",
            "peripherals.keyboards", "gaming.consoles"
        ],
        "avg_basket_size": 2.5,
        "price_sensitivity": "medium",
        "review_propensity": 0.6,      # P(że napisze opinię po zakupie)
        "active_hour": (18, 24),
        "dwell_time_mean_ms": 45000,
    },
    "office_worker": {
        "preferred_categories": [
            "computers.office", "laptops.office",
            "peripherals.printers", "furniture.desks",
            "office.accessories"
        ],
        "avg_basket_size": 1.5,
        "price_sensitivity": "high",
        "review_propensity": 0.2,
        "active_hour": (6, 12),
        "dwell_time_mean_ms": 25000,
    },
    "content_creator": {
        "preferred_categories": [
            "peripherals.microphones", "peripherals.webcams",
            "components.graphics", "peripherals.monitors",
            "cameras.stabilizers", "peripherals.headphones"
        ],
        "avg_basket_size": 3.0,
        "price_sensitivity": "low",
        "review_propensity": 0.8,
        "active_hour": (12, 18),
        "dwell_time_mean_ms": 60000,
    },
    "gift_buyer": {
        "preferred_categories": [
            "wearables.watches", "electronics.tablets",
            "electronics.phones", "drones", "gadgets"
        ],
        "avg_basket_size": 1.2,
        "price_sensitivity": "medium",
        "review_propensity": 0.4,
        "active_hour": (18, 24),
        "dwell_time_mean_ms": 30000,
        "seasonality": {"11": 2.5, "12": 3.0, "2": 1.8, "5": 1.5},
    },
    "tech_enthusiast": {
        "preferred_categories": [
            "components.processors", "components.motherboards",
            "components.memoryRam", "components.disks",
            "components.cooling", "drones"
        ],
        "avg_basket_size": 4.0,
        "price_sensitivity": "low",
        "review_propensity": 0.9,
        "active_hour": (0, 6),
        "dwell_time_mean_ms": 75000,
    },
}
```

#### 2.1.2 Skala danych — kompromis jakość vs czas obliczeń

| Parametr | Aktualnie | `seed_research` | CLI argument |
|----------|-----------|-----------------|--------------|
| Klienci | 15 | 200 | `--clients 200` |
| Admini | 5 | 5 (bez zmian) | `--admins 5` |
| Produkty | ~500 | ~500 (bez zmian) | `--products 500` |
| Zamówienia | 10 / klient | 5–25 / klient (zależne od persony) | `--orders-per-client-mean 12` |
| Interakcje | brak | 30–150 / klient (view → click → cart → purchase) | `--interactions-per-client-mean 80` |
| Opinie | 2–5 / produkt | 0–8 / produkt (zależne od persony i kategorii) | (auto) |
| Okno czasowe | 365 dni | 730 dni, gęstość rośnie w czasie | `--days-back 730` |
| Seed losowości | brak | `--random-seed 42` (powtarzalność) | `--random-seed 42` |

**Liczby kluczowe**: 200 klientów × 80 interakcji ≈ **16 000 interakcji** + ok. 2 400 zamówień + ok. 3 000 opinii. To wystarcza na wiarygodne Precision@10 (rule of thumb w literaturze: powyżej 5 000 punktów ewaluacyjnych w teście).

#### 2.1.3 Spójność danych (kluczowe ulepszenia)

W stosunku do obecnego `seed.py`:

1. **Zamówienia z kategorii zgodnych z personą**: 80% produktów z kategorii preferowanych, 20% "eksploracji" (poza preferencją) — dzięki temu CF i CBF mają strukturę, którą mogą wykryć.
2. **Sentyment opinii skorelowany z dopasowaniem produktu do persony**: gamer kupujący kartę graficzną wystawia opinię o `sentiment_score ≈ +0.7`; office_worker kupujący tę samą kartę przez przypadek (eksploracja) — `sentiment ≈ −0.2`.
3. **Opinie po zakupie, nie przed**: `Opinion.created_at > Order.date_order` (Opinion nie ma jeszcze pola `created_at` — propozycja migracji w 2.1.4).
4. **Interakcje przed zakupem**: dla każdego zakupu generowane są 3–15 wpisów `UserInteraction` (sekwencja: 5×view → 2×click → 1×add_to_cart → 1×purchase) z timestampami przed zamówieniem.
5. **Sezonowość**: `gift_buyer` kupuje 3× częściej w grudniu, `tech_enthusiast` ma boom w listopadzie (Black Friday) i sierpniu (powrót do nauki).

#### 2.1.4 Migracje schematu bazy

Konieczne dodatki do `home/models.py`:

```python
class UserInteraction(models.Model):
    # ... istniejące pola: user, product, interaction_type, timestamp ...
    duration_ms = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Czas spędzony na karcie produktu w ms (tylko dla 'view')"
    )

class Opinion(models.Model):
    # ... istniejące pola: product, user, content, rating ...
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class UserPersona(models.Model):
    """Powiązanie testowych użytkowników z personą.
    Tylko dla danych badawczych — produkcja używa user.role."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    persona_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'research_user_persona'

class ExperimentRun(models.Model):
    """Tabela logująca wyniki eksperymentów dla pracy magisterskiej."""
    experiment_id = models.CharField(max_length=100, unique=True)
    method_or_combination = models.CharField(max_length=200)
    parameters_json = models.JSONField()
    seed_research_version = models.CharField(max_length=20)

    # Metryki rekomendacji
    precision_at_10 = models.FloatField()
    recall_at_10 = models.FloatField()
    ndcg_at_10 = models.FloatField()
    map_score = models.FloatField()
    coverage = models.FloatField()
    diversity = models.FloatField()

    # Wydajność
    train_size = models.PositiveIntegerField()
    test_size = models.PositiveIntegerField()
    duration_seconds = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'research_experiment_run'
        ordering = ['-created_at']
```

`python manage.py makemigrations && python manage.py migrate` — bez breaking changes do istniejącego kodu produkcyjnego, tylko nowe pola opcjonalne.

#### 2.1.5 Wspólny moduł oceny

Plik: `backend/home/experiments/metrics.py` eksportuje:

- `temporal_split(test_ratio=0.2)` — zwraca `(train_orders, test_orders)` z gwarancją że test = ostatnie X% czasu
- `precision_at_k`, `recall_at_k`, `ndcg_at_k`, `map_score`, `coverage`, `diversity`
- `evaluate_method(method_callable, k=10)` — uniwersalny wrapper

Plik: `backend/home/experiments/runner.py` — klasa `ExperimentRunner`:

1. Wywołuje metodę rekomendacyjną (lub kombinację) dla każdego użytkownika z testu
2. Liczy metryki
3. Zapisuje wynik do tabeli `ExperimentRun`
4. Generuje raport CSV w `experiments/results/`

---

## 3. Ostateczny podział tematów

Po analizie:

- korespondencji od promotora (kombinacja metod, LLM, IT2-FLS, segmentacja — wszystkie zaakceptowane)
- własnych metod inżynierskich (CF, Sentyment, Apriori po stronie Olko)
- metod kolegi (CBF, Fuzzy, Probabilistic po stronie Smoły)
- realistyczności w okresie pracy magisterskiej (12–15 mc)

**Rekomendowany podział**: każdy bierze 2 obszary tak, aby NIE przeszkadzać sobie nawzajem, ale dzielić wspólną infrastrukturę (seeder + ewaluacja + ExperimentRun).

### 3.1 Praca Dawida Olko — CF + Sentyment + Apriori

#### Tytuł roboczy

> **„Hybrydowe łączenie metod rekomendacji z udziałem dużych modeli językowych w systemie e-commerce"**
>
> ang.: *Hybrid Recommendation Method Combination with Large Language Models in an E-commerce System*

#### Pytanie badawcze

Czy kombinacja klasycznych metod rekomendacyjnych (CF + Sentyment + Apriori) ze sobą oraz z modelem LLM daje istotnie lepsze rekomendacje niż każda metoda osobno? Czy LLM rozwiązuje problem zimnego startu lepiej niż CF + Apriori?

#### Hipotezy

- **H1**: Fuzja rankingowa (RRF / Borda / weighted average) z 3 metod (CF + Sentyment + Apriori) poprawia NDCG@10 o ≥10% względem najlepszego pojedynczego rankera.
- **H2**: Dla użytkowników z <3 zamówieniami w historii LLM (Bielik 11B lub Mistral Small) daje wyższy NDCG@10 niż klasyczne CF i Apriori (przewaga w cold-start).
- **H3**: Hybryda LLM + klasyka (LLM jako jeden z rankerów w fuzji) przewyższa zarówno czysty LLM jak i czystą klasykę.
- **H4**: Hallucination rate (rekomendacje produktów spoza katalogu) dla LLM jest niezerowe i zależy od wielkości modelu.

#### Co konkretnie zrobić w kodzie

**Część A — Refactor metod do wspólnego interfejsu**:

```python
# backend/home/experiments/base_recommender.py
from abc import ABC, abstractmethod

class BaseRecommender(ABC):
    @abstractmethod
    def recommend(self, user_id: int, k: int = 10) -> list[tuple[int, float]]:
        """Zwraca listę [(product_id, score), ...] długości k, sortowane malejąco."""

class CollaborativeFilteringRecommender(BaseRecommender):
    def recommend(self, user_id, k=10):
        # opakowuje istniejące process_collaborative_filtering()
        ...

class SentimentRecommender(BaseRecommender):
    ...

class AprioriRecommender(BaseRecommender):
    ...
```

**Część B — Strategie fuzji rankingów**:

```python
# backend/home/experiments/fusion.py
class ReciprocalRankFusion:
    def __init__(self, recommenders, k_const=60):
        self.recommenders = recommenders
        self.k_const = k_const

    def recommend(self, user_id, k=10):
        scores = defaultdict(float)
        for r in self.recommenders:
            ranking = r.recommend(user_id, k=50)
            for rank, (pid, _) in enumerate(ranking, start=1):
                scores[pid] += 1.0 / (self.k_const + rank)
        return sorted(scores.items(), key=lambda x: -x[1])[:k]

class BordaCount: ...        # sumowanie pozycji
class WeightedAverage: ...   # ważona średnia score'ów (po normalizacji)
class Switching: ...         # wybór metody zależny od profilu użytkownika
```

**Część C — LLM channel**:

```python
# backend/home/experiments/llm_recommender.py
class LLMRecommender(BaseRecommender):
    def __init__(self, model_name="bielik-11b-v3.0-instruct", mode="zero_shot"):
        # mode in {"zero_shot", "few_shot", "rag"}
        self.client = ollama.Client()
        self.model_name = model_name
        self.mode = mode

    def recommend(self, user_id, k=10):
        # 1. Pobierz historię zakupów użytkownika
        # 2. Pobierz listę kandydatów (np. top-100 z CBF żeby nie szukał po 500)
        # 3. Build prompt: "Ten użytkownik kupił X, Y, Z. Mając kandydatów [...],
        #    zarekomenduj 10 produktów uszeregowanych malejąco, w formacie JSON."
        # 4. Wywołaj LLM, sparsuj listę produktów
        # 5. Zwaliduj że ID są w katalogu (hallucination check)
        ...
```

Wybór modeli (open-source):

- **Bielik v3 11B** (polski, Apache 2.0) — kluczowy element pracy ze względu na polskie nazwy produktów i opisy
- **Mistral Small 3 24B** (Apache 2.0) — referencyjny zachodni
- **Qwen 2.5 14B** (Apache 2.0) — referencyjny azjatycki
- Uruchomienie: **Ollama** (najprostsze, działa na karcie GPU 12+ GB lub na CPU dla Bielik 7B)

**Część D — Eksperymenty (zapisywane do `ExperimentRun`)**:

| ID | Konfiguracja | Liczba runów |
|----|--------------|--------------|
| E1.1–E1.3 | CF / Sentyment / Apriori — pojedynczo | 3 |
| E1.4–E1.6 | Pary: CF+Sentyment, CF+Apriori, Sentyment+Apriori (RRF) | 3 |
| E1.7 | Trójka CF+Sentyment+Apriori (RRF) | 1 |
| E1.8–E1.10 | Trójka — Borda, Weighted, Switching | 3 |
| E2.1–E2.3 | Czysty LLM (Bielik 7B, Bielik 11B, Mistral Small) | 3 |
| E2.4–E2.5 | LLM zero-shot vs few-shot (best Bielik) | 2 |
| E2.6 | LLM RAG (Bielik + retrieval z bazy opinii) | 1 |
| E3.1–E3.3 | Hybryda LLM + klasyka (LLM jako 4. ranker w RRF) | 3 |
| **Razem** | | **~19 runów × 5 powtórzeń CV ≈ 95 eksperymentów** |

#### Stack technologiczny — Olko

| Element | Technologia |
|---------|-------------|
| LLM inference | **Ollama** (lokalnie); opcjonalnie vLLM przy GPU |
| Embeddings (RAG) | sentence-transformers, `paraphrase-multilingual-mpnet-base-v2` |
| Vector DB | Qdrant (lekki, lokalny Docker) |
| Statystyka | scipy.stats — Friedman + post-hoc Nemenyi |
| Tracking | własna tabela `ExperimentRun` + eksport CSV (bez MLflow — overhead niepotrzebny) |
| Wizualizacja | matplotlib, seaborn, heatmapa synergii 3×3 |

#### Innowacyjność pracy Olko

1. **Polskie modele LLM** — Bielik v3 jest praktycznie nieobecny w literaturze rekomendacyjnej (stan na styczeń 2026). Praca uzupełnia tę lukę.
2. **Praktyczne porównanie 4 strategii fuzji** dla systemu e-commerce — większość artykułów testuje 1–2 strategie.
3. **Hallucination rate** w kontekście rekomendacji produktowych — nowa metryka, wcześniej rzadko mierzona w literaturze rec-sys.
4. **Reprodukowalny seed** — dane testowe i konfiguracja dostępne razem z pracą (open science).

#### Kluczowa literatura — Olko

- Burke, R. (2002). *Hybrid Recommender Systems: Survey and Experiments*. UMUAI 12(4).
- Sarwar, B. et al. (2001). *Item-based collaborative filtering recommendation algorithms*. WWW '01.
- Wu, L. et al. (2024). *A Survey on Large Language Models for Recommendation*. arXiv:2305.19860.
- Bao, K. et al. (2023). *TALLRec: An Effective and Efficient Tuning Framework to Align LLM with Recommendation*. RecSys '23.
- Hou, Y. et al. (2024). *Large Language Models are Zero-Shot Rankers for Recommender Systems*. ECIR '24.
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS.
- Ociepa, K. et al. (2026). *Advancing Polish Language Modeling — Bielik v3*. arXiv.

---

### 3.2 Praca Piotra Smoły — CBF + Fuzzy + Probabilistic

#### Tytuł roboczy

> **„Segmentacja użytkowników i wnioskowanie przedziałowe (IT2-FLS) w hybrydowym systemie rekomendacji produktów"**
>
> ang.: *User Segmentation and Interval Type-2 Fuzzy Inference in a Hybrid Product Recommendation System*

#### Pytania badawcze

1. Czy podział użytkowników na segmenty (K-Means / DBSCAN) i osobny dobór wag metod CBF / Fuzzy / Probabilistic dla każdego segmentu poprawia jakość rekomendacji względem konfiguracji globalnej?
2. Czy wnioskowanie rozmyte typu drugiego (IT2-FLS, biblioteka **pyit2fls** wskazana przez promotora) — które uwzględnia niepewność funkcji przynależności — daje lepsze rekomendacje niż obecny system Mamdani T1, szczególnie w warunkach rzadkich danych (cold-start)?

#### Hipotezy

- **H1**: Strategia świadoma segmentacji (cluster-aware) przewyższa najlepszą globalną konfigurację o ≥3% w NDCG@10.
- **H2**: Optymalna liczba segmentów dla zbioru testowego mieści się w przedziale 4–7 (zgodnie z RFM).
- **H3**: IT2-FLS daje wyższą Precision@10 niż T1 dla użytkowników z <5 ocenami (gdzie niepewność jest istotna).
- **H4**: Szerokość przedziału ufności (output IT2-FLS) koreluje istotnie z błędem predykcji — szeroki przedział = niska pewność.
- **H5**: Koszt obliczeniowy IT2-FLS (defuzy Karnik–Mendel) jest 5–20× wyższy niż T1, ale opłacalny tylko w cold-start.

#### Co konkretnie zrobić w kodzie

**Część A — Feature engineering użytkowników**:

```python
# backend/home/experiments/user_features.py
def build_user_feature_vector(user) -> np.ndarray:
    return np.array([
        avg_order_value(user),            # 1. RFM-Monetary
        purchase_frequency(user),         # 2. RFM-Frequency
        category_entropy(user),           # 3. Shannon nad kategoriami
        review_to_order_ratio(user),      # 4. ile pisze opinii
        avg_sentiment_of_opinions(user),  # 5. tonacja
        avg_dwell_time_ms(user),          # 6. z UserInteraction.duration_ms
        recency_days(user),               # 7. RFM-Recency
        seasonality_score(user),          # 8. jak bardzo sezonowy
        active_hour_avg(user),            # 9.
    ])
```

**Część B — Klasteryzacja**:

```python
# backend/home/experiments/segmentation.py
class UserSegmentation:
    def __init__(self, method="kmeans"):
        self.method = method

    def fit(self, X):
        if self.method == "kmeans":
            best_k, best_model = self._find_best_kmeans(X, k_range=range(2, 11))
            self.model = best_model
        elif self.method == "dbscan":
            self.model = DBSCAN(eps=self._auto_eps(X), min_samples=5).fit(X)
        elif self.method == "gmm":
            best_n, best_model = self._find_best_gmm(X, n_range=range(2, 11))
            self.model = best_model

    def predict(self, X):
        return self.model.predict(X) if self.method != "dbscan" else self.model.fit_predict(X)
```

**Część C — Optymalizacja wag per-segment**:

```python
# backend/home/experiments/segment_optimizer.py
class PerSegmentOptimizer:
    """Dla każdego segmentu znajduje najlepsze wagi (w_cbf, w_fuzzy, w_prob)."""

    def fit(self, segments_dict, train_orders):
        for cluster_id, user_ids in segments_dict.items():
            best_weights = self._grid_search_weights(user_ids, train_orders)
            self.weights[cluster_id] = best_weights

    def recommend(self, user_id, k=10):
        cluster = self.cluster_of(user_id)
        w_cbf, w_fuzzy, w_prob = self.weights[cluster]
        s_cbf = self.cbf.score(user_id)
        s_fuzzy = self.fuzzy.score(user_id)
        s_prob = self.prob.score(user_id)
        final = w_cbf * s_cbf + w_fuzzy * s_fuzzy + w_prob * s_prob
        return top_k(final, k)
```

**Część D — IT2-FLS jako alternatywa Mamdani T1**:

```python
# backend/home/it2_fuzzy_logic_engine.py
import pyit2fls

class IT2RecommendationEngine:
    """Wnioskowanie rozmyte typu drugiego dla scoringu produktów.

    Wymiary wejściowe:
      - cena: tani / średni / drogi (IT2FS z FOU = ±20% względem T1)
      - jakość: niska / średnia / wysoka (sentiment-based)
      - popularność: niska / średnia / wysoka (zakupy w okresie)

    Wyjście:
      - score: niski / średni / wysoki (przedział [low, high])
    """

    def __init__(self):
        # Definicja FOU (Footprint of Uncertainty)
        self.cena_tani = pyit2fls.IT2FS_Gaussian_UncertMean(...)
        self.cena_sredni = pyit2fls.IT2FS_Gaussian_UncertMean(...)
        # ...
        self.system = pyit2fls.IT2Mamdani(...)
        self._add_rules()

    def score_product(self, product, user):
        cena_norm = normalize_price(product.price)
        jakosc = sentiment_summary(product)
        popularnosc = buy_count_30d(product)
        # Defuzyfikacja Karnik-Mendel
        result = self.system.evaluate({
            "cena": cena_norm,
            "jakosc": jakosc,
            "popularnosc": popularnosc
        })
        return result["score"]

    def score_with_uncertainty(self, product, user):
        result = self.system.evaluate(...)
        return result["score_low"], result["score_high"]
```

**Część E — Eksperymenty**:

| ID | Konfiguracja | Liczba runów |
|----|--------------|--------------|
| E1.1–E1.3 | CBF / Fuzzy T1 / Probabilistic — pojedynczo | 3 |
| E2.1 | Globalna kombinacja CBF+Fuzzy T1+Prob (najlepsze wagi globalne) | 1 |
| E2.2–E2.4 | K-Means k=4/5/6 — weighted CBF+Fuzzy+Prob per segment | 3 |
| E2.5 | DBSCAN — outlier detection + fallback to global | 1 |
| E2.6 | GMM 5 klastrów | 1 |
| E3.1 | IT2-FLS pojedynczo | 1 |
| E3.2 | IT2-FLS + CBF + Prob (per segment) | 1 |
| E3.3 | T1 vs IT2-FLS — sparowane porównanie na 3 segmentach | 3 |
| E3.4 | Pomiar szerokości CI vs błąd predykcji | 1 |
| **Razem** | | **~15 runów × 5 CV ≈ 75 eksperymentów** |

#### Stack technologiczny — Smoła

| Element | Technologia |
|---------|-------------|
| Klasteryzacja | scikit-learn (KMeans, DBSCAN, GaussianMixture) |
| Redukcja wymiarów | scikit-learn PCA, umap-learn |
| Walidacja klastrów | Silhouette, Davies-Bouldin, Calinski-Harabasz |
| **IT2-FLS** | **pyit2fls** (`pip install pyit2fls`) — wskazane przez promotora |
| Numeryka | NumPy, SciPy |
| Wizualizacja | matplotlib (membership, FOU plots), seaborn |
| Statystyka | scipy.stats — sparowany Wilcoxon |

#### Innowacyjność pracy Smoły

1. **Zastosowanie IT2-FLS w rekomendacjach** — w polskim środowisku akademickim praktycznie nieobecne; większość prac IT2-FLS dotyczy sterowania i finansów.
2. **Empiryczne porównanie T1 vs T2 fuzzy w warunkach cold-start** — odpowiedź na pytanie "czy złożoność IT2 się opłaca".
3. **Confidence-aware ranking** — produkty z szerokim przedziałem ufności są deprezjonowane lub oznaczane do uwagi użytkownika (mod UI).
4. **Per-segment weight tuning** — automatyczne mapowanie segment → konfiguracja, rzadko spotykane systemowo w literaturze.

#### Kluczowa literatura — Smoła

- Pazzani, M. & Billsus, D. (2007). *Content-Based Recommendation Systems*. The Adaptive Web.
- Mendel, J. M. (2017). *Uncertain Rule-Based Fuzzy Systems*, wyd. 2. Springer.
- Karnik, N. N. & Mendel, J. M. (2001). *Centroid of a type-2 fuzzy set*. Information Sciences.
- Wu, D. (2013). *Approaches for reducing the computational cost of IT2-FLS*. IEEE TFS.
- Haghrah, A. A. & Ghaemi, S. (2023). *PyIT2FLS: A New Python Toolkit for IT2-FLS*. arXiv:1909.10051.
- MacQueen, J. (1967). *Some methods for classification and analysis*. Berkeley Symp.
- Ester, M. et al. (1996). *DBSCAN*. KDD.
- Hennig-Thurau, T. et al. (2012). *Automated Group Recommender Systems*. J. of Marketing.

---

## 4. Wspólny rdzeń projektu

Kawałki, które każdy z autorów musi mieć w swojej pracy, więc warto zaimplementować raz i podzielić się autorstwem rozdziału (np. „Rozdział: Infrastruktura badawcza" w obu pracach z odpowiednimi referencjami do siebie nawzajem).

### 4.1 `seed_research` — szczegółowy plan

Plik: `backend/home/management/commands/seed_research.py`

```python
class Command(BaseCommand):
    help = "Generuje powtarzalny zbiór badawczy z personami."

    def add_arguments(self, parser):
        parser.add_argument("--clients", type=int, default=200)
        parser.add_argument("--admins", type=int, default=5)
        parser.add_argument("--products", type=int, default=500)
        parser.add_argument("--days-back", type=int, default=730)
        parser.add_argument("--orders-per-client-mean", type=int, default=12)
        parser.add_argument("--interactions-per-client-mean", type=int, default=80)
        parser.add_argument("--random-seed", type=int, default=42)
        parser.add_argument("--reset", action="store_true",
                          help="Wyczyść bazę przed seedowaniem (DROP CASCADE)")

    def handle(self, *args, **opts):
        random.seed(opts["random_seed"])
        np.random.seed(opts["random_seed"])

        if opts["reset"]:
            self._drop_research_data()

        # 1. Produkty (zachowujemy z istniejącego seeda lub importujemy)
        self._ensure_products(opts["products"])

        # 2. Persony — rozdziel klientów po 5 personach
        personas = self._distribute_personas(opts["clients"])

        # 3. Użytkownicy z personami (zapis do UserPersona)
        users = self._create_users(personas, opts["admins"])

        # 4. Zamówienia (temporalnie spójne, persona-driven)
        self._create_orders(users, days_back=opts["days_back"])

        # 5. Interakcje (view/click przed zakupem, persona-driven)
        self._create_interactions(users)

        # 6. Opinie (po zakupie, sentyment-persona-correlated)
        self._create_opinions(users)

        # 7. Sentiment summary, similarity, association rules — przeliczenia
        self._recompute_all_methods()

        # 8. Zapisz metadane seedowania
        self._log_seed_metadata(opts)
```

### 4.2 `home/experiments/` — wspólny moduł

```
backend/home/experiments/
├── __init__.py
├── base_recommender.py    # BaseRecommender + adaptery do istniejących metod
├── metrics.py              # precision@k, recall@k, ndcg@k, map, coverage, diversity
├── splits.py               # temporal_split, leave_last_one_out, k_fold_user
├── runner.py               # ExperimentRunner — uruchamia, mierzy, loguje
├── reporter.py             # generator raportów CSV i wykresów
└── tests/
    ├── test_metrics.py
    └── test_splits.py
```

Wspólne API:

```python
from home.experiments import temporal_split, ExperimentRunner

train, test = temporal_split(test_ratio=0.2)
runner = ExperimentRunner(method=my_recommender, k=10)
results = runner.evaluate(test_users=test["users"], ground_truth=test["orders"])
runner.save_to_db(experiment_id="E1.1_CF_solo", notes="Baseline CF")
```

### 4.3 Tracking dwell time (frontend + backend) — opcjonalny

Implementujemy tylko jeśli Smoła w rzeczywistości używa `dwell_time_mean_ms` w `build_user_feature_vector()`.

**Backend**: migracja `UserInteraction.duration_ms`, rozszerzenie endpointu `POST /api/interaction/` o pole `duration_ms`.

**Frontend** (`frontend/src/components/ProductSection/ProductPage.jsx`):

```javascript
useEffect(() => {
  const enterTime = Date.now();
  return () => {
    const durationMs = Date.now() - enterTime;
    axios.post('/api/interaction/', {
      product: productId,
      interaction_type: 'view',
      duration_ms: durationMs
    });
  };
}, [productId]);
```

Drobne zmiany, kilka godzin pracy. Może być wyłączone feature flagiem `REACT_APP_TRACK_DWELL=true` w produkcji.

### 4.4 Panel diagnostyczny eksperymentów (opcjonalnie)

W panelu admina dodać kartę **„Eksperymenty"** w `frontend/src/components/AdminPanel/`:

- Lista zdefiniowanych eksperymentów (z `ExperimentRun.experiment_id`)
- Wykres porównawczy NDCG@10 dla wybranego zbioru eksperymentów
- Eksport do CSV
- Przycisk „Uruchom" wyzwalający Django management command w tle (Celery lub po prostu `subprocess.Popen`)

To opcjonalne — eksperymenty można uruchamiać z terminala. Panel UI dodaje wartości jeśli promotor chce widzieć demo na obronie.

---

## 5. Tabelaryczne porównanie tematów

| Aspekt | Olko (Konfig. A) | Smoła (Konfig. B) |
|--------|------------------|-------------------|
| Tytuł skrócony | Hybrydy + LLM | Segmentacja + IT2-FLS |
| Bazuje na | CF / Sentyment / Apriori | CBF / Fuzzy / Probabilistic |
| Główne pytanie | Czy fuzja + LLM > klasyka? | Czy segmenty + IT2-FLS > globalna T1? |
| Liczba hipotez | 4 | 5 |
| Liczba eksperymentów | ~95 | ~75 |
| Najtrudniejszy element | Uruchomienie LLM (GPU lub CPU+czas) | Implementacja IT2-FLS dla 3 wymiarów wejściowych |
| Wymagania sprzętowe | GPU 12 GB+ albo CPU + 16 GB RAM (Bielik 7B) | Standardowy laptop, IT2-FLS jest CPU-bound |
| Ryzyka | Hallucinations LLM, długi czas inferencji | Złożoność defuzy KM, czasochłonny grid search wag |
| Wsparcie literaturowe | bardzo dobre (Da'u 2025, Bao 2023, Wu 2024) | dobre (Mendel 2017, Karnik–Mendel 2001, Haghrah 2023) |
| Stanowisko promotora | LLM „interesujące, na topie" + kombinacja „dobra ścieżka" | IT2-FLS „moja propozycja" + segmentacja „warto" |

---

## 6. Harmonogram (12 miesięcy, oboje równolegle)

| Mies. | Kamień milowy | Wspólne | Olko | Smoła |
|-------|---------------|---------|------|-------|
| 1 | Infrastruktura | seed_research v1, ExperimentRun, metrics module | – | – |
| 2 | Refactor metod | adaptery `BaseRecommender` | CF/Sent/Apr → Recommender | CBF/Fuzzy/Prob → Recommender |
| 3 | Baseline | – | E1.* (single) | E1.* (single) |
| 4–5 | Główne metody | – | Fuzja + LLM channel | Segmentacja + IT2-FLS |
| 6–7 | Eksperymenty | – | E2.*, E3.* | E2.*, E3.* |
| 8 | Analiza statystyczna | wspólne testy Friedman | wykresy synergii | wykresy CI vs error |
| 9–10 | Pisanie pracy | – | rozdziały 1–7 | rozdziały 1–7 |
| 11 | Dopracowanie | – | review koleżeńskie | review koleżeńskie |
| 12 | Obrona | – | – | – |

---

## 7. Ryzyka i plany awaryjne

| Ryzyko | Prawdop. | Plan B |
|--------|----------|--------|
| LLM nie chce się uruchomić lokalnie (Olko) | średnie | Przejście na API OpenRouter z creditem; lub redukcja modelu do Bielik 7B na CPU |
| pyit2fls okazuje się buggy / niedokończony (Smoła) | niskie | Implementacja własna IT2-FLS na bazie NumPy + Karnik–Mendel z literatury |
| Dane są zbyt mało zróżnicowane (oboje) | niskie | Zwiększenie skali seedera do 500 użytkowników, dodanie kolejnych person |
| Eksperymenty trwają zbyt długo | średnie | Próbkowanie testowe na 50% użytkowników, zwężenie zakresu CV |
| Promotor zmienia zdanie co do podziału | niskie | Konfiguracja jest modułowa — każdy temat samodzielny, zamiana o nic nie utrudnia |

---

## 8. Pytania do uzgodnienia z promotorem

1. Czy zaproponowany podział (Olko = LLM + kombinacja, Smoła = segmentacja + IT2-FLS) jest akceptowalny?
2. Czy promotor przewiduje publikację wyników (artykuł na konferencję, np. PP-RAI, FedCSIS)? To wpłynie na język pisania (pl/en) i staranność eksperymentu.
3. Czy dostępne jest zaplecze obliczeniowe na uczelni (GPU, klaster) dla części LLM Olko?
4. Czy akceptowalny jest wybór modeli LLM open-source (Bielik) zamiast komercyjnych (GPT-4)? Argumentacja: reprodukowalność + brak kosztów + polski model = lokalny wkład naukowy.
5. Czy rozszerzyć UI o panel diagnostyczny eksperymentów (przyciski „Uruchom E1.1", live preview wyników) czy zostać przy management commands z terminala?
6. Jaka jest minimalna i maksymalna oczekiwana objętość pracy magisterskiej (liczba stron) w Pana wymaganiach?

---

*Dokument przygotowany jako finalna rekomendacja po analizie istniejącej bazy kodu, korespondencji z promotorem oraz dwóch wcześniejszych dokumentów propozycji (`propozycje.md` i `propozycje_tematow_magisterskich_v2.pdf`). Wszystkie wskazane interwencje w kodzie zostały zweryfikowane na obecnej strukturze projektu.*
