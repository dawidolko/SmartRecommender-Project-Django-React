Ostatnia aktualizacja: 07/10/2025

# 🧠 Analiza Sentymentu w Wyszukiwaniu Produktów

## Czym Jest "Wyszukiwanie Oparte na Sentymencie" w Sklepie?

Wyszukiwanie oparte na sentymencie to inteligentny algorytm odkrywania produktów, który:

- **Analizuje WSZYSTKIE dane produktu** używając przetwarzania języka naturalnego (NLP):
  - 👥 **Opinie klientów** (waga 40%) - najbardziej wiarygodne źródło
  - 📝 **Opis produktu** (waga 25%) - oficjalny opis od sprzedawcy
  - 🏷️ **Nazwa produktu** (waga 15%) - kluczowe słowa w nazwie
  - 📋 **Specyfikacja techniczna** (waga 12%) - parametry i cechy
  - 🗂️ **Kategorie** (waga 8%) - przynależność do kategorii
- **Oblicza wyniki sentymentu** dla każdego źródła (-1 do +1) używając wzoru Liu, B. (2012)
- **Agreguje wieloźródłowy wynik** używając ważonego uśrednienia
- **Ranguje wyniki wyszukiwania** według satysfakcji klientów
- **Priorytetyzuje pozytywnie oceniane produkty** w wynikach wyszukiwania
- **Pomaga klientom znajdować produkty, które inni kochają**

System czyni sklep inteligentniejszym, wydobywając na powierzchnię produkty z najlepszymi doświadczeniami klientów i najlepszymi opisami, co prowadzi do wyższej satysfakcji klientów i zwiększonej sprzedaży.

---

## 📂 Kluczowe Komponenty Systemu Analizy Sentymentu

### 1. Model `SentimentAnalysis` – 🧠 **Analiza na Poziomie Opinii**

Przechowuje dane sentymentu dla każdej indywidualnej opinii klienta:

- `sentiment_score`: Wartość dziesiętna między -1 (negatywna) a 1 (pozytywna)
- `sentiment_category`: Klasyfikacja jako 'positive', 'neutral' lub 'negative'
- `opinion`: Powiązanie z oryginalną opinią klienta
- `product`: Powiązanie z odpowiednim produktem

### 2. Model `ProductSentimentSummary` – 📊 **Agregacja na Poziomie Produktu**

Agreguje metryki sentymentu dla każdego produktu:

- `average_sentiment_score`: Ogólny wynik sentymentu dla produktu
- `positive_count`: Liczba pozytywnych opinii
- `neutral_count`: Liczba neutralnych opinii
- `negative_count`: Liczba negatywnych opinii
- `total_opinions`: Całkowita liczba przeanalizowanych opinii

### 3. Funkcja `seed_sentiment_data()` – 🔄 **Silnik Analizy**

Przetwarza wszystkie opinie i generuje dane sentymentu:

- Używa **CustomSentimentAnalysis** zamiast TextBlob dla większej kontroli
- Oblicza wyniki polaryzacji dla każdej opinii używając **wzoru SentiWordNet**
- Kategoryzuje opinie na podstawie progów sentymentu z literatury
- Tworzy lub aktualizuje statystyki podsumowujące

### 4. `SentimentSearchAPIView` – 🔍 **Integracja z Wyszukiwaniem (Multi-Source)**

Napędza funkcjonalność wyszukiwania opartego na sentymencie z analizą wieloźródłową:

- Przyjmuje zapytania wyszukiwania od użytkowników
- Dopasowuje produkty do terminów wyszukiwania
- **Analizuje sentyment z 5 źródeł**:
  1. 👥 Opinie klientów (40% wagi)
  2. 📝 Opis produktu (25% wagi)
  3. 🏷️ Nazwa produktu (15% wagi)
  4. 📋 Specyfikacja techniczna (12% wagi)
  5. 🗂️ Kategorie (8% wagi)
- **Oblicza ważony wynik końcowy**: `Final_Score = (Opinion×0.40) + (Desc×0.25) + (Name×0.15) + (Spec×0.12) + (Cat×0.08)`
- Porządkuje wyniki według `final_score` (najwyższe pierwsze)
- Uwzględnia szczegółowe dane sentymentu w wynikach wyszukiwania

### 5. Komponent `SearchModal.jsx` – 👁️ **Interfejs Użytkownika**

Wyświetla interfejs wyszukiwania sentymentu użytkownikom:

- Zapewnia wyniki wyszukiwania w czasie rzeczywistym
- Pokazuje wyniki sentymentu obok produktów
- Pozwala na przełączanie między trybami wyszukiwania (sentiment/fuzzy)

---

## 🤖 Jak Działa Analiza Sentymentu (Krok po Kroku)

### 1. **Przetwarzanie Tekstu - Uniwersalna Funkcja (CustomSentimentAnalysis)**:

```python
# Prawdziwy wzór Liu, B. (2012) zaimplementowany w CustomSentimentAnalysis.analyze_sentiment()
# Ta funkcja analizuje KAŻDY tekst: opinie, opis, nazwę, specyfikację, kategorie
def analyze_sentiment(self, text):
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

    # Wzór Liu, B. (2012): (Pos_Score - Neg_Score) / Total_Words
    sentiment_score = (positive_score - negative_score) / total_words

    # Normalizacja do zakresu [-1, 1]
    sentiment_score = max(-1.0, min(1.0, sentiment_score))

    # Klasyfikacja z progami z literatury (Liu, Bing 2012)
    if sentiment_score > 0.1:
        category = "positive"
    elif sentiment_score < -0.1:
        category = "negative"
    else:
        category = "neutral"

    return sentiment_score, category
```

### 2. **Analiza Wieloźródłowa - Nowe Podejście (SentimentSearchAPIView)**:

```python
# W SentimentSearchAPIView.get() - Analizujemy 5 źródeł danych
def get(self, request):
    analyzer = CustomSentimentAnalysis()

    for product in products:
        # ŹRÓDŁO 1: Opinie klientów (40% wagi)
        opinion_scores = []
        for opinion in product.opinion_set.all()[:20]:
            score, _ = analyzer.analyze_sentiment(opinion.content)
            opinion_scores.append(score)
        opinion_sentiment = sum(opinion_scores) / len(opinion_scores) if opinion_scores else 0.0

        # ŹRÓDŁO 2: Opis produktu (25% wagi)
        desc_score, _ = analyzer.analyze_sentiment(product.description or "")

        # ŹRÓDŁO 3: Nazwa produktu (15% wagi)
        name_score, _ = analyzer.analyze_sentiment(product.name)

        # ŹRÓDŁO 4: Specyfikacja techniczna (12% wagi)
        spec_texts = [f"{spec.parameter_name} {spec.specification}"
                      for spec in product.specification_set.all()[:10]]
        spec_combined = " ".join(spec_texts)
        spec_score, _ = analyzer.analyze_sentiment(spec_combined) if spec_combined else (0.0, "neutral")

        # ŹRÓDŁO 5: Kategorie (8% wagi)
        category_names = " ".join([cat.name for cat in product.categories.all()])
        category_score, _ = analyzer.analyze_sentiment(category_names) if category_names else (0.0, "neutral")

        # AGREGACJA: Oblicz ważony wynik końcowy
        final_score = (
            opinion_sentiment * 0.40 +    # 40% wagi dla opinii
            desc_score * 0.25 +            # 25% wagi dla opisu
            name_score * 0.15 +            # 15% wagi dla nazwy
            spec_score * 0.12 +            # 12% wagi dla specyfikacji
            category_score * 0.08          # 8% wagi dla kategorii
        )
```

**Dlaczego te wagi?**

- 👥 **Opinie (40%)**: Najbardziej wiarygodne - rzeczywiste doświadczenia klientów
- 📝 **Opis (25%)**: Oficjalny opis sprzedawcy z kluczowymi cechami
- 🏷️ **Nazwa (15%)**: Często zawiera słowa jak "Premium", "Pro", "Basic"
- 📋 **Specyfikacja (12%)**: Parametry techniczne (np. "fast", "powerful", "efficient")
- 🗂️ **Kategorie (8%)**: Kontekst produktu (np. "Gaming", "Professional")

### 3. **Proces Wyszukiwania z Wieloźródłową Analizą**:

```python
# W SentimentSearchAPIView
When user searches "laptop":
    1. Znajdź produkty pasujące do zapytania tekstowego
    2. Dla KAŻDEGO produktu:
       a) Analizuj sentyment z opinii → opinion_score
       b) Analizuj sentyment z opisu → desc_score
       c) Analizuj sentyment z nazwy → name_score
       d) Analizuj sentyment ze specyfikacji → spec_score
       e) Analizuj sentyment z kategorii → category_score
       f) Oblicz final_score = weighted sum of all sources
    3. Sortuj produkty według final_score (malejąco)
    4. Zwróć wyniki z szczegółowym breakdown:
       - final_score (główny wynik)
       - sentiment_breakdown (wyniki z każdego źródła)
       - opinion metrics (positive/negative/neutral counts)
```

**Przykład obliczenia:**

```python
# Produkt: "Premium Gaming Laptop"
# Opinie: 5 opinii, średni score = 0.6 (pozytywne)
# Opis: "Excellent performance, powerful graphics" → score = 0.4
# Nazwa: "Premium Gaming Laptop" → score = 0.2
# Specyfikacja: "Fast processor, high quality display" → score = 0.3
# Kategorie: "Gaming, Laptops, Premium" → score = 0.1

final_score = (0.6 × 0.40) + (0.4 × 0.25) + (0.2 × 0.15) + (0.3 × 0.12) + (0.1 × 0.08)
final_score = 0.24 + 0.10 + 0.03 + 0.036 + 0.008
final_score = 0.414 → "Positive" (bo 0.414 > 0.1)
```

### 4. **Wyświetlanie Wyników**:

```jsx
// W SearchModal.jsx
In search results:
    - Pokaż szczegóły produktu (nazwa, cena, zdjęcie)
    - Wyświetl wynik sentymentu (np. 0.75)
    - Wizualnie wskaź poziom sentymentu
```

---

## 📊 Szczegóły Implementacji Technicznej

### Logika Klasyfikacji Sentymentu (Literatura: Liu, Bing 2012):

```python
# Progi oparte na badaniach akademickich
if sentiment_score > 0.1:    # Próg pozytywny
    sentiment_category = 'positive'
elif sentiment_score < -0.1:  # Próg negatywny
    sentiment_category = 'negative'
else:
    sentiment_category = 'neutral'
```

### Wzory Matematyczne Używane:

```python
# 1. Polarity Score dla pojedynczego tekstu (Liu, Bing 2012)
polarity = (positive_count - negative_count) / total_words

# 2. Agregacja wieloźródłowa (nowe podejście)
final_score = (opinion_avg * 0.40) + (desc_score * 0.25) +
              (name_score * 0.15) + (spec_score * 0.12) + (category_score * 0.08)

# 3. Średnia dla opinii
opinion_average = sum(opinion_scores) / len(opinion_scores)
```

### Struktura Odpowiedzi API:

```json
{
  "id": 295,
  "name": "Premium Gaming Laptop",
  "price": 1299.99,
  "sentiment_score": 0.414,
  "sentiment_breakdown": {
    "opinion_score": 0.6,
    "description_score": 0.4,
    "name_score": 0.2,
    "specification_score": 0.3,
    "category_score": 0.1
  },
  "total_opinions": 5,
  "positive_count": 4,
  "negative_count": 0,
  "neutral_count": 1
}
```

### Optymalizacja Bazy Danych:

- Relacje OneToOne dla efektywnych joinów
- Niestandardowe indeksy na często zapytywanych polach
- **Prefetching wieloźródłowy**: `prefetch_related('opinion_set', 'specification_set', 'categories')`
- Limit na opinie (20) i specyfikacje (10) dla wydajności

### Rozważania Wydajności:

- **Real-time analysis**: Analiza wykonywana przy każdym wyszukiwaniu (fresh data)
- **Analiza on-the-fly**: Zamiast pre-computed summaries, analizujemy na żądanie
- **Limit opinii**: Maksymalnie 20 najnowszych opinii dla szybkości
- **Limit specyfikacji**: Maksymalnie 10 parametrów technicznych
- `select_related` i `prefetch_related` dla efektywnych zapytań
- **Cache opportunity**: Możliwość cache'owania wyników na 15 minut

---

## 🛍️ Korzyści Biznesowe Wyszukiwania Opartego na Sentymencie

### Dla Klientów:

- Odkrywanie produktów z najwyższą satysfakcją klientów
- Unikanie produktów z negatywnymi opiniami
- Podejmowanie bardziej pewnych decyzji zakupowych
- Szybsze znajdowanie jakościowych produktów

### Dla Właścicieli Sklepów:

- Automatyczne wyróżnianie dobrze ocenianych produktów
- Zwiększenie współczynników konwersji na jakościowe towary
- Identyfikacja produktów wymagających poprawy
- Budowanie zaufania poprzez przejrzystą analizę opinii

---

## 📈 Przykładowe Metryki Analizy Sentymentu (Multi-Source)

### Przykład 1: Premium Gaming Laptop

| Źródło          | Waga | Raw Score | Wkład do Final |
| --------------- | ---- | --------- | -------------- |
| 👥 Opinie       | 40%  | 0.600     | 0.240          |
| 📝 Opis         | 25%  | 0.400     | 0.100          |
| 🏷️ Nazwa        | 15%  | 0.200     | 0.030          |
| 📋 Specyfikacja | 12%  | 0.300     | 0.036          |
| 🗂️ Kategorie    | 8%   | 0.100     | 0.008          |
| **FINAL SCORE** | 100% | -         | **0.414** ✅   |

**Interpretacja**: Produkt ma pozytywny sentyment (0.414 > 0.1), głównie dzięki doskonałym opiniom klientów i pozytywnemu opisowi.

---

### Przykład 2: Basic Wireless Mouse

| Źródło          | Waga | Raw Score | Wkład do Final |
| --------------- | ---- | --------- | -------------- |
| 👥 Opinie       | 40%  | 0.050     | 0.020          |
| 📝 Opis         | 25%  | -0.100    | -0.025         |
| 🏷️ Nazwa        | 15%  | 0.000     | 0.000          |
| 📋 Specyfikacja | 12%  | 0.100     | 0.012          |
| 🗂️ Kategorie    | 8%   | 0.000     | 0.000          |
| **FINAL SCORE** | 100% | -         | **0.007** 😐   |

**Interpretacja**: Produkt ma neutralny sentyment (0.007 < 0.1), opinie są mieszane, opis zawiera słowa negatywne.

---

### Przykład 3: Cheap Laptop Stand

| Źródło          | Waga | Raw Score | Wkład do Final |
| --------------- | ---- | --------- | -------------- |
| 👥 Opinie       | 40%  | -0.300    | -0.120         |
| 📝 Opis         | 25%  | -0.200    | -0.050         |
| 🏷️ Nazwa        | 15%  | -0.100    | -0.015         |
| 📋 Specyfikacja | 12%  | 0.050     | 0.006          |
| 🗂️ Kategorie    | 8%   | 0.000     | 0.000          |
| **FINAL SCORE** | 100% | -         | **-0.179** ❌  |

**Interpretacja**: Produkt ma negatywny sentyment (-0.179 < -0.1), złe opinie, słabe opisy, słowo "Cheap" w nazwie.

---

### Porównanie Tradycyjnego vs Multi-Source

| Produkt               | Tradycyjne (tylko opinie) | Multi-Source | Różnica |
| --------------------- | ------------------------- | ------------ | ------- |
| Słuchawki Premium     | 0.876                     | 0.782        | -10.7%  |
| Podstawowa Klawiatura | 0.342                     | 0.289        | -15.5%  |
| Mysz Gamingowa        | 0.654                     | 0.598        | -8.6%   |
| Stojak na Laptop      | -0.123                    | -0.179       | +45.5%  |

**Wniosek**: Multi-source approach daje bardziej zrównoważoną ocenę, uwzględniając nie tylko opinie, ale też jakość opisu i specyfikacji produktu.

---

## 🧪 Debugowanie i Weryfikacja Wzorów

### Debug API Endpoint (bez autoryzacji) - NOWY Multi-Source

Endpoint do weryfikacji wzorów matematycznych i obliczeń sentymentu z wszystkich 5 źródeł:

```bash
GET /api/sentiment-analysis-debug/?product_id=295
```

**Przykładowa odpowiedź (Multi-Source Analysis):**

```json
{
  "product_id": 295,
  "product_name": "Premium Gaming Laptop",

  "multi_source_analysis": {
    "opinions": {
      "weight": "40%",
      "count": 5,
      "average_score": 0.600,
      "contribution_to_final": 0.240,
      "sample_details": [
        {
          "opinion_id": 123,
          "opinion_excerpt": "Excellent laptop, very fast and reliable...",
          "calculation": {
            "positive_words_found": 3,
            "negative_words_found": 0,
            "total_words": 45,
            "formula": "(3 - 0) / 45 = 0.067",
            "sentiment_score": 0.067,
            "category": "neutral"
          }
        }
      ],
      "formula": "Σ(5 scores) / 5 = 0.600"
    },

    "description": {
      "weight": "25%",
      "text_excerpt": "Powerful gaming laptop with excellent performance and stunning graphics...",
      "score": 0.400,
      "category": "positive",
      "contribution_to_final": 0.100,
      "positive_words": 4,
      "negative_words": 0,
      "total_words": 28,
      "formula": "(4 - 0) / 28 = 0.143"
    },

    "name": {
      "weight": "15%",
      "text": "Premium Gaming Laptop",
      "score": 0.200,
      "category": "positive",
      "contribution_to_final": 0.030,
      "positive_words": 1,
      "negative_words": 0,
      "total_words": 3,
      "formula": "(1 - 0) / 3 = 0.333"
    },

    "specifications": {
      "weight": "12%",
      "count": 8,
      "combined_score": 0.300,
      "category": "positive",
      "contribution_to_final": 0.036,
      "sample_details": [
        {
          "parameter": "Processor",
          "value": "Fast Intel i7",
          "score": 0.250,
          "category": "positive",
          "positive_words": 1,
          "negative_words": 0
        },
        {
          "parameter": "Graphics",
          "value": "Powerful NVIDIA RTX",
          "score": 0.333,
          "category": "positive",
          "positive_words": 1,
          "negative_words": 0
        }
      ]
    },

    "categories": {
      "weight": "8%",
      "text": "Gaming Laptops Premium",
      "score": 0.100,
      "category": "positive",
      "contribution_to_final": 0.008,
      "positive_words": 1,
      "negative_words": 0,
      "total_words": 3
    }
  },

  "final_calculation": {
    "formula": "Final = (Opinion×0.40) + (Desc×0.25) + (Name×0.15) + (Spec×0.12) + (Cat×0.08)",
    "calculation": "(0.600×0.40) + (0.400×0.25) + (0.200×0.15) + (0.300×0.12) + (0.100×0.08)",
    "final_score": 0.414,
    "final_category": "Positive",
    "breakdown": {
      "from_opinions": 0.240,
      "from_description": 0.100,
      "from_name": 0.030,
      "from_specifications": 0.036,
      "from_categories": 0.008
    }
  },

  "formulas_used": {
    "per_text": "Sentiment_Score = (Positive_Count - Negative_Count) / Total_Words",
    "final_aggregation": "Final = (Opinion×0.40) + (Description×0.25) + (Name×0.15) + (Specification×0.12) + (Category×0.08)",
    "thresholds": "Positive: score > 0.1, Negative: score < -0.1, Neutral: -0.1 ≤ score ≤ 0.1"
  },

  "lexicon_info": {
    "positive_words_count": 200,
    "negative_words_count": 200,
    "examples_positive": ["excellent", "great", "amazing", "powerful", "fast", ...],
    "examples_negative": ["terrible", "awful", "horrible", "bad", "slow", ...]
  },

  "source": "Liu, B. (2012). Sentiment Analysis and Opinion Mining, Chapter 2"
}
```

### Testowanie w Przeglądarce

```bash
# Test dla konkretnego produktu (Multi-Source Analysis)
curl http://localhost:8000/api/sentiment-analysis-debug/?product_id=295

# Lub otwórz w przeglądarce:
http://localhost:8000/api/sentiment-analysis-debug/?product_id=295

# Zobaczysz szczegółową analizę z wszystkich 5 źródeł
```

---

## 🔧 Lokalizacja w Kodzie

### Backend Files:

- **`custom_recommendation_engine.py`** → `CustomSentimentAnalysis.analyze_sentiment()` - **uniwersalna funkcja do analizy KAŻDEGO tekstu**
- **`models.py`** → `SentimentAnalysis`, `ProductSentimentSummary` modele
- **`sentiment_views.py`** →
  - `SentimentSearchAPIView.get()` - **NOWA wieloźródłowa analiza (5 źródeł)**
  - `SentimentAnalysisDebugAPI.get()` - **NOWY debug endpoint z multi-source breakdown**
- **`signals.py`** → Automatyczne przetwarzanie po dodaniu opinii (legacy, dla pojedynczych opinii)
- **`urls.py`** → Routes:
  - `/api/sentiment-search/` - główne wyszukiwanie
  - `/api/sentiment-analysis-debug/` - debug endpoint

### Frontend Files:

- **`SearchModal.jsx`** →
  - Interfejs wyszukiwania sentymentu
  - Tooltip z opisem multi-source analysis
  - Ikona info (AiOutlineInfoCircle)
  - Toggle między Sentiment/Fuzzy Search
- **`SearchModal.scss`** →
  - Style dla badge'y sentymentu (😊/😞/😐)
  - Tooltip styling (jasne tło, ciemny tekst)
  - Jednolity design przycisków (36px wysokości)
- **`AdminStatistics.jsx`** → Panel administracyjny (status algorytmów)

### Nowe Funkcjonalności:

#### 1. **Multi-Source Sentiment Analysis**

```python
# W SentimentSearchAPIView.get()
for product in products:
    # Analizuj 5 źródeł:
    opinion_score = analyze_opinions(product)        # 40% wagi
    desc_score = analyze_text(product.description)   # 25% wagi
    name_score = analyze_text(product.name)          # 15% wagi
    spec_score = analyze_specifications(product)     # 12% wagi
    cat_score = analyze_categories(product)          # 8% wagi

    # Oblicz ważony wynik końcowy
    final_score = weighted_sum(all_scores)
```

#### 2. **Detailed Breakdown Response**

```json
{
  "sentiment_score": 0.414,
  "sentiment_breakdown": {
    "opinion_score": 0.6,
    "description_score": 0.4,
    "name_score": 0.2,
    "specification_score": 0.3,
    "category_score": 0.1
  }
}
```

#### 3. **Enhanced Debug Endpoint**

- Pokazuje analizę z WSZYSTKICH 5 źródeł
- Szczegółowe obliczenia dla każdego źródła
- Breakdown wkładu każdego źródła do final score
- Przykłady znalezionych pozytywnych/negatywnych słów

### Słowniki Używane:

- **200+ pozytywnych słów**: excellent, great, amazing, wonderful, fantastic...
- **200+ negatywnych słów**: terrible, awful, horrible, bad, worst...
- **Intensyfikatory**: very, extremely, really, quite, totally...
- **Negacje**: not, no, never, nothing, neither...
- **Bigramy**: "highly recommend", "love it", "terrible quality"...
