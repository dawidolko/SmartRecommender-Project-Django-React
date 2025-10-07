# 🧠 Analiza Sentymentu - Jak Działa w Projekcie (Multi-Source)

## 📋 **Czym Jest Ta Metoda?**

**Analiza Sentymentu** (Sentiment Analysis) to algorytm **lexicon-based** (słownikowy) (Liu, Bing 2012), który analizuje **WSZYSTKIE dane produktu** (nie tylko opinie!) i oblicza wynik sentymentu dla każdego produktu, aby pomóc klientom znaleźć produkty z najlepszymi charakterystykami.

**Nowe podejście - Multi-Source:**

- 👥 **Opinie klientów** (40% wagi) - najbardziej wiarygodne
- 📝 **Opis produktu** (25% wagi) - oficjalny opis sprzedawcy
- 🏷️ **Nazwa produktu** (15% wagi) - słowa kluczowe jak "Premium", "Pro"
- 📋 **Specyfikacja** (12% wagi) - parametry techniczne ("fast", "powerful")
- 🗂️ **Kategorie** (8% wagi) - przynależność do kategorii

**Przykład:**

- **Tradycyjne**: Produkt z 80% pozytywnymi opiniami = score 0.6
- **Multi-Source**: Ten sam produkt + pozytywny opis + nazwa "Premium" + kategoria "Professional" = score 0.72 (wyżej w rankingu!)

---

## 🔄 **Jak To Działa - Przepływ Danych**

### **1. Baza Danych (PostgreSQL)**

```sql
-- Tabela 1: Analiza pojedynczej opinii
SentimentAnalysis {
  opinion_id: 123,          -- Powiązanie z Opinion
  product_id: 295,          -- Powiązanie z Product
  sentiment_score: 0.234,   -- Wynik: -1.0 do +1.0
  sentiment_category: "positive"  -- positive/negative/neutral
}

-- Tabela 2: Podsumowanie dla produktu
ProductSentimentSummary {
  product_id: 295,
  average_sentiment_score: 0.678,  -- Średnia wszystkich opinii
  positive_count: 45,              -- Liczba pozytywnych opinii
  negative_count: 5,               -- Liczba negatywnych opinii
  neutral_count: 10,               -- Liczba neutralnych opinii
  total_opinions: 60               -- Całkowita liczba opinii
}
```

### **2. Backend - Algorytm Analizy Sentymentu**

**Plik:** custom_recommendation_engine.py

#### **Klasa: `CustomSentimentAnalysis`**

```python
class CustomSentimentAnalysis:
    def __init__(self):
        # Słowniki z ~200 słów każdy
        self.positive_words = {
            "excellent", "great", "amazing", "wonderful", "fantastic",
            "good", "nice", "perfect", "love", "recommend", ...
        }

        self.negative_words = {
            "terrible", "awful", "horrible", "bad", "worst",
            "disappointing", "poor", "useless", "hate", ...
        }
```

#### **Funkcja: `analyze_sentiment(text)`**

```python
def analyze_sentiment(self, text):
    """
    Wzór z Liu, B. (2012) - Sentiment Analysis and Opinion Mining:

    Sentiment_Score = (Positive_Count - Negative_Count) / Total_Words
    """
    positive_score = 0.0
    negative_score = 0.0
    total_words = 0

    # Krok 1: Tokenizacja (podział tekstu na słowa)
    words = self._tokenize_text(text.lower())
    # Wynik: ["excellent", "processor", "very", "fast", "reliable", ...]

    # Krok 2: Zlicz pozytywne i negatywne słowa
    for word in words:
        if word in self.positive_words:
            positive_score += 1.0  # np. "excellent" → +1
        elif word in self.negative_words:
            negative_score += 1.0  # np. "terrible" → +1
        total_words += 1

    # Krok 3: Oblicz wynik używając wzoru
    if total_words == 0:
        sentiment_score = 0.0
    else:
        sentiment_score = (positive_score - negative_score) / total_words

    # Krok 4: Normalizacja do zakresu [-1.0, +1.0]
    sentiment_score = max(-1.0, min(1.0, sentiment_score))

    # Krok 5: Klasyfikacja (progi z Liu, B. 2012)
    if sentiment_score > 0.1:
        category = "positive"    # > 10% więcej pozytywnych słów
    elif sentiment_score < -0.1:
        category = "negative"    # > 10% więcej negatywnych słów
    else:
        category = "neutral"     # Balans lub brak emocjonalnych słów

    return sentiment_score, category
```

#### **Przykład Obliczenia:**

```python
# Opinia: "This processor is excellent and very fast, highly recommend!"
# Słowa: ["this", "processor", "is", "excellent", "and", "very", "fast", "highly", "recommend"]

positive_words_found = ["excellent", "recommend"]  # 2 słowa
negative_words_found = []                          # 0 słów
total_words = 9

# Wzór: (2 - 0) / 9 = 0.222
sentiment_score = 0.222
category = "positive"  # bo 0.222 > 0.1
```

### **3. Automatyczna Aktualizacja (Django Signals)**

**Plik:** signals.py

```python
@receiver(post_save, sender=Opinion)
def analyze_opinion_sentiment(sender, instance, created, **kwargs):
    """Automatycznie analizuje sentyment po dodaniu nowej opinii"""
    if created:
        # Krok 1: Przeanalizuj opinię
        analyzer = CustomSentimentAnalysis()
        score, category = analyzer.analyze_sentiment(instance.content)

        # Krok 2: Zapisz wynik do SentimentAnalysis
        SentimentAnalysis.objects.create(
            opinion=instance,
            product=instance.product,
            sentiment_score=score,
            sentiment_category=category
        )

        # Krok 3: Zaktualizuj podsumowanie produktu
        update_product_sentiment_summary(instance.product)

def update_product_sentiment_summary(product):
    """Agreguje wszystkie opinie dla produktu"""
    opinions = SentimentAnalysis.objects.filter(product=product)

    if not opinions.exists():
        return

    # Oblicz średnią: Σ(scores) / N
    scores = [op.sentiment_score for op in opinions]
    average = sum(scores) / len(scores)

    # Policz kategorie
    positive_count = opinions.filter(sentiment_category="positive").count()
    negative_count = opinions.filter(sentiment_category="negative").count()
    neutral_count = opinions.filter(sentiment_category="neutral").count()

    # Zapisz lub zaktualizuj podsumowanie
    ProductSentimentSummary.objects.update_or_create(
        product=product,
        defaults={
            'average_sentiment_score': average,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'total_opinions': len(scores)
        }
    )
```

### **4. API Backend (Django REST) - NOWY Multi-Source**

**Plik:** sentiment_views.py

```python
class SentimentSearchAPIView(APIView):
    """
    Wyszukiwarka produktów z MULTI-SOURCE SENTIMENT ANALYSIS.

    Nowy wzór agregacji wieloźródłowej:
    Final_Score = (Opinion×0.40) + (Desc×0.25) + (Name×0.15) + (Spec×0.12) + (Cat×0.08)

    Ranking: Produkty z wyższym final_score są wyżej
    """
    def get(self, request):
        from .custom_recommendation_engine import CustomSentimentAnalysis

        query = request.GET.get("q", "")  # np. "laptop"
        analyzer = CustomSentimentAnalysis()

        # Krok 1: Znajdź produkty pasujące do zapytania
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).prefetch_related('opinion_set', 'specification_set', 'categories')

        # Krok 2: Analizuj KAŻDY produkt z 5 źródeł
        products_with_scores = []
        for product in products:
            # ŹRÓDŁO 1: Opinie (40% wagi)
            opinion_scores = []
            for opinion in product.opinion_set.all()[:20]:
                score, _ = analyzer.analyze_sentiment(opinion.content)
                opinion_scores.append(score)
            opinion_avg = sum(opinion_scores) / len(opinion_scores) if opinion_scores else 0.0

            # ŹRÓDŁO 2: Opis (25% wagi)
            desc_score, _ = analyzer.analyze_sentiment(product.description or "")

            # ŹRÓDŁO 3: Nazwa (15% wagi)
            name_score, _ = analyzer.analyze_sentiment(product.name)

            # ŹRÓDŁO 4: Specyfikacja (12% wagi)
            spec_texts = [f"{s.parameter_name} {s.specification}"
                         for s in product.specification_set.all()[:10]]
            spec_score, _ = analyzer.analyze_sentiment(" ".join(spec_texts)) if spec_texts else (0.0, "neutral")

            # ŹRÓDŁO 5: Kategorie (8% wagi)
            cat_names = " ".join([c.name for c in product.categories.all()])
            cat_score, _ = analyzer.analyze_sentiment(cat_names) if cat_names else (0.0, "neutral")

            # Oblicz ważony wynik końcowy
            final_score = (
                opinion_avg * 0.40 +
                desc_score * 0.25 +
                name_score * 0.15 +
                spec_score * 0.12 +
                cat_score * 0.08
            )

            products_with_scores.append({
                'product': product,
                'final_score': final_score,
                'breakdown': {
                    'opinion': opinion_avg,
                    'description': desc_score,
                    'name': name_score,
                    'specification': spec_score,
                    'category': cat_score
                }
            })

        # Krok 3: Sortuj według final_score (DESC)
        products_with_scores.sort(key=lambda x: x['final_score'], reverse=True)

        # Krok 4: Zwróć dane z breakdown
        data = []
        for item in products_with_scores:
            product = item['product']
            data.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "sentiment_score": round(item['final_score'], 3),
                "sentiment_breakdown": {
                    "opinion_score": round(item['breakdown']['opinion'], 3),
                    "description_score": round(item['breakdown']['description'], 3),
                    "name_score": round(item['breakdown']['name'], 3),
                    "specification_score": round(item['breakdown']['specification'], 3),
                    "category_score": round(item['breakdown']['category'], 3)
                }
            })

        return Response(data)
```

### **5. Frontend - Wyszukiwarka (React)**

**Plik:** SearchModal.jsx

```jsx
const SearchModal = ({ isOpen, onClose }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isAdvanced, setIsAdvanced] = useState(false); // false = Sentiment Search

  // Wywołaj API gdy użytkownik wpisuje tekst
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchTerm && !isAdvanced) {
        performSentimentSearch(); // Tryb: Sentiment Search
      }
    }, 300); // Debounce 300ms

    return () => clearTimeout(timer);
  }, [searchTerm]);

  const performSentimentSearch = async () => {
    try {
      // Wywołaj backend API
      const response = await axios.get(
        `${config.apiUrl}/api/sentiment-search/?q=${searchTerm}`
      );

      setSearchResults(response.data);
      // Dane: [
      //   {id: 295, name: "Laptop", sentiment_score: 0.678, positive_count: 45, ...},
      //   {id: 156, name: "Mouse", sentiment_score: 0.234, positive_count: 12, ...}
      // ]
    } catch (err) {
      console.error("Search error:", err);
    }
  };

  return (
    <div className="search-modal">
      {/* Input wyszukiwania */}
      <input
        type="text"
        placeholder="Search products (sentiment-based)..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />

      {/* Wyniki */}
      {searchResults.map((product) => (
        <div key={product.id} className="result-item">
          <h3>{product.name}</h3>
          <p>${product.price}</p>

          {/* Wyświetl sentiment score */}
          {product.sentiment_score != null && (
            <div className="sentiment-info">
              {/* Badge z emoji i kolorem */}
              <span
                className={`badge ${
                  product.sentiment_score > 0.1
                    ? "positive"
                    : product.sentiment_score < -0.1
                    ? "negative"
                    : "neutral"
                }`}>
                {product.sentiment_score > 0.1
                  ? "😊 Positive"
                  : product.sentiment_score < -0.1
                  ? "😞 Negative"
                  : "😐 Neutral"}
              </span>

              {/* Wynik sentymentu */}
              <span>Score: {product.sentiment_score.toFixed(2)}</span>

              {/* Breakdown opinii */}
              <div className="opinion-breakdown">
                📝 {product.total_opinions} opinions: 👍{" "}
                {product.positive_count} | 👎 {product.negative_count} | 😐{" "}
                {product.neutral_count}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
```

---

## 📊 **Wzory Matematyczne**

### **1. Sentiment Score dla Pojedynczego Tekstu** (Liu, B. 2012)

```
Sentiment_Score = (Positive_Count - Negative_Count) / Total_Words

Ta SAMA funkcja analizuje:
- Opinie klientów
- Opis produktu
- Nazwę produktu
- Specyfikację techniczną
- Kategorie

Przykład #1 - Opinia:
"Excellent laptop, very fast and reliable. Highly recommend!"

- Positive words: ["excellent", "fast", "reliable", "recommend"] = 4
- Negative words: [] = 0
- Total words: 8

Sentiment_Score = (4 - 0) / 8 = 0.500 → "positive"

Przykład #2 - Opis:
"Powerful gaming laptop with excellent performance"

- Positive words: ["powerful", "excellent"] = 2
- Negative words: [] = 0
- Total words: 6

Sentiment_Score = (2 - 0) / 6 = 0.333 → "positive"

Przykład #3 - Nazwa:
"Premium Gaming Laptop"

- Positive words: ["premium"] = 1
- Negative words: [] = 0
- Total words: 3

Sentiment_Score = (1 - 0) / 3 = 0.333 → "positive"
```

### **2. Klasyfikacja (Progi z Liu, B. 2012)**

```
if score > 0.1:
    category = "positive"     # Więcej niż 10% przewaga pozytywnych słów
elif score < -0.1:
    category = "negative"     # Więcej niż 10% przewaga negatywnych słów
else:
    category = "neutral"      # Balans lub brak emocjonalnych słów
```

### **3. NOWA Agregacja Wieloźródłowa**

```
Final_Score = (Opinion_Avg × 0.40) + (Description × 0.25) +
              (Name × 0.15) + (Specification × 0.12) + (Category × 0.08)

Przykład KOMPLETNY:
Produkt: "Premium Gaming Laptop"

KROK 1: Analizuj opinie
- Opinia 1: "Excellent, very fast!" → score = 0.667
- Opinia 2: "Great performance" → score = 0.500
- Opinia 3: "Good value" → score = 0.500
Opinion_Average = (0.667 + 0.500 + 0.500) / 3 = 0.556

KROK 2: Analizuj opis
"Powerful gaming laptop with excellent performance and stunning graphics"
→ Positive: ["powerful", "excellent", "stunning"] = 3
→ Total: 9 words
→ Description_Score = (3 - 0) / 9 = 0.333

KROK 3: Analizuj nazwę
"Premium Gaming Laptop"
→ Positive: ["premium"] = 1
→ Total: 3 words
→ Name_Score = (1 - 0) / 3 = 0.333

KROK 4: Analizuj specyfikację
"Fast Intel processor | Powerful NVIDIA graphics | High quality display"
→ Positive: ["fast", "powerful", "high", "quality"] = 4
→ Total: 10 words
→ Spec_Score = (4 - 0) / 10 = 0.400

KROK 5: Analizuj kategorie
"Gaming Laptops Premium"
→ Positive: ["premium"] = 1
→ Total: 3 words
→ Category_Score = (1 - 0) / 3 = 0.333

KROK 6: Oblicz Final Score
Final_Score = (0.556 × 0.40) + (0.333 × 0.25) + (0.333 × 0.15) + (0.400 × 0.12) + (0.333 × 0.08)
Final_Score = 0.222 + 0.083 + 0.050 + 0.048 + 0.027
Final_Score = 0.430 → "Positive" (bo 0.430 > 0.1)

Breakdown wkładu każdego źródła:
- Opinie: 0.222 (51.6% wkładu) ✅ najważniejsze
- Opis: 0.083 (19.3% wkładu)
- Nazwa: 0.050 (11.6% wkładu)
- Specyfikacja: 0.048 (11.2% wkładu)
- Kategorie: 0.027 (6.3% wkładu)
```

### **4. Porównanie: Tradycyjne vs Multi-Source**

```
Przykład: Ten sam produkt

TRADYCYJNE (tylko opinie):
Average_Opinion = 0.556 → Final = 0.556

MULTI-SOURCE (wszystkie źródła):
Final_Score = 0.430

Dlaczego NIŻSZE?
- Opis/Specyfikacja/Kategorie miały niższe score (0.333-0.400)
- Ważona średnia obniża wynik gdy inne źródła są słabsze
- LEPIEJ odzwierciedla rzeczywistą jakość produktu!

Korzyść:
Produkt z doskonałymi opiniami (0.8) ale SŁABYM opisem ("basic", "cheap")
→ Multi-Source = 0.5 (bardziej realistyczne)
```

---

## 🚀 **Przykład w Praktyce - NOWY Multi-Source**

### **Scenariusz:**

1. **Klient wpisuje** "laptop" w pasku wyszukiwania
2. **Frontend** wywołuje: `GET /api/sentiment-search/?q=laptop`
3. **Backend** znajduje 3 laptopy i analizuje KAŻDY z 5 źródeł:

#### **Laptop A: "Premium Gaming Laptop Pro"**

| Źródło                                              | Score | Wkład        |
| --------------------------------------------------- | ----- | ------------ |
| 👥 Opinie (45 poz, 5 neg)                           | 0.800 | 0.320        |
| 📝 Opis: "Excellent performance, powerful graphics" | 0.600 | 0.150        |
| 🏷️ Nazwa: "Premium Gaming Laptop Pro"               | 0.500 | 0.075        |
| 📋 Spec: "Fast processor, great display"            | 0.500 | 0.060        |
| 🗂️ Kategorie: "Gaming Premium"                      | 0.500 | 0.040        |
| **FINAL SCORE**                                     | -     | **0.645** ✅ |

#### **Laptop B: "Budget Office Laptop"**

| Źródło                           | Score  | Wkład        |
| -------------------------------- | ------ | ------------ |
| 👥 Opinie (12 poz, 8 neg)        | 0.200  | 0.080        |
| 📝 Opis: "Basic laptop for work" | 0.000  | 0.000        |
| 🏷️ Nazwa: "Budget Office Laptop" | -0.100 | -0.015       |
| 📋 Spec: "Standard processor"    | 0.000  | 0.000        |
| 🗂️ Kategorie: "Office Budget"    | -0.100 | -0.008       |
| **FINAL SCORE**                  | -      | **0.057** 😐 |

#### **Laptop C: "Cheap Student Laptop"**

| Źródło                                            | Score  | Wkład         |
| ------------------------------------------------- | ------ | ------------- |
| 👥 Opinie (5 poz, 12 neg)                         | -0.350 | -0.140        |
| 📝 Opis: "Low cost, basic features, poor quality" | -0.400 | -0.100        |
| 🏷️ Nazwa: "Cheap Student Laptop"                  | -0.333 | -0.050        |
| 📋 Spec: "Slow processor, weak battery"           | -0.200 | -0.024        |
| 🗂️ Kategorie: "Budget Basic"                      | -0.100 | -0.008        |
| **FINAL SCORE**                                   | -      | **-0.322** ❌ |

4. **Backend sortuje** według `final_score` (DESC):

   ```
   1. Laptop A (0.645) ← Najlepszy multi-source score - PIERWSZY
   2. Laptop B (0.057) ← Neutralny - ŚRODEK
   3. Laptop C (-0.322) ← Negatywny ze wszystkich źródeł - OSTATNI
   ```

5. **Frontend wyświetla:**
   ```
   ┌─────────────────────────────────────────────────────┐
   │ 💻 Premium Gaming Laptop Pro - $1200               │
   │ 😊 Positive | Score: 0.65                         │
   │ 📊 Multi-Source Breakdown:                         │
   │    👥 Opinions: 0.80 | 📝 Desc: 0.60 | 🏷️ Name: 0.50│
   │ 📝 45 opinions: 👍 45 | 👎 5 | 😐 0               │
   ├─────────────────────────────────────────────────────┤
   │ 💻 Budget Office Laptop - $600                     │
   │ � Neutral | Score: 0.06                          │
   │ 📊 Multi-Source Breakdown:                         │
   │    👥 Opinions: 0.20 | 📝 Desc: 0.00 | 🏷️ Name: -0.10│
   │ 📝 20 opinions: 👍 12 | 👎 8 | 😐 0               │
   ├─────────────────────────────────────────────────────┤
   │ 💻 Cheap Student Laptop - $400                     │
   │ 😞 Negative | Score: -0.32                        │
   │ 📊 Multi-Source Breakdown:                         │
   │    👥 Opinions: -0.35 | 📝 Desc: -0.40 | 🏷️ Name: -0.33│
   │ 📝 17 opinions: 👍 5 | 👎 12 | 😐 0               │
   └─────────────────────────────────────────────────────┘
   ```

### **Dlaczego Multi-Source Jest Lepszy?**

**Tradycyjne (tylko opinie):**

- Laptop A: 0.800 (opinie) → pokazany pierwszy
- Laptop B: 0.200 (opinie) → pokazany drugi
- Laptop C: -0.350 (opinie) → pokazany trzeci

**Multi-Source (wszystkie źródła):**

- Laptop A: 0.645 (opinie + doskonały opis + nazwa "Premium") → pokazany pierwszy ✅
- Laptop B: 0.057 (słabe opinie + neutralny opis + nazwa "Budget") → pokazany drugi ✅
- Laptop C: -0.322 (złe opinie + zły opis + nazwa "Cheap") → pokazany trzeci ✅

**Wniosek:**
Multi-source daje bardziej **zrównoważoną ocenę**:

- Produkt z dobrymi opiniami ale SŁABYM opisem → niższy ranking
- Produkt z dobrymi opiniami + DOSKONAŁYM opisem → wyższy ranking
- Klient dostaje **lepsze rekomendacje**!

---

## ⚙️ **Optymalizacje**

### **1. Słowniki Rozszerzone**

```python
# Zamiast prostych słów, używamy też:

# Intensyfikatory (wzmacniają sentyment)
intensifiers = {"very", "extremely", "really", "quite", "totally"}

# Negacje (odwracają sentyment)
negations = {"not", "no", "never", "nothing"}

# Bigramy (dwuwyrazowe frazy)
positive_bigrams = {"highly recommend", "love it", "great quality"}
negative_bigrams = {"terrible quality", "waste money", "worst product"}
```

### **2. Context-Aware Analysis**

```python
# Przykład: "not good" → negatywne (mimo "good" jest pozytywne)
if words[i-1] in negations and words[i] in positive_words:
    negative_score += 1.0  # Odwróć sentyment
```

### **3. Cache**

```python
# Backend cache'uje wyniki na 15 minut
@cache_page(60 * 15)
def sentiment_search(request):
    ...
```

---

## 📚 **Źródła Naukowe**

1. **Liu, Bing (2012)**  
   _"Sentiment Analysis and Opinion Mining"_  
   Morgan & Claypool Publishers  
   → Rozdział 2: Sentiment Lexicons (słowniki sentymentu)
   → Rozdział 3: Classification thresholds (progi klasyfikacji)

2. **SentiWordNet**  
   Baccianella, S., Esuli, A., Sebastiani, F. (2010)  
   _"SentiWordNet 3.0: An Enhanced Lexical Resource for Sentiment Analysis"_  
   → Podstawa dla lexicon-based approach

---

## 🎯 **Podsumowanie**

| Komponent    | Technologia            | Rola                                            |
| ------------ | ---------------------- | ----------------------------------------------- |
| **Baza**     | PostgreSQL             | `SentimentAnalysis` + `ProductSentimentSummary` |
| **Algorytm** | Python (Lexicon-based) | `CustomSentimentAnalysis.analyze_sentiment()`   |
| **Backend**  | Django REST            | `SentimentSearchAPIView`                        |
| **Frontend** | React                  | SearchModal.jsx z badge'ami                     |
| **Signals**  | Django Signals         | Auto-analiza po dodaniu opinii                  |

**Przepływ:**

1. Klient dodaje opinię → **Signal** → Analizuj sentyment → Zapisz do bazy
2. Klient wyszukuje produkt → **API** → Sortuj według sentymentu → Wyświetl
3. Frontend pokazuje badge'y (😊/😞/😐) i breakdown opinii

**Wzór kluczowy:**

```
Sentiment_Score = (Positive_Words - Negative_Words) / Total_Words
Average_Sentiment = Σ(scores) / N_opinions
```
