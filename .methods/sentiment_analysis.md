To be corrected: 06/06/2025

# 🧠 Sentiment Analysis in Product Search

## What Is "Sentiment-Based Search" in Shop?

Sentiment-based search is an intelligent product discovery algorithm that:

- **Analyzes customer reviews** using Natural Language Processing
- **Calculates sentiment scores** for each product (-1 to +1)
- **Ranks search results** by customer satisfaction
- **Prioritizes positively reviewed products** in search results
- **Helps customers find products others love**

This system makes shop smarter by surfacing products with the best customer experiences, leading to higher customer satisfaction and increased sales.

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

### 3. `seed_sentiment_data()` Function – 🔄 **Analysis Engine**

Processes all opinions and generates sentiment data:

- Uses TextBlob for Natural Language Processing
- Calculates polarity scores for each opinion
- Categorizes opinions based on sentiment thresholds
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
- Allows toggling between search modes

---

## 🤖 How Sentiment Analysis Works (Step by Step)

### 1. **Opinion Processing**:

```
For each product:
    For each customer opinion:
        - Apply TextBlob NLP to opinion text
        - Calculate sentiment polarity score (-1 to +1)
        - Categorize as:
            * Positive if score > 0.05
            * Negative if score < -0.05
            * Neutral otherwise
        - Store individual analysis in SentimentAnalysis
```

### 2. **Product Summary Calculation**:

```
For each product:
    - Calculate average sentiment score across all opinions
    - Count positive, neutral, and negative opinions
    - Store aggregate metrics in ProductSentimentSummary
```

### 3. **Search Process**:

```
When user searches:
    - Find products matching search query text
    - Join with sentiment_summary data
    - Sort by average_sentiment_score (descending)
    - Return enriched product data with sentiment metrics
```

### 4. **Result Display**:

```
In search results:
    - Show product details (name, price, image)
    - Display sentiment score (e.g., 0.75)
    - Visually indicate sentiment level
```

---

## 📊 Technical Implementation Details

### Sentiment Classification Logic:

```python
if sentiment_score > 0.05:
    sentiment_category = 'positive'
elif sentiment_score < -0.05:
    sentiment_category = 'negative'
else:
    sentiment_category = 'neutral'
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
