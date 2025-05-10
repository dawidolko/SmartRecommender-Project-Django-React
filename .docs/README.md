# .docs: Product Recommendation Platform Documentation

## Directory Structure

```
.docs/
├── .methods/
│   ├── collaborative_filtering.md
│   ├── content_based_filtering.md
│   ├── association_rules.md
│   ├── fuzzy_search.md
│   ├── sentiment_analysis.md
└── └── probabilistic_methods.md

```

## Documentation Contents

### .methods/database_schema.md

Comprehensive documentation of the 24-table database schema, organized into:

- Core Entities (`db_user`, `db_product`, `db_category`, `db_tag`)
- E-Commerce Functionality (`db_order`, `db_order_product`, etc.)
- Product Details (`db_photo_product`, `db_specification`, `db_opinion`)
- Recommendation Systems (`method_user_interactions`, `method_product_similarity`, etc.)
- Sentiment Analysis (`method_sentiment_analysis`, `method_product_sentiment_summary`)
- Probabilistic Models (`method_purchase_probability`, `method_sales_forecast`, etc.)

### .database/entity-relationship-diagram/erd.png

Detailed explanation of database relationships:

- User relationships (Orders, Opinions, etc.)
- Product relationships (Categories, Tags, Photos, etc.)
- Recommendation relationships (Similarities, Associations)
- Specialized relationships for ML functionality

### .methods/collaborative_filtering.md

Detailed explanation of Collaborative Filtering implementation:

- Methodology for both user-based and item-based approaches
- Implementation details using cosine similarity
- Related models and components
- Process flows and API integration

### .methods/content_based_filtering.md

Documentation of Content-Based Filtering:

- Feature extraction from product attributes
- User profile creation
- Similarity calculation for recommendations

### .methods/association_rules.md

Comprehensive guide to Association Rules implementation:

- Apriori algorithm for frequent itemset mining
- Support, confidence, and lift metrics
- ProductAssociation model structure
- Automatic rule generation via signals
- Frontend implementation for "Frequently Bought Together"

### .methods/fuzzy_search.md

Detailed documentation of the Fuzzy Search system:

- FuzzySearchAPIView implementation
- Similarity calculation methodology
- Price range filtering
- Weighted scoring across product attributes
- User controls for threshold adjustment

### .methods/sentiment_analysis.md

Explanation of sentiment-based recommendations:

- Opinion processing using TextBlob
- Sentiment categorization thresholds
- Product summary aggregation
- Integration with search functionality
- Frontend implementation of sentiment indicators

### .methods/probabilistic_methods.md

Detailed guide to probabilistic analytics:

- Purchase probability prediction
- Sales forecasting methodology
- User purchase pattern analysis
- Risk assessment techniques
- Admin dashboard integration

---
