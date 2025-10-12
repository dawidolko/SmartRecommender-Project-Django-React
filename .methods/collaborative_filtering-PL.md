````markdown
Updated: 07/10/2025

# 🔄 Collaborative Filtering - System Rekomendacji Opartych na Produktach (Item-Based)

## Czym Jest "Collaborative Filtering" w Tym Sklepie?

Silnik rekomendacji w tym sklepie obsługuje dwa inteligentne algorytmy do rekomendacji produktów:

- **Collaborative Filtering (CF)** – Rekomenduje produkty na podstawie **podobieństwa między produktami** (item-to-item) analizując wzorce zakupowe użytkowników
- **Content-Based Filtering (CBF)** – Rekomenduje na podstawie cech produktów (własna implementacja manualna)

Te systemy pomagają personalizować odkrywanie produktów dla użytkowników i pozwalają administratorom wybierać, którą metodę zastosować.

---

## 📂 Przegląd Struktury Projektu (Kluczowe Pliki i Role)

### 1. `backend/home/recommendation_views.py` – ⚙️ **Główna Logika CF**

Ten plik przetwarza rekomendacje używając **Item-Based Collaborative Filtering**:

| Nazwa Funkcji                                     | Co Robi                                                                                                                       |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `process_collaborative_filtering()`               | Buduje macierz użytkownik-produkt i oblicza podobieństwo między **produktami** (nie użytkownikami) używając cosine similarity |
| `generate_user_recommendations_after_order(user)` | Generuje finalne rekomendacje per użytkownik na podstawie wybranego algorytmu                                                 |

**Wzór Item-Based CF z Adjusted Cosine Similarity** (Sarwar et al. 2001):

```python
# sim(i,j) = Σu (Ru,i - R̄u)(Ru,j - R̄u) / √(Σu(Ru,i - R̄u)²) √(Σu(Ru,j - R̄u)²)
#
# gdzie:
# - Ru,i = ocena/ilość zakupu użytkownika u dla produktu i
# - R̄u = średnia ocena/ilość użytkownika u
# - sim(i,j) = podobieństwo między produktem i a produktem j
```

### 2. `backend/home/signals.py` – 🔁 **Uruchamia CF Po Zamówieniu**

- Automatycznie wywoływane po złożeniu nowego zamówienia
- **Invaliduje cache CF** aby zapewnić świeże rekomendacje
- Przebudowuje reguły asocjacyjne, oblicza prognozy i **uruchamia CF w zależności od ustawień użytkownika**

```python
def run_all_analytics_after_order(order):
    # Invalidate collaborative filtering cache
    cache_key = "collaborative_similarity_matrix"
    cache.delete(cache_key)
    print(f"Invalidated CF cache after order {order.id}")

    # ... reszta logiki
```

### 3. `frontend/src/components/AdminPanel/AdminStatistics.jsx` – 🧪 **Panel Kontrolny Administratora**

Administrator może:

- Przełączać między CF a CBF za pomocą przycisków radio
- Zastosować wybrany algorytm, co:
  - Uruchamia ponowne przetwarzanie podobieństw produktów
  - Aktualizuje tabele bazy danych
- Zobaczyć podgląd na żywo najlepiej rekomendowanych produktów pod aktualnym algorytmem

### 4. `frontend/src/pages/Product/ProductPage.jsx` – 🛍️ **Logowanie Interakcji**

Gdy użytkownik:

- Dodaje produkt do koszyka
- Dodaje produkt do ulubionych

Tworzony jest log poprzez API: `POST /api/interaction/`, który aktualizuje:

- Tabelę `user_interactions` dla przyszłego trenowania modelu i analizy

### 5. `backend/home/models.py` – 🗃️ **Kluczowe Modele**

| Nazwa Modelu                | Opis                                                                            |
| --------------------------- | ------------------------------------------------------------------------------- |
| `ProductSimilarity`         | Przechowuje wyniki podobieństwa dla każdej pary produktów (typ: CF)             |
| `UserProductRecommendation` | Przechowuje punktowane rekomendacje produktów dla użytkowników                  |
| `RecommendationSettings`    | Zapisuje, który algorytm jest aktualnie aktywny per użytkownik                  |
| `UserInteraction`           | Loguje wyświetlenia produktów, kliknięcia, dodania do koszyka, ulubione, zakupy |

---

## 🔁 Jak To Działa (Krok po Kroku)

### 🛒 Ze Strony Użytkownika

1. Użytkownik dodaje produkt do koszyka → `ProductPage.jsx`
2. To loguje zdarzenie `add_to_cart` przez API → przechowywane w `UserInteraction`
3. Po ukończeniu zamówienia:
   - Django `signals.py` uruchamia `run_all_analytics_after_order()`
   - Wywołuje generowanie rekomendacji na podstawie wybranego algorytmu użytkownika
   - Aktualizuje `ProductSimilarity` i `UserProductRecommendation`

### 🧑‍💼 Ze Strony Administratora

1. Administrator odwiedza panel → `AdminStatistics.jsx`
2. Wybiera metodę filtrowania: CF
3. Klika **Apply Algorithm**
   - Backend zapisuje preferencję w `RecommendationSettings`
   - Uruchamia ponowne obliczenia podobieństw przez API `/api/process-recommendations/`
4. Administrator widzi zaktualizowany podgląd rekomendacji z `/api/recommendation-preview/`

---

## 🧮 Matematyczne Podstawy Collaborative Filtering

### Wzór Item-Based CF z Adjusted Cosine Similarity (Sarwar et al. 2001):

```python
def process_collaborative_filtering(self):
    """
    Item-Based Collaborative Filtering using Adjusted Cosine Similarity
    Reference: Sarwar, B., Karypis, G., Konstan, J., Riedl, J. (2001)
    "Item-based collaborative filtering recommendation algorithms"
    """
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    # Buduj macierz user-product
    users = User.objects.all()
    products = Product.objects.all()

    user_product_matrix = defaultdict(dict)
    for order in OrderProduct.objects.select_related("order", "product").all():
        user_product_matrix[order.order.user_id][order.product_id] = order.quantity

    user_ids = list(user_product_matrix.keys())
    product_ids = list(products.values_list("id", flat=True))

    # Utwórz macierz numpy
    matrix = []
    for user_id in user_ids:
        row = []
        for product_id in product_ids:
            row.append(user_product_matrix[user_id].get(product_id, 0))
        matrix.append(row)

    matrix = np.array(matrix, dtype=np.float32)

    # Mean-centering (centrowanie względem średniej użytkownika)
    # To jest kluczowe dla Adjusted Cosine Similarity
    print("Applying mean-centering (Adjusted Cosine Similarity - Sarwar et al. 2001)")
    normalized_matrix = np.zeros_like(matrix, dtype=np.float32)

    for i, user_row in enumerate(matrix):
        # Oblicz średnią tylko z zakupionych produktów (wartości > 0)
        purchased_items = user_row[user_row > 0]

        if len(purchased_items) > 0:
            user_mean = np.mean(purchased_items)
            # Odejmij średnią użytkownika od wszystkich wartości
            normalized_matrix[i] = user_row - user_mean
        else:
            # Użytkownik nie ma zakupów, zostaw zera
            normalized_matrix[i] = user_row

    # Oblicz podobieństwo MIĘDZY PRODUKTAMI (transpozycja macierzy)
    # Każda kolumna reprezentuje produkt, wiersze to użytkownicy
    product_similarity = cosine_similarity(normalized_matrix.T)

    # Zapisz podobieństwa w bazie danych
    ProductSimilarity.objects.filter(similarity_type="collaborative").delete()

    similarity_threshold = 0.3
    similarities_to_create = []
    similarity_count = 0

    for i, product1_id in enumerate(product_ids):
        for j, product2_id in enumerate(product_ids):
            if i != j and product_similarity[i][j] > similarity_threshold:
                similarities_to_create.append(
                    ProductSimilarity(
                        product1_id=product1_id,
                        product2_id=product2_id,
                        similarity_type="collaborative",
                        similarity_score=float(product_similarity[i][j])
                    )
                )
                similarity_count += 1

                # Bulk create w paczkach dla wydajności
                if len(similarities_to_create) >= 1000:
                    ProductSimilarity.objects.bulk_create(similarities_to_create)
                    similarities_to_create = []

    # Zapisz pozostałe podobieństwa
    if similarities_to_create:
        ProductSimilarity.objects.bulk_create(similarities_to_create)

    print(f"Created {similarity_count} collaborative similarities using Adjusted Cosine")
    return similarity_count
```

---

## 🛠️ Technologie Zaangażowane

| Warstwa         | Użyte Technologie                                                      |
| --------------- | ---------------------------------------------------------------------- |
| Backend         | Django, Django REST Framework, NumPy, scikit-learn (cosine similarity) |
| Frontend        | React, Axios, Toastify, Framer Motion                                  |
| Przechowywanie  | PostgreSQL, Django Models                                              |
| Przepływ Danych | REST APIs zabezpieczone JWT                                            |

---

## 📊 Wzory Matematyczne Używane w CF

### 1. **Adjusted Cosine Similarity między produktami** (Sarwar et al. 2001):

```python
# Podobieństwo między produktem i a produktem j:
sim(i,j) = Σu∈U (Ru,i - R̄u)(Ru,j - R̄u) / √(Σu∈U (Ru,i - R̄u)²) √(Σu∈U (Ru,j - R̄u)²)

gdzie:
- Ru,i = ocena/ilość zakupu użytkownika u dla produktu i
- Ru,j = ocena/ilość zakupu użytkownika u dla produktu j
- R̄u = średnia ocena/ilość użytkownika u (tylko z zakupionych produktów)
- U = zbiór wszystkich użytkowników którzy kupili oba produkty
```

**Dlaczego Adjusted Cosine zamiast zwykłej Cosine?**

- Zwykła cosine nie uwzględnia różnic w skalach ocen między użytkownikami
- Niektórzy użytkownicy kupują dużo (high-volume buyers), inni mało
- Adjusted Cosine odejmuje średnią użytkownika, eliminując ten bias

### 2. **Mean-Centering (Centrowanie Względem Średniej)**:

```python
# Dla każdego użytkownika u:
normalized_Ru,i = Ru,i - R̄u

gdzie:
- Ru,i = oryginalna wartość (ilość zakupu)
- R̄u = średnia z zakupionych produktów użytkownika u
- normalized_Ru,i = wartość po centrowaniu
```

**Przykład**:

- Użytkownik A kupił produkty: [5, 3, 1, 0, 0] (średnia z >0: 3.0)
- Po mean-centering: [2, 0, -2, -3, -3]
- Teraz produkty z ilością 5 są "powyżej średniej" (+2), a 1 "poniżej średniej" (-2)

### 3. **Threshold Filtering (Filtrowanie Progowe)**:

```python
# Zapisz tylko podobieństwa powyżej progu:
if sim(i,j) > 0.3:
    store_similarity(product_i, product_j, similarity_score)
```

**Powód**: Redukuje szum i rozmiar danych, przechowując tylko silne podobieństwa

---

## 🔍 Różnice między Podejściami CF

### 📊 **User-Based CF** vs **Item-Based CF**:

| Aspekt                    | User-Based CF                               | Item-Based CF (Nasza Implementacja)        |
| ------------------------- | ------------------------------------------- | ------------------------------------------ |
| **Podobieństwo**          | Między użytkownikami                        | Między produktami                          |
| **Macierz**               | Wiersze = użytkownicy, podobieństwo wierszy | Kolumny = produkty, podobieństwo kolumn    |
| **Rekomendacja**          | "Użytkownicy podobni do Ciebie lubią X"     | "Skoro kupiłeś Y, może spodoba Ci się X"   |
| **Skalowalność**          | Słaba (liczba użytkowników rośnie szybko)   | Dobra (liczba produktów stabilna)          |
| **Obliczenia**            | Przy każdym zapytaniu (online)              | Pre-computed (offline), szybkie odpowiedzi |
| **Cold Start (new user)** | Problem (brak podobnych użytkowników)       | Działa (rekomenduje na podstawie 1 zakupu) |
| **Przykład zastosowania** | Netflix (ratings predictions)               | Amazon (frequently bought together)        |

### ⚠️ **Poprzednia Implementacja (MinMax Normalizacja)**:

```python
# MinMax per user: normalizuje każdy wiersz do [0,1]
scaler = MinMaxScaler()
normalized_row = scaler.fit_transform(user_row.reshape(-1, 1)).flatten()
```

**Problem**:

- Użytkownik który kupił 1 produkt: wartość = 1.0 (100%)
- Użytkownik który kupił 100 produktów: każdy produkt = mała wartość
- **Zawyża znaczenie** pojedynczych zakupów u małoaktywnych użytkowników

### ✅ **Obecna Implementacja (Mean-Centering)**:

```python
# Mean-centering: odejmuje średnią użytkownika
user_mean = np.mean(user_row[user_row > 0])
normalized_matrix[i] = user_row - user_mean
```

**Zalety**:

- Eliminuje bias wynikający z różnych poziomów aktywności użytkowników
- Zgodne z literaturą naukową (Sarwar et al. 2001)
- Lepsze wyniki dla heterogenicznych użytkowników

---

## 📈 Przykład Działania Item-Based CF

### Scenariusz (Dane Zakupowe):

- **Użytkownik A** kupił: Laptop (qty=1), Mysz (qty=2), Klawiatura (qty=1)
- **Użytkownik B** kupił: Laptop (qty=1), Mysz (qty=1), Monitor (qty=1)
- **Użytkownik C** kupił: Telefon (qty=1), Słuchawki (qty=1)

### Krok 1: Macierz User-Product (Oryginalna)

```
          Laptop  Mysz  Klawiatura  Monitor  Telefon  Słuchawki
User A      1      2       1          0        0         0
User B      1      1       0          1        0         0
User C      0      0       0          0        1         1
```

### Krok 2: Mean-Centering (Odejmij średnią użytkownika)

```python
# User A: średnia = (1+2+1)/3 = 1.33
# Po centrowaniu: [-0.33, 0.67, -0.33, -1.33, -1.33, -1.33]

# User B: średnia = (1+1+1)/3 = 1.0
# Po centrowaniu: [0, 0, -1, 0, -1, -1]

# User C: średnia = (1+1)/2 = 1.0
# Po centrowaniu: [-1, -1, -1, -1, 0, 0]
```

### Krok 3: Oblicz Podobieństwo między Produktami

```python
# Podobieństwo Laptop-Mysz (używając mean-centered wartości):
# Wektory kolumn (transpozycja):
# Laptop_vector = [-0.33, 0, -1]
# Mysz_vector = [0.67, 0, -1]

sim(Laptop, Mysz) = cosine_similarity(Laptop_vector, Mysz_vector) = 0.82 (wysokie!)
sim(Laptop, Telefon) = cosine_similarity(Laptop_vector, Telefon_vector) = 0.05 (niskie)
```

### Krok 4: Generuj Rekomendacje

**Dla nowego użytkownika D, który właśnie kupił Laptop**:

1. System znajduje produkty podobne do Laptop
2. Najbardziej podobne: Mysz (0.82), Monitor (0.65), Klawiatura (0.58)
3. **Rekomendacja**: Mysz, Monitor, Klawiatura (w tej kolejności)

### Dlaczego To Działa?

- Użytkownicy A i B kupili zarówno Laptop jak i Mysz → **silny wzorzec**
- Mean-centering sprawia że użytkownik A (który kupił 2 myszy) nie dominuje nad B (który kupił 1)
- System wykrywa że produkty są często kupowane razem

---

## ✅ Podsumowanie Kluczowych Tabel

| Nazwa Tabeli                  | Cel                                                                        |
| ----------------------------- | -------------------------------------------------------------------------- |
| `user_interactions`           | Śledzi wszystkie akcje produktowe (wyświetlenia, kliknięcia, koszyk, itp.) |
| `product_similarity`          | Wyniki podobieństwa między produktami dla CF i CBF                         |
| `user_product_recommendation` | Przechowuje finalne rekomendacje per użytkownik                            |
| `recommendation_settings`     | Śledzi, który algorytm jest aktywny dla każdego użytkownika                |

---

## 🚀 Co Jest Dynamiczne? Co Jest Manualne?

| Zdarzenie                       | Regeneruje CF?         | Invaliduje Cache? | Używa Prawdziwych Wzorów?         |
| ------------------------------- | ---------------------- | ----------------- | --------------------------------- |
| ✅ Użytkownik składa zamówienie | ✅ Tak (automatycznie) | ✅ Tak            | ✅ Tak (Sarwar et al. 2001)       |
| ✅ Admin wybiera CF w panelu    | ✅ Tak (manualnie)     | ✅ Tak            | ✅ Tak (Item-Based + Adj. Cosine) |
| ❌ Dodawanie do koszyka         | ❌ Nie                 | ❌ Nie            | -                                 |
| ❌ Przeglądanie produktu        | ❌ Nie                 | ❌ Nie            | -                                 |

### Cache Strategy:

- **Czas życia cache**: 2 godziny (7200 sekund)
- **Invalidacja**: Automatyczna po każdym nowym zamówieniu
- **Powód**: Nowe zamówienia zmieniają wzorce zakupowe, wymagają przeliczenia podobieństw

---

## 🔍 Bibliografia

### Artykuły Naukowe (Główne Źródła):

1. **Sarwar, B., Karypis, G., Konstan, J., Riedl, J. (2001)**

   - "Item-based collaborative filtering recommendation algorithms"
   - _Proceedings of the 10th International Conference on World Wide Web (WWW '01)_
   - **Główne źródło dla naszej implementacji** - wprowadza Adjusted Cosine Similarity

2. **Linden, G., Smith, B., York, J. (2003)**

   - "Amazon.com recommendations: Item-to-item collaborative filtering"
   - _IEEE Internet Computing, Vol. 7, No. 1_
   - Przemysłowe zastosowanie item-based CF w Amazonie

3. **Deshpande, M., Karypis, G. (2004)**
   - "Item-based top-n recommendation algorithms"
   - _ACM Transactions on Information Systems (TOIS), Vol. 22, No. 1_
   - Optymalizacje dla dużych zbiorów danych

### Porównanie Podejść:

4. **Resnick, P., Varian, H. R. (1997)**

   - "Recommender systems"
   - _Communications of the ACM, Vol. 40, No. 3_
   - Klasyczne user-based CF (dla porównania)

5. **Herlocker, J. L., Konstan, J. A., Riedl, J. (1999)**
   - "Algorithmic framework for performing collaborative filtering"
   - _Proceedings of the 22nd Annual International ACM SIGIR Conference_
   - Podstawy teoretyczne CF

### Książki:

6. **Aggarwal, C. C. (2016)**

   - "Recommender Systems: The Textbook"
   - Springer, ISBN: 978-3-319-29659-3
   - Rozdział 2: Collaborative Filtering (teoria i praktyka)

7. **Ricci, F., Rokach, L., Shapira, B. (2015)**
   - "Recommender Systems Handbook"
   - Springer, 2nd Edition, ISBN: 978-1-4899-7637-6
   - Rozdział 3: Collaborative Filtering Techniques

---

## 🎯 Lokalizacja w Kodzie

### Backend Files:

- `recommendation_views.py` → `process_collaborative_filtering()` - główna logika CF
- `models.py` → `UserProductRecommendation`, `ProductSimilarity`, `RecommendationSettings`
- `signals.py` → Automatyczne uruchamianie po zamówieniach

### Frontend Files:

- `AdminStatistics.jsx` → Panel wyboru algorytmu CF/CBF
- `ProductPage.jsx` → Logowanie interakcji użytkowników

### API Endpoints:

- `/api/process-recommendations/` → Uruchamia CF
- `/api/recommendation-settings/` → Zarządza ustawieniami algorytmu
- `/api/recommendation-preview/` → Podgląd rekomendacji
````

https://files.grouplens.org/papers/www10_sarwar.pdf
