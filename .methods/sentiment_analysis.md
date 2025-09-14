To be corrected: 14/09/2025

# 🧠 Sentiment Analysis in Product Search

## What Is "Sentiment-Based Search" in the Shop?

Sentiment-based search is an intelligent product discovery algorithm that:

- **Analyzes customer reviews** using Natural Language Processing with **custom implementation**
- **Calculates sentiment scores** for each product (-1 to +1) using **SentiWordNet formula**
- **Ranks search results** by customer satisfaction
- **Prioritizes positively reviewed products** in search results
- **Helps customers find products others love**

This system makes the shop smarter by surfacing products with the best customer experiences, leading to higher customer satisfaction and increased sales.

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

### 4. `SentimentSearchAPIView` – 🔍 **Search Integration**

Powers the sentiment-based search functionality:

- Accepts search queries from users
- Matches products against search terms
- Orders results by `average_sentiment_score` (highest first)
- Includes sentiment data in search results

### 5. `SearchModal.jsx` Component – 👁️ **User Interface**

Displays the sentiment search interface to users:

- Provides real-time search results
- Shows sentiment scores alongside products
- Allows toggling between sentiment and fuzzy search modes

---

## 🤖 How Sentiment Analysis Works (Step by Step)

### 1. **Opinion Processing (CustomSentimentAnalysis)**:

```python
# Real SentiWordNet formula implemented in CustomSentimentAnalysis.analyze_sentiment()
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

    # SentiWordNet Formula: (Pos_Score - Neg_Score) / Total_Words
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

### 2. **Product Summary Calculation**:

```python
# In CustomSentimentAnalysis.analyze_product_sentiment()
For each product:
    - Calculate average sentiment score across all opinions
    - Count positive, neutral, and negative opinions
    - Store aggregate metrics in ProductSentimentSummary
```

### 3. **Search Process**:

```python
# In SentimentSearchAPIView
When user searches:
    - Find products matching search query text
    - Join with sentiment_summary data
    - Sort by average_sentiment_score (descending)
    - Return enriched product data with sentiment metrics
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
# Polarity Score (Liu, Bing 2012)
polarity = (positive_count - negative_count) / total_words

# Subjectivity Score (TextBlob approach)
subjectivity = subjective_words / total_words
```

### Database Optimization:

- OneToOne relationships for efficient joins
- Custom indexes on frequently queried fields
- Prefetching related data to minimize database queries

### Performance Considerations:

- Sentiment calculation performed once during opinion creation/update
- Pre-aggregated summaries for fast search ranking
- `select_related` and `prefetch_related` for efficient queries

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

## 📈 Example Sentiment Analysis Metrics

| Product            | Avg. Sentiment | Positive | Neutral | Negative | Total Opinions |
| ------------------ | -------------- | -------- | ------- | -------- | -------------- |
| Premium Headphones | 0.876          | 45       | 5       | 2        | 52             |
| Basic Keyboard     | 0.342          | 12       | 8       | 3        | 23             |
| Gaming Mouse       | 0.654          | 28       | 7       | 4        | 39             |
| Laptop Stand       | -0.123         | 5        | 4       | 12       | 21             |

---

## 🔧 Code Location

### Backend Files:

- `custom_recommendation_engine.py` → `CustomSentimentAnalysis` class
- `models.py` → `SentimentAnalysis`, `ProductSentimentSummary` models
- `sentiment_views.py` → `SentimentSearchAPIView`
- `signals.py` → Automatic processing after opinion addition

### Frontend Files:

- `SearchModal.jsx` → Sentiment search interface
- `AdminStatistics.jsx` → Admin panel (algorithm status)

### Dictionaries Used:

- **200+ positive words**: excellent, great, amazing, wonderful, fantastic...
- **200+ negative words**: terrible, awful, horrible, bad, worst...
- **Intensifiers**: very, extremely, really, quite, totally...
- **Negations**: not, no, never, nothing, neither...
- **Bigrams**: "highly recommend", "love it", "terrible quality"...
