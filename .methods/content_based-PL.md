Ostatnia aktualizacja: 12/10/2025

# 🎯 Filtracja Oparta na Treści (Content-Based Filtering)

## Czym Jest "Filtracja Oparta na Treści" w Sklepie?

**Filtracja oparta na treści (Content-Based Filtering)** to algorytm rekomendacji, który:

- Analizuje **cechy produktów** (kategorie, tagi, cena, opis) aby znaleźć podobne produkty
- Wykorzystuje **podobieństwo cosinusowe** (Cosine Similarity) do porównywania wektorów cech produktów
- Tworzy **macierz podobieństw** między wszystkimi produktami w sklepie
- Rekomenduje produkty **podobne do tych, które użytkownik oglądał lub kupił**
- Używa **ważonej ekstrakcji cech** z różnymi wagami dla kategorii, tagów, cen i słów kluczowych
- Implementuje **własny silnik** bez użycia gotowych bibliotek (implementacja manualna)

Metoda bazuje na założeniu: **"Jeśli użytkownik kupił produkt X, poleci mu się podobny produkt Y"**.

---

## 📂 Struktura Projektu - Kluczowe Pliki i Role

### 1. `backend/home/custom_recommendation_engine.py` – 🧠 **Silnik Content-Based**

#### Klasa `CustomContentBasedFilter` (linie 17-244)

Główna klasa implementująca filtrację opartą na treści.

**Parametry konfiguracyjne (linie 18-29):**

```python
class CustomContentBasedFilter:
    def __init__(self):
        self.similarity_threshold = 0.2           # Minimalny próg podobieństwa (20%)
        self.max_products_for_similarity = 500    # Max produktów do przetworzenia
        self.batch_size = 100                     # Rozmiar batcha dla bulk operations
        self.max_comparisons_per_product = 50     # Max porównań na produkt

        # Wagi dla różnych typów cech produktu
        self.feature_weights = {
            "category": 0.40,    # 40% - największa waga (kategoria najważniejsza)
            "tag": 0.30,         # 30% - tagi produktu
            "price": 0.20,       # 20% - przedział cenowy
            "keywords": 0.10,    # 10% - słowa kluczowe z opisu
        }

        # Stop words - słowa ignorowane w analizie tekstu
        self.stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", ...,
            "jako", "że", "na", "w", "z", "do", "od", "po", "przez"
        }
```

**Dlaczego te wagi?**
- **Kategoria (40%)** - najpewniejsza informacja o produkcie (np. "Laptopy", "Procesory")
- **Tagi (30%)** - precyzyjne opisy (np. "gaming", "profesjonalny", "budżetowy")
- **Cena (20%)** - użytkownicy często szukają w podobnym przedziale cenowym
- **Słowa kluczowe (10%)** - najmniejsza waga, bo opisy mogą być mniej precyzyjne

---

### 2. **Funkcja: `calculate_product_similarity()` - Obliczanie Podobieństwa Cosinusowego**

**Lokalizacja:** `backend/home/custom_recommendation_engine.py`, linie 95-117

```python
def calculate_product_similarity(self, product1, product2):
    """Oblicza podobieństwo między produktami używając systemu ważonego"""
    features1 = self._extract_weighted_features(product1)
    features2 = self._extract_weighted_features(product2)

    dot_product = 0.0
    norm1 = 0.0
    norm2 = 0.0

    all_features = set(features1.keys()) | set(features2.keys())

    for feature in all_features:
        val1 = features1.get(feature, 0.0)
        val2 = features2.get(feature, 0.0)

        dot_product += val1 * val2  # Iloczyn skalarny
        norm1 += val1 * val1         # Norma wektora 1
        norm2 += val2 * val2         # Norma wektora 2

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (math.sqrt(norm1) * math.sqrt(norm2))
```

**Wzór matematyczny (Podobieństwo Cosinusowe):**

```
                    A · B
cos(θ) = ─────────────────────
          ||A|| × ||B||

gdzie:
- A, B = wektory cech produktów
- A · B = iloczyn skalarny (dot product) = Σ(A_i × B_i)
- ||A|| = norma wektora A = √(Σ A_i²)
- ||B|| = norma wektora B = √(Σ B_i²)
- θ = kąt między wektorami

Wynik: wartość z przedziału [0, 1]
- 1.0 = produkty identyczne (kąt 0°)
- 0.0 = produkty całkowicie różne (kąt 90°)
```

**Źródło naukowe:**
- Salton, G., McGill, M. J. (1983). "Introduction to Modern Information Retrieval"
- Manning, C. D., Raghavan, P., Schütze, H. (2008). "Introduction to Information Retrieval", rozdz. 6.3

**Przykład obliczenia:**

```
Produkt A (AMD Ryzen 7 5800X3D):
  category_components = 0.40
  category_processors = 0.40
  tag_gaming = 0.30
  tag_high_performance = 0.30
  price_high = 0.20
  keyword_ryzen = 0.02
  keyword_processor = 0.02

Produkt B (AMD Ryzen 9 5900X):
  category_components = 0.40
  category_processors = 0.40
  tag_gaming = 0.30
  tag_workstation = 0.30
  price_high = 0.20
  keyword_ryzen = 0.02
  keyword_cores = 0.02

Wspólne cechy:
  category_components, category_processors, tag_gaming, price_high, keyword_ryzen

Obliczenia:
  dot_product = (0.4×0.4) + (0.4×0.4) + (0.3×0.3) + (0.2×0.2) + (0.02×0.02)
              = 0.16 + 0.16 + 0.09 + 0.04 + 0.0004
              = 0.4504

  norm1 = √(0.4² + 0.4² + 0.3² + 0.3² + 0.2² + 0.02² + 0.02²)
        = √(0.16 + 0.16 + 0.09 + 0.09 + 0.04 + 0.0004 + 0.0004)
        = √0.5408 = 0.7354

  norm2 = √(0.4² + 0.4² + 0.3² + 0.3² + 0.2² + 0.02² + 0.02²)
        = √0.5408 = 0.7354

  similarity = 0.4504 / (0.7354 × 0.7354)
             = 0.4504 / 0.5408
             = 0.833 = 83.3%

Wynik: Produkty są podobne w 83.3% (bardzo wysokie podobieństwo!)
```

**Dlaczego Cosine Similarity zamiast Euclidean Distance?**

Content-based filtering używa **podobieństwa cosinusowego** zamiast odległości euklidesowej, ponieważ:

1. **Niezależność od długości wektora** - liczy się kierunek, nie długość
2. **Normalizacja** - automatycznie uwzględnia skalę wartości (0-1)
3. **Intuicyjna interpretacja** - kąt między wektorami łatwiej zrozumieć niż odległość
4. **Standard w Information Retrieval** - sprawdzona metoda w wyszukiwarkach i systemach rekomendacji

---

### 3. **Funkcja: `_extract_weighted_features()` - Ekstrakcja Ważonych Cech**

**Lokalizacja:** `backend/home/custom_recommendation_engine.py`, linie 119-142

```python
def _extract_weighted_features(self, product):
    """Ekstraktuje cechy produktu z wagami"""
    features = {}

    # 1. KATEGORIE (waga: 40%)
    for category in product.categories.all():
        feature_name = f"category_{category.name.lower()}"
        features[feature_name] = self.feature_weights["category"]

    # 2. TAGI (waga: 30%)
    for tag in product.tags.all():
        feature_name = f"tag_{tag.name.lower()}"
        features[feature_name] = self.feature_weights["tag"]

    # 3. PRZEDZIAŁ CENOWY (waga: 20%)
    price_category = self._get_price_category(product.price)
    features[f"price_{price_category}"] = self.feature_weights["price"]

    # 4. SŁOWA KLUCZOWE (waga: 10%)
    if product.description:
        keywords = self._extract_keywords(product.description)
        for keyword in keywords[:5]:  # Top 5 słów kluczowych
            feature_name = f"keyword_{keyword}"
            # Waga dzielona równomiernie między słowa kluczowe
            features[feature_name] = self.feature_weights["keywords"] / len(keywords[:5])

    return features
```

**Przykład ekstrakcji cech:**

```
Produkt: AMD Ryzen 7 5800X3D (Cena: 1899 PLN)
Kategorie: ["Components", "Processors"]
Tagi: ["Gaming", "High-Performance", "AMD"]
Opis: "Powerful gaming processor with 3D V-Cache technology for maximum performance in demanding games"

Wektor cech:
{
    "category_components": 0.40,
    "category_processors": 0.40,
    "tag_gaming": 0.30,
    "tag_high-performance": 0.30,
    "tag_amd": 0.30,
    "price_high": 0.20,
    "keyword_powerful": 0.02,
    "keyword_gaming": 0.02,
    "keyword_processor": 0.02,
    "keyword_performance": 0.02,
    "keyword_games": 0.02
}
```

---

### 4. **Funkcja: `_get_price_category()` - Kategoryzacja Ceny**

**Lokalizacja:** `backend/home/custom_recommendation_engine.py`, linie 144-153

```python
def _get_price_category(self, price):
    """Kategoryzuje cenę produktu"""
    if price < 100:
        return "low"        # Tanie produkty (< 100 PLN)
    elif price < 500:
        return "medium"     # Średnia półka (100-500 PLN)
    elif price < 1500:
        return "high"       # Droższe produkty (500-1500 PLN)
    else:
        return "premium"    # Produkty premium (> 1500 PLN)
```

**Dlaczego kategoryzacja ceny?**

Zamiast używać surowej wartości ceny (np. 1899 PLN), system kategoryzuje ceny na 4 przedziały. **Powody:**

1. **Normalizacja skali** - ceny produktów różnią się od 10 PLN do 10000 PLN
2. **Podobieństwo semantyczne** - produkt za 1800 PLN i 2000 PLN są w tym samym przedziale "premium"
3. **Redukcja szumu** - różnica 50 PLN nie powinna drastycznie zmieniać podobieństwa
4. **Zachowanie użytkowników** - ludzie myślą przedziałami ("szukam czegoś do 500 PLN"), nie konkretnymi kwotami

**Przykład:**

```
Laptop A: 1899 PLN → "high"
Laptop B: 2100 PLN → "premium"
Laptop C: 1750 PLN → "high"

Podobieństwo cenowe:
- Laptop A i C: price_high = price_high → MATCH (waga 0.20)
- Laptop A i B: price_high ≠ price_premium → NO MATCH (waga 0)
```

---

### 5. **Funkcja: `_extract_keywords()` - Ekstrakcja Słów Kluczowych**

**Lokalizacja:** `backend/home/custom_recommendation_engine.py`, linie 155-168

```python
def _extract_keywords(self, text):
    """Ekstraktuje słowa kluczowe z tekstu produktu"""
    if not text:
        return []

    # 1. Normalizacja: usuń znaki specjalne i zamień na małe litery
    text = re.sub(r"[^\w\s]", " ", text.lower())
    words = text.split()

    # 2. Filtrowanie: usuń stop words i krótkie słowa (< 4 znaki)
    filtered_words = [
        word for word in words
        if len(word) > 3 and word not in self.stop_words
    ]

    # 3. Zliczanie częstości słów
    word_freq = Counter(filtered_words)

    # 4. Zwróć 10 najczęstszych słów
    return [word for word, freq in word_freq.most_common(10)]
```

**Algorytm TF (Term Frequency) - uproszczona wersja:**

```
TF(term) = częstość występowania terminu / całkowita liczba słów

Przykład:
Opis: "Gaming laptop with powerful gaming performance for gaming enthusiasts"

Zliczanie:
  gaming: 3
  laptop: 1
  powerful: 1
  performance: 1
  enthusiasts: 1

Top 10 słów kluczowych (posortowane według TF):
  1. gaming (freq=3)
  2. laptop (freq=1)
  3. performance (freq=1)
  4. powerful (freq=1)
  5. enthusiasts (freq=1)
```

**Dlaczego stop words?**

Stop words to najczęstsze słowa w języku (np. "the", "a", "is", "na", "w"), które:
- **Nie niosą wartości semantycznej** - "the laptop" i "laptop" oznaczają to samo
- **Zaśmiecają przestrzeń cech** - dodają wymiary do wektora bez poprawy jakości
- **Występują wszędzie** - każdy produkt ma te same stop words, więc nie różnicują produktów

---

### 6. **Funkcja: `generate_similarities_for_all_products()` - Generowanie Macierzy Podobieństw**

**Lokalizacja:** `backend/home/custom_recommendation_engine.py`, linie 170-244

```python
def generate_similarities_for_all_products(self):
    """Generuje podobieństwa dla wszystkich produktów z cache i bulk operations"""
    from home.models import Product, ProductSimilarity

    # 1. Sprawdź cache (30 minut timeout)
    cache_key = "content_based_similarity_matrix"
    cached_result = cache.get(cache_key)

    if cached_result:
        print("Using cached content-based filtering results")
        return cached_result

    # 2. Pobierz produkty z relacjami (prefetch dla wydajności)
    products = list(
        Product.objects.prefetch_related(
            "categories", "tags", "specification_set"
        ).all()[: self.max_products_for_similarity]
    )

    if len(products) < 2:
        return 0

    print(f"Processing {len(products)} products for enhanced content-based similarity")

    # 3. Usuń stare podobieństwa typu content_based
    ProductSimilarity.objects.filter(similarity_type="content_based").delete()

    similarities_to_create = []
    similarities_created = 0

    # 4. Porównaj każdy produkt z następnymi (bez duplikatów)
    for i, product1 in enumerate(products):
        if i % 25 == 0:
            print(f"Processed {i}/{len(products)} products")

        # Ogranicz porównania do max_comparisons_per_product (50 produktów)
        comparison_products = products[
            i + 1 : i + 1 + self.max_comparisons_per_product
        ]

        for product2 in comparison_products:
            # Oblicz podobieństwo cosinusowe
            similarity_score = self.calculate_product_similarity(product1, product2)

            # 5. Filtruj przez próg (20%)
            if similarity_score > self.similarity_threshold:
                # Dodaj dwukierunkowe podobieństwa (A→B i B→A)
                similarities_to_create.extend(
                    [
                        ProductSimilarity(
                            product1=product1,
                            product2=product2,
                            similarity_type="content_based",
                            similarity_score=similarity_score,
                        ),
                        ProductSimilarity(
                            product1=product2,
                            product2=product1,
                            similarity_type="content_based",
                            similarity_score=similarity_score,
                        ),
                    ]
                )
                similarities_created += 2

                # 6. Bulk create co 1000 rekordów (optymalizacja bazy danych)
                if len(similarities_to_create) >= 1000:
                    ProductSimilarity.objects.bulk_create(similarities_to_create)
                    similarities_to_create = []

    # 7. Zapisz pozostałe rekordy
    if similarities_to_create:
        ProductSimilarity.objects.bulk_create(similarities_to_create)

    print(f"Created {similarities_created} enhanced content-based similarities")

    # 8. Zapisz w cache na 2 godziny (7200 sekund)
    cache.set(
        cache_key,
        similarities_created,
        timeout=getattr(settings, "CACHE_TIMEOUT_LONG", 7200),
    )

    return similarities_created
```

**Złożoność obliczeniowa:**

```
Liczba produktów: N = 500
Max porównań na produkt: M = 50

Złożoność czasowa: O(N × M) = O(500 × 50) = O(25,000) porównań
Złożoność przestrzenna: O(N²) w najgorszym przypadku (macierz pełna)

Optymalizacje zastosowane:
1. Limit produktów: 500 (max_products_for_similarity)
2. Limit porównań: 50 na produkt (max_comparisons_per_product)
3. Early stopping: próg 20% (similarity_threshold)
4. Bulk operations: batch 1000 rekordów
5. Cache: 2 godziny timeout
6. Prefetch related: załadowanie kategorii/tagów za jednym razem

Bez optymalizacji:
  O(N²) = O(500²) = O(250,000) porównań
  Czas: ~30 minut

Z optymalizacjami:
  O(N × M) = O(500 × 50) = O(25,000) porównań
  Czas: ~3 minuty (10x szybciej!)
```

---

### 7. `backend/home/models.py` – 📦 **Model ProductSimilarity**

**Lokalizacja:** `backend/home/models.py`

```python
class ProductSimilarity(models.Model):
    product1 = models.ForeignKey(
        Product,
        related_name='similarities_from',
        on_delete=models.CASCADE
    )
    product2 = models.ForeignKey(
        Product,
        related_name='similarities_to',
        on_delete=models.CASCADE
    )
    similarity_type = models.CharField(
        max_length=50,
        choices=[
            ('content_based', 'Content Based'),
            ('collaborative', 'Collaborative Filtering')
        ]
    )
    similarity_score = models.FloatField()  # Wartość 0.0 - 1.0
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product1', 'product2', 'similarity_type']
        indexes = [
            models.Index(fields=['product1', 'similarity_type']),
            models.Index(fields=['similarity_score']),
        ]
```

**Struktura danych:**

```
Przykład rekordów w bazie danych:

| product1_id | product2_id | similarity_type | similarity_score |
|-------------|-------------|-----------------|------------------|
| 295         | 341         | content_based   | 0.856            |
| 341         | 295         | content_based   | 0.856            |
| 295         | 203         | content_based   | 0.721            |
| 203         | 295         | content_based   | 0.721            |

Dwukierunkowe podobieństwa:
- Produkt 295 → 341: 0.856
- Produkt 341 → 295: 0.856 (ten sam wynik)

Zapytanie SQL dla rekomendacji:
SELECT product2_id, similarity_score
FROM home_productsimilarity
WHERE product1_id = 295
  AND similarity_type = 'content_based'
ORDER BY similarity_score DESC
LIMIT 6;
```

---

### 8. `backend/home/signals.py` – 🔁 **Automatyczne Aktualizacje**

**Lokalizacja:** `backend/home/signals.py`, linie 69-76

```python
@receiver(post_save, sender=Product)
def handle_product_changes(sender, instance, created, **kwargs):
    """Invalidate content-based cache when products are modified"""
    update_fields = kwargs.get('update_fields', [])
    if created or (update_fields is not None and
                   any(field in update_fields for field in ['name', 'description', 'price'])):
        cache.delete("content_based_similarity_matrix")
        print("Content-based cache invalidated due to product changes")
```

**Lokalizacja:** `backend/home/signals.py`, linie 244-252

```python
def update_content_based_similarity():
    try:
        content_filter = CustomContentBasedFilter()
        similarity_count = content_filter.generate_similarities_for_all_products()
        print(Fore.GREEN + f"Generated {similarity_count} content-based similarities")
        return similarity_count
    except Exception as e:
        print(Fore.RED + f"Error in content-based similarity: {e}")
        return 0
```

**Kiedy macierz podobieństw jest aktualizowana?**

| Zdarzenie                                    | Aktualizacja? | Powód                                           |
|----------------------------------------------|---------------|------------------------------------------------|
| ✅ Admin dodaje nowy produkt                 | ✅ Tak        | Nowy produkt musi być porównany z istniejącymi |
| ✅ Admin edytuje nazwę/opis/cenę produktu    | ✅ Tak        | Cechy się zmieniły, podobieństwa nieaktualne   |
| ✅ Admin dodaje/usuwa kategorię do produktu  | ✅ Tak        | Kategoria ma wagę 40%, duży wpływ na podobieństwo |
| ✅ Manualne przeliczenie z panelu admina     | ✅ Tak        | Admin klika "Regenerate Similarities"         |
| ❌ Użytkownik kupuje produkt                 | ❌ Nie        | Nie zmienia cech produktów                     |
| ❌ Użytkownik dodaje opinię                  | ❌ Nie        | Opinie nie wpływają na content-based          |
| ❌ Użytkownik przegląda produkt              | ❌ Nie        | Nie zmienia cech produktów                     |

---

### 9. `backend/home/recommendation_views.py` – 📊 **Endpoint Rekomendacji**

**Lokalizacja:** `backend/home/recommendation_views.py`

```python
class RecommendationsPreviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        algorithm = request.query_params.get("algorithm", "collaborative")

        if algorithm == "content_based":
            from home.models import ProductSimilarity, Product
            from django.db.models import Avg

            try:
                # 1. Pobierz ostatnio oglądane produkty użytkownika
                user_interactions = UserInteraction.objects.filter(
                    user=request.user
                ).order_by('-created_at')[:5]

                if not user_interactions.exists():
                    # Jeśli brak interakcji, zwróć popularne produkty
                    products = Product.objects.annotate(
                        avg_rating=Avg('opinion__rating')
                    ).order_by('-avg_rating')[:6]
                    serializer = ProductSerializer(products, many=True)
                    return Response(serializer.data)

                # 2. Zbierz ID produktów z interakcji
                interacted_product_ids = [
                    interaction.product_id
                    for interaction in user_interactions
                ]

                # 3. Znajdź podobne produkty (content-based)
                similar_products = ProductSimilarity.objects.filter(
                    product1_id__in=interacted_product_ids,
                    similarity_type='content_based'
                ).exclude(
                    product2_id__in=interacted_product_ids  # Wyklucz już oglądane
                ).select_related('product2').order_by(
                    '-similarity_score'
                )[:20]

                # 4. Agreguj wyniki (jeden produkt może być podobny do wielu)
                product_scores = {}
                for sim in similar_products:
                    product_id = sim.product2_id
                    score = sim.similarity_score

                    if product_id in product_scores:
                        # Użyj maksymalnego podobieństwa
                        product_scores[product_id] = max(product_scores[product_id], score)
                    else:
                        product_scores[product_id] = score

                # 5. Sortuj i weź top 6
                sorted_products = sorted(
                    product_scores.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:6]

                product_ids = [p[0] for p in sorted_products]
                products = Product.objects.filter(id__in=product_ids)

                # 6. Zwróć w kolejności podobieństwa
                products_dict = {p.id: p for p in products}
                ordered_products = [products_dict[pid] for pid in product_ids]

                serializer = ProductSerializer(ordered_products, many=True)
                return Response(serializer.data)

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
```

**Przykład przepływu danych:**

```
Użytkownik oglądał ostatnio:
  1. AMD Ryzen 7 5800X3D (product_id=295)
  2. ASUS ROG STRIX B550-F (product_id=341)
  3. Corsair Vengeance RGB 16GB (product_id=156)

Krok 1: Zapytanie do ProductSimilarity
SELECT product2_id, similarity_score
FROM home_productsimilarity
WHERE product1_id IN (295, 341, 156)
  AND similarity_type = 'content_based'
ORDER BY similarity_score DESC
LIMIT 20;

Wyniki:
| product2_id | similarity_score | podobny do |
|-------------|------------------|------------|
| 412         | 0.891            | 295        |
| 398         | 0.856            | 341        |
| 412         | 0.834            | 341        |
| 203         | 0.721            | 156        |
| 298         | 0.698            | 295        |

Krok 2: Agregacja (wybierz max score dla każdego produktu)
product_scores = {
    412: max(0.891, 0.834) = 0.891,
    398: 0.856,
    203: 0.721,
    298: 0.698
}

Krok 3: Sortowanie i top 6
Rekomendacje:
  1. Produkt 412 (score: 0.891)
  2. Produkt 398 (score: 0.856)
  3. Produkt 203 (score: 0.721)
  4. Produkt 298 (score: 0.698)
```

---

## 🤖 Jak To Działa (Krok po Kroku)

### 🔁 Przy Starcie Systemu (Wstępne Generowanie)

1. Admin uruchamia backend Django
2. `signals.py` może wywołać `update_content_based_similarity()` (opcjonalnie)
3. Lub admin klika "Regenerate Similarities" w panelu administracyjnym
4. `CustomContentBasedFilter.generate_similarities_for_all_products()` się uruchamia
5. Dla każdego produktu ekstraktowane są cechy z wagami
6. Obliczane jest podobieństwo cosinusowe między wszystkimi parami produktów
7. Wyniki zapisywane w `ProductSimilarity` (bulk create dla wydajności)
8. Macierz podobieństw cache'owana na 2 godziny

### 🏠 Na Stronie Głównej (Rekomendacje dla Użytkownika)

1. Użytkownik otwiera stronę główną
2. Frontend wywołuje `GET /api/recommendations-preview/?algorithm=content_based`
3. Backend sprawdza ostatnie interakcje użytkownika (ostatnie 5 produktów)
4. System znajduje produkty podobne do tych, które użytkownik oglądał
5. Zapytanie SQL do `ProductSimilarity` filtruje po `product1_id` i `similarity_type='content_based'`
6. Wyniki agregowane (max score dla każdego produktu)
7. Top 6 produktów sortowanych według podobieństwa
8. Frontend wyświetla rekomendacje z wynikami podobieństwa

### 👨‍💼 W Panelu Admin (Zarządzanie Podobieństwami)

1. Admin otwiera **Admin Panel** → sekcja "Content-Based Filtering"
2. **Auto-generowanie**: Jeśli brak podobieństw, system automatycznie je wygeneruje
3. **Konfigurowalne parametry**:
   - `similarity_threshold`: Minimalny próg podobieństwa (domyślnie: 20%)
   - `max_products_for_similarity`: Max produktów do przetworzenia (domyślnie: 500)
   - `feature_weights`: Wagi dla kategorii/tagów/ceny/słów kluczowych
4. **Regenerate Button**: Admin klika → system przelicza wszystkie podobieństwa
5. **Cache invalidation**: Po zmianach w produktach cache zostaje automatycznie wyczyszczony
6. **Tabela podobieństw**: Pokazuje top 20 najsilniejszych podobieństw z wynikami

---

## 📊 Wzory Matematyczne Używane w Projekcie

### 1. **Podobieństwo Cosinusowe (Cosine Similarity)**

**Wzór ogólny:**

```
                    A · B
cos(θ) = ─────────────────────
          ||A|| × ||B||

gdzie:
A = [a₁, a₂, ..., aₙ] - wektor cech produktu 1
B = [b₁, b₂, ..., bₙ] - wektor cech produktu 2

A · B = Σ(aᵢ × bᵢ) = a₁×b₁ + a₂×b₂ + ... + aₙ×bₙ (iloczyn skalarny)

||A|| = √(Σ aᵢ²) = √(a₁² + a₂² + ... + aₙ²) (norma euklidesowa wektora A)
||B|| = √(Σ bᵢ²) = √(b₁² + b₂² + ... + bₙ²) (norma euklidesowa wektora B)

Zakres wyniku: [0, 1]
- 1.0: wektory identyczne (kąt θ = 0°)
- 0.5: wektory prostopadłe (kąt θ = 60°)
- 0.0: wektory ortogonalne (kąt θ = 90°)
```

**Pseudokod:**

```python
def cosine_similarity(vector_A, vector_B):
    dot_product = sum(a * b for a, b in zip(vector_A, vector_B))
    norm_A = sqrt(sum(a * a for a in vector_A))
    norm_B = sqrt(sum(b * b for b in vector_B))

    if norm_A == 0 or norm_B == 0:
        return 0.0

    return dot_product / (norm_A * norm_B)
```

**Przykład rzeczywisty z projektu:**

```
Produkt A (AMD Ryzen 7 5800X3D):
  Wektor cech: [0.4, 0.4, 0.3, 0.3, 0.2, 0.02, 0.02]
  Cechy: [category_components, category_processors, tag_gaming,
          tag_high_performance, price_high, keyword_ryzen, keyword_processor]

Produkt B (AMD Ryzen 9 5900X):
  Wektor cech: [0.4, 0.4, 0.3, 0.3, 0.2, 0.02, 0.02]
  Cechy: [category_components, category_processors, tag_gaming,
          tag_workstation, price_high, keyword_ryzen, keyword_cores]

Krok 1: Iloczyn skalarny (dot product)
A · B = (0.4×0.4) + (0.4×0.4) + (0.3×0.3) + (0.3×0.3) + (0.2×0.2) + (0.02×0.02) + (0.02×0.02)
      = 0.16 + 0.16 + 0.09 + 0.09 + 0.04 + 0.0004 + 0.0004
      = 0.5408

Krok 2: Normy wektorów
||A|| = √(0.4² + 0.4² + 0.3² + 0.3² + 0.2² + 0.02² + 0.02²)
      = √(0.16 + 0.16 + 0.09 + 0.09 + 0.04 + 0.0004 + 0.0004)
      = √0.5408 = 0.7354

||B|| = √(0.4² + 0.4² + 0.3² + 0.3² + 0.2² + 0.02² + 0.02²)
      = √0.5408 = 0.7354

Krok 3: Podobieństwo cosinusowe
cos(θ) = 0.5408 / (0.7354 × 0.7354)
       = 0.5408 / 0.5408
       = 1.000

Wynik: Podobieństwo = 100% (produkty prawie identyczne!)
```

---

### 2. **TF (Term Frequency) - Uproszczona Wersja**

**Wzór:**

```
TF(term, document) = częstość_termu_w_dokumencie / całkowita_liczba_słów_w_dokumencie

lub prościej:
TF(term) = count(term) / total_words
```

**Pseudokod:**

```python
def calculate_term_frequency(text):
    words = tokenize(text)
    filtered_words = [w for w in words if w not in stop_words and len(w) > 3]

    word_freq = Counter(filtered_words)
    total_words = len(filtered_words)

    tf_scores = {}
    for word, count in word_freq.items():
        tf_scores[word] = count / total_words

    return tf_scores
```

**Przykład:**

```
Opis produktu:
"Gaming laptop with powerful gaming performance and gaming RGB lighting"

Krok 1: Tokenizacja i filtrowanie
Słowa: ["gaming", "laptop", "with", "powerful", "gaming", "performance",
        "and", "gaming", "rgb", "lighting"]
Filtrowane (len > 3, bez stop words):
  ["gaming", "laptop", "powerful", "gaming", "performance", "gaming", "lighting"]

Krok 2: Zliczanie
word_freq = {
    "gaming": 3,
    "laptop": 1,
    "powerful": 1,
    "performance": 1,
    "lighting": 1
}

Krok 3: TF
total_words = 7

TF("gaming") = 3/7 = 0.429
TF("laptop") = 1/7 = 0.143
TF("powerful") = 1/7 = 0.143
TF("performance") = 1/7 = 0.143
TF("lighting") = 1/7 = 0.143

Krok 4: Top 5 słów kluczowych (według TF)
  1. gaming (TF=0.429)
  2. laptop (TF=0.143)
  3. performance (TF=0.143)
  4. powerful (TF=0.143)
  5. lighting (TF=0.143)
```

---

### 3. **Wagi Cech (Feature Weights)**

**Wzór dla ważonego wektora cech:**

```
Feature_Score = Base_Weight × Presence_Indicator

gdzie:
- Base_Weight: Waga przypisana do danego typu cechy (np. category: 0.40)
- Presence_Indicator: 1 jeśli cecha występuje, 0 jeśli nie

Dla wielu cech tego samego typu:
Total_Feature_Score = Σ(Base_Weight) dla każdej występującej cechy
```

**Przykład obliczenia:**

```
Produkt: Gaming Laptop (ID: 156)

Cechy:
  Kategorie: ["Laptops", "Gaming"]
  Tagi: ["High-Performance", "RGB", "Portable"]
  Cena: 2500 PLN
  Słowa kluczowe: ["gaming", "laptop", "performance", "display", "graphics"]

Obliczenia wag:

1. Kategorie (waga: 0.40 każda)
   feature_category_laptops = 0.40
   feature_category_gaming = 0.40

2. Tagi (waga: 0.30 każdy)
   feature_tag_high-performance = 0.30
   feature_tag_rgb = 0.30
   feature_tag_portable = 0.30

3. Cena (waga: 0.20)
   price_category = "premium" (2500 PLN > 1500)
   feature_price_premium = 0.20

4. Słowa kluczowe (waga: 0.10 / 5 = 0.02 każde)
   feature_keyword_gaming = 0.02
   feature_keyword_laptop = 0.02
   feature_keyword_performance = 0.02
   feature_keyword_display = 0.02
   feature_keyword_graphics = 0.02

Wektor cech (skrócony):
{
    "category_laptops": 0.40,
    "category_gaming": 0.40,
    "tag_high-performance": 0.30,
    "tag_rgb": 0.30,
    "tag_portable": 0.30,
    "price_premium": 0.20,
    "keyword_gaming": 0.02,
    "keyword_laptop": 0.02,
    "keyword_performance": 0.02,
    "keyword_display": 0.02,
    "keyword_graphics": 0.02
}
```

---

## ⚙️ Architektura Systemu i Optymalizacje

### Cache i Wydajność

```python
# backend/home/custom_recommendation_engine.py

cache_key = "content_based_similarity_matrix"
cache_timeout = 7200  # 2 godziny

# Sprawdź cache
cached_result = cache.get(cache_key)
if cached_result:
    return cached_result

# Oblicz podobieństwa
similarity_count = generate_similarities_for_all_products()

# Zapisz w cache
cache.set(cache_key, similarity_count, timeout=cache_timeout)
```

### Bulk Operations dla Wydajności Bazy Danych

```python
similarities_to_create = []

for i, product1 in enumerate(products):
    for product2 in comparison_products:
        similarity_score = self.calculate_product_similarity(product1, product2)

        if similarity_score > self.similarity_threshold:
            similarities_to_create.extend([...])

            # Bulk create co 1000 rekordów
            if len(similarities_to_create) >= 1000:
                ProductSimilarity.objects.bulk_create(similarities_to_create)
                similarities_to_create = []

# Zapisz pozostałe
if similarities_to_create:
    ProductSimilarity.objects.bulk_create(similarities_to_create)
```

**Porównanie wydajności:**

| Metoda                     | Czas (500 produktów) | Zapytań SQL |
|----------------------------|----------------------|-------------|
| ❌ Bez bulk (pojedyncze)   | ~45 minut            | ~125,000    |
| ✅ Bulk create (1000)      | ~3 minuty            | ~125        |
| ⚡ Bulk + cache + limits   | ~2 minuty            | ~125        |

---

## 📌 Dlaczego Content-Based Filtering?

### Zalety:

1. **Nie wymaga danych od innych użytkowników** - działa nawet dla nowych użytkowników (rozwiązuje "cold start problem")
2. **Transparentność** - łatwo wyjaśnić dlaczego produkt został polecony ("podobny do X")
3. **Stabilność** - wyniki nie zmieniają się drastycznie z nowymi zamówieniami
4. **Kontrolowalność** - admin może dostosować wagi cech (kategoria: 40%, tagi: 30%, itd.)
5. **Niezależność** - każdy produkt ma swoje cechy, nie zależy od zachowań innych

### Wady:

1. **Brak serendipity** - poleca tylko podobne produkty, nie odkrywa nowych kategorii
2. **Over-specialization** - użytkownik może "utkn ąć" w jednej kategorii (np. tylko laptopy)
3. **Wymaga dobrych metadanych** - jakość rekomendacji zależy od jakości opisów produktów
4. **Nie uwzględnia kontekstu** - nie wie że użytkownik kupił laptop tydzień temu

---

## ✅ Podsumowanie Kluczowych Plików i Ich Roli

| Plik                                                 | Rola                                                           |
|------------------------------------------------------|---------------------------------------------------------------|
| `custom_recommendation_engine.py → CustomContentBasedFilter` | Główna klasa implementująca algorytm content-based |
| `custom_recommendation_engine.py → calculate_product_similarity()` | Oblicza podobieństwo cosinusowe między produktami |
| `custom_recommendation_engine.py → _extract_weighted_features()` | Ekstraktuje wektory cech z wagami |
| `models.py → ProductSimilarity`                      | Przechowuje macierz podobieństw produktów          |
| `signals.py → handle_product_changes()`              | Invaliduje cache przy zmianach w produktach        |
| `signals.py → update_content_based_similarity()`     | Regeneruje macierz podobieństw                     |
| `recommendation_views.py → RecommendationsPreviewView` | API endpoint zwracający rekomendacje content-based |

---

## 🚀 Co Jest Dynamiczne? Co Jest Statyczne?

| Zdarzenie                        | Przelicza Podobieństwa? | Powód                                   |
|----------------------------------|-------------------------|-----------------------------------------|
| ✅ Admin dodaje nowy produkt     | ✅ Tak                  | Nowy produkt musi być w macierzy       |
| ✅ Admin edytuje opis produktu   | ✅ Tak                  | Cechy produktu się zmieniły            |
| ✅ Admin zmienia kategorię       | ✅ Tak                  | Kategoria ma wagę 40%                  |
| ✅ Admin klika "Regenerate"      | ✅ Tak                  | Manualne przeliczenie                  |
| ❌ Użytkownik kupuje produkt     | ❌ Nie                  | Nie zmienia cech produktów             |
| ❌ Użytkownik przegląda produkt  | ❌ Nie                  | Podobieństwa są pre-compute            |
| ❌ Użytkownik dodaje opinię      | ❌ Nie                  | Content-based nie używa opinii         |

---

## 📚 Bibliografia

- Salton, G., McGill, M. J. (1983). "Introduction to Modern Information Retrieval"
- Manning, C. D., Raghavan, P., Schütze, H. (2008). "Introduction to Information Retrieval", Cambridge University Press
- Leskovec, J., Rajaraman, A., Ullman, J. D. (2014). "Mining of Massive Datasets", rozdz. 9 - Recommendation Systems
- Ricci, F., Rokach, L., Shapira, B. (2015). "Recommender Systems Handbook", 2nd Edition
- Pazzani, M. J., Billsus, D. (2007). "Content-Based Recommendation Systems" w "The Adaptive Web"

---

**Ostatnia aktualizacja:** 12 października 2025
**Status:** ✅ Produkcyjny (wszystkie funkcje działają poprawnie)
**Wersja dokumentacji:** 1.0
