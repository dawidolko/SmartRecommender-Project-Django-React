### Description of methods used in the project:

1. Collaborative Filtering (CF)

- Analyzes similarities between users (or between products) based on purchase history and ratings.
- In the project, it will be used to suggest products that other, similar customers have bought (User-Based CF) or products related to each other in the purchase history (Item-Based CF).

2. Content-Based Filtering (CBF)

- Focuses on product features (e.g. category, keywords, description).

- In the project, it will suggest products similar to those that the user has already liked/bought, based on the analysis of their attributes (e.g. TF-IDF in descriptions).

3. Probabilistic Models (Naive Bayes)

- Use data on users and products to estimate the probability of interest in a specific offer.
- In the project, they will help determine the probability with which a user will buy a given product, which will allow for better prioritization of recommendations.

4. Fuzzy Decision Systems (Fuzzy Logic)

- Introduces the concepts of "degree of belonging" (e.g. a product can be "a bit expensive" or "moderately cheap"), which allows for better reflection of subjective features.

- In the project, it will enable more flexible recommendation rules, e.g. combining attributes such as "low price" and "high quality" in order to select the best offers.

5. Sentiment-Based Recommendations

- Analyzes user opinions and reviews to determine their tone (positive/negative).

- In the project, it will allow to recommend products that collect mainly positive comments, while filtering those with negative opinions.

6. Association Rules

- Detect dependencies between products based on transaction analysis, which allows to identify products often purchased together.

- In the project, they allow to identify related products that can be recommended to customers.
