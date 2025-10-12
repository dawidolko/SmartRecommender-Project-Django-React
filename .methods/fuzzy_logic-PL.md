Ostatnia aktualizacja: 12/10/2025

# 🌐 Logika Rozmyta (Fuzzy Logic) w Rekomendacjach Produktów

## Czym Jest "Logika Rozmyta" w Sklepie?

**Logika rozmyta (Fuzzy Logic)** to algorytm rekomendacji, który:

- **Modeluje niepewność** w preferencjach użytkowników - zamiast "TAK/NIE" używa stopni przynależności (0.0 - 1.0)
- Wykorzystuje **funkcje przynależności** (membership functions) do opisania rozmytych pojęć jak "tani", "dobry", "popularny"
- Implementuje **silnik wnioskowania rozmytego** (Fuzzy Inference Engine) w stylu Mamdani
- Używa **6 reguł rozmytych** (IF-THEN) do oceny produktów
- Tworzy **profile użytkowników** na podstawie historii zakupów
- Oblicza **podobieństwo hierarchiczne kategorii** z wagami
- **Implementacja manualna** bez gotowych bibliotek - zgodnie z wymaganiami pracy inżynierskiej

Metoda bazuje na pracach:
- **Zadeh, L. A. (1965)** - "Fuzzy sets" (teoria zbiorów rozmytych)
- **Mamdani, E. H. (1975)** - "Application of fuzzy algorithms" (wnioskowanie rozmyte)

---

## 📂 Struktura Projektu - Kluczowe Pliki i Role

### 1. `backend/home/fuzzy_logic_engine.py` – 🧠 **Główny Silnik Rozmyty**

Plik zawiera 3 kluczowe klasy:

1. **`FuzzyMembershipFunctions`** (linie 19-230) - Funkcje przynależności
2. **`FuzzyUserProfile`** (linie 232-482) - Profil rozmyty użytkownika
3. **`SimpleFuzzyInference`** (linie 484-710) - Silnik wnioskowania

---

## 🔢 CZĘŚĆ I: Funkcje Przynależności (Membership Functions)

### Klasa `FuzzyMembershipFunctions` (linie 19-230)

**Parametry konfiguracyjne (linie 27-43):**

```python
class FuzzyMembershipFunctions:
    def __init__(self):
        # Progi cenowe (w PLN)
        self.price_low = 100          # Granica "tanich" produktów
        self.price_mid_low = 500      # Początek "średniej półki"
        self.price_mid = 700          # Środek "średniej półki"
        self.price_mid_high = 1200    # Początek "drogich"
        self.price_high = 2000        # Granica "premium"

        # Progi ocen (skala 0-5)
        self.rating_low = 2.5         # Słabe oceny
        self.rating_mid = 3.5         # Średnie oceny
        self.rating_high = 4.5        # Dobre oceny

        # Progi popularności (liczba zamówień)
        self.pop_low = 2              # Mało popularne
        self.pop_mid = 10             # Średnio popularne
        self.pop_high = 30            # Bardzo popularne
```

**Dlaczego te progi?**
- Oparte na rzeczywistych danych z bazy (ceny produktów: 50-5000 PLN)
- Dostosowane do liczby zamówień (większość produktów ma 0-15 zamówień)
- Progi ocen odpowiadają intuicji (2.5 = słabe, 3.5 = OK, 4.5 = świetne)

---

### 1.1. Funkcje Przynależności dla CENY

#### **Funkcja: `mu_price_cheap()` - "Tani" Produkt**

**Lokalizacja:** `backend/home/fuzzy_logic_engine.py`, linie 47-68

```python
def mu_price_cheap(self, price):
    """
    Trójkątna funkcja przynależności dla 'taniej' ceny.

    μ(price) = {
        1.0                         if price <= 100
        (500 - price) / 400         if 100 < price < 500
        0.0                         if price >= 500
    }
    """
    if price <= self.price_low:
        return 1.0
    elif price < self.price_mid_low:
        return (self.price_mid_low - price) / (self.price_mid_low - self.price_low)
    else:
        return 0.0
```

**Wzór matematyczny (Triangular Membership Function):**

```
         μ
        1.0 |     ╱╲
            |    ╱  ╲
        0.5 |   ╱    ╲
            |  ╱      ╲
        0.0 |─────────────────> price (PLN)
            0   100  500

Wzór:
         ⎧  1.0                     jeśli x ≤ a
μ(x) =   ⎨  (b - x) / (b - a)      jeśli a < x < b
         ⎩  0.0                     jeśli x ≥ b

gdzie: a = 100, b = 500
```

**Przykład obliczenia:**

```
Produkt A: cena = 50 PLN
  μ_cheap(50) = 1.0
  Interpretacja: "Produkt jest w 100% tani"

Produkt B: cena = 300 PLN
  μ_cheap(300) = (500 - 300) / (500 - 100)
                = 200 / 400
                = 0.5
  Interpretacja: "Produkt jest w 50% tani"

Produkt C: cena = 600 PLN
  μ_cheap(600) = 0.0
  Interpretacja: "Produkt nie jest tani"
```

---

#### **Funkcja: `mu_price_medium()` - "Średnia" Cena**

**Lokalizacja:** `backend/home/fuzzy_logic_engine.py`, linie 70-91

```python
def mu_price_medium(self, price):
    """
    Trapezoidalna funkcja przynależności dla 'średniej' ceny.

    μ(price) = {
        0.0                         if price < 300
        (price - 300) / 200         if 300 <= price < 500
        1.0                         if 500 <= price <= 1200
        (1500 - price) / 300        if 1200 < price < 1500
        0.0                         if price >= 1500
    }
    """
    if price < 300:
        return 0.0
    elif price < self.price_mid_low:
        return (price - 300) / (self.price_mid_low - 300)
    elif price <= self.price_mid_high:
        return 1.0
    elif price < 1500:
        return (1500 - price) / (1500 - self.price_mid_high)
    else:
        return 0.0
```

**Wzór matematyczny (Trapezoidal Membership Function):**

```
         μ
        1.0 |      ╱‾‾‾‾╲
            |     ╱      ╲
        0.5 |    ╱        ╲
            |   ╱          ╲
        0.0 |──────────────────> price (PLN)
            0  300 500  1200 1500

Wzór:
         ⎧  0.0                     jeśli x < a
         ⎪  (x - a) / (b - a)       jeśli a ≤ x < b
μ(x) =   ⎨  1.0                     jeśli b ≤ x ≤ c
         ⎪  (d - x) / (d - c)       jeśli c < x < d
         ⎩  0.0                     jeśli x ≥ d

gdzie: a = 300, b = 500, c = 1200, d = 1500
```

**Dlaczego trapez zamiast trójkąta?**

Trapezoidalna funkcja ma **płaski szczyt** (plateau), co oznacza:
- Ceny od 500 do 1200 PLN są **w pełni "średnie"** (μ = 1.0)
- Nie ma sztucznego spadku w środku przedziału
- Lepiej modeluje naturalną kategorię "średnia półka cenowa"

---

#### **Funkcja: `mu_price_expensive()` - "Drogi" Produkt**

**Lokalizacja:** `backend/home/fuzzy_logic_engine.py`, linie 93-108

```python
def mu_price_expensive(self, price):
    """
    Trójkątna funkcja przynależności dla 'drogiej' ceny.

    μ(price) = {
        0.0                         if price <= 1000
        (price - 1000) / 1000       if 1000 < price < 2000
        1.0                         if price >= 2000
    }
    """
    if price <= 1000:
        return 0.0
    elif price < self.price_high:
        return (price - 1000) / (self.price_high - 1000)
    else:
        return 1.0
```

**Przykład kompletnego zbioru rozmytego dla ceny:**

```
Produkt: Cena = 800 PLN

μ_cheap(800) = 0.0       (nie jest tani)
μ_medium(800) = 1.0      (jest w pełni średnio-cenowy)
μ_expensive(800) = 0.0   (nie jest drogi)

Rozmyty zbiór ceny = {cheap: 0.0, medium: 1.0, expensive: 0.0}

Interpretacja: "Produkt za 800 PLN jest w 100% średniej ceny"
```

---

### 1.2. Funkcje Przynależności dla JAKOŚCI (Ocen)

#### **Funkcja: `mu_quality_high()` - "Wysoka Jakość"**

**Lokalizacja:** `backend/home/fuzzy_logic_engine.py`, linie 146-163

```python
def mu_quality_high(self, rating):
    """
    Funkcja przynależności dla 'wysokiej jakości' (doskonałe oceny).

    μ(rating) = {
        0.0                         if rating < 3.5
        (rating - 3.5) / 1.0        if 3.5 ≤ rating < 4.5
        1.0                         if rating ≥ 4.5
    }

    Modeluje niepewność: ocena 4.0 jest "częściowo" wysoką jakością (μ=0.5)
    """
    if rating < self.rating_mid:
        return 0.0
    elif rating < self.rating_high:
        return (rating - self.rating_mid) / (self.rating_high - self.rating_mid)
    else:
        return 1.0
```

**Przykład obliczenia:**

```
Produkt A: rating = 4.8
  μ_high(4.8) = 1.0
  Interpretacja: "Produkt ma w 100% wysoką jakość"

Produkt B: rating = 4.0
  μ_high(4.0) = (4.0 - 3.5) / (4.5 - 3.5)
                = 0.5 / 1.0
                = 0.5
  Interpretacja: "Produkt ma w 50% wysoką jakość"

Produkt C: rating = 3.2
  μ_high(3.2) = 0.0
  Interpretacja: "Produkt nie ma wysokiej jakości"
```

**Dlaczego to jest lepsze niż klasyczna logika?**

Klasyczna logika (Boolean):
```
IF rating >= 4.5 THEN "dobry produkt"
ELSE "zły produkt"
```
Problem: Ocena 4.49 → "zły", ocena 4.50 → "dobry" (sztuczna granica!)

Logika rozmyta:
```
rating = 4.0 → μ_high = 0.5 (częściowo dobry)
rating = 4.5 → μ_high = 1.0 (w pełni dobry)
```
Stopniowe przejście, brak sztucznych granic.

---

### 1.3. Funkcje Przynależności dla POPULARNOŚCI

#### **Funkcja: `mu_popularity_medium()` - "Średnia Popularność"**

**Lokalizacja:** `backend/home/fuzzy_logic_engine.py`, linie 176-189

```python
def mu_popularity_medium(self, view_count):
    """
    Trapezoidalna funkcja przynależności dla 'średniej' popularności.

    Pełna przynależność przy pop_low do pop_mid, potem maleje do pop_high.
    """
    if view_count < self.pop_low:
        return 0.0
    elif view_count <= self.pop_mid:
        return 1.0
    elif view_count < self.pop_high:
        return (self.pop_high - view_count) / (self.pop_high - self.pop_mid)
    else:
        return 0.0
```

**Przykład:**

```
Produkt ma 5 zamówień:
  μ_low(5) = 0.375         (trochę mało popularne)
  μ_medium(5) = 1.0        (w pełni średnio popularne)
  μ_high(5) = 0.0          (nie jest bardzo popularne)

Rozmyty zbiór popularności = {low: 0.375, medium: 1.0, high: 0.0}
```

---

## 👤 CZĘŚĆ II: Profile Rozmyte Użytkowników

### Klasa `FuzzyUserProfile` (linie 232-482)

**Zadanie:** Buduje rozmyty profil użytkownika na podstawie historii zakupów.

**Inicjalizacja (linie 240-258):**

```python
class FuzzyUserProfile:
    def __init__(self, user=None, session_data=None):
        self.user = user
        self.session_data = session_data or {}
        self.category_interests = {}        # Dict[str, float] - zainteresowania kategoriami
        self.price_sensitivity = 0.5        # Domyślnie: średnia wrażliwość na cenę

        # Budowa profilu
        if user and user.is_authenticated:
            self._build_from_user_history()
        elif session_data:
            self._build_from_session()
        else:
            self._build_default_profile()
```

---

### 2.1. Budowa Profilu z Historii Zakupów

**Funkcja: `_build_from_user_history()`**

**Lokalizacja:** `backend/home/fuzzy_logic_engine.py`, linie 259-311

```python
def _build_from_user_history(self):
    """
    Buduje rozmyty profil z historii zakupów zalogowanego użytkownika.

    Używa częstości zakupów kategorii do określenia rozmytych stopni przynależności.
    """
    from home.models import Order

    # Pobierz zamówienia użytkownika
    orders = Order.objects.filter(user=self.user).prefetch_related(
        "orderproduct_set__product__categories"
    )

    if not orders.exists():
        self._build_default_profile()
        return

    # Zlicz zakupy w kategoriach
    category_counts = defaultdict(int)
    total_items = 0
    total_spending = 0

    for order in orders:
        for order_product in order.orderproduct_set.all():
            product = order_product.product
            quantity = order_product.quantity

            # Zlicz kategorie
            for category in product.categories.all():
                category_counts[category.name] += quantity

            total_items += quantity
            total_spending += float(product.price) * quantity

    # Normalizuj do [0, 1] - rozmyte stopnie przynależności
    if total_items > 0:
        self.category_interests = {
            cat: count / total_items
            for cat, count in category_counts.items()
        }

    # Oblicz wrażliwość na cenę
    if orders.count() > 0:
        avg_price = total_spending / total_items if total_items > 0 else 500

        # Niska średnia cena → wysoka wrażliwość (1.0)
        # Wysoka średnia cena → niska wrażliwość (0.0)
        if avg_price < 300:
            self.price_sensitivity = 0.9
        elif avg_price < 700:
            self.price_sensitivity = 0.6
        elif avg_price < 1500:
            self.price_sensitivity = 0.4
        else:
            self.price_sensitivity = 0.2
```

**Wzór matematyczny dla zainteresowań kategoriami:**

```
μ_interest(kategoria) = liczba_zakupów_w_kategorii / suma_wszystkich_zakupów

Przykład:
Użytkownik kupił:
  - 5 produktów z kategorii "Electronics"
  - 3 produkty z kategorii "Components"
  - 2 produkty z kategorii "Peripherals"
  Suma: 10 produktów

Rozmyte zainteresowania:
  μ_interest(Electronics) = 5/10 = 0.5  (50% zainteresowania)
  μ_interest(Components) = 3/10 = 0.3   (30% zainteresowania)
  μ_interest(Peripherals) = 2/10 = 0.2  (20% zainteresowania)
```

**Wzór dla wrażliwości na cenę:**

```
                    ⎧  0.9   jeśli avg_price < 300
                    ⎪  0.6   jeśli 300 ≤ avg_price < 700
price_sensitivity = ⎨  0.4   jeśli 700 ≤ avg_price < 1500
                    ⎩  0.2   jeśli avg_price ≥ 1500

Interpretacja:
- 0.9 = bardzo wrażliwy na cenę (kupuje tanie rzeczy)
- 0.2 = mało wrażliwy na cenę (kupuje drogie rzeczy)
```

**Przykład rzeczywisty:**

```
Użytkownik: client1@example.com

Historia zamówień:
  Order #1:
    - AMD Ryzen 7 5800X3D (1899 PLN) x1, kategoria: Components
    - ASUS ROG STRIX B550-F (850 PLN) x1, kategoria: Components
  Order #2:
    - Corsair Vengeance RGB 16GB (400 PLN) x2, kategoria: Components
  Order #3:
    - Samsung 970 EVO SSD (350 PLN) x1, kategoria: Components

Obliczenia:
  Suma produktów: 5
  Wszystkie w kategorii "Components"

  category_interests = {
      "Components": 5/5 = 1.0
  }

  total_spending = 1899 + 850 + (400×2) + 350 = 3899 PLN
  avg_price = 3899 / 5 = 779.8 PLN

  price_sensitivity = 0.4  (średnia wrażliwość, bo avg_price ∈ [700, 1500))

Profil rozmyty:
  - Użytkownik jest w 100% zainteresowany "Components"
  - Wrażliwość na cenę: 0.4 (średnia, kupuje produkty średnio-drogie)
```

---

### 2.2. Dopasowanie Kategorii - Hierarchiczne Podobieństwo

**Funkcja: `fuzzy_category_match()`**

**Lokalizacja:** `backend/home/fuzzy_logic_engine.py`, linie 376-402

```python
def fuzzy_category_match(self, product_category):
    """
    Rozmyte dopasowanie między zainteresowaniami użytkownika a kategorią produktu.

    Używa ważonej kombinacji zainteresowania użytkownika i podobieństwa kategorii
    aby zapewnić lepsze różnicowanie między produktami.

    Returns:
        Stopień przynależności [0.0, 1.0] reprezentujący jak dobrze kategoria pasuje
    """
    max_match = 0.0

    for user_cat, user_interest in self.category_interests.items():
        # Oblicz rozmyte podobieństwo między kategoriami
        similarity = self._calculate_category_similarity(user_cat, product_category)

        # Kombinacja ważona (60% podobieństwo, 40% zainteresowanie)
        # Daje większą wagę podobieństwu kategorii, uwzględniając zainteresowanie użytkownika
        match = (similarity * 0.6) + (user_interest * 0.4)

        # T-konorma (max) dla OR: akumuluj najlepsze dopasowanie
        max_match = max(max_match, match)

    return max_match
```

**Dlaczego ważona kombinacja zamiast T-normy (min)?**

Problem z czystym T-norm:
```
user_interest = 0.148
similarity = 0.7

T-norm (min): min(0.148, 0.7) = 0.148

Wynik: WSZYSTKIE produkty tech mają category_match = 0.148 (bottleneck!)
```

Rozwiązanie - ważona kombinacja:
```
match = (0.7 × 0.6) + (0.148 × 0.4)
      = 0.42 + 0.059
      = 0.479

Wynik: Różne produkty mają RÓŻNE wyniki (0.3 - 0.6)
```

---

**Funkcja: `_calculate_category_similarity()` - Hierarchiczne Podobieństwo**

**Lokalizacja:** `backend/home/fuzzy_logic_engine.py`, linie 404-469

```python
def _calculate_category_similarity(self, cat1, cat2):
    """
    Oblicza rozmyte podobieństwo między dwiema kategoriami z hierarchicznym dopasowaniem.

    Używa notacji kropkowej hierarchii (np. 'electronics.phones'):
    - Dokładne dopasowanie: 1.0
    - Ta sama główna + podkategoria: 0.85-0.95
    - Ta sama główna, inna podkategoria: 0.5-0.7
    - Powiązane kategorie: 0.3-0.5
    - Niepowiązane: 0.1-0.2
    """
    cat1_lower = cat1.lower()
    cat2_lower = cat2.lower()

    # Dokładne dopasowanie
    if cat1_lower == cat2_lower:
        return 1.0

    # Sprawdź substring match
    if cat1_lower in cat2_lower or cat2_lower in cat1_lower:
        return 0.85

    # Parsuj strukturę hierarchiczną (np. "electronics.phones")
    cat1_parts = cat1_lower.split('.')
    cat2_parts = cat2_lower.split('.')

    cat1_main = cat1_parts[0] if cat1_parts else cat1_lower
    cat2_main = cat2_parts[0] if cat2_parts else cat2_lower
    cat1_sub = cat1_parts[1] if len(cat1_parts) > 1 else None
    cat2_sub = cat2_parts[1] if len(cat2_parts) > 1 else None

    # Ta sama główna kategoria
    if cat1_main == cat2_main:
        if cat1_sub and cat2_sub:
            return 0.95 if cat1_sub == cat2_sub else 0.6
        return 0.7

    # Zdefiniuj relacje między kategoriami
    relations = {
        'electronics': ['components', 'peripherals', 'wearables'],
        'components': ['electronics', 'peripherals', 'gaming'],
        'peripherals': ['components', 'accessories', 'gaming'],
        'accessories': ['peripherals', 'power', 'office'],
        'gaming': ['components', 'peripherals', 'computers'],
        'computers': ['components', 'gaming', 'laptops'],
        'laptops': ['computers', 'components'],
        'wearables': ['electronics', 'accessories'],
    }

    # Sprawdź bezpośrednią relację
    if cat2_main in relations.get(cat1_main, []):
        pos = relations[cat1_main].index(cat2_main)
        return 0.5 if pos == 0 else (0.4 if pos <= 1 else 0.3)

    # Sprawdź odwrotną relację
    if cat1_main in relations.get(cat2_main, []):
        pos = relations[cat2_main].index(cat1_main)
        return 0.5 if pos == 0 else (0.4 if pos <= 1 else 0.3)

    # Sprawdź czy obie są tech-related (fallback)
    tech_cats = {'electronics', 'components', 'peripherals', 'gaming', 'computers', 'laptops', 'wearables'}
    if cat1_main in tech_cats and cat2_main in tech_cats:
        return 0.25

    # Niepowiązane kategorie
    return 0.1
```

**Przykład obliczenia hierarchicznego podobieństwa:**

```
Użytkownik zainteresowany: "Components" (μ = 0.5)

Produkt A: kategoria = "Components.Processors"
  similarity("Components", "Components.Processors") = 0.7  (ta sama główna)
  match = (0.7 × 0.6) + (0.5 × 0.4) = 0.42 + 0.20 = 0.62

Produkt B: kategoria = "Electronics"
  similarity("Components", "Electronics") = 0.5  (powiązane, pos=0 w relations)
  match = (0.5 × 0.6) + (0.5 × 0.4) = 0.30 + 0.20 = 0.50

Produkt C: kategoria = "Peripherals"
  similarity("Components", "Peripherals") = 0.4  (powiązane, pos=1)
  match = (0.4 × 0.6) + (0.5 × 0.4) = 0.24 + 0.20 = 0.44

Produkt D: kategoria = "Home"
  similarity("Components", "Home") = 0.1  (niepowiązane)
  match = (0.1 × 0.6) + (0.5 × 0.4) = 0.06 + 0.20 = 0.26

Wyniki category_match:
  A: 0.62 (najlepsze dopasowanie)
  B: 0.50
  C: 0.44
  D: 0.26 (najsłabsze dopasowanie)
```

---

## ⚙️ CZĘŚĆ III: Silnik Wnioskowania Rozmytego (Fuzzy Inference Engine)

### Klasa `SimpleFuzzyInference` (linie 484-710)

Implementuje **wnioskowanie w stylu Mamdani** (Mamdani, 1975).

**Architektura systemu rozmytego:**

```
┌──────────────────────────────────────────────────────────┐
│                    WEJŚCIE (Input)                       │
│  • Cena produktu (price)                                 │
│  • Ocena produktu (rating)                               │
│  • Popularność (view_count)                              │
│  • Dopasowanie kategorii (category_match)                │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│              FUZZYFIKACJA (Fuzzification)                │
│  Przekształcenie wartości ostrych na rozmyte             │
│  • price = 800 → {cheap: 0.0, medium: 1.0, exp: 0.0}    │
│  • rating = 4.2 → {low: 0.0, medium: 0.3, high: 0.7}    │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│          BAZA REGUŁ (Rule Base - 6 reguł IF-THEN)        │
│  R1: IF quality=HIGH AND price=CHEAP/MEDIUM              │
│      THEN recommendation=HIGH (waga: 0.9)                │
│  R2: IF category_match AND popularity=HIGH               │
│      THEN recommendation=MEDIUM-HIGH (waga: 0.7)         │
│  R3: IF user_sensitive AND price=CHEAP                   │
│      THEN recommendation=BOOST (waga: 0.6)               │
│  R4: IF category_match AND quality=MEDIUM/HIGH           │
│      THEN recommendation=HIGH (waga: 0.85)               │
│  R5: IF user_premium AND price=EXPENSIVE AND quality=HIGH│
│      THEN recommendation=BOOST (waga: 0.8)               │
│  R6: IF (quality=HIGH AND price=REASONABLE) OR           │
│         (quality=MEDIUM AND price=CHEAP)                 │
│      THEN recommendation=MODERATE (waga: 0.75)           │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│       WNIOSKOWANIE (Inference - T-normy i T-konormy)     │
│  Dla każdej reguły:                                      │
│  • Oblicz aktywację antecedenta (IF część) - T-norma    │
│  • Przypisz wagę reguły                                  │
│  • Akumuluj wyniki - T-konorma (max)                     │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│      DEFUZZYFIKACJA (Defuzzification - Weighted Avg)     │
│  fuzzy_score = Σ(activation × weight) / Σ(weight)       │
│  Wynik: liczba ostra [0.0, 1.0]                          │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│                   WYJŚCIE (Output)                       │
│  fuzzy_score = 0.745 (74.5% rekomendacji)               │
└──────────────────────────────────────────────────────────┘
```

---

### 3.1. Definicja Reguł Rozmytych

**Funkcja: `_define_rules()`**

**Lokalizacja:** `backend/home/fuzzy_logic_engine.py`, linie 511-608

```python
def _define_rules(self):
    """
    Definiuje uproszczoną bazę reguł rozmytych.

    Reguły mają format:
    IF (warunki antecedenta) THEN (stopień rekomendacji)

    Returns:
        list of rule functions
    """
    rules = [
        # Reguła 1: Wysoka jakość + rozsądna cena → wysoka rekomendacja
        {
            "name": "R1: High Quality Bargain",
            "eval": lambda p, cat_match: min(
                self.mf.mu_quality_high(p.get("rating", 0)),
                max(
                    self.mf.mu_price_cheap(p.get("price", 0)),
                    self.mf.mu_price_medium(p.get("price", 0)),
                ),
            ),
            "weight": 0.9,
        },

        # Reguła 2: Dopasowanie kategorii + popularność → rekomendacja
        {
            "name": "R2: Popular in Category",
            "eval": lambda p, cat_match: min(
                cat_match,
                max(
                    self.mf.mu_popularity_medium(p.get("view_count", 0)),
                    self.mf.mu_popularity_high(p.get("view_count", 0))
                )
            ),
            "weight": 0.7,
        },

        # Reguła 3: Wrażliwy na cenę + tani produkt → boost rekomendacji
        {
            "name": "R3: Price Sensitive Match",
            "eval": lambda p, cat_match: (
                min(
                    self.user_profile.price_sensitivity,
                    self.mf.mu_price_cheap(p.get("price", 0)),
                )
                if self.user_profile.price_sensitivity > 0.6
                else 0.0
            ),
            "weight": 0.6,
        },

        # Reguła 4: Wysokie dopasowanie kategorii + dobra jakość → wysoka rekomendacja
        {
            "name": "R4: Category Quality Match",
            "eval": lambda p, cat_match: min(
                cat_match,
                max(
                    self.mf.mu_quality_medium(p.get("rating", 0)),
                    self.mf.mu_quality_high(p.get("rating", 0)),
                ),
            ),
            "weight": 0.85,
        },

        # Reguła 5: Użytkownik premium + drogi + wysoka jakość → boost
        {
            "name": "R5: Premium Match",
            "eval": lambda p, cat_match: (
                min(
                    1.0 - self.user_profile.price_sensitivity,  # Niska wrażliwość
                    self.mf.mu_price_expensive(p.get("price", 0)),
                    self.mf.mu_quality_high(p.get("rating", 0)),
                )
                if self.user_profile.price_sensitivity < 0.4
                else 0.0
            ),
            "weight": 0.8,
        },

        # Reguła 6: Stosunek jakości do ceny (niezależny od kategorii)
        {
            "name": "R6: Quality-Price Balance",
            "eval": lambda p, cat_match: max(
                # Dobra jakość + jakakolwiek rozsądna cena
                min(
                    self.mf.mu_quality_high(p.get("rating", 0)),
                    max(
                        self.mf.mu_price_cheap(p.get("price", 0)) * 0.8,
                        self.mf.mu_price_medium(p.get("price", 0)) * 1.0,
                        self.mf.mu_price_expensive(p.get("price", 0)) * 0.6
                    )
                ),
                # Średnia jakość + tania cena
                min(
                    self.mf.mu_quality_medium(p.get("rating", 0)),
                    self.mf.mu_price_cheap(p.get("price", 0))
                ) * 0.7
            ),
            "weight": 0.75,
        },
    ]

    return rules
```

**Operatory rozmyte używane w regułach:**

```
T-norma (AND) - min():
  min(a, b) = najmniejsza z dwóch wartości
  Przykład: min(0.7, 0.5) = 0.5

T-konorma (OR) - max():
  max(a, b) = największa z dwóch wartości
  Przykład: max(0.3, 0.8) = 0.8

Zastosowanie:
  IF quality=HIGH AND price=CHEAP
    = min(μ_quality_high, μ_price_cheap)
    = min(0.8, 0.6)
    = 0.6

  IF price=CHEAP OR price=MEDIUM
    = max(μ_price_cheap, μ_price_medium)
    = max(0.3, 0.7)
    = 0.7
```

**Źródło naukowe:**
- T-normy i T-konormy z pracy Zadeh, L. A. (1965) "Fuzzy sets"
- Interpretacja AND jako min() i OR jako max() z pracy Zadeh, L. A. (1973)

---

### 3.2. Ewaluacja Produktu

**Funkcja: `evaluate_product()`**

**Lokalizacja:** `backend/home/fuzzy_logic_engine.py`, linie 610-645

```python
def evaluate_product(self, product_data, category_match=0.0):
    """
    Ewaluuje produkt używając wnioskowania rozmytego.

    Args:
        product_data: dict z kluczami: 'price', 'rating', 'view_count', etc.
        category_match: rozmyty stopień dopasowania kategorii [0.0, 1.0]

    Returns:
        dict: {
            'fuzzy_score': końcowy stopień rekomendacji [0.0, 1.0],
            'rule_activations': dict aktywacji reguł dla wyjaśnialności
        }
    """
    rule_activations = {}
    weighted_sum = 0.0
    weight_sum = 0.0

    for rule in self.rules:
        # Ewaluuj antecedent reguły (T-norma zastosowana wewnątrz eval reguły)
        activation = rule["eval"](product_data, category_match)

        rule_activations[rule["name"]] = round(activation, 3)

        # Akumuluj dla defuzzyfikacji (średnia ważona)
        weighted_sum += activation * rule["weight"]
        weight_sum += rule["weight"]

    # Uproszczona defuzzyfikacja: średnia ważona
    fuzzy_score = weighted_sum / weight_sum if weight_sum > 0 else 0.0

    return {
        "fuzzy_score": round(fuzzy_score, 3),
        "rule_activations": rule_activations,
        "category_match": round(category_match, 3),
    }
```

**Wzór matematyczny defuzzyfikacji (Weighted Average):**

```
                 Σ(activationᵢ × weightᵢ)
fuzzy_score = ────────────────────────────
                     Σ(weightᵢ)

gdzie:
- activationᵢ = stopień aktywacji i-tej reguły [0.0, 1.0]
- weightᵢ = waga i-tej reguły (ważność reguły)
- n = liczba reguł (6)

Przykład:
R1: activation = 0.7, weight = 0.9 → wkład = 0.7 × 0.9 = 0.63
R2: activation = 0.5, weight = 0.7 → wkład = 0.5 × 0.7 = 0.35
R3: activation = 0.0, weight = 0.6 → wkład = 0.0 × 0.6 = 0.00
R4: activation = 0.6, weight = 0.85 → wkład = 0.6 × 0.85 = 0.51
R5: activation = 0.0, weight = 0.8 → wkład = 0.0 × 0.8 = 0.00
R6: activation = 0.8, weight = 0.75 → wkład = 0.8 × 0.75 = 0.60

Suma wkładów = 0.63 + 0.35 + 0.00 + 0.51 + 0.00 + 0.60 = 2.09
Suma wag = 0.9 + 0.7 + 0.6 + 0.85 + 0.8 + 0.75 = 4.6

fuzzy_score = 2.09 / 4.6 = 0.454 = 45.4%
```

---

### 3.3. Pełny Przykład Ewaluacji

**Produkt do oceny:**
```
AMD Ryzen 7 5800X3D
  price: 1899 PLN
  rating: 4.8
  view_count: 8 zamówień
  kategoria: "Components.Processors"
```

**Profil użytkownika:**
```
category_interests = {"Components": 0.5}
price_sensitivity = 0.4
```

**Krok 1: Fuzzyfikacja**

```
Cena (1899 PLN):
  μ_cheap(1899) = 0.0
  μ_medium(1899) = 0.0
  μ_expensive(1899) = (1899 - 1000) / (2000 - 1000) = 0.899

Ocena (4.8):
  μ_low(4.8) = 0.0
  μ_medium(4.8) = 0.0
  μ_high(4.8) = 1.0

Popularność (8):
  μ_low(8) = (10 - 8) / (10 - 2) = 0.25
  μ_medium(8) = 1.0
  μ_high(8) = 0.0

Dopasowanie kategorii:
  similarity("Components", "Components.Processors") = 0.7
  category_match = (0.7 × 0.6) + (0.5 × 0.4) = 0.62
```

**Krok 2: Aktywacja reguł**

```
R1: High Quality Bargain
  = min(μ_high(4.8), max(μ_cheap(1899), μ_medium(1899)))
  = min(1.0, max(0.0, 0.0))
  = min(1.0, 0.0)
  = 0.0

R2: Popular in Category
  = min(category_match, max(μ_medium(8), μ_high(8)))
  = min(0.62, max(1.0, 0.0))
  = min(0.62, 1.0)
  = 0.62

R3: Price Sensitive Match
  = 0.0  (bo price_sensitivity = 0.4 ≤ 0.6)

R4: Category Quality Match
  = min(category_match, max(μ_medium(4.8), μ_high(4.8)))
  = min(0.62, max(0.0, 1.0))
  = min(0.62, 1.0)
  = 0.62

R5: Premium Match
  = min(1.0 - 0.4, μ_expensive(1899), μ_high(4.8))
  = min(0.6, 0.899, 1.0)
  = 0.6

R6: Quality-Price Balance
  = max(
      min(1.0, max(0.0×0.8, 0.0×1.0, 0.899×0.6)),
      min(0.0, 0.0) × 0.7
    )
  = max(
      min(1.0, 0.539),
      0.0
    )
  = 0.539
```

**Krok 3: Defuzzyfikacja**

```
weighted_sum = (0.0×0.9) + (0.62×0.7) + (0.0×0.6) + (0.62×0.85) + (0.6×0.8) + (0.539×0.75)
             = 0.0 + 0.434 + 0.0 + 0.527 + 0.48 + 0.404
             = 1.845

weight_sum = 0.9 + 0.7 + 0.6 + 0.85 + 0.8 + 0.75 = 4.6

fuzzy_score = 1.845 / 4.6 = 0.401 = 40.1%
```

**Interpretacja:**
Produkt otrzymuje wynik **40.1%**, co oznacza **średnią rekomendację** dla tego użytkownika. Główne powody:
- ✅ Dobra jakość (rating 4.8) → aktywacja R4, R6
- ✅ Dopasowanie kategorii (62%) → aktywacja R2, R4
- ✅ Użytkownik premium (price_sens=0.4) → aktywacja R5
- ❌ Produkt drogi, ale nie tani/średni → brak aktywacji R1
- ❌ Popularność średnia, nie wysoka → R2 tylko częściowo aktywna

---

## 📊 Wzory Matematyczne - Kompletna Lista

### 1. Funkcje Przynależności (Membership Functions)

**Trójkątna funkcja przynależności (Triangular):**

```
         ⎧  0                       jeśli x ≤ a
         ⎪  (x - a) / (b - a)       jeśli a < x ≤ b
μ(x) =   ⎨  (c - x) / (c - b)       jeśli b < x < c
         ⎩  0                       jeśli x ≥ c

gdzie: a, b, c - parametry kształtu (a < b < c)
```

**Trapezoidalna funkcja przynależności (Trapezoidal):**

```
         ⎧  0                       jeśli x < a
         ⎪  (x - a) / (b - a)       jeśli a ≤ x < b
μ(x) =   ⎨  1                       jeśli b ≤ x ≤ c
         ⎪  (d - x) / (d - c)       jeśli c < x < d
         ⎩  0                       jeśli x ≥ d

gdzie: a, b, c, d - parametry kształtu (a < b < c < d)
```

---

### 2. Operatory Rozmyte (Fuzzy Operators)

**T-norma (AND operator) - min():**

```
T(a, b) = min(a, b)

Właściwości:
  • Komutacja: min(a, b) = min(b, a)
  • Asocjacja: min(min(a, b), c) = min(a, min(b, c))
  • Monotonność: jeśli a ≤ c to min(a, b) ≤ min(c, b)
  • Warunki brzegowe: min(a, 1) = a, min(a, 0) = 0
```

**T-konorma (OR operator) - max():**

```
S(a, b) = max(a, b)

Właściwości:
  • Komutacja: max(a, b) = max(b, a)
  • Asocjacja: max(max(a, b), c) = max(a, max(b, c))
  • Monotonność: jeśli a ≤ c to max(a, b) ≤ max(c, b)
  • Warunki brzegowe: max(a, 0) = a, max(a, 1) = 1
```

**Źródło:** Zadeh, L. A. (1965) "Fuzzy sets", Information and Control, 8(3), pp. 338-353

---

### 3. Budowa Profilu Użytkownika

**Rozmyte zainteresowanie kategorią:**

```
μ_interest(kategoria) = liczba_zakupów_w_kategorii / Σ(wszystkie_zakupy)

Zakres: [0.0, 1.0]
Interpretacja: stopień zainteresowania użytkownika daną kategorią
```

**Wrażliwość na cenę:**

```
                    ⎧  0.9   jeśli avg_price < 300
                    ⎪  0.6   jeśli 300 ≤ avg_price < 700
price_sensitivity = ⎨  0.4   jeśli 700 ≤ avg_price < 1500
                    ⎩  0.2   jeśli avg_price ≥ 1500

gdzie: avg_price = suma_wydatków / liczba_produktów
```

---

### 4. Dopasowanie Kategorii

**Kombinacja ważona:**

```
match(user_cat, prod_cat) = (similarity × w₁) + (interest × w₂)

gdzie:
  • similarity = _calculate_category_similarity(user_cat, prod_cat)
  • interest = μ_interest(user_cat)
  • w₁ = 0.6 (waga podobieństwa)
  • w₂ = 0.4 (waga zainteresowania)
```

**Agregacja dopasowań (T-konorma max):**

```
category_match = max{match(user_catᵢ, prod_cat) : i ∈ user_categories}

Interpretacja: wybierz najlepsze dopasowanie spośród wszystkich kategorii użytkownika
```

---

### 5. Defuzzyfikacja (Weighted Average Method)

**Średnia ważona:**

```
                  n
                  Σ (activationᵢ × weightᵢ)
                 i=1
fuzzy_score = ──────────────────────────────
                  n
                  Σ weightᵢ
                 i=1

gdzie:
  • n = liczba reguł (6)
  • activationᵢ = stopień aktywacji i-tej reguły
  • weightᵢ = waga i-tej reguły
```

**Źródło:** Sugeno, M. (1985) "Industrial applications of fuzzy control"

**Alternatywne metody defuzzyfikacji (niewykorzystane w projekcie):**

1. **Center of Gravity (COG):**
   ```
            ∫ x × μ(x) dx
   xCOG = ─────────────────
             ∫ μ(x) dx
   ```

2. **Maximum Method:**
   ```
   x* = arg max μ(x)
   ```

Wybraliśmy **Weighted Average**, bo:
- Prostsze obliczeniowo (O(n) vs O(∞) dla COG)
- Nie wymaga całkowania numerycznego
- Wystarczająco dokładne dla 6 reguł
- Standard w uproszczonych systemach rozmytych

---

## 🔧 Integracja z Django Backend

### 1. `backend/home/sentiment_views.py` - Endpoint Rozmytych Rekomendacji

**Lokalizacja:** `backend/home/sentiment_views.py`

```python
class FuzzyLogicRecommendationsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Inicjalizacja systemu rozmytego
        membership_functions = FuzzyMembershipFunctions()
        user_profile = FuzzyUserProfile(user=request.user if request.user.is_authenticated else None)
        fuzzy_engine = SimpleFuzzyInference(membership_functions, user_profile)

        # Pobierz produkty z bazy danych
        products_query = Product.objects.all().annotate(
            review_count=Count("opinion"),
            avg_rating=Avg("opinion__rating"),
            order_count=Count("orderproduct", distinct=True)
        )

        # Oceń każdy produkt
        scored_products = []
        for product in products_query[:100]:
            # Pobierz kategorie produktu
            product_categories = [cat.name for cat in product.categories.all()]

            # Oblicz dopasowanie kategorii
            category_match = max([user_profile.fuzzy_category_match(cat) for cat in product_categories] or [0.0])

            # Przygotuj dane produktu
            product_data = {
                'price': float(product.price),
                'rating': float(product.avg_rating) if product.avg_rating else 3.0,
                'view_count': product.order_count if hasattr(product, 'order_count') else 0
            }

            # Ewaluuj produkt
            fuzzy_result = fuzzy_engine.evaluate_product(product_data, category_match)

            scored_products.append({
                'product': product,
                'fuzzy_score': fuzzy_result['fuzzy_score'],
                'rule_activations': fuzzy_result['rule_activations'],
                'category_match': fuzzy_result['category_match']
            })

        # Sortuj według fuzzy_score
        scored_products.sort(key=lambda x: x['fuzzy_score'], reverse=True)

        # Zwróć top 6
        top_products = scored_products[:6]

        return Response({
            'products': [
                {
                    'id': item['product'].id,
                    'name': item['product'].name,
                    'price': float(item['product'].price),
                    'fuzzy_score': item['fuzzy_score'],
                    'rule_activations': item['rule_activations'],
                    'category_match': item['category_match']
                }
                for item in top_products
            ],
            'user_profile': user_profile.get_profile_summary()
        })
```

---

### 2. Panel Admina - Podgląd Reguł

**Lokalizacja:** `backend/home/recommendation_views.py`

```python
if algorithm == "fuzzy_logic":
    from home.fuzzy_logic_engine import (
        FuzzyMembershipFunctions,
        FuzzyUserProfile,
        SimpleFuzzyInference
    )

    membership_functions = FuzzyMembershipFunctions()
    user_profile = FuzzyUserProfile(user=request.user)
    fuzzy_engine = SimpleFuzzyInference(membership_functions, user_profile)

    # Pobierz produkty z adnotacjami
    products_query = Product.objects.all().annotate(
        review_count=Count('opinion'),
        avg_rating=Avg('opinion__rating'),
        order_count=Count('orderproduct', distinct=True)
    )[:100]

    # ... ocena produktów (jak wyżej) ...

    return Response(serializer.data)
```

---

## 🎨 Frontend - Wyświetlanie dla Użytkownika

### `frontend/src/components/ClientPanel/ClientFuzzyLogic.jsx`

**Wyświetlanie profilu użytkownika:**

```javascript
<div className="category-interests">
  <h3>Your Favorite Categories</h3>
  <p>These categories are ranked based on your shopping behavior.</p>
  <div className="interests-list">
    {(userProfile.top_interests || []).map(([category, degree], idx) => (
      <div key={idx} className="interest-item">
        <div className="interest-header">
          <span className="category-name">{category}</span>
          <span className="interest-percentage">
            {(degree * 100).toFixed(0)}%
          </span>
        </div>
        <div className="interest-bar">
          <div
            className="interest-fill"
            style={{ width: `${degree * 100}%` }}
          />
        </div>
      </div>
    ))}
  </div>
</div>
```

**Wyświetlanie aktywacji reguł:**

```javascript
<div className="rules-activations">
  <h4>Rule Activations for This Product</h4>
  {Object.entries(product.rule_activations || {}).map(([rule, value]) => (
    <div key={rule} className="rule-activation-item">
      <span className="rule-name">{rule}</span>
      <div className="activation-bar">
        <div
          className="activation-fill"
          style={{
            width: `${value * 100}%`,
            backgroundColor: value > 0.5 ? '#4caf50' : '#ff9800'
          }}
        />
      </div>
      <span className="activation-value">{(value * 100).toFixed(1)}%</span>
    </div>
  ))}
</div>
```

---

## ✅ Podsumowanie Kluczowych Plików

| Plik                                                | Rola                                                    |
|-----------------------------------------------------|---------------------------------------------------------|
| `fuzzy_logic_engine.py → FuzzyMembershipFunctions`  | Funkcje przynależności (μ) dla ceny, ocen, popularności |
| `fuzzy_logic_engine.py → FuzzyUserProfile`          | Budowa profilu rozmytego z historii użytkownika         |
| `fuzzy_logic_engine.py → SimpleFuzzyInference`      | Silnik wnioskowania (6 reguł IF-THEN)                  |
| `sentiment_views.py → FuzzyLogicRecommendationsView`| API endpoint dla rozmytych rekomendacji                |
| `recommendation_views.py`                           | Podgląd rekomendacji w panelu admina                    |
| `ClientFuzzyLogic.jsx`                              | Widok klienta z aktywacjami reguł                       |

---

## 📚 Bibliografia

- Zadeh, L. A. (1965). "Fuzzy sets". Information and Control, 8(3), 338-353.
- Zadeh, L. A. (1973). "Outline of a new approach to the analysis of complex systems and decision processes". IEEE Transactions on Systems, Man, and Cybernetics, 3(1), 28-44.
- Mamdani, E. H. (1975). "Application of fuzzy algorithms for control of simple dynamic plant". Proceedings of the Institution of Electrical Engineers, 121(12), 1585-1588.
- Sugeno, M. (1985). "Industrial applications of fuzzy control". Elsevier Science Inc.
- Ross, T. J. (2010). "Fuzzy Logic with Engineering Applications", 3rd Edition, Wiley.
- Klir, G. J., Yuan, B. (1995). "Fuzzy Sets and Fuzzy Logic: Theory and Applications", Prentice Hall.

---

**Ostatnia aktualizacja:** 12 października 2025
**Status:** ✅ Produkcyjny (wszystkie funkcje działają poprawnie)
**Wersja dokumentacji:** 1.0
