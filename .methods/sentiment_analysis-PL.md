To be corrected: 14/09/2025

# 🧠 Analiza Sentymentu w Wyszukiwaniu Produktów

## Czym Jest "Wyszukiwanie Oparte na Sentymencie" w Sklepie?

Wyszukiwanie oparte na sentymencie to inteligentny algorytm odkrywania produktów, który:

- **Analizuje opinie klientów** używając przetwarzania języka naturalnego (NLP)
- **Oblicza wyniki sentymentu** dla każdego produktu (-1 do +1) używając wzoru SentiWordNet
- **Ranguje wyniki wyszukiwania** według satysfakcji klientów
- **Priorytetyzuje pozytywnie oceniane produkty** w wynikach wyszukiwania
- **Pomaga klientom znajdować produkty, które inni kochają**

System czyni sklep inteligentniejszym, wydobywając na powierzchnię produkty z najlepszymi doświadczeniami klientów, co prowadzi do wyższej satysfakcji klientów i zwiększonej sprzedaży.

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

### 4. `SentimentSearchAPIView` – 🔍 **Integracja z Wyszukiwaniem**

Napędza funkcjonalność wyszukiwania opartego na sentymencie:

- Przyjmuje zapytania wyszukiwania od użytkowników
- Dopasowuje produkty do terminów wyszukiwania
- Porządkuje wyniki według `average_sentiment_score` (najwyższe pierwsze)
- Uwzględnia dane sentymentu w wynikach wyszukiwania

### 5. Komponent `SearchModal.jsx` – 👁️ **Interfejs Użytkownika**

Wyświetla interfejs wyszukiwania sentymentu użytkownikom:

- Zapewnia wyniki wyszukiwania w czasie rzeczywistym
- Pokazuje wyniki sentymentu obok produktów
- Pozwala na przełączanie między trybami wyszukiwania (sentiment/fuzzy)

---

## 🤖 Jak Działa Analiza Sentymentu (Krok po Kroku)

### 1. **Przetwarzanie Opinii (CustomSentimentAnalysis)**:

```python
# Prawdziwy wzór SentiWordNet zaimplementowany w CustomSentimentAnalysis.analyze_sentiment()
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

    # Wzór SentiWordNet: (Pos_Score - Neg_Score) / Total_Words
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

### 2. **Obliczanie Podsumowania Produktu**:

```python
# W CustomSentimentAnalysis.analyze_product_sentiment()
For each product:
    - Oblicz średni wynik sentymentu ze wszystkich opinii
    - Policz pozytywne, neutralne i negatywne opinie
    - Przechowuj zagregowane metryki w ProductSentimentSummary
```

### 3. **Proces Wyszukiwania**:

```python
# W SentimentSearchAPIView
When user searches:
    - Znajdź produkty pasujące do zapytania tekstowego
    - Połącz z danymi sentiment_summary
    - Sortuj według average_sentiment_score (malejąco)
    - Zwróć wzbogacone dane produktu z metrykami sentymentu
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
# Polarity Score (Liu, Bing 2012)
polarity = (positive_count - negative_count) / total_words

# Subjectivity Score (TextBlob)
subjectivity = subjective_words / total_words
```

### Optymalizacja Bazy Danych:

- Relacje OneToOne dla efektywnych joinów
- Niestandardowe indeksy na często zapytywanych polach
- Prefetching powiązanych danych w celu minimalizacji zapytań do bazy danych

### Rozważania Wydajności:

- Obliczanie sentymentu wykonywane raz podczas tworzenia/aktualizacji opinii
- Wstępnie zagregowane podsumowania dla szybkiego rankingu wyszukiwania
- `select_related` i `prefetch_related` dla efektywnych zapytań

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

## 📈 Przykładowe Metryki Analizy Sentymentu

| Produkt               | Śr. Sentyment | Pozytywne | Neutralne | Negatywne | Całkowite Opinie |
| --------------------- | ------------- | --------- | --------- | --------- | ---------------- |
| Słuchawki Premium     | 0.876         | 45        | 5         | 2         | 52               |
| Podstawowa Klawiatura | 0.342         | 12        | 8         | 3         | 23               |
| Mysz Gamingowa        | 0.654         | 28        | 7         | 4         | 39               |
| Stojak na Laptop      | -0.123        | 5         | 4         | 12        | 21               |

---

## 🔧 Lokalizacja w Kodzie

### Backend Files:

- `custom_recommendation_engine.py` → `CustomSentimentAnalysis` klasa
- `models.py` → `SentimentAnalysis`, `ProductSentimentSummary` modele
- `sentiment_views.py` → `SentimentSearchAPIView`
- `signals.py` → Automatyczne przetwarzanie po dodaniu opinii

### Frontend Files:

- `SearchModal.jsx` → Interfejs wyszukiwania sentymentu
- `AdminStatistics.jsx` → Panel administracyjny (status algorytmów)

### Słowniki Używane:

- **200+ pozytywnych słów**: excellent, great, amazing, wonderful, fantastic...
- **200+ negatywnych słów**: terrible, awful, horrible, bad, worst...
- **Intensyfikatory**: very, extremely, really, quite, totally...
- **Negacje**: not, no, never, nothing, neither...
- **Bigramy**: "highly recommend", "love it", "terrible quality"...
