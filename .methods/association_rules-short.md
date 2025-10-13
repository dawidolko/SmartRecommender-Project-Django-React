# 🔗 Reguły Asocjacyjne - Jak Działa w Projekcie

## 📋 **Czym Jest Ta Metoda?**

**Reguły asocjacyjne** (Association Rules) to algorytm **Apriori** (Agrawal & Srikant, 1994), który analizuje historię zamówień i znajduje produkty często kupowane razem.

**Przykład:** Jeśli 80% klientów kupujących laptopa kupuje też mysz, system rekomenduje mysz przy laptopie.

---

## 🔄 **Jak To Działa - Przepływ Danych**

### **1. Baza Danych (PostgreSQL)**

```sql
-- Tabela przechowująca reguły
ProductAssociation {
  product_1_id: 123,        -- Produkt A
  product_2_id: 456,        -- Produkt B
  support: 0.05,            -- 5% transakcji ma oba
  confidence: 0.8,          -- 80% pewność
  lift: 3.2                 -- 3.2x silniejsza korelacja
}
```

### **2. Backend - Algorytm Apriori**

**Plik:** custom_recommendation_engine.py

#### **Krok 1: Znajdź częste itemsety (produkty kupowane razem)**

```python
def _find_frequent_itemsets_with_bitmap(transactions):
    """
    Wzór: Support(X) = count(X) / total_transactions
    Źródło: Agrawal & Srikant (1994)
    """
    # 1. Zlicz pojedyncze produkty
    for transaction in transactions:
        item_counts[item] += 1

    # 2. Filtruj przez min_support (np. 0.5% = pojawia się w min 0.5% zamówień)
    frequent_1_itemsets = [item for item, count in item_counts.items()
                           if count / total >= min_support]

    # 3. Generuj pary (2-itemsets) z optymalizacją bitmap
    return _generate_2_itemsets_with_bitmap(frequent_1_itemsets, transactions)
```

**Optymalizacja Bitmap (Zaki, 2000):**

```python
# Zamiast zagnieżdżonych pętli, użyj operacji bitowych
bitmap = 0
for item in transaction:
    bitmap |= (1 << item_to_id[item])  # Ustaw bit na pozycji item_id

# Sprawdź czy para występuje: O(1) zamiast O(n)
if (transaction_bitmap & pair_bitmap) == pair_bitmap:
    pair_count += 1
```

#### **Krok 2: Oblicz metryki reguł**

```python
def _generate_optimized_rules_from_itemsets(itemsets, transactions):
    """
    Wzory (Agrawal 1994, Brin 1997):
    """
    for (item1, item2), support_ab in itemsets.items():
        support_a = support_counts[item1]
        support_b = support_counts[item2]

        # Confidence(A→B) = Support(A,B) / Support(A)
        confidence = support_ab / support_a

        # Lift(A→B) = Support(A,B) / (Support(A) × Support(B))
        lift = support_ab / (support_a * support_b)

        # Filtruj przez progi
        if confidence >= min_confidence and lift >= min_lift:
            save_rule(item1, item2, support_ab, confidence, lift)
```

### **3. Automatyczna Aktualizacja (Django Signals)**

**Plik:** signals.py

```python
@receiver(post_save, sender=Order)
def update_association_rules_after_order(sender, instance, created, **kwargs):
    """Automatycznie przelicza reguły po każdym nowym zamówieniu"""
    if created and instance.ordered:
        transactions = get_all_transactions()  # Pobierz całą historię
        engine = CustomAssociationRules(min_support=0.005, min_confidence=0.05)
        rules = engine.generate_association_rules(transactions)
        save_to_database(rules)  # Bulk insert (500 rekordów na raz)
```

### **4. API Backend (Django REST)**

**Plik:** association_views.py

```python
# Endpoint dla koszyka
@api_view(['GET'])
def frequently_bought_together(request):
    product_ids = request.GET.getlist('product_ids[]')

    # Pobierz reguły dla produktów w koszyku
    rules = ProductAssociation.objects.filter(
        antecedent__in=product_ids
    ).order_by('-lift', '-confidence')[:5]  # Top 5 najlepszych

    return Response(rules)
```

### **5. Frontend - Koszyk (React)**

**Plik:** CartContent.jsx

```jsx
const fetchRecommendations = async () => {
  const productIds = Object.keys(items); // [123, 456]

  const response = await axios.get(
    `/api/frequently-bought-together/?product_ids[]=${productIds.join(
      "&product_ids[]="
    )}`
  );

  setRecommendations(response.data); // Wyświetl "Frequently Bought Together"
};

useEffect(() => {
  fetchRecommendations();
}, [items]); // Odśwież gdy koszyk się zmieni
```

### **6. Frontend - Admin Panel (React)**

**Plik:** AdminStatistics.jsx

```jsx
// Admin klika "Update Rules"
const updateAssociationRules = async () => {
  await axios.post("/api/update-association-rules/", {
    headers: { Authorization: `Bearer ${token}` },
  });

  fetchAssociationRules(); // Odśwież tabelę (cache-busting: ?t=${Date.now()})
};
```

---

## 📊 **Wzory Matematyczne**

### **1. Support (Wsparcie)**

```
Support(A,B) = count(transactions zawierających A i B) / total_transactions

Przykład: 3 zamówienia z 200 mają laptop+mysz
Support = 3/200 = 0.015 = 1.5%
```

### **2. Confidence (Pewność)**

```
Confidence(A→B) = Support(A,B) / Support(A)

Przykład:
- Support(laptop, mysz) = 0.015
- Support(laptop) = 0.05 (5% zamówień ma laptop)
Confidence = 0.015 / 0.05 = 0.3 = 30%

Interpretacja: 30% kupujących laptop kupuje też mysz
```

### **3. Lift (Siła Korelacji)**

```
Lift(A→B) = Support(A,B) / (Support(A) × Support(B))

Przykład:
- Support(laptop, mysz) = 0.015
- Support(laptop) = 0.05
- Support(mysz) = 0.02
Lift = 0.015 / (0.05 × 0.02) = 15.0

Interpretacja:
- Lift = 1.0  → produkty niezależne (losowość)
- Lift > 1.0  → pozytywna korelacja (kupowane razem)
- Lift = 15.0 → produkty kupowane 15x częściej niż losowo!
```

---

## 🚀 **Przykład w Praktyce**

### **Scenariusz:**

1. Klient dodaje **Laptop ASUS** (ID: 295) do koszyka
2. System pobiera reguły: `GET /api/frequently-bought-together/?product_ids[]=295`
3. Backend zwraca:

```json
[
  {
    "product_2": { "id": 203, "name": "Huzaro Hero 5.0 Red" },
    "support": 0.006, // 0.6% transakcji
    "confidence": 1.0, // 100% pewność
    "lift": 165.0 // 165x silniejsza korelacja!
  },
  {
    "product_2": { "id": 471, "name": "Orico Hub USB-C" },
    "support": 0.006,
    "confidence": 1.0,
    "lift": 82.5
  }
]
```

4. Frontend wyświetla w koszyku:

```
┌─────────────────────────────────────┐
│ Frequently Bought Together          │
├─────────────────────────────────────┤
│ 🪑 Huzaro Hero 5.0 Red              │
│ Confidence: 100% | Lift: 165.00x    │
│ [Add to Cart]                       │
├─────────────────────────────────────┤
│ 🔌 Orico Hub USB-C                  │
│ Confidence: 100% | Lift: 82.50x     │
│ [Add to Cart]                       │
└─────────────────────────────────────┘
```

---

## ⚙️ **Optymalizacje**

### **1. Bitmap Pruning (Zaki, 2000)**

```python
# Zamiast zagnieżdżonych pętli O(n²):
for transaction in transactions:
    for pair in pairs:
        if pair[0] in transaction and pair[1] in transaction:
            count += 1

# Używamy bitmap O(n):
bitmap = sum(1 << item_id for item in transaction)
if (bitmap & pair_bitmap) == pair_bitmap:
    count += 1
```

**Przyspieszenie:** 10-50x na dużych datasetach

### **2. Bulk Insert**

```python
ProductAssociation.objects.bulk_create(rules[:500])  # 500 rekordów naraz
```

### **3. Cache**

```python
@cache_page(60 * 15)  # Cache na 15 minut
def association_rules(request):
    ...
```

---

## 📚 **Źródła Naukowe**

1. **Agrawal, R., Srikant, R. (1994)**  
   _"Fast algorithms for mining association rules"_  
   VLDB Conference  
   → Oryginalny algorytm Apriori

2. **Brin, S., Motwani, R., Silverstein, C. (1997)**  
   _"Beyond market baskets: Generalizing association rules to correlations"_  
   ACM SIGMOD  
   → Metryka Lift

3. **Zaki, M. J. (2000)**  
   _"Scalable algorithms for association mining"_  
   IEEE TKDE  
   → Optymalizacja bitmap

---

## 🎯 **Podsumowanie**

| Komponent    | Technologia      | Rola                                      |
| ------------ | ---------------- | ----------------------------------------- |
| **Baza**     | PostgreSQL       | Przechowuje reguły (`ProductAssociation`) |
| **Algorytm** | Python (Apriori) | Oblicza Support/Confidence/Lift           |
| **Backend**  | Django REST      | API endpoints + Django Signals            |
| **Frontend** | React            | Koszyk + Admin Panel                      |
| **Cache**    | Django Cache     | Przyspiesza odczyt (15 min TTL)           |

**Przepływ:**

1. Klient składa zamówienie → **Signal** → Przelicz reguły
2. Klient dodaje do koszyka → **API** → Pokaż rekomendacje
3. Admin klika "Update Rules" → **API** → Wymuś przeliczenie

---

## 🔍 **Kluczowe Odkrycie: Dlaczego 165, Nie 200?**

### **Problem:**

Algorytm używa 165 transakcji, ale w bazie jest 200 zamówień. Dlaczego?

### **Odpowiedź:**

```python
# W seederze (seed.py, linia 16776):
num_products = random.randint(1, 5)  # Losuje 1-5 produktów

# Rezultat:
# - 35 zamówień (17.5%) ma tylko 1 produkt → WYKLUCZANE
# - 165 zamówień (82.5%) ma 2+ produkty → UŻYWANE

# W algorytmie (custom_recommendation_engine.py, linia 488-490):
if len(limited_transaction) >= 2:  # ← FILTRUJE!
    filtered_transactions.append(limited_transaction)
```

### **Dlaczego to ważne:**

**Reguły asocjacyjne** szukają produktów **kupowanych RAZEM**. Zamówienie z tylko 1 produktem nie ma sensu w tym kontekście.

### **Przykład obliczeń:**

```
Product 100: AMD Ryzen 5 8600G (występuje w 2 zamówieniach)
Product 358: DJI Hub (występuje w 2 zamówieniach, ale 1 ma tylko 1 produkt!)

POPRAWNE obliczenia (algorytm):
Support(100) = 2/165 = 0.0121
Support(358) = 1/165 = 0.0061  (Order #97 z 1 produktem WYKLUCZONY!)
Support(100,358) = 1/165 = 0.0061
Lift = 0.0061 / (0.0121 × 0.0061) = 82.5 ✅

BŁĘDNE obliczenia (gdyby używać 200):
Support(100) = 2/200 = 0.01
Support(358) = 2/200 = 0.01  (Błąd: liczył Order #97!)
Support(100,358) = 1/200 = 0.005
Lift = 0.005 / (0.01 × 0.01) = 50.0 ❌
```

**Weryfikacja:**

```bash
cd backend
python3 find_single_product_orders.py  # Pokaże 35 wykluczonych zamówień
python3 manage.py shell < shell_verify_apriori.py  # Zweryfikuje obliczenia
```

---

## 🧪 **Testowanie**

### **1. Skrypty Python:**

```bash
# Analiza zamówień (165 vs 200)
python3 find_single_product_orders.py

# Weryfikacja obliczeń Lift
python3 manage.py shell < shell_verify_apriori.py
```

### **2. Debug API:**

```bash
curl "http://localhost:8000/api/product-association-debug/?product_id=100"
```

Zwróci:

- Statystyki: 200 zamówień, 35 wykluczonych, 165 używanych
- Listę zamówień z danymi użytkowników
- Weryfikację wzorów matematycznych
- Wyjaśnienie zachowania algorytmu

### **3. Django Shell:**

```python
from home.models import Order, ProductAssociation
from django.db.models import Count

# Sprawdź rozkład
multi = Order.objects.annotate(
    product_count=Count('orderproduct')
).filter(product_count__gte=2).count()
print(f"Multi-product orders: {multi}")  # 165

# Sprawdź reguły
rules = ProductAssociation.objects.filter(product_1_id=100)
for rule in rules:
    print(f"{rule.product_1.name} → {rule.product_2.name}")
    print(f"  Lift: {rule.lift:.2f}x")
```

---

## 📚 **Źródła**

https://www-users.cse.umn.edu/~kumar001/dmbook/ch6.pdf
