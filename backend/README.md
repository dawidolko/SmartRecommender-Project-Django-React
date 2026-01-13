# Dokumentacja Architektury Django - Models, Views, Serializers

## Autorzy: Dawid Olko & Piotr Smoła

## Data: 2025-11-02

## Wersja: 2.0

---

# Spis Treści

1. [Wprowadzenie do Architektury](#1-wprowadzenie-do-architektury)
2. [Models - Warstwa Danych](#2-models---warstwa-danych)
3. [Serializers - Warstwa Transformacji](#3-serializers---warstwa-transformacji)
4. [Views - Warstwa Logiki Biznesowej](#4-views---warstwa-logiki-biznesowej)
5. [Przepływ Danych w Aplikacji](#5-przepływ-danych-w-aplikacji)

---

# 1. Wprowadzenie do Architektury

## 1.1 Czym jest Django REST Framework?

Aplikacja SmartRecommender używa **Django REST Framework (DRF)** - rozszerzenia Django do budowy Web API. Architektura opiera się na wzorcu **MVS (Model-View-Serializer)**, który jest adaptacją klasycznego MVC:

| Warstwa        | Odpowiedzialność                             | Plik w projekcie              |
| -------------- | -------------------------------------------- | ----------------------------- |
| **Model**      | Definicja struktury danych i relacji w bazie | `backend/home/models.py`      |
| **View**       | Logika biznesowa, obsługa żądań HTTP         | `backend/home/views.py`       |
| **Serializer** | Konwersja danych Model ↔ JSON                | `backend/home/serializers.py` |

## 1.2 Dlaczego taka architektura?

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ARCHITEKTURA MVS - PRZEPŁYW                           │
└─────────────────────────────────────────────────────────────────────────┘

    Frontend (React)                    Backend (Django)
    ────────────────                    ────────────────
         │
         │  HTTP Request (JSON)
         │  GET /api/products/
         ▼
    ┌─────────────┐
    │    View     │ ◄── Odbiera żądanie, sprawdza uprawnienia
    └─────────────┘
         │
         │  Pobiera dane
         ▼
    ┌─────────────┐
    │    Model    │ ◄── Wykonuje zapytanie SQL do bazy danych
    └─────────────┘
         │
         │  Zwraca obiekty Python
         ▼
    ┌─────────────┐
    │ Serializer  │ ◄── Konwertuje obiekty na JSON
    └─────────────┘
         │
         │  HTTP Response (JSON)
         ▼
    Frontend (React)
```

**Korzyści:**

1. **Separacja odpowiedzialności** - każda warstwa ma jedną rolę
2. **Testowalność** - można testować każdą warstwę osobno
3. **Skalowalność** - łatwe dodawanie nowych endpointów
4. **Bezpieczeństwo** - Serializer waliduje dane wejściowe

---

# 2. Models - Warstwa Danych

## 2.1 Co to jest Model?

**Model** to klasa Pythona reprezentująca tabelę w bazie danych PostgreSQL. Każdy atrybut klasy odpowiada kolumnie w tabeli.

**Lokalizacja:** `backend/home/models.py`

## 2.2 Modele Biznesowe (E-commerce)

### 2.2.1 User - Model Użytkownika

```python
class User(AbstractUser):
    """
    Rozszerza wbudowany model Django o pole 'role'.
    Używa email jako pola logowania zamiast username.
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # Logowanie przez email
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'db_user'
```

**Po co?**

- Przechowuje dane użytkowników (klientów i administratorów)
- Umożliwia logowanie przez email zamiast username
- Role (`admin`/`client`) kontrolują dostęp do funkcji

**Tabela w bazie:** `db_user`

---

### 2.2.2 Product - Model Produktu

```python
class Product(models.Model):
    """
    Główny model produktu - centrum systemu rekomendacji.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, blank=True, null=True)
    categories = models.ManyToManyField('Category', through='ProductCategory')
    tags = models.ManyToManyField('Tag', blank=True)

    class Meta:
        db_table = 'db_product'
```

**Po co?**

- Przechowuje informacje o produktach w sklepie
- `categories` - wielokrotna klasyfikacja (laptop może być w "Electronics" i "Gaming")
- `tags` - etykiety ("New", "Sale", "Best Seller")
- `description` - używany w Content-Based Filtering do ekstrakcji słów kluczowych

**Tabela w bazie:** `db_product`

**Relacje:**

- `ForeignKey(Sale)` - jeden produkt może mieć jedną promocję
- `ManyToManyField(Category)` - wiele produktów ↔ wiele kategorii
- `ManyToManyField(Tag)` - wiele produktów ↔ wiele tagów

---

### 2.2.3 Order i OrderProduct - Modele Zamówień

```python
class Order(models.Model):
    """Nagłówek zamówienia - kto, kiedy, status."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)  # "Pending", "Shipped", "Delivered"

    class Meta:
        db_table = 'db_order'


class OrderProduct(models.Model):
    """Pozycja zamówienia - co i ile sztuk."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'db_order_product'
```

**Po co?**

- `Order` - nagłówek zamówienia (użytkownik, data, status)
- `OrderProduct` - pozycje zamówienia (produkt, ilość)
- **Kluczowe dla Collaborative Filtering** - historia zakupów buduje macierz user-product

**Diagram relacji:**

```
User (1) ──────► (N) Order (1) ──────► (N) OrderProduct (N) ◄────── (1) Product
```

---

### 2.2.4 Opinion - Model Opinii

```python
class Opinion(models.Model):
    """Opinia/recenzja produktu od użytkownika."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField()  # 1-5 gwiazdek

    class Meta:
        db_table = 'db_opinion'
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1, rating__lte=5), name="rating_range"),
            models.UniqueConstraint(fields=['user', 'product'], name="unique_user_product_opinion")
        ]
```

**Po co?**

- Przechowuje recenzje tekstowe i oceny (1-5 gwiazdek)
- **Kluczowe dla Sentiment Analysis** - tekst `content` jest analizowany
- `UniqueConstraint` - użytkownik może wystawić tylko jedną opinię na produkt

---

### 2.2.5 Specification - Model Specyfikacji

```python
class Specification(models.Model):
    """Parametry techniczne produktu (klucz-wartość)."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parameter_name = models.CharField(max_length=50)  # np. "RAM"
    specification = models.TextField(blank=True, null=True)  # np. "16GB DDR4"

    class Meta:
        db_table = 'db_specification'
```

**Po co?**

- Przechowuje parametry techniczne produktów
- Używane w **Sentiment Analysis** do wieloźródłowej agregacji (waga 12%)
- Przykład: `{"parameter_name": "Procesor", "specification": "Intel Core i7-12700H"}`

---

## 2.3 Modele Metod Rekomendacyjnych

### 2.3.1 ProductSimilarity - Podobieństwo Produktów

```python
class ProductSimilarity(models.Model):
    """
    Cache podobieństw między produktami.
    Obliczane przez Collaborative Filtering lub Content-Based.
    """
    SIMILARITY_TYPES = [
        ('collaborative', 'Collaborative Filtering'),
        ('content_based', 'Content Based'),
    ]

    product1 = models.ForeignKey(Product, related_name='similarity_from', on_delete=models.CASCADE)
    product2 = models.ForeignKey(Product, related_name='similarity_to', on_delete=models.CASCADE)
    similarity_type = models.CharField(max_length=20, choices=SIMILARITY_TYPES)
    similarity_score = models.DecimalField(max_digits=5, decimal_places=3)  # [0.000, 1.000]
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'method_product_similarity'
        unique_together = ('product1', 'product2', 'similarity_type')
```

**Po co?**

- **Cache wyników Collaborative Filtering** - zamiast obliczać podobieństwa przy każdym żądaniu
- Przechowuje pary produktów z wynikiem podobieństwa
- `similarity_type` rozróżnia algorytm (CF vs Content-Based)

**Przykład rekordu:**
| product1_id | product2_id | similarity_type | similarity_score |
|-------------|-------------|-----------------|------------------|
| 45 | 67 | collaborative | 0.892 |

---

### 2.3.2 ProductAssociation - Reguły Asocjacyjne

```python
class ProductAssociation(models.Model):
    """
    Reguły asocjacyjne z algorytmu Apriori.
    Reguła: product_1 → product_2 (kto kupił 1, kupi też 2)
    """
    product_1 = models.ForeignKey(Product, related_name='associations_from', on_delete=models.CASCADE)
    product_2 = models.ForeignKey(Product, related_name='associations_to', on_delete=models.CASCADE)
    support = models.FloatField()     # Częstość pary w transakcjach
    confidence = models.FloatField()  # P(product_2 | product_1)
    lift = models.FloatField()        # Siła korelacji

    class Meta:
        db_table = 'method_productassociation'
        unique_together = ('product_1', 'product_2')
```

**Po co?**

- **Cache wyników algorytmu Apriori** - "Frequently Bought Together"
- Przechowuje metryki: Support, Confidence, Lift
- Używane w koszyku do sugerowania dodatkowych produktów

**Przykład rekordu:**
| product_1_id | product_2_id | support | confidence | lift |
|--------------|--------------|---------|------------|------|
| 12 | 34 | 0.035 | 0.78 | 2.45 |

Interpretacja: 3.5% transakcji zawiera oba produkty, 78% kupujących produkt 12 kupiło też 34, korelacja 2.45x silniejsza niż losowa.

---

### 2.3.3 SentimentAnalysis - Analiza Sentymentu

```python
class SentimentAnalysis(models.Model):
    """Wynik analizy sentymentu dla pojedynczej opinii."""
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    opinion = models.OneToOneField(Opinion, on_delete=models.CASCADE)
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=3)  # [-1.000, 1.000]
    sentiment_category = models.CharField(max_length=20, choices=SENTIMENT_CHOICES)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'method_sentiment_analysis'
```

**Po co?**

- Przechowuje wynik analizy sentymentu dla każdej opinii
- `sentiment_score` - wartość liczbowa [-1, 1]
- `sentiment_category` - klasyfikacja (positive/neutral/negative)

---

### 2.3.4 ProductSentimentSummary - Podsumowanie Sentymentu

```python
class ProductSentimentSummary(models.Model):
    """Zagregowany sentyment dla całego produktu."""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='sentiment_summary')
    average_sentiment_score = models.DecimalField(max_digits=5, decimal_places=3)
    positive_count = models.PositiveIntegerField(default=0)
    neutral_count = models.PositiveIntegerField(default=0)
    negative_count = models.PositiveIntegerField(default=0)
    total_opinions = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'method_product_sentiment_summary'
```

**Po co?**

- **Prekalkulowane statystyki** dla każdego produktu
- Unika obliczania średniej przy każdym żądaniu
- Pokazuje rozkład opinii (ile pozytywnych/neutralnych/negatywnych)

---

### 2.3.5 RecommendationSettings - Ustawienia Algorytmu

```python
class RecommendationSettings(models.Model):
    """Który algorytm jest aktywny dla użytkownika."""
    ALGORITHM_CHOICES = [
        ('collaborative', 'Collaborative Filtering'),
        ('content_based', 'Content Based'),
        ('fuzzy_logic', 'Fuzzy Logic'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active_algorithm = models.CharField(max_length=30, choices=ALGORITHM_CHOICES, default='collaborative')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'method_recommendation_settings'
```

**Po co?**

- Administrator wybiera który algorytm jest używany
- Frontend pobiera to ustawienie i odpowiednio wyświetla rekomendacje

---

## 2.4 Diagram Relacji (ERD)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ENTITY RELATIONSHIP DIAGRAM                          │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │     User     │
                              │──────────────│
                              │ id (PK)      │
                              │ email        │
                              │ role         │
                              │ first_name   │
                              │ last_name    │
                              └──────────────┘
                                     │
           ┌─────────────────────────┼─────────────────────────┐
           │                         │                         │
           ▼                         ▼                         ▼
    ┌──────────────┐          ┌──────────────┐          ┌──────────────┐
    │    Order     │          │   Opinion    │          │   CartItem   │
    │──────────────│          │──────────────│          │──────────────│
    │ id (PK)      │          │ id (PK)      │          │ id (PK)      │
    │ user_id (FK) │          │ user_id (FK) │          │ user_id (FK) │
    │ date_order   │          │ product_id   │          │ product_id   │
    │ status       │          │ content      │          │ quantity     │
    └──────────────┘          │ rating       │          └──────────────┘
           │                  └──────────────┘                 │
           │                         │                         │
           ▼                         │                         │
    ┌──────────────┐                 │                         │
    │ OrderProduct │                 │                         │
    │──────────────│                 │                         │
    │ id (PK)      │                 │                         │
    │ order_id (FK)│                 │                         │
    │ product_id   │                 ▼                         ▼
    │ quantity     │          ┌──────────────────────────────────────┐
    └──────────────┘          │              Product                 │
           │                  │──────────────────────────────────────│
           │                  │ id (PK)                              │
           └─────────────────►│ name                                 │
                              │ price                                │
                              │ old_price                            │
                              │ description                          │
                              └──────────────────────────────────────┘
                                     │
           ┌─────────────────────────┼─────────────────────────┐
           │                         │                         │
           ▼                         ▼                         ▼
    ┌──────────────┐          ┌──────────────┐          ┌──────────────┐
    │ PhotoProduct │          │Specification │          │  Category    │
    │──────────────│          │──────────────│          │──────────────│
    │ id (PK)      │          │ id (PK)      │          │ id (PK)      │
    │ product_id   │          │ product_id   │          │ name         │
    │ path         │          │ param_name   │          │ description  │
    └──────────────┘          │ specification│          └──────────────┘
                              └──────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                    MODELE METOD REKOMENDACYJNYCH                             │
└─────────────────────────────────────────────────────────────────────────────┘

    Product ◄────────────────┬────────────────┬────────────────►Product
           │                 │                │                │
           ▼                 ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ProductSimilar│  │ProductAssoc. │  │SentimentAnal.│  │ProductSentim.│
    │──────────────│  │──────────────│  │──────────────│  │   Summary    │
    │ product1_id  │  │ product_1_id │  │ product_id   │  │──────────────│
    │ product2_id  │  │ product_2_id │  │ opinion_id   │  │ product_id   │
    │ similarity   │  │ support      │  │ score        │  │ avg_score    │
    │ _type        │  │ confidence   │  │ category     │  │ pos_count    │
    │ _score       │  │ lift         │  │              │  │ neg_count    │
    └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

---

# 3. Serializers - Warstwa Transformacji

## 3.1 Co to jest Serializer?

**Serializer** konwertuje dane między formatami:

- **Serializacja:** Python Object → JSON (odpowiedź do frontendu)
- **Deserializacja:** JSON → Python Object (dane z frontendu)
- **Walidacja:** Sprawdza poprawność danych wejściowych

**Lokalizacja:** `backend/home/serializers.py`

## 3.2 Dlaczego Serializers są potrzebne?

```python
# BEZ Serializera - trzeba ręcznie budować JSON
def get_product(request, pk):
    product = Product.objects.get(pk=pk)
    return JsonResponse({
        "id": product.id,
        "name": product.name,
        "price": str(product.price),  # Decimal → string ręcznie
        "photos": [{"path": p.path} for p in product.photoproduct_set.all()],  # Ręczna iteracja
        # ... 20 linii kodu dla każdego pola
    })

# Z Serializerem - jedna linia
def get_product(request, pk):
    product = Product.objects.get(pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)  # Automatyczna konwersja
```

## 3.3 Serializery Produktów

### 3.3.1 ProductSerializer - Lista Produktów

```python
class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer do list produktów (GET /api/products/).
    Lżejsza wersja bez opinii i specyfikacji.
    """
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    categories = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        many=True,
        slug_field='name',  # Zwraca nazwy kategorii zamiast ID
        required=False
    )
    photos = PhotoProductSerializer(source='photoproduct_set', many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'old_price', 'description', 'categories', 'photos', 'tags']
```

**Po co?**

- Używany na stronie sklepu (lista produktów)
- Zawiera tylko podstawowe dane (szybsze ładowanie)
- `SlugRelatedField` - zwraca nazwy kategorii (`"Electronics"`) zamiast ID (`5`)

**Przykład output:**

```json
{
  "id": 45,
  "name": "Gaming Laptop",
  "price": "1299.99",
  "old_price": "1499.99",
  "description": "Powerful laptop for gaming",
  "categories": ["Electronics", "Gaming"],
  "photos": [{ "path": "products/laptop1.jpg" }],
  "tags": [1, 5, 8]
}
```

---

### 3.3.2 ProductDetailSerializer - Szczegóły Produktu

```python
class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Pełny serializer produktu (GET /api/products/{id}/).
    Zawiera opinie, specyfikacje, wszystkie relacje.
    """
    photos = PhotoProductSerializer(source='photoproduct_set', many=True)
    tags = serializers.StringRelatedField(many=True)  # Nazwy tagów
    categories = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    opinions = OpinionSerializer(source='opinion_set', many=True)
    specifications = SpecificationSerializer(source='specification_set', many=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'old_price', 'description', 'categories',
            'photos', 'opinions', 'specifications', 'tags'
        ]
```

**Po co?**

- Używany na stronie szczegółów produktu
- Zawiera **zagnieżdżone obiekty** (opinions, specifications)
- `source='opinion_set'` - Django automatycznie tworzy relację odwrotną

**Przykład output:**

```json
{
  "id": 45,
  "name": "Gaming Laptop",
  "price": "1299.99",
  "opinions": [
    {
      "user_email": "john@example.com",
      "content": "Great laptop!",
      "rating": 5
    },
    { "user_email": "jane@example.com", "content": "Good value", "rating": 4 }
  ],
  "specifications": [
    { "parameter_name": "RAM", "specification": "16GB DDR4" },
    { "parameter_name": "Storage", "specification": "512GB SSD" }
  ]
}
```

---

## 3.4 Serializery Użytkowników

### 3.4.1 UserSerializer - Podstawowe Dane

```python
class UserSerializer(serializers.ModelSerializer):
    """Podstawowe informacje o użytkowniku (bez hasła)."""
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role', 'first_name', 'last_name']
```

**Po co?**

- Zwraca publiczne dane użytkownika
- **Nigdy nie zwraca hasła** - bezpieczeństwo

---

### 3.4.2 UserRegisterSerializer - Rejestracja

```python
class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Rejestracja nowego użytkownika z walidacją.
    """
    nickname = serializers.CharField(source="username", required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['nickname', 'email', 'first_name', 'last_name', 'password']

    def validate_first_name(self, value):
        """Walidacja: tylko litery, max 50 znaków."""
        if not value or len(value) > 50:
            raise serializers.ValidationError("First name must be 1-50 characters")
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only letters")
        return value

    def validate_email(self, value):
        """Walidacja: unikalny email."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def validate_password(self, value):
        """Walidacja: min 8 znaków, co najmniej 1 cyfra."""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit")
        return value

    def create(self, validated_data):
        """Tworzy użytkownika z zahashowanym hasłem."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],  # Automatycznie hashowane
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role='client'  # Zawsze client, nie można się zarejestrować jako admin
        )
        return user
```

**Po co?**

- Obsługuje endpoint rejestracji
- **Walidacja po stronie serwera** - nie ufamy danym z frontendu
- `write_only=True` - hasło nigdy nie jest zwracane w odpowiedzi
- `role='client'` - hardcoded, użytkownik nie może wybrać roli

---

### 3.4.3 MyTokenObtainPairSerializer - JWT z Custom Claims

```python
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Rozszerzony serializer JWT - dodaje dane użytkownika do tokenu.
    """
    username_field = "email"  # Logowanie przez email

    @classmethod
    def get_token(cls, user):
        """Dodaje custom claims do tokenu JWT."""
        token = super().get_token(user)

        # Dodatkowe dane w tokenie (dekodowalne przez frontend)
        token['role'] = user.role
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token
```

**Po co?**

- Frontend może odczytać role użytkownika z tokenu bez dodatkowego API call
- Token zawiera: `user_id`, `role`, `first_name`, `last_name`

**Struktura tokenu JWT:**

```json
{
  "token_type": "access",
  "exp": 1730563200,
  "iat": 1730559600,
  "jti": "abc123def456...",
  "user_id": 12,
  "role": "client",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

## 3.5 Serializery Zamówień

### 3.5.1 OrderSerializer - Zamówienie z Produktami

```python
class OrderSerializer(serializers.ModelSerializer):
    """Zamówienie z zagnieżdżonymi produktami i obliczonym total."""
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(required=False)
    order_products = OrderProductSerializer(many=True, read_only=True, source='orderproduct_set')
    total = serializers.SerializerMethodField()  # Obliczane dynamicznie
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_email', 'date_order', 'status', 'order_products', 'total']

    def get_total(self, obj):
        """Oblicza sumę: Σ(cena × ilość) dla wszystkich produktów."""
        total = sum(
            item.product.price * item.quantity
            for item in obj.orderproduct_set.all()
        )
        return str(total)
```

**Po co?**

- `SerializerMethodField` - pole obliczane (nie istnieje w modelu)
- `source='orderproduct_set'` - pobiera powiązane produkty
- `read_only=True` dla user - ustawiany automatycznie z request.user

**Przykład output:**

```json
{
  "id": 789,
  "user": 12,
  "user_email": "john@example.com",
  "date_order": "2025-11-02T14:30:00Z",
  "status": "Pending",
  "order_products": [
    {
      "id": 1,
      "product": { "id": 45, "name": "Laptop", "price": "1299.99" },
      "quantity": 1
    },
    {
      "id": 2,
      "product": { "id": 67, "name": "Mouse", "price": "49.99" },
      "quantity": 2
    }
  ],
  "total": "1399.97"
}
```

---

## 3.6 Serializery Pomocnicze

### 3.6.1 OpinionSerializer - Opinie

```python
class OpinionSerializer(serializers.ModelSerializer):
    """Opinia z emailem użytkownika (zamiast ID)."""
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Opinion
        fields = ["user_email", "content", "rating"]

    def create(self, validated_data):
        """Automatycznie ustawia user i product z kontekstu."""
        validated_data["user"] = self.context["request"].user
        validated_data["product"] = self.context["product"]
        return super().create(validated_data)
```

**Po co?**

- `source="user.email"` - rozwija relację, zwraca email zamiast user_id
- `self.context` - dostęp do request i innych danych przekazanych z View

---

# 4. Views - Warstwa Logiki Biznesowej

## 4.1 Co to jest View?

**View** to klasa lub funkcja obsługująca żądania HTTP:

1. Odbiera żądanie (GET/POST/PUT/DELETE)
2. Sprawdza uprawnienia użytkownika
3. Wykonuje logikę biznesową
4. Zwraca odpowiedź HTTP

**Lokalizacja:** `backend/home/views.py`

## 4.2 Typy Views w Django REST Framework

| Typ                            | Metody HTTP             | Użycie            |
| ------------------------------ | ----------------------- | ----------------- |
| `APIView`                      | Dowolne                 | Custom logika     |
| `ListAPIView`                  | GET                     | Lista obiektów    |
| `CreateAPIView`                | POST                    | Tworzenie obiektu |
| `ListCreateAPIView`            | GET, POST               | Lista + tworzenie |
| `RetrieveAPIView`              | GET                     | Pojedynczy obiekt |
| `UpdateAPIView`                | PUT, PATCH              | Aktualizacja      |
| `DestroyAPIView`               | DELETE                  | Usuwanie          |
| `RetrieveUpdateDestroyAPIView` | GET, PUT, PATCH, DELETE | CRUD na obiekcie  |

## 4.3 System Uprawnień (Permissions)

```python
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdminUser

# Publiczne - każdy może
permission_classes = [AllowAny]

# Zalogowani użytkownicy
permission_classes = [IsAuthenticated]

# Tylko administratorzy
permission_classes = [IsAuthenticated, IsAdminUser]
```

**Custom Permission (IsAdminUser):**

```python
# backend/home/permissions.py
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """Sprawdza czy user.role == 'admin'."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
```

## 4.4 Views Produktów

### 4.4.1 ProductsAPIView - Lista Produktów

```python
class ProductsAPIView(APIView):
    """
    GET /api/products/
    Zwraca wszystkie produkty z kategoriami i zdjęciami.
    """
    permission_classes = [AllowAny]  # Publiczny endpoint

    def get(self, request):
        products = Product.objects.prefetch_related(
            "categories", "photoproduct_set"
        ).all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
```

**Po co?**

- `prefetch_related` - optymalizacja N+1 queries
- `many=True` - serializuje listę obiektów

---

### 4.4.2 ProductDetailAPIView - Szczegóły Produktu

```python
class ProductDetailAPIView(RetrieveAPIView):
    """
    GET /api/products/{id}/
    Zwraca pełne dane produktu z opiniami i specyfikacjami.
    """
    permission_classes = [AllowAny]
    queryset = Product.objects.prefetch_related(
        "categories", "photoproduct_set", "opinion_set", "specification_set"
    )
    serializer_class = ProductDetailSerializer
```

**Po co?**

- `RetrieveAPIView` - automatycznie obsługuje GET na pojedynczym obiekcie
- `prefetch_related` - ładuje wszystkie relacje w 4 zapytaniach zamiast N+1

---

### 4.4.3 ProductListCreateAPIView - CRUD Produktów (Admin)

```python
class ProductListCreateAPIView(ListCreateAPIView):
    """
    GET /api/admin/products/ - lista (admin)
    POST /api/admin/products/ - tworzenie (admin)
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]  # Lista publiczna
        return [IsAuthenticated(), IsAdminUser()]  # Tworzenie tylko admin
```

**Po co?**

- `get_permissions()` - różne uprawnienia dla GET vs POST
- `ListCreateAPIView` - dwa endpointy w jednej klasie

---

## 4.5 Views Zamówień

### 4.5.1 OrderListCreateAPIView - Zamówienia

```python
class OrderListCreateAPIView(ListCreateAPIView):
    """
    GET /api/orders/ - lista zamówień użytkownika
    POST /api/orders/ - składanie zamówienia
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Admin widzi wszystkie, klient tylko swoje."""
        user = self.request.user
        if user.role == "admin" or user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        """Tworzy zamówienie z produktami z koszyka."""
        items = self.request.data.get("items", {})  # {product_id: quantity}
        order = serializer.save(user=self.request.user, status="Pending")

        for product_id, quantity in items.items():
            product = Product.objects.get(pk=product_id)
            OrderProduct.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

        # Uruchom analizy po zamówieniu (CF, Apriori, etc.)
        run_all_analytics_after_order(order)
```

**Po co?**

- `get_queryset()` - filtrowanie danych na podstawie roli
- `perform_create()` - custom logika przy tworzeniu
- `run_all_analytics_after_order()` - trigger dla metod rekomendacyjnych

---

## 4.6 Views Autentykacji

### 4.6.1 CustomTokenObtainPairView - Logowanie

```python
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/token/
    Logowanie - zwraca JWT access + refresh token.
    """
    serializer_class = CustomTokenObtainPairSerializer
```

**Żądanie:**

```json
POST /api/token/
{
    "email": "john@example.com",
    "password": "secret123"
}
```

**Odpowiedź:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 12,
    "email": "john@example.com",
    "role": "client",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

---

### 4.6.2 UserRegisterView - Rejestracja

```python
class UserRegisterView(APIView):
    """
    POST /api/register/
    Rejestracja nowego użytkownika.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Automatyczne generowanie tokenów po rejestracji
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**Po co?**

- Po rejestracji od razu zwraca tokeny (użytkownik nie musi się logować)
- `serializer.errors` - zwraca błędy walidacji

---

## 4.7 Views Administracyjne

### 4.7.1 AdminStatsView - Statystyki

```python
class AdminStatsView(APIView):
    """
    GET /api/admin/stats/
    Statystyki dashboardu administratora.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({
            "total_users": User.objects.count(),
            "total_products": Product.objects.count(),
            "total_orders": Order.objects.count(),
            "pending_orders": Order.objects.filter(status="Pending").count(),
        })
```

---

### 4.7.2 AdminDashboardStatsView - Zaawansowane Statystyki

```python
class AdminDashboardStatsView(APIView):
    """
    GET /api/admin/dashboard/
    Statystyki z wykresami (sprzedaż miesięczna, etc.)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Suma sprzedaży: Σ(cena × ilość)
        total_sales = OrderProduct.objects.aggregate(
            total=Sum(F('product__price') * F('quantity'), output_field=FloatField())
        )['total'] or 0

        # Nowi użytkownicy (ostatnie 30 dni)
        new_users = User.objects.filter(
            date_joined__gte=timezone.now() - timedelta(days=30)
        ).count()

        # Sprzedaż miesięczna (do wykresu)
        orders_by_month = OrderProduct.objects.annotate(
            month=TruncMonth("order__date_order")
        ).values("month").annotate(
            total_sales=Sum(F('product__price') * F('quantity'), output_field=FloatField())
        ).order_by("month")

        return Response({
            "total_sales": total_sales,
            "new_users": new_users,
            "monthly_sales": list(orders_by_month),
        })
```

**Po co?**

- `F()` - odwołanie do pola w bazie (operacje na poziomie SQL)
- `TruncMonth()` - grupowanie po miesiącu
- `aggregate()` vs `annotate()`:
  - `aggregate` - jeden wynik dla całej tabeli
  - `annotate` - dodaje pole do każdego rekordu

---

# 5. Przepływ Danych w Aplikacji

## 5.1 Przykład: Pobieranie Listy Produktów

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PRZEPŁYW: GET /api/products/                          │
└─────────────────────────────────────────────────────────────────────────┘

1. FRONTEND (React)
   ┌──────────────────────────────────────────────────────────────────┐
   │ const response = await axios.get(`${API_URL}/api/products/`);   │
   │ setProducts(response.data);                                      │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP GET /api/products/
                                    ▼
2. DJANGO URL ROUTING (urls.py)
   ┌──────────────────────────────────────────────────────────────────┐
   │ path("api/products/", ProductsAPIView.as_view()),               │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
3. VIEW - ProductsAPIView (views.py)
   ┌──────────────────────────────────────────────────────────────────┐
   │ class ProductsAPIView(APIView):                                  │
   │     permission_classes = [AllowAny]  ◄── Sprawdź uprawnienia    │
   │                                                                  │
   │     def get(self, request):                                      │
   │         products = Product.objects.prefetch_related(...)        │
   │         serializer = ProductSerializer(products, many=True)     │
   │         return Response(serializer.data)                        │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
4. MODEL - Product (models.py)
   ┌──────────────────────────────────────────────────────────────────┐
   │ SELECT * FROM db_product                                         │
   │ JOIN db_product_category ON ...                                  │
   │ JOIN db_photo_product ON ...                                     │
   │                                                                  │
   │ → QuerySet<[Product, Product, Product, ...]>                    │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
5. SERIALIZER - ProductSerializer (serializers.py)
   ┌──────────────────────────────────────────────────────────────────┐
   │ [                                                                │
   │   Product(id=1, name="Laptop", price=1299.99)                   │
   │   Product(id=2, name="Mouse", price=49.99)                      │
   │ ]                                                                │
   │                        ↓ Serializacja                           │
   │ [                                                                │
   │   {"id": 1, "name": "Laptop", "price": "1299.99", ...}         │
   │   {"id": 2, "name": "Mouse", "price": "49.99", ...}            │
   │ ]                                                                │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP 200 OK (JSON)
                                    ▼
6. FRONTEND (React)
   ┌──────────────────────────────────────────────────────────────────┐
   │ products.map(product => <ProductCard key={product.id} ... />)   │
   └──────────────────────────────────────────────────────────────────┘
```

---

## 5.2 Przykład: Składanie Zamówienia

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PRZEPŁYW: POST /api/orders/                           │
└─────────────────────────────────────────────────────────────────────────┘

1. FRONTEND (React) - CartContent.jsx
   ┌──────────────────────────────────────────────────────────────────┐
   │ const response = await axios.post(                               │
   │   `${API_URL}/api/orders/`,                                     │
   │   { items: {"45": 1, "67": 2} },  // product_id: quantity       │
   │   { headers: { Authorization: `Bearer ${token}` }}              │
   │ );                                                               │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP POST /api/orders/
                                    │ + JWT Token w headerze
                                    ▼
2. DJANGO MIDDLEWARE - JWT Authentication
   ┌──────────────────────────────────────────────────────────────────┐
   │ 1. Wyciągnij token z headera Authorization                      │
   │ 2. Zweryfikuj podpis JWT                                        │
   │ 3. Zdekoduj user_id z tokenu                                    │
   │ 4. Ustaw request.user = User.objects.get(id=user_id)           │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
3. VIEW - OrderListCreateAPIView (views.py)
   ┌──────────────────────────────────────────────────────────────────┐
   │ permission_classes = [IsAuthenticated]  ◄── Sprawdź JWT         │
   │                                                                  │
   │ def perform_create(self, serializer):                           │
   │     items = request.data.get("items", {})                       │
   │     order = serializer.save(user=request.user, status="Pending")│
   │                                                                  │
   │     for product_id, quantity in items.items():                  │
   │         OrderProduct.objects.create(...)                        │
   │                                                                  │
   │     run_all_analytics_after_order(order)  ◄── Trigger ML       │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
4. MODEL - Order + OrderProduct (models.py)
   ┌──────────────────────────────────────────────────────────────────┐
   │ INSERT INTO db_order (user_id, status, date_order) VALUES (...) │
   │ INSERT INTO db_order_product (order_id, product_id, quantity)   │
   │ INSERT INTO db_order_product (order_id, product_id, quantity)   │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
5. SIGNALS - run_all_analytics_after_order (signals.py)
   ┌──────────────────────────────────────────────────────────────────┐
   │ 1. Inwalidacja cache CF                                         │
   │ 2. Aktualizacja macierzy podobieństw                            │
   │ 3. Przeliczenie reguł asocjacyjnych                             │
   │ 4. Log interakcji użytkownika                                   │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
6. SERIALIZER - OrderSerializer (serializers.py)
   ┌──────────────────────────────────────────────────────────────────┐
   │ Order(id=789, user=12, status="Pending")                        │
   │                        ↓ Serializacja                           │
   │ {                                                                │
   │   "id": 789,                                                    │
   │   "user_email": "john@example.com",                             │
   │   "status": "Pending",                                          │
   │   "order_products": [...],                                      │
   │   "total": "1399.97"                                            │
   │ }                                                                │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP 201 Created (JSON)
                                    ▼
7. FRONTEND (React)
   ┌──────────────────────────────────────────────────────────────────┐
   │ toast.success("Order placed successfully!");                    │
   │ clearCart();                                                     │
   │ navigate("/orders");                                             │
   └──────────────────────────────────────────────────────────────────┘
```

---

## 5.3 Przykład: Rejestracja Użytkownika

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PRZEPŁYW: POST /api/register/                         │
└─────────────────────────────────────────────────────────────────────────┘

1. FRONTEND - Formularz rejestracji
   ┌──────────────────────────────────────────────────────────────────┐
   │ {                                                                │
   │   "nickname": "johndoe",                                        │
   │   "email": "john@example.com",                                  │
   │   "first_name": "John",                                         │
   │   "last_name": "Doe",                                           │
   │   "password": "secure123"                                       │
   │ }                                                                │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
2. VIEW - UserRegisterView
   ┌──────────────────────────────────────────────────────────────────┐
   │ serializer = UserRegisterSerializer(data=request.data)          │
   │ if serializer.is_valid():                                       │
   │     user = serializer.save()                                    │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
3. SERIALIZER - UserRegisterSerializer - WALIDACJA
   ┌──────────────────────────────────────────────────────────────────┐
   │ validate_first_name("John")     ✓ Tylko litery, max 50 znaków  │
   │ validate_last_name("Doe")       ✓ Tylko litery, max 50 znaków  │
   │ validate_email("john@...")      ✓ Unikalny email               │
   │ validate_password("secure123")  ✓ Min 8 znaków, 1 cyfra        │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
4. SERIALIZER - create()
   ┌──────────────────────────────────────────────────────────────────┐
   │ User.objects.create_user(                                       │
   │     username="johndoe",                                         │
   │     email="john@example.com",                                   │
   │     password="secure123",  ──► HASHOWANE przez Django          │
   │     first_name="John",                                          │
   │     last_name="Doe",                                            │
   │     role="client"  ◄── Hardcoded, nie z request                │
   │ )                                                                │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
5. MODEL - User (baza danych)
   ┌──────────────────────────────────────────────────────────────────┐
   │ INSERT INTO db_user                                              │
   │ (username, email, password, first_name, last_name, role)        │
   │ VALUES                                                           │
   │ ('johndoe', 'john@...', 'pbkdf2_sha256$...', 'John', 'Doe',    │
   │  'client')                                                       │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
6. VIEW - Generowanie JWT
   ┌──────────────────────────────────────────────────────────────────┐
   │ refresh = RefreshToken.for_user(user)                           │
   │ return Response({                                                │
   │     "access": str(refresh.access_token),                        │
   │     "refresh": str(refresh),                                    │
   │     "user": {...}                                               │
   │ })                                                               │
   └──────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP 201 Created
                                    ▼
7. FRONTEND - Zapisz tokeny
   ┌──────────────────────────────────────────────────────────────────┐
   │ localStorage.setItem("access", response.data.access);           │
   │ localStorage.setItem("refresh", response.data.refresh);         │
   │ setUser(response.data.user);                                    │
   │ navigate("/");  // Przekierowanie na stronę główną              │
   └──────────────────────────────────────────────────────────────────┘
```

---

# Podsumowanie

## Tabela Odpowiedzialności

| Warstwa        | Plik             | Odpowiedzialność                                        |
| -------------- | ---------------- | ------------------------------------------------------- |
| **Model**      | `models.py`      | Struktura danych, relacje, constrainty bazodanowe       |
| **Serializer** | `serializers.py` | Walidacja, konwersja Model ↔ JSON, zagnieżdżone obiekty |
| **View**       | `views.py`       | Logika biznesowa, uprawnienia, obsługa HTTP             |
| **URL**        | `urls.py`        | Routing - mapowanie URL → View                          |
| **Permission** | `permissions.py` | Kontrola dostępu (admin/client)                         |
| **Signal**     | `signals.py`     | Automatyczne akcje po zdarzeniach (np. po zamówieniu)   |

## Kluczowe Koncepcje

1. **Model = Tabela w bazie** - każda klasa = tabela, każdy atrybut = kolumna
2. **Serializer = Transformator** - Python ↔ JSON + walidacja
3. **View = Kontroler** - odbiera żądanie, zwraca odpowiedź
4. **Permission = Strażnik** - sprawdza uprawnienia użytkownika
5. **Signal = Trigger** - automatyczne akcje po zdarzeniach

## Bezpieczeństwo w Aplikacji

| Warstwa    | Mechanizm                                                  |
| ---------- | ---------------------------------------------------------- |
| View       | `permission_classes` - kto ma dostęp                       |
| Serializer | `write_only=True` - hasło nie zwracane                     |
| Serializer | `validate_*()` - walidacja danych wejściowych              |
| Model      | `UniqueConstraint` - unikalność na poziomie DB             |
| Model      | `CheckConstraint` - ograniczenia wartości (np. rating 1-5) |
