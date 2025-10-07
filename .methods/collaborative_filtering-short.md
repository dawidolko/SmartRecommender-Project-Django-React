# 🔄 Collaborative Filtering - Krótki Przewodnik "Jak To Działa"

## 📊 **PRZEPŁYW DANYCH: OD BAZY DO FRONTENDU**

---

## 1️⃣ **BAZA DANYCH** - Co Jest Przechowywane?

### Tabele Kluczowe:

```sql
-- 1. Zamówienia użytkowników
OrderProduct (order_id, user_id, product_id, quantity)
Przykład: User #5 kupił Product #10 w ilości 2

-- 2. Podobieństwa między produktami (WYNIK CF)
ProductSimilarity (product1_id, product2_id, similarity_score, similarity_type)
Przykład: Product #10 jest podobny do Product #15 (score: 0.85)

-- 3. Rekomendacje dla użytkowników
UserProductRecommendation (user_id, product_id, score, recommendation_type)
Przykład: User #5 → rekomendujemy Product #15 (score: 0.85)

-- 4. Ustawienia algorytmu
RecommendationSettings (user_id, active_algorithm)
Przykład: User #5 używa "collaborative"
```

---

## 2️⃣ **BACKEND** - Jak Oblicza Podobieństwa?

### Krok 1: **Budowanie Macierzy User-Product**

```python
# Z bazy danych pobieramy wszystkie zakupy
OrderProduct: [(User1, Product1, qty=2), (User1, Product2, qty=1), ...]

# Tworzymy macierz:
           Product1  Product2  Product3  Product4
User1         2         1         0         0
User2         1         0         2         0
User3         0         1         0         3
```

---

### Krok 2: **Mean-Centering (Normalizacja)**

**DLACZEGO?** Bo różni użytkownicy kupują w różnych ilościach:

- User A kupuje dużo (10+ produktów) → wysokie wartości
- User B kupuje mało (2-3 produkty) → niskie wartości

**CO ROBIMY?** Odejmujemy średnią użytkownika:

```python
# User1 średnia = (2+1)/2 = 1.5
User1: [2, 1, 0, 0] → [2-1.5, 1-1.5, 0-1.5, 0-1.5] = [0.5, -0.5, -1.5, -1.5]

# User2 średnia = (1+2)/2 = 1.5
User2: [1, 0, 2, 0] → [1-1.5, 0-1.5, 2-1.5, 0-1.5] = [-0.5, -1.5, 0.5, -1.5]

# Teraz wartości pokazują "powyżej/poniżej średniej użytkownika"
```

**WZÓR Z LITERATURY** (Sarwar et al. 2001):

```
sim(i,j) = Σu (Ru,i - R̄u)(Ru,j - R̄u) / √[Σu(Ru,i - R̄u)²] √[Σu(Ru,j - R̄u)²]
```

---

### Krok 3: **Obliczanie Podobieństwa między Produktami**

**TRANSPOZYCJA MACIERZY** → Teraz kolumny = produkty:

```python
product_similarity = cosine_similarity(normalized_matrix.T)
#                                                       ^^^ TRANSPOSE!

# Wynik: macierz podobieństw produkt-do-produkt
           Product1  Product2  Product3  Product4
Product1     1.00      0.85      0.12      0.05
Product2     0.85      1.00      0.42      0.08
Product3     0.12      0.42      1.00      0.67
Product4     0.05      0.08      0.67      1.00
```

**Cosine Similarity** mierzy kąt między wektorami:

- `1.0` = identyczne (ten sam produkt)
- `0.85` = bardzo podobne (często kupowane razem)
- `0.05` = niezwiązane

---

### Krok 4: **Filtrowanie i Zapis do Bazy**

```python
# Zapisz tylko podobieństwa > 0.3 (threshold)
for i, product1 in enumerate(products):
    for j, product2 in enumerate(products):
        if i != j and similarity[i][j] > 0.3:
            ProductSimilarity.objects.create(
                product1=product1,
                product2=product2,
                similarity_score=similarity[i][j],
                similarity_type="collaborative"
            )
```

**REZULTAT W BAZIE**:

```
Product1 ↔ Product2 (score: 0.85) ✅
Product2 ↔ Product3 (score: 0.42) ✅
Product3 ↔ Product4 (score: 0.67) ✅
Product1 ↔ Product3 (score: 0.12) ❌ Poniżej 0.3, nie zapisane
```

---

## 3️⃣ **BACKEND API** - Jak Generuje Rekomendacje?

### Endpoint: `POST /api/generate-user-recommendations/`

```python
def generate_recommendations(user):
    # 1. Pobierz co użytkownik kupił
    user_purchases = [Product1, Product2, Product5]

    # 2. Dla każdego kupionego produktu znajdź podobne
    for product in user_purchases:
        similar = ProductSimilarity.objects.filter(
            product1=product,
            similarity_type="collaborative"
        ).order_by("-similarity_score")[:5]  # Top 5

        # 3. Agreguj scores
        for sim in similar:
            recommendations[sim.product2] += sim.similarity_score

    # 4. Zapisz do UserProductRecommendation
    # Product X → score 1.42 (suma podobieństw)
```

**PRZYKŁAD**:

```
User kupił: Laptop, Mouse
↓
Laptop podobny do: Monitor (0.85), Keyboard (0.72), Webcam (0.45)
Mouse podobny do: Keyboard (0.65), MousePad (0.58)
↓
Agregacja:
- Keyboard: 0.72 + 0.65 = 1.37 (najwyższy!)
- Monitor: 0.85
- MousePad: 0.58
- Webcam: 0.45
↓
Rekomendacje: [Keyboard, Monitor, MousePad, Webcam]
```

---

## 4️⃣ **FRONTEND** - Jak Wyświetla Rekomendacje?

### A. **Admin Panel** (`AdminStatistics.jsx`)

```jsx
// Admin wybiera algorytm
<button onClick={() => handleAlgorithmChange("collaborative")}>
  Collaborative Filtering
</button>;

// Apply Algorithm
const handleApplyAlgorithm = async () => {
  // 1. Zapisz ustawienie użytkownika
  await axios.post("/api/recommendation-settings/", {
    algorithm: "collaborative",
  });

  // 2. Przelicz podobieństwa (może zająć 10-30s)
  await axios.post("/api/process-recommendations/", {
    algorithm: "collaborative",
  });

  // 3. Pobierz podgląd rekomendacji
  const preview = await axios.get(
    "/api/recommendation-preview/?algorithm=collaborative"
  );

  // 4. Wyświetl top 6 produktów
  setRecommendationPreview(preview.data);
};
```

**CO WIDZI ADMIN**:

- Przyciski: [Collaborative Filtering] [Content-Based]
- Po kliknięciu "Apply": Loading spinner → Success message
- Preview: 6 najlepiej rekomendowanych produktów z obrazkami

---

### B. **Client Dashboard** (`ClientDashboard.jsx`)

```jsx
useEffect(() => {
  // 1. Sprawdź jaki algorytm użytkownik ma ustawiony
  const algorithmResponse = await axios.get('/api/recommendation-settings/');
  const algorithm = algorithmResponse.data.active_algorithm; // "collaborative"

  // 2. Pobierz rekomendacje dla tego algorytmu
  const recommendationsResponse = await axios.get(
    `/api/recommendation-preview/?algorithm=${algorithm}`
  );

  // 3. Wyświetl produkty
  setRecommendedProducts(recommendationsResponse.data);
}, []);
```

**CO WIDZI KLIENT**:

- Sekcja: "Recommended For You (Collaborative Filtering)"
- 6 produktów w kartkach z obrazkami i cenami
- Kliknięcie → przekierowanie na `/product/{id}`

---

### C. **Home Page** (`Testimonials.jsx`, `NewProducts.jsx`)

```jsx
// Pobierz algorytm z localStorage lub API
const algorithm =
  localStorage.getItem("recommendationAlgorithm") || "collaborative";

// Fetch produktów
const products = await axios.get(
  `/api/recommendation-preview/?algorithm=${algorithm}`
);

// Slider z produktami (react-slick)
<Slider {...settings}>
  {products.map((product) => (
    <TestimonialsItem key={product.id} {...product} />
  ))}
</Slider>;
```

**CO WIDZI UŻYTKOWNIK NA HOME**:

- Tytuł: "Personalized Recommendations (Collaborative Filtering)"
- Carousel/Slider z produktami (3 na raz na desktop)
- Autoplay co 4 sekundy

---

## 5️⃣ **TRIGGERS** - Kiedy Się Przelicza?

### Automatyczne Przeliczanie:

```python
# signals.py - Po każdym zamówieniu
@receiver(post_save, sender=Order)
def order_saved(sender, instance, **kwargs):
    # 1. Invaliduj cache CF
    cache.delete("collaborative_similarity_matrix")

    # 2. Wygeneruj nowe rekomendacje dla użytkownika
    generate_user_recommendations_after_order(instance.user)
```

**FLOW**:

```
User składa zamówienie
    ↓
Signal: post_save(Order)
    ↓
Cache CF invalidated
    ↓
Rekomendacje użytkownika przeliczone
    ↓
Następne request → świeże dane
```

### Manualne Przeliczanie:

```
Admin → Panel → Select "Collaborative" → Click "Apply Algorithm"
    ↓
POST /api/process-recommendations/
    ↓
Przelicz wszystkie podobieństwa (10-30s)
    ↓
Cache zapisany (2h TTL)
    ↓
Preview zaktualizowany
```

---

## 6️⃣ **FILTROWANIE I RANKING**

### Backend Filtering:

```python
# 1. Threshold Filtering (0.3)
if similarity_score > 0.3:
    save_to_database()  # Zapisz tylko silne podobieństwa

# 2. Top-N Selection (5 podobnych per produkt)
similar_products = ProductSimilarity.objects.filter(
    product1=purchased_product
).order_by("-similarity_score")[:5]

# 3. Score Aggregation (suma podobieństw)
for sim in similar_products:
    recommendations[sim.product2] += sim.similarity_score

# 4. Final Ranking (sortuj po score)
top_recommendations = sorted(
    recommendations.items(),
    key=lambda x: x[1],
    reverse=True
)[:6]  # Top 6 dla frontendu
```

---

### Frontend Display:

```jsx
// ClientDashboard.jsx
<div className="recommendations-grid">
  {recommendedProducts.map((product) => (
    <div
      className="recommendation-card"
      onClick={() => navigate(`/product/${product.id}`)}>
      <img src={`${apiUrl}/media/${product.photos[0].path}`} />
      <p>{product.name}</p>
      <p>${product.price}</p>
    </div>
  ))}
</div>
```

**REZULTAT**: 6 produktów w grid, każdy klikalny

---

## 🔄 **PEŁNY FLOW - OD POCZĄTKU DO KOŃCA**

```
1. USER KUPUJE PRODUKT
   ↓
2. BAZA DANYCH: OrderProduct.create(user, product, qty)
   ↓
3. SIGNAL: post_save(Order) → Invaliduj cache
   ↓
4. BACKEND: Przelicz podobieństwa CF (jeśli nie w cache)
   - Buduj macierz user-product
   - Mean-centering
   - Cosine similarity (transposed)
   - Zapisz do ProductSimilarity
   ↓
5. BACKEND: Generuj rekomendacje dla użytkownika
   - Pobierz zakupy użytkownika
   - Znajdź podobne produkty (top 5 per zakup)
   - Agreguj scores
   - Zapisz do UserProductRecommendation
   ↓
6. API: GET /api/recommendation-preview/?algorithm=collaborative
   - Pobierz UserProductRecommendation dla użytkownika
   - Sortuj po score DESC
   - Zwróć top 6
   ↓
7. FRONTEND: Wyświetl w Dashboard/Home/Testimonials
   - Fetch z API
   - Renderuj karty produktów
   - Slider/Grid layout
   ↓
8. USER KLIKA PRODUKT → Przekierowanie do /product/{id}
```

---

## ⚡ **OPTYMALIZACJE**

### Cache Strategy:

```python
# Cache result na 2h
cache.set("collaborative_similarity_matrix", result, timeout=7200)

# Invalidacja po zamówieniu
cache.delete("collaborative_similarity_matrix")
```

### Bulk Operations:

```python
# Zapisz 1000 podobieństw naraz
if len(similarities_to_create) >= 1000:
    ProductSimilarity.objects.bulk_create(similarities_to_create)
    similarities_to_create = []
```

### Database Queries:

```python
# select_related zamiast N+1 queries
OrderProduct.objects.select_related("order", "product").all()
```

---

## 📊 **METRYKI DZIAŁANIA**

| Operacja                      | Czas     | Cache?   |
| ----------------------------- | -------- | -------- |
| Process CF (1000 products)    | 10-30s   | ✅ 2h    |
| Generate user recommendations | 50-200ms | ✅ 30min |
| Fetch recommendation preview  | 10-30ms  | ❌       |
| Frontend render               | <100ms   | ❌       |

---

## 🎯 **KLUCZOWE RÓŻNICE: PRZED vs PO**

### PRZED (MinMax):

```
User A: [1, 5] → MinMax → [0.0, 1.0]
User B: [1, 1, 1] → MinMax → [0.0, 0.0, 0.0]
Problem: User B wygląda jakby nic nie kupił
```

### PO (Mean-Centering):

```
User A: [1, 5] → Mean 3.0 → [-2, +2]
User B: [1, 1, 1] → Mean 1.0 → [0, 0, 0]
Lepsze: Pokazuje relatywne preferencje
```

---

## 📚 **TL;DR - W 3 ZDANIACH**

1. **Backend** buduje macierz zakupów użytkowników, odejmuje średnią per użytkownik (mean-centering), i oblicza cosine similarity między **produktami** (nie użytkownikami).

2. **Baza danych** przechowuje podobieństwa między produktami (ProductSimilarity) i rekomendacje per użytkownik (UserProductRecommendation), które są agregacją scores z podobnych produktów.

3. **Frontend** pobiera top 6 rekomendacji z API endpoint `/api/recommendation-preview/` i wyświetla je w Dashboard, Home page (slider), i Testimonials, aktualizując się automatycznie gdy admin zmieni algorytm.

---

**Status**: ✅ Item-Based Collaborative Filtering z Adjusted Cosine Similarity  
**Reference**: Sarwar et al. (2001) - WWW '01  
**Implementacja**: Mean-Centering + Cosine Similarity + Cache Invalidation
