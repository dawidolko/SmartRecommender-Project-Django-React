To be corrected: 14/09/2025

# 🔗 Reguły Asocjacyjne - System "Często Kupowane Razem"

## Czym Są "Reguły Asocjacyjne" w Sklepie?

**Reguły asocjacyjne** to algorytm rekomendacji oparty na metodzie **Apriori**, który:

- Identyfikuje produkty, które są **często kupowane razem**
- Pomaga klientom odkrywać **powiązane produkty** podczas zakupów
- Umożliwia administratorom przeglądanie i **zarządzanie tymi relacjami** w panelu
- Używa **prawdziwych wzorów matematycznych** z literatury naukowej (Agrawal & Srikant 1994)

Reguły bazują na **rzeczywistej historii zamówień** i są przeliczane dynamicznie przy nowych zakupach.

---

## 📂 Struktura Projektu - Kluczowe Pliki i Role

### 1. `backend/home/models.py` – 📦 **Model ProductAssociation**

```python
class ProductAssociation(models.Model):
    product_1 = models.ForeignKey(Product, related_name='associations_from', ...)
    product_2 = models.ForeignKey(Product, related_name='associations_to', ...)
    support = models.FloatField()      # Wsparcie - jak często para występuje razem
    confidence = models.FloatField()   # Pewność - prawdopodobieństwo zakupu B gdy kupiono A
    lift = models.FloatField()         # Lift - o ile silniejsza jest reguła niż przypadek
```

Model przechowuje reguły asocjacyjne z **prawdziwymi metrykami Apriori**:

- `support`: Support(A,B) = |A∩B| / |D| (częstość występowania pary)
- `confidence`: Confidence(A→B) = Support(A,B) / Support(A) (pewność reguły)
- `lift`: Lift(A→B) = Confidence(A→B) / Support(B) (siła reguły)

---

### 2. `backend/home/signals.py` – 🔁 **Automatyczne Generowanie Reguł**

Uruchamiane po złożeniu zamówienia:

```python
@receiver(post_save, sender=Order)
def handle_new_order_and_analytics(sender, instance, created, **kwargs):
    ...
    transaction.on_commit(lambda: run_all_analytics_after_order(instance))
```

Wywołuje `generate_association_rules_after_order(order)`, które:

- Czyta wszystkie poprzednie zamówienia
- Ekstraktuje kombinacje produktów (jako transakcje)
- Wywołuje `CustomAssociationRules.generate_association_rules(transactions)`
- Przechowuje wyniki w `ProductAssociation` używając **prawdziwych wzorów**

⮕ Zapewnia **automatyczne aktualizowanie** reguł po każdym nowym zakupie.

---

### 3. `backend/home/custom_recommendation_engine.py` – 🧠 **Obliczanie Reguł**

Klasa `CustomAssociationRules` implementuje **prawdziwy algorytm Apriori**:

```python
def _calculate_support(self, itemset, transactions):
    """
    Wzór Support z literatury (Agrawal & Srikant 1994):
    Support(X) = |transactions containing X| / |total transactions|
    """
    count = 0
    for transaction in transactions:
        if itemset.issubset(set(transaction)):
            count += 1
    return count / len(transactions)

def _calculate_confidence(self, antecedent, consequent, transactions):
    """
    Wzór Confidence z literatury:
    Confidence(X → Y) = Support(X ∪ Y) / Support(X)
    """
    union_support = self._calculate_support(antecedent.union(consequent), transactions)
    antecedent_support = self._calculate_support(antecedent, transactions)

    if antecedent_support == 0:
        return 0
    return union_support / antecedent_support

def _calculate_lift(self, antecedent, consequent, transactions):
    """
    Wzór Lift z literatury (Brin, Motwani, Silverstein 1997):
    Lift(X → Y) = Confidence(X → Y) / Support(Y)
    """
    confidence = self._calculate_confidence(antecedent, consequent, transactions)
    consequent_support = self._calculate_support(consequent, transactions)

    if consequent_support == 0:
        return 0
    return confidence / consequent_support
```

**Algorytm Apriori z optymalizacją bitmap** dla wydajności:

```python
def generate_association_rules(self, transactions):
    """
    Prawdziwy algorytm Apriori z wzorami z literatury
    Reference: Agrawal, R., Srikant, R. (1994) "Fast algorithms for mining association rules"
    """
    # 1. Bitmap pruning dla wydajności
    frequent_itemsets = self._find_frequent_itemsets_with_bitmap(transactions)

    # 2. Generuj reguły używając prawdziwych wzorów
    rules = []
    for itemset, support in frequent_itemsets.items():
        if len(itemset) == 2:  # Skupiamy się na parach produktów
            items = list(itemset)
            item1, item2 = items[0], items[1]

            # Oblicz metryki używając prawdziwych wzorów
            confidence = self._calculate_confidence(
                frozenset([item1]), frozenset([item2]), transactions
            )
            lift = self._calculate_lift(
                frozenset([item1]), frozenset([item2]), transactions
            )

            if confidence >= self.min_confidence:
                rules.append({
                    'product_1': item1,
                    'product_2': item2,
                    'support': support,
                    'confidence': confidence,
                    'lift': lift
                })

    return rules
```

---

### 4. `frontend/src/components/CartContent/CartContent.jsx` – 🛒 **Klient Widzi Rekomendacje**

Gdy użytkownik ma produkty w koszyku:

```js
const response = await axios.get(
  `${config.apiUrl}/api/frequently-bought-together/?${params.toString()}`
);
```

Zwrócone reguły z backendu są używane do wyświetlania:

- Nazwa produktu
- Zdjęcie
- Cena
- **Confidence %** (prawdziwa metryka z algorytmu Apriori)

```jsx
<span>Confidence: {(rec.confidence * 100).toFixed(0)}%</span>
```

---

### 5. `frontend/src/components/AdminPanel/AdminStatistics.jsx` – 📊 **Admin Widzi Wszystkie Reguły**

Panel administracyjny pokazuje wszystkie akttualne reguły z:

```js
fetch(`${config.apiUrl}/api/association-rules/`);
```

Dane są pokazane w tabeli z **prawdziwymi metrykami Apriori**:

- Product 1 & 2
- **Support %** - jak często para występuje
- **Confidence %** - prawdopodobieństwo zakupu B gdy kupiono A
- **Lift** - siła reguły vs. przypadek

Administratorzy mogą też kliknąć "**Update Rules**":

```js
await fetch(`${config.apiUrl}/api/update-association-rules/`);
```

⮕ Uruchamia pełne przeliczenie reguł manualnie.

---

## 🤖 Jak To Działa (Krok po Kroku)

### 🔁 Po Każdym Zamówieniu

1. Użytkownik finalizuje zamówienie → `/api/orders/`
2. Django `signals.py` wykrywa nowe `Order`
3. `run_all_analytics_after_order()` się uruchamia
4. `generate_association_rules_after_order()` buduje transakcje
5. `CustomAssociationRules.generate_association_rules()` używa **prawdziwych wzorów Apriori**
6. Wyniki zapisane w tabeli `ProductAssociation` z metrykami support/confidence/lift

### 🛒 Na Stronie Koszyka

1. Produkty w koszyku wykryte w `CartContent.jsx`
2. `GET /api/frequently-bought-together/?product_ids=...`
3. Zwracane są top powiązane produkty (na podstawie `confidence`)
4. Pokazane pod **"Frequently Bought Together"** z prawdziwymi metrykami

### 👨‍💼 W Panelu Admin

1. Admin otwiera `AdminStatistics.jsx`
2. Dane pobrane z `/api/association-rules/`
3. Tabela wyświetla wszystkie reguły z **prawdziwymi metrykami Apriori**
4. Admin może kliknąć **Update Rules** (manualne odświeżenie)

---

## 📊 Prawdziwe Wzory Matematyczne Używane

### Wzory z Literatury Naukowej:

```
Support(A,B) = |transactions containing both A and B| / |total transactions|

Confidence(A→B) = Support(A,B) / Support(A)

Lift(A→B) = Confidence(A→B) / Support(B)

Conviction(A→B) = (1 - Support(B)) / (1 - Confidence(A→B))
```

### Interpretacja Metryk:

- **Support = 0.05** → Para występuje w 5% transakcji
- **Confidence = 0.80** → Jeśli kupiono A, to B kupowane w 80% przypadków
- **Lift = 2.5** → Reguła jest 2.5x silniejsza niż przypadek
- **Lift > 1** → Pozytywna korelacja, **Lift < 1** → Negatywna korelacja

---

## 🔬 Optymalizacje Algorytmiczne

### Bitmap Pruning:

```python
# Konwersja transakcji na bitmapy dla szybkich operacji
for transaction in transactions:
    bitmap = 0
    for item in transaction:
        if item in item_to_id:
            bitmap |= (1 << item_to_id[item])
    transaction_bitmaps.append(bitmap)

# Szybkie sprawdzanie czy para występuje razem
count = 0
for transaction_bitmap in transaction_bitmaps:
    if (transaction_bitmap & pair_bitmap) == pair_bitmap:
        count += 1
```

### Bulk Operations:

- `bulk_create()` dla wydajności bazy danych
- Caching wyników z timeout
- Ograniczenie do max 1000 reguł dla UI

---

## 📌 Czy To Jest Losowe?

**NIE - to nie jest losowe.**

Reguły asocjacyjne są **w pełni oparte na danych**. Bazują na:

- Rzeczywistych wpisach `Order` i `OrderProduct`
- Wszystkie historyczne transakcje są przetwarzane
- Brak `random.uniform()` czy sztucznego generowania
- **Prawdziwy algorytm eksploracji asocjacji** (styl Apriori)
- Wzory matematyczne z literatury naukowej (Agrawal & Srikant 1994)

---

## ✅ Podsumowanie Kluczowych Plików i Ich Roli

| Plik                                                       | Rola                                                                 |
| ---------------------------------------------------------- | -------------------------------------------------------------------- |
| `models.py → ProductAssociation`                           | Przechowuje rzeczywiste dane reguł asocjacyjnych z metrykami Apriori |
| `custom_recommendation_engine.py → CustomAssociationRules` | Implementuje prawdziwe wzory Support, Confidence, Lift               |
| `signals.py → run_all_analytics_after_order()`             | Uruchamia generowanie reguł po złożeniu zamówienia                   |
| `signals.py → generate_association_rules_after_order()`    | Główna logika obliczająca relacje między produktami                  |
| `CartContent.jsx`                                          | Pokazuje sugestie "Frequently Bought Together"                       |
| `AdminStatistics.jsx`                                      | Pozwala adminowi przeglądać i regenerować reguły asocjacyjne         |
| API Endpoints                                              | `/api/frequently-bought-together/`, `/api/update-association-rules/` |

---

## 🚀 Co Jest Dynamiczne? Co Jest Manualne?

| Zdarzenie                        | Regeneruje Reguły?     | Używa Prawdziwych Wzorów? |
| -------------------------------- | ---------------------- | ------------------------- |
| ✅ Użytkownik składa zamówienie  | ✅ Tak (automatycznie) | ✅ Tak (Apriori)          |
| ✅ Admin klika "Update"          | ✅ Tak (manualnie)     | ✅ Tak (Apriori)          |
| ❌ Dodawanie produktu do koszyka | ❌ Nie                 | -                         |
| ❌ Przeglądanie strony produktu  | ❌ Nie                 | -                         |

---

## 🔍 Bibliografia

- Agrawal, R., Srikant, R. (1994). "Fast algorithms for mining association rules in large databases"
- Brin, S., Motwani, R., Silverstein, C. (1997). "Beyond market baskets: Generalizing association rules to correlations"
- Tan, P., Steinbach, M., Kumar, V. (2005). "Introduction to Data Mining" - rozdział Association Rules
