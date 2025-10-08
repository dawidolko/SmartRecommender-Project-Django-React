# 🧠 Fuzzy Logic System for Product Search

## What Is Fuzzy Logic in This System?

**Fuzzy Logic** is a mathematical framework for handling uncertainty and imprecise information using **membership functions** and **linguistic variables** instead of binary true/false values.

This implementation uses **Mamdani Fuzzy Inference System** to convert text similarity scores into product relevance rankings through linguistic reasoning.

---

## 📚 Theoretical Foundation

### References:

1. **Zadeh, L.A. (1965)**. "Fuzzy Sets". _Information and Control_, 8(3), pp. 338-353.

   - Introduced concept of fuzzy sets with membership functions μ(x) ∈ [0, 1]
   - Basis for all modern fuzzy logic systems

2. **Mamdani, E.H., Assilian, S. (1975)**. "An Experiment in Linguistic Synthesis with a Fuzzy Logic Controller". _International Journal of Man-Machine Studies_, 7(1), pp. 1-13.

   - Developed Mamdani fuzzy inference method
   - IF-THEN rules with linguistic terms
   - MIN-MAX inference operators

3. **Ross, T.J. (2010)**. "Fuzzy Logic with Engineering Applications", 3rd edition. _John Wiley & Sons_.
   - Comprehensive guide to fuzzy logic applications
   - Defuzzification methods (Centroid, Bisector, MOM, etc.)

---

## 🎯 System Architecture

### 1. Linguistic Variables

#### Input Variable 1: **name_match** [0, 1]

Measures how well the product name matches the search query.

**Linguistic Terms:**

- `very_low` (0.0 - 0.2): Almost no match
- `low` (0.0 - 0.4): Poor match
- `medium` (0.2 - 0.7): Moderate match
- `high` (0.5 - 0.9): Good match
- `very_high` (0.7 - 1.0): Excellent match

#### Input Variable 2: **category_match** [0, 1]

Measures how well the product category matches the search query.

**Linguistic Terms:**

- `poor` (0.0 - 0.3): Category doesn't match
- `fair` (0.1 - 0.6): Partial category match
- `good` (0.4 - 0.9): Good category match
- `excellent` (0.7 - 1.0): Perfect category match

#### Input Variable 3: **price_suitability** [0, 1]

Measures how suitable the product price is for the user.

**Linguistic Terms:**

- `poor` (0.0 - 0.3): Too expensive/cheap
- `acceptable` (0.2 - 0.7): Reasonable price
- `good` (0.5 - 0.95): Good price
- `perfect` (0.8 - 1.0): Ideal price

#### Output Variable: **relevance** [0, 1]

Final relevance score for the product.

**Linguistic Terms:**

- `irrelevant` (0.0 - 0.25): Not relevant
- `somewhat_relevant` (0.15 - 0.65): Moderately relevant
- `relevant` (0.5 - 0.85): Relevant
- `highly_relevant` (0.7 - 1.0): Very relevant

---

## 📐 Membership Functions

### Triangular Membership Function (trimf)

Mathematical formula:

```
μ(x) = {
    0,              if x ≤ a or x ≥ c
    (x-a)/(b-a),    if a < x ≤ b
    (c-x)/(c-b),    if b < x < c
}
```

Where:

- `a` = left foot (start)
- `b` = peak (center)
- `c` = right foot (end)

**Example:** `medium = trimf(0.2, 0.5, 0.7)`

```
μ(x=0.35) = (0.35-0.2)/(0.5-0.2) = 0.5
μ(x=0.6)  = (0.7-0.6)/(0.7-0.5) = 0.5
μ(x=0.5)  = 1.0  (peak)
```

### Trapezoidal Membership Function (trapmf)

Mathematical formula:

```
μ(x) = {
    0,              if x ≤ a or x ≥ d
    (x-a)/(b-a),    if a < x ≤ b
    1,              if b < x ≤ c
    (d-x)/(d-c),    if c < x < d
}
```

Where:

- `a` = left foot
- `b` = left shoulder
- `c` = right shoulder
- `d` = right foot

**Example:** `very_high = trapmf(0.7, 0.85, 1.0, 1.0)`

```
μ(x=0.8)  = (0.8-0.7)/(0.85-0.7) ≈ 0.67
μ(x=0.9)  = 1.0  (plateau)
μ(x=1.0)  = 1.0
```

---

## 🔧 Fuzzy Rules (IF-THEN)

The system uses **12 fuzzy rules** for reasoning:

### High Priority Rules (Name Match)

**R1:** `IF name_match is VERY_HIGH THEN relevance is HIGHLY_RELEVANT` (weight: 1.0)

- If product name almost perfectly matches query → Highly relevant

**R2:** `IF name_match is HIGH AND category_match is GOOD THEN relevance is HIGHLY_RELEVANT` (weight: 0.9)

- Strong name match + good category → Highly relevant

**R3:** `IF name_match is HIGH AND category_match is FAIR THEN relevance is RELEVANT` (weight: 0.85)

- Strong name match + fair category → Relevant

**R4:** `IF name_match is MEDIUM AND category_match is EXCELLENT THEN relevance is RELEVANT` (weight: 0.8)

- Moderate name match + perfect category → Relevant

**R5:** `IF name_match is MEDIUM AND category_match is GOOD THEN relevance is RELEVANT` (weight: 0.75)

- Moderate name + good category → Relevant

**R6:** `IF name_match is MEDIUM THEN relevance is SOMEWHAT_RELEVANT` (weight: 0.7)

- Moderate name match alone → Somewhat relevant

**R7:** `IF name_match is LOW AND category_match is EXCELLENT THEN relevance is SOMEWHAT_RELEVANT` (weight: 0.5)

- Poor name but perfect category → Somewhat relevant

**R8:** `IF name_match is LOW THEN relevance is IRRELEVANT` (weight: 0.6)

- Poor name match → Irrelevant

**R9:** `IF name_match is VERY_LOW THEN relevance is IRRELEVANT` (weight: 1.0)

- Almost no name match → Irrelevant

### Price Rules (Lower Priority)

**R10:** `IF name_match is HIGH AND price_suitability is PERFECT THEN relevance is HIGHLY_RELEVANT` (weight: 0.7)

- Good name + perfect price → Highly relevant

**R11:** `IF name_match is MEDIUM AND price_suitability is GOOD THEN relevance is RELEVANT` (weight: 0.6)

- Moderate name + good price → Relevant

**R12:** `IF category_match is EXCELLENT AND price_suitability is PERFECT THEN relevance is RELEVANT` (weight: 0.55)

- Perfect category + perfect price → Relevant

---

## 🔄 Mamdani Fuzzy Inference Process

### Step 1: **Fuzzification**

Convert crisp input values to fuzzy membership degrees.

**Example:**

```
Input: name_match = 0.75

Fuzzification result:
- μ_medium(0.75) = 0.0     (outside range)
- μ_high(0.75) = 1.0       (at peak)
- μ_very_high(0.75) = 0.33 (partial membership)
```

### Step 2: **Rule Evaluation**

Evaluate each fuzzy rule using **MIN operator** for AND.

**Example (Rule R1):**

```
Rule: IF name_match is VERY_HIGH THEN relevance is HIGHLY_RELEVANT

Input memberships:
- μ_very_high(0.75) = 0.33

Rule activation:
- α = 0.33 × weight(1.0) = 0.33
```

**Example (Rule R2):**

```
Rule: IF name_match is HIGH AND category_match is GOOD THEN relevance is HIGHLY_RELEVANT

Input memberships:
- μ_high(0.75) = 1.0
- μ_good(0.85) = 0.67

Rule activation:
- α = min(1.0, 0.67) × weight(0.9) = 0.67 × 0.9 = 0.603
```

### Step 3: **Aggregation**

Combine rule outputs using **MAX operator**.

**Example:**

```
Rule R1 → highly_relevant: 0.33
Rule R2 → highly_relevant: 0.603
Rule R6 → somewhat_relevant: 0.0

Aggregated output:
- highly_relevant: max(0.33, 0.603) = 0.603
- somewhat_relevant: 0.0
- relevant: 0.0
- irrelevant: 0.0
```

### Step 4: **Defuzzification (Centroid Method)**

Convert fuzzy output to crisp value using center of gravity.

**Mathematical Formula:**

```
y* = Σ(μ(y_i) × y_i) / Σ(μ(y_i))
```

Where:

- `y_i` = discrete points in [0, 1] (e.g., 0.00, 0.01, 0.02, ..., 1.00)
- `μ(y_i)` = aggregated membership at point `y_i`
- `y*` = crisp output (final relevance score)

**Implementation:**

1. Discretize output universe [0, 1] into 101 points
2. For each point `y`, calculate maximum membership across all activated terms
3. Clip membership at rule activation height (Mamdani implication)
4. Calculate weighted average (centroid)

**Example:**

```
Activated terms:
- highly_relevant (0.603): μ(y) clipped at 0.603 for y ∈ [0.7, 1.0]

Centroid calculation:
numerator = Σ(μ(y_i) × y_i) = 0.603×0.7 + 0.603×0.71 + ... + 0.603×1.0
denominator = Σ(μ(y_i)) = 0.603 + 0.603 + ... + 0.603

y* ≈ 0.87 (final relevance score)
```

---

## 📊 Complete Example

### Input:

```python
query = "gaming laptop"
product_name = "Dell Gaming Laptop G5"
category = "Laptops"

# Text similarity scores (from Levenshtein + trigram)
name_score = 0.85
category_score = 0.90
price_score = 0.80
```

### Fuzzification:

```
name_match (0.85):
- very_low: 0.0
- low: 0.0
- medium: 0.0
- high: 0.6
- very_high: 0.67

category_match (0.90):
- poor: 0.0
- fair: 0.0
- good: 0.25
- excellent: 0.83

price_suitability (0.80):
- poor: 0.0
- acceptable: 0.0
- good: 0.75
- perfect: 0.0
```

### Rule Evaluation:

```
R1: IF name_match is VERY_HIGH → α = 0.67 × 1.0 = 0.67 → highly_relevant
R2: IF name_match is HIGH AND category_match is GOOD → α = min(0.6, 0.25) × 0.9 = 0.225 → highly_relevant
R4: IF name_match is MEDIUM AND category_match is EXCELLENT → α = min(0.0, 0.83) × 0.8 = 0.0 → relevant
...
```

### Aggregation:

```
highly_relevant: max(0.67, 0.225, ...) = 0.67
relevant: max(0.0, ...) = 0.0
somewhat_relevant: 0.0
irrelevant: 0.0
```

### Defuzzification:

```
Final relevance score: 0.88
```

### Combined Score:

```
Final score = fuzzy_relevance × 0.7 + desc × 0.15 + spec × 0.10 + tag × 0.05
            = 0.88 × 0.7 + 0.65 × 0.15 + 0.40 × 0.10 + 0.30 × 0.05
            = 0.616 + 0.098 + 0.040 + 0.015
            = 0.769
```

---

## 🆚 Comparison: Fuzzy Logic vs. Traditional Weighted Sum

### Traditional Approach (Before):

```python
total_score = (name_score × 0.45) + (desc_score × 0.25) + (category_score × 0.20) + (spec_score × 0.10)
            = (0.85 × 0.45) + (0.65 × 0.25) + (0.90 × 0.20) + (0.40 × 0.10)
            = 0.3825 + 0.1625 + 0.18 + 0.04
            = 0.765
```

**Issues:**

- ❌ Fixed weights don't adapt to context
- ❌ Linear combination can't capture linguistic rules
- ❌ No handling of uncertainty
- ❌ Poor match in one field penalizes entire score

### Fuzzy Logic Approach (Now):

```python
# Step 1: Fuzzify inputs
name_fuzzy = {very_low: 0.0, low: 0.0, medium: 0.0, high: 0.6, very_high: 0.67}

# Step 2: Apply linguistic rules
R1: IF name_match is VERY_HIGH → 0.67 activation
R2: IF name_match is HIGH AND category is GOOD → 0.225 activation

# Step 3: Aggregate
aggregated = {highly_relevant: 0.67, ...}

# Step 4: Defuzzify
final_relevance = 0.88

# Combine with supplementary scores
combined_score = 0.88 × 0.7 + ... = 0.769
```

**Advantages:**

- ✅ Linguistic rules capture human reasoning ("IF name match is HIGH THEN...")
- ✅ Handles uncertainty with membership degrees
- ✅ Non-linear inference adapts to context
- ✅ Strong match in one field can compensate for weak matches elsewhere
- ✅ More interpretable (can explain "why" a product ranked high)

---

## 💡 Key Insights

### Why Fuzzy Logic?

1. **Natural Language Reasoning**

   - Rules use human-understandable terms: "high", "medium", "poor"
   - Easier to tune and explain than black-box ML models

2. **Uncertainty Handling**

   - Gracefully handles imprecise inputs
   - Partial matches get partial credit (e.g., μ = 0.67 instead of 0 or 1)

3. **Non-linear Relationships**

   - Can model complex interactions between features
   - "High name match + good category" has synergistic effect

4. **Robustness**
   - Doesn't break with boundary cases
   - Smooth transitions between linguistic terms

### When to Use Fuzzy Logic?

**Best for:**

- ✅ Problems with linguistic/qualitative inputs
- ✅ Systems requiring interpretability
- ✅ Handling uncertainty and imprecision
- ✅ Rule-based expert systems

**Not ideal for:**

- ❌ Problems with clear mathematical models
- ❌ Large-scale ML with training data
- ❌ Real-time systems requiring extreme speed

---

## 🔬 Future Enhancements

1. **Adaptive Rules**

   - Learn rule weights from user feedback
   - A/B test different rule configurations

2. **Type-2 Fuzzy Logic**

   - Handle uncertainty in membership functions themselves
   - More robust to noise

3. **Sugeno Inference**

   - Faster defuzzification (weighted average)
   - Better for high-dimensional spaces

4. **Fuzzy Clustering**
   - Group products into fuzzy categories
   - Soft product classification

---

## 📖 Implementation Details

### File: `custom_recommendation_engine.py`

**Key Methods:**

- `_init_fuzzy_system()`: Initialize membership functions and rules
- `_membership_function()`: Calculate μ(x) for trimf/trapmf
- `_fuzzify()`: Convert crisp → fuzzy
- `_evaluate_rule()`: Apply single rule with MIN operator
- `_defuzzify_centroid()`: Fuzzy → crisp using centroid
- `fuzzy_inference()`: Complete Mamdani inference pipeline
- `search_products()`: Main search with fuzzy logic

### Usage Example:

```python
fuzzy_search = CustomFuzzySearch()

# Calculate text similarities
name_score = 0.85
category_score = 0.90

# Apply fuzzy inference
relevance = fuzzy_search.fuzzy_inference(
    name_score=name_score,
    category_score=category_score,
    price_score=0.80
)

print(f"Fuzzy Relevance: {relevance}")  # 0.88
```

---

## 📚 Additional Reading

1. **Zadeh, L.A. (1965)**. "Fuzzy Sets". Information and Control, 8(3), 338-353.
2. **Mamdani, E.H., Assilian, S. (1975)**. "An Experiment in Linguistic Synthesis with a Fuzzy Logic Controller". International Journal of Man-Machine Studies, 7(1), 1-13.
3. **Ross, T.J. (2010)**. "Fuzzy Logic with Engineering Applications", 3rd edition. Wiley.
4. **Jang, J.-S.R., Sun, C.-T., Mizutani, E. (1997)**. "Neuro-Fuzzy and Soft Computing". Prentice Hall.
5. **Klir, G.J., Yuan, B. (1995)**. "Fuzzy Sets and Fuzzy Logic: Theory and Applications". Prentice Hall.

---

**Last Updated:** 2025-01-08  
**Implementation:** `backend/home/custom_recommendation_engine.py` (Lines 243-676)  
**View:** `backend/home/sentiment_views.py` (FuzzySearchAPIView)  
**Frontend:** `frontend/src/components/Navbar/SearchModal.jsx`
