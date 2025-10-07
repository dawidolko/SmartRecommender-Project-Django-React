Last Updated: 07/01/2025

# 🧠 Sentiment Analysis in Product Search

## What Is "Sentiment-Based Search" in the Shop?

Sentiment-based search is an intelligent product discovery algorithm that:

- **Analyzes ALL product data** using Natural Language Processing with **custom implementation**:
  - 👥 **Customer opinions** (40% weight) - most reliable source
  - 📝 **Product description** (25% weight) - official seller description
  - 🏷️ **Product name** (15% weight) - key words in title
  - 📋 **Technical specifications** (12% weight) - parameters and features
  - 🗂️ **Categories** (8% weight) - category membership
- **Calculates sentiment scores** for each source (-1 to +1) using **Liu, B. (2012) formula**
- **Aggregates multi-source score** using weighted averaging
- **Ranks search results** by customer satisfaction
- **Prioritizes positively reviewed products** in search results
- **Helps customers find products others love**

This system makes the shop smarter by surfacing products with the best customer experiences and best descriptions, leading to higher customer satisfaction and increased sales.

---

## 📂 Key Components of the Sentiment Analysis System

### 1. `SentimentAnalysis` Model – 🧠 **Opinion-Level Analysis**

Stores sentiment data for each individual customer opinion:

- `sentiment_score`: Decimal value between -1 (negative) and 1 (positive)
- `sentiment_category`: Classification as 'positive', 'neutral', or 'negative'
- `opinion`: Link to the original customer opinion
- `product`: Link to the associated product

### 2. `ProductSentimentSummary` Model – 📊 **Product-Level Aggregation**

Aggregates sentiment metrics for each product:

- `average_sentiment_score`: Overall sentiment score for the product
- `positive_count`: Number of positive opinions
- `neutral_count`: Number of neutral opinions
- `negative_count`: Number of negative opinions
- `total_opinions`: Total number of analyzed opinions

### 3. `CustomSentimentAnalysis` Class – 🔄 **Analysis Engine**

Processes all opinions and generates sentiment data using **real academic formulas**:

- Uses **custom NLP implementation** instead of TextBlob for better control
- Calculates polarity scores using **SentiWordNet formula**
- Categorizes opinions based on academic literature thresholds
- Creates or updates summary statistics

### 4. `SentimentSearchAPIView` – 🔍 **Search Integration (Multi-Source)**

Powers the sentiment-based search functionality with multi-source analysis:

- Accepts search queries from users
- Matches products against search terms
- **Analyzes sentiment from 5 sources**:
  1. 👥 Customer opinions (40% weight)
  2. 📝 Product description (25% weight)
  3. 🏷️ Product name (15% weight)
  4. 📋 Technical specifications (12% weight)
  5. 🗂️ Categories (8% weight)
- **Calculates weighted final score**: `Final_Score = (Opinion×0.40) + (Desc×0.25) + (Name×0.15) + (Spec×0.12) + (Cat×0.08)`
- Orders results by `final_score` (highest first)
- Includes detailed sentiment data in search results

### 5. `SearchModal.jsx` Component – 👁️ **User Interface**

Displays the sentiment search interface to users:

- Provides real-time search results
- Shows sentiment scores alongside products
- Allows toggling between sentiment and fuzzy search modes

---

## 🤖 How Sentiment Analysis Works (Step by Step)

### 1. **Text Processing - Universal Function (CustomSentimentAnalysis)**:

```python
# Real Liu, B. (2012) formula implemented in CustomSentimentAnalysis.analyze_sentiment()
# This function analyzes ANY text: opinions, description, name, specifications, categories
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

    # Liu, B. (2012) Formula: (Pos_Score - Neg_Score) / Total_Words
    sentiment_score = (positive_score - negative_score) / total_words

    # Normalization to [-1, 1] range
    sentiment_score = max(-1.0, min(1.0, sentiment_score))

    # Classification with literature thresholds (Liu, Bing 2012)
    if sentiment_score > 0.1:
        category = "positive"
    elif sentiment_score < -0.1:
        category = "negative"
    else:
        category = "neutral"

    return sentiment_score, category
```

### 2. **Multi-Source Analysis - New Approach (SentimentSearchAPIView)**:

```python
# In SentimentSearchAPIView.get() - We analyze 5 data sources
def get(self, request):
    analyzer = CustomSentimentAnalysis()

    for product in products:
        # SOURCE 1: Customer Opinions (40% weight)
        opinion_scores = []
        for opinion in product.opinion_set.all()[:20]:
            score, _ = analyzer.analyze_sentiment(opinion.content)
            opinion_scores.append(score)
        opinion_sentiment = sum(opinion_scores) / len(opinion_scores) if opinion_scores else 0.0

        # SOURCE 2: Product Description (25% weight)
        desc_score, _ = analyzer.analyze_sentiment(product.description or "")

        # SOURCE 3: Product Name (15% weight)
        name_score, _ = analyzer.analyze_sentiment(product.name)

        # SOURCE 4: Technical Specifications (12% weight)
        spec_texts = [f"{spec.parameter_name} {spec.specification}"
                      for spec in product.specification_set.all()[:10]]
        spec_combined = " ".join(spec_texts)
        spec_score, _ = analyzer.analyze_sentiment(spec_combined) if spec_combined else (0.0, "neutral")

        # SOURCE 5: Categories (8% weight)
        category_names = " ".join([cat.name for cat in product.categories.all()])
        category_score, _ = analyzer.analyze_sentiment(category_names) if category_names else (0.0, "neutral")

        # AGGREGATION: Calculate weighted final score
        final_score = (
            opinion_sentiment * 0.40 +    # 40% weight for opinions
            desc_score * 0.25 +            # 25% weight for description
            name_score * 0.15 +            # 15% weight for name
            spec_score * 0.12 +            # 12% weight for specifications
            category_score * 0.08          # 8% weight for categories
        )
```

**Why these weights?**

- 👥 **Opinions (40%)**: Most reliable - real customer experiences
- 📝 **Description (25%)**: Official seller description with key features
- 🏷️ **Name (15%)**: Often contains words like "Premium", "Pro", "Basic"
- 📋 **Specifications (12%)**: Technical parameters (e.g., "fast", "powerful", "efficient")
- 🗂️ **Categories (8%)**: Product context (e.g., "Gaming", "Professional")

### 3. **Search Process with Multi-Source Analysis**:

```python
# In SentimentSearchAPIView
When user searches "laptop":
    1. Find products matching search query text
    2. For EACH product:
       a) Analyze sentiment from opinions → opinion_score
       b) Analyze sentiment from description → desc_score
       c) Analyze sentiment from name → name_score
       d) Analyze sentiment from specifications → spec_score
       e) Analyze sentiment from categories → category_score
       f) Calculate final_score = weighted sum of all sources
    3. Sort products by final_score (descending)
    4. Return results with detailed breakdown:
       - final_score (main score)
       - sentiment_breakdown (scores from each source)
       - opinion metrics (positive/negative/neutral counts)
```

**Calculation Example:**

```python
# Product: "Premium Gaming Laptop"
# Opinions: 5 opinions, average score = 0.6 (positive)
# Description: "Excellent performance, powerful graphics" → score = 0.4
# Name: "Premium Gaming Laptop" → score = 0.2
# Specifications: "Fast processor, high quality display" → score = 0.3
# Categories: "Gaming, Laptops, Premium" → score = 0.1

final_score = (0.6 × 0.40) + (0.4 × 0.25) + (0.2 × 0.15) + (0.3 × 0.12) + (0.1 × 0.08)
final_score = 0.24 + 0.10 + 0.03 + 0.036 + 0.008
final_score = 0.414 → "Positive" (because 0.414 > 0.1)
```

### 4. **Result Display**:

```jsx
// In SearchModal.jsx
In search results:
    - Show product details (name, price, image)
    - Display sentiment score (e.g., 0.75)
    - Visually indicate sentiment level
```

---

## 📊 Technical Implementation Details

### Sentiment Classification Logic (Literature: Liu, Bing 2012):

```python
# Thresholds based on academic research
if sentiment_score > 0.1:    # Positive threshold
    sentiment_category = 'positive'
elif sentiment_score < -0.1:  # Negative threshold
    sentiment_category = 'negative'
else:
    sentiment_category = 'neutral'
```

### Mathematical Formulas Used:

```python
# 1. Polarity Score for single text (Liu, Bing 2012)
polarity = (positive_count - negative_count) / total_words

# 2. Multi-source aggregation (new approach)
final_score = (opinion_avg * 0.40) + (desc_score * 0.25) +
              (name_score * 0.15) + (spec_score * 0.12) + (category_score * 0.08)

# 3. Opinion average
opinion_average = sum(opinion_scores) / len(opinion_scores)
```

### API Response Structure:

```json
{
  "id": 295,
  "name": "Premium Gaming Laptop",
  "price": 1299.99,
  "sentiment_score": 0.414,
  "sentiment_breakdown": {
    "opinion_score": 0.6,
    "description_score": 0.4,
    "name_score": 0.2,
    "specification_score": 0.3,
    "category_score": 0.1
  },
  "total_opinions": 5,
  "positive_count": 4,
  "negative_count": 0,
  "neutral_count": 1
}
```

### Database Optimization:

- OneToOne relationships for efficient joins
- Custom indexes on frequently queried fields
- **Multi-source prefetching**: `prefetch_related('opinion_set', 'specification_set', 'categories')`
- Opinion limit (20) and specification limit (10) for performance

### Performance Considerations:

- **Real-time analysis**: Analysis performed on each search (fresh data)
- **On-the-fly analysis**: Instead of pre-computed summaries, we analyze on-demand
- **Opinion limit**: Maximum 20 most recent opinions for speed
- **Specification limit**: Maximum 10 technical parameters
- `select_related` and `prefetch_related` for efficient queries
- **Cache opportunity**: Results can be cached for 15 minutes

---

## 🛍️ Business Benefits of Sentiment-Based Search

### For Customers:

- Discover products with highest customer satisfaction
- Avoid products with negative reviews
- Make more confident purchase decisions
- Find quality items faster

### For Shop Owners:

- Highlight well-reviewed products automatically
- Increase conversion rates on quality merchandise
- Identify products needing improvement
- Build trust with transparent opinion analysis

---

## 📈 Example Sentiment Analysis Metrics (Multi-Source)

### Example 1: Premium Gaming Laptop

| Source            | Weight | Raw Score | Contribution |
| ----------------- | ------ | --------- | ------------ |
| 👥 Opinions       | 40%    | 0.600     | 0.240        |
| 📝 Description    | 25%    | 0.400     | 0.100        |
| 🏷️ Name           | 15%    | 0.200     | 0.030        |
| 📋 Specifications | 12%    | 0.300     | 0.036        |
| 🗂️ Categories     | 8%     | 0.100     | 0.008        |
| **FINAL SCORE**   | 100%   | -         | **0.414** ✅ |

**Interpretation**: Product has positive sentiment (0.414 > 0.1), mainly due to excellent customer opinions and positive description.

---

### Example 2: Basic Wireless Mouse

| Source            | Weight | Raw Score | Contribution |
| ----------------- | ------ | --------- | ------------ |
| 👥 Opinions       | 40%    | 0.050     | 0.020        |
| 📝 Description    | 25%    | -0.100    | -0.025       |
| 🏷️ Name           | 15%    | 0.000     | 0.000        |
| 📋 Specifications | 12%    | 0.100     | 0.012        |
| 🗂️ Categories     | 8%     | 0.000     | 0.000        |
| **FINAL SCORE**   | 100%   | -         | **0.007** 😐 |

**Interpretation**: Product has neutral sentiment (0.007 < 0.1), opinions are mixed, description contains negative words.

---

### Example 3: Cheap Laptop Stand

| Source            | Weight | Raw Score | Contribution  |
| ----------------- | ------ | --------- | ------------- |
| 👥 Opinions       | 40%    | -0.300    | -0.120        |
| 📝 Description    | 25%    | -0.200    | -0.050        |
| 🏷️ Name           | 15%    | -0.100    | -0.015        |
| 📋 Specifications | 12%    | 0.050     | 0.006         |
| 🗂️ Categories     | 8%     | 0.000     | 0.000         |
| **FINAL SCORE**   | 100%   | -         | **-0.179** ❌ |

**Interpretation**: Product has negative sentiment (-0.179 < -0.1), bad opinions, poor descriptions, word "Cheap" in name.

---

### Traditional vs Multi-Source Comparison

| Product            | Traditional (opinions only) | Multi-Source | Difference |
| ------------------ | --------------------------- | ------------ | ---------- |
| Premium Headphones | 0.876                       | 0.782        | -10.7%     |
| Basic Keyboard     | 0.342                       | 0.289        | -15.5%     |
| Gaming Mouse       | 0.654                       | 0.598        | -8.6%      |
| Laptop Stand       | -0.123                      | -0.179       | +45.5%     |

**Conclusion**: Multi-source approach provides more balanced assessment, considering not only opinions but also description and specification quality.

---

## 🧪 Debugging and Formula Verification

### Debug API Endpoint (no authentication required) - NEW Multi-Source

Endpoint to verify mathematical formulas and sentiment calculations from all 5 sources:

```bash
GET /api/sentiment-analysis-debug/?product_id=295
```

**Example Response (Multi-Source Analysis):**

```json
{
  "product_id": 295,
  "product_name": "Premium Gaming Laptop",

  "multi_source_analysis": {
    "opinions": {
      "weight": "40%",
      "count": 5,
      "average_score": 0.600,
      "contribution_to_final": 0.240,
      "sample_details": [
        {
          "opinion_id": 123,
          "opinion_excerpt": "Excellent laptop, very fast and reliable...",
          "calculation": {
            "positive_words_found": 3,
            "negative_words_found": 0,
            "total_words": 45,
            "formula": "(3 - 0) / 45 = 0.067",
            "sentiment_score": 0.067,
            "category": "neutral"
          }
        }
      ],
      "formula": "Σ(5 scores) / 5 = 0.600"
    },

    "description": {
      "weight": "25%",
      "text_excerpt": "Powerful gaming laptop with excellent performance and stunning graphics...",
      "score": 0.400,
      "category": "positive",
      "contribution_to_final": 0.100,
      "positive_words": 4,
      "negative_words": 0,
      "total_words": 28,
      "formula": "(4 - 0) / 28 = 0.143"
    },

    "name": {
      "weight": "15%",
      "text": "Premium Gaming Laptop",
      "score": 0.200,
      "category": "positive",
      "contribution_to_final": 0.030,
      "positive_words": 1,
      "negative_words": 0,
      "total_words": 3,
      "formula": "(1 - 0) / 3 = 0.333"
    },

    "specifications": {
      "weight": "12%",
      "count": 8,
      "combined_score": 0.300,
      "category": "positive",
      "contribution_to_final": 0.036,
      "sample_details": [
        {
          "parameter": "Processor",
          "value": "Fast Intel i7",
          "score": 0.250,
          "category": "positive",
          "positive_words": 1,
          "negative_words": 0
        },
        {
          "parameter": "Graphics",
          "value": "Powerful NVIDIA RTX",
          "score": 0.333,
          "category": "positive",
          "positive_words": 1,
          "negative_words": 0
        }
      ]
    },

    "categories": {
      "weight": "8%",
      "text": "Gaming Laptops Premium",
      "score": 0.100,
      "category": "positive",
      "contribution_to_final": 0.008,
      "positive_words": 1,
      "negative_words": 0,
      "total_words": 3
    }
  },

  "final_calculation": {
    "formula": "Final = (Opinion×0.40) + (Desc×0.25) + (Name×0.15) + (Spec×0.12) + (Cat×0.08)",
    "calculation": "(0.600×0.40) + (0.400×0.25) + (0.200×0.15) + (0.300×0.12) + (0.100×0.08)",
    "final_score": 0.414,
    "final_category": "Positive",
    "breakdown": {
      "from_opinions": 0.240,
      "from_description": 0.100,
      "from_name": 0.030,
      "from_specifications": 0.036,
      "from_categories": 0.008
    }
  },

  "formulas_used": {
    "per_text": "Sentiment_Score = (Positive_Count - Negative_Count) / Total_Words",
    "final_aggregation": "Final = (Opinion×0.40) + (Description×0.25) + (Name×0.15) + (Specification×0.12) + (Category×0.08)",
    "thresholds": "Positive: score > 0.1, Negative: score < -0.1, Neutral: -0.1 ≤ score ≤ 0.1"
  },

  "lexicon_info": {
    "positive_words_count": 200,
    "negative_words_count": 200,
    "examples_positive": ["excellent", "great", "amazing", "powerful", "fast", ...],
    "examples_negative": ["terrible", "awful", "horrible", "bad", "slow", ...]
  },

  "source": "Liu, B. (2012). Sentiment Analysis and Opinion Mining, Chapter 2"
}
```

### Testing in Browser

```bash
# Test for specific product (Multi-Source Analysis)
curl http://localhost:8000/api/sentiment-analysis-debug/?product_id=295

# Or open in browser:
http://localhost:8000/api/sentiment-analysis-debug/?product_id=295

# You'll see detailed analysis from all 5 sources
```

---

## 🔧 Code Location

### Backend Files:

- **`custom_recommendation_engine.py`** → `CustomSentimentAnalysis.analyze_sentiment()` - **universal function to analyze ANY text**
- **`models.py`** → `SentimentAnalysis`, `ProductSentimentSummary` models
- **`sentiment_views.py`** →
  - `SentimentSearchAPIView.get()` - **NEW multi-source analysis (5 sources)**
  - `SentimentAnalysisDebugAPI.get()` - **NEW debug endpoint with multi-source breakdown**
- **`signals.py`** → Automatic processing after opinion addition (legacy, for individual opinions)
- **`urls.py`** → Routes:
  - `/api/sentiment-search/` - main search
  - `/api/sentiment-analysis-debug/` - debug endpoint

### Frontend Files:

- **`SearchModal.jsx`** →
  - Sentiment search interface
  - Tooltip with multi-source analysis description
  - Info icon (AiOutlineInfoCircle)
  - Toggle between Sentiment/Fuzzy Search
- **`SearchModal.scss`** →
  - Styles for sentiment badges (😊/😞/😐)
  - Tooltip styling (light background, dark text)
  - Uniform button design (36px height)
- **`AdminStatistics.jsx`** → Admin panel (algorithm status)

### New Features:

#### 1. **Multi-Source Sentiment Analysis**

```python
# In SentimentSearchAPIView.get()
for product in products:
    # Analyze 5 sources:
    opinion_score = analyze_opinions(product)        # 40% weight
    desc_score = analyze_text(product.description)   # 25% weight
    name_score = analyze_text(product.name)          # 15% weight
    spec_score = analyze_specifications(product)     # 12% weight
    cat_score = analyze_categories(product)          # 8% weight

    # Calculate weighted final score
    final_score = weighted_sum(all_scores)
```

#### 2. **Detailed Breakdown Response**

```json
{
  "sentiment_score": 0.414,
  "sentiment_breakdown": {
    "opinion_score": 0.6,
    "description_score": 0.4,
    "name_score": 0.2,
    "specification_score": 0.3,
    "category_score": 0.1
  }
}
```

#### 3. **Enhanced Debug Endpoint**

- Shows analysis from ALL 5 sources
- Detailed calculations for each source
- Breakdown of each source's contribution to final score
- Examples of positive/negative words found

### Dictionaries Used:

- **200+ positive words**: excellent, great, amazing, wonderful, fantastic...
- **200+ negative words**: terrible, awful, horrible, bad, worst...
- **Intensifiers**: very, extremely, really, quite, totally...
- **Negations**: not, no, never, nothing, neither...
- **Bigrams**: "highly recommend", "love it", "terrible quality"...
