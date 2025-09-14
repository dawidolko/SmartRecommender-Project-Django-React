To be corrected: 14/09/2025

# 🔄 Collaborative Filtering - System Rekomendacji Opartych na Użytkownikach

## Czym Jest "Collaborative Filtering" w Tym Sklepie?

Silnik rekomendacji w tym sklepie obsługuje dwa inteligentne algorytmy do rekomendacji produktów:

- **Collaborative Filtering (CF)** – Rekomenduje produkty na podstawie tego, co kupili _podobni użytkownicy_
- **Content-Based Filtering (CBF)** – Rekomenduje na podstawie cech produktów

Te systemy pomagają personalizować odkrywanie produktów dla użytkowników i pozwalają administratorom wybierać, którą metodę zastosować.

---

## 📂 Przegląd Struktury Projektu (Kluczowe Pliki i Role)

### 1. `backend/home/recommendation_views.py` – ⚙️ **Główna Logika CF**

Ten plik przetwarza rekomendacje używając **prawdziwego User-Based Collaborative Filtering**:

| Nazwa Funkcji                                     | Co Robi                                                                                                                       |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `process_collaborative_filtering()`               | Buduje macierz użytkownik-produkt i oblicza podobieństwo między **użytkownikami** (nie produktami) używając cosine similarity |
| `generate_user_recommendations_after_order(user)` | Generuje finalne rekomendacje per użytkownik na podstawie wybranego algorytmu                                                 |

**Prawdziwy wzór User-Based CF** zaimplementowany:

```python
# r̂(u,i) = r̄u + (Σ(sim(u,v) × (rv,i - r̄v))) / (Σ|sim(u,v)|)
predicted_rating = user_mean + (numerator / denominator)
```

### 2. `backend/home/signals.py` – 🔁 **Uruchamia CF Po Zamówieniu**

- Automatycznie wywoływane po złożeniu nowego zamówienia
- Przebudowuje reguły asocjacyjne, oblicza prognozy i **uruchamia CF w zależności od ustawień użytkownika**

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

### Prawdziwy Wzór User-Based CF (Resnick & Varian 1997):

```python
def process_collaborative_filtering(self):
    """
    Prawdziwy User-Based Collaborative Filtering
    Reference: Resnick, P., & Varian, H. R. (1997). "Recommender systems"
    """
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    # Buduj macierz user-item
    users = User.objects.all()
    products = Product.objects.all()

    user_item_matrix = []
    user_ids = []

    for user in users:
        user_ratings = []
        user_ids.append(user.id)

        for product in products:
            # Użyj rzeczywistych ocen z Opinion lub ilości z OrderProduct
            rating = 0
            order_items = OrderProduct.objects.filter(order__user=user, product=product)
            if order_items.exists():
                # Normalizuj ilość do skali 1-5
                total_quantity = sum(item.quantity for item in order_items)
                rating = min(5, total_quantity)

            user_ratings.append(rating)

        user_item_matrix.append(user_ratings)

    user_item_matrix = np.array(user_item_matrix)

    # Oblicz podobieństwo użytkowników (nie produktów!)
    user_similarity = cosine_similarity(user_item_matrix)

    # Generuj rekomendacje używając wzoru z literatury
    for i, user1_id in enumerate(user_ids):
        for j, product in enumerate(products):
            if user_item_matrix[i][j] == 0:  # Użytkownik nie kupił tego produktu
                # Wzór Collaborative Filtering:
                # r̂(u,i) = r̄u + (Σ(sim(u,v) × (rv,i - r̄v))) / (Σ|sim(u,v)|)

                numerator = 0
                denominator = 0
                user_mean = np.mean(user_item_matrix[i][user_item_matrix[i] > 0])

                for k, other_user_id in enumerate(user_ids):
                    if k != i and user_item_matrix[k][j] > 0:  # Inny użytkownik kupił produkt
                        other_user_mean = np.mean(user_item_matrix[k][user_item_matrix[k] > 0])
                        similarity = user_similarity[i][k]

                        numerator += similarity * (user_item_matrix[k][j] - other_user_mean)
                        denominator += abs(similarity)

                if denominator > 0:
                    predicted_rating = user_mean + (numerator / denominator)

                    # Zapisz jako rekomendację dla danego użytkownika
                    if predicted_rating > 0:
                        UserProductRecommendation.objects.update_or_create(
                            user_id=user1_id,
                            product=product,
                            recommendation_type="collaborative",
                            defaults={'score': min(5.0, max(0.0, predicted_rating))}
                        )
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

### 1. **Podobieństwo Użytkowników (Cosine Similarity)**:

```python
# Cosine Similarity między użytkownikami u i v:
sim(u,v) = (Σ(ru,i × rv,i)) / (√(Σ(ru,i)²) × √(Σ(rv,i)²))
```

### 2. **Przewidywanie Ocen (User-Based CF)**:

```python
# Przewidywana ocena użytkownika u dla produktu i:
r̂(u,i) = r̄u + (Σ(sim(u,v) × (rv,i - r̄v))) / (Σ|sim(u,v)|)

gdzie:
- r̂(u,i) = przewidywana ocena
- r̄u = średnia ocena użytkownika u
- sim(u,v) = podobieństwo między użytkownikami u i v
- rv,i = ocena użytkownika v dla produktu i
- r̄v = średnia ocena użytkownika v
```

### 3. **Normalizacja Danych**:

```python
# Ilości zamówień normalizowane do skali ocen 1-5:
rating = min(5, total_quantity_purchased)
```

---

## 🔍 Jak Różni Się od Implementacji Błędnej

### ❌ **Błędne Podejście (Poprzednie)**:

- Obliczanie podobieństwa między **produktami** na macierzy user-item
- Używanie MinMax normalizacji per użytkownik
- Product-Based zamiast User-Based CF

### ✅ **Prawdziwe Podejście (Poprawione)**:

- Obliczanie podobieństwa między **użytkownikami**
- Przewidywanie ocen na podstawie podobnych użytkowników
- Implementacja klasycznego wzoru Resnick & Varian (1997)

---

## 📈 Przykład Działania CF

### Scenariusz:

- **Użytkownik A** kupił: [Laptop, Mysz, Klawiatura]
- **Użytkownik B** kupił: [Laptop, Mysz, Monitor]
- **Użytkownik C** kupił: [Telefon, Słuchawki]

### Obliczenia:

1. **Podobieństwo A-B** = wysokie (2/3 wspólne produkty)
2. **Podobieństwo A-C** = niskie (0/3 wspólne produkty)
3. **Rekomendacja dla A**: Monitor (bo podobny użytkownik B go kupił)

### Wzór w Praktyce:

```python
# Dla użytkownika A, produkt Monitor:
r̂(A,Monitor) = r̄A + (sim(A,B) × (rB,Monitor - r̄B)) / |sim(A,B)|
r̂(A,Monitor) = 3.0 + (0.85 × (4 - 3.2)) / 0.85 = 3.0 + 0.8 = 3.8
```

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

| Zdarzenie                       | Regeneruje CF?         | Używa Prawdziwych Wzorów? |
| ------------------------------- | ---------------------- | ------------------------- |
| ✅ Użytkownik składa zamówienie | ✅ Tak (automatycznie) | ✅ Tak (Resnick & Varian) |
| ✅ Admin wybiera CF w panelu    | ✅ Tak (manualnie)     | ✅ Tak (User-Based CF)    |
| ❌ Dodawanie do koszyka         | ❌ Nie                 | -                         |
| ❌ Przeglądanie produktu        | ❌ Nie                 | -                         |

---

## 🔍 Bibliografia

- Resnick, P., Varian, H. R. (1997). "Recommender systems"
- Herlocker, J. L., Konstan, J. A., Riedl, J. (1999). "Algorithmic framework for performing collaborative filtering"
- Sarwar, B., Karypis, G., Konstan, J., Riedl, J. (2001). "Item-based collaborative filtering recommendation algorithms"

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
