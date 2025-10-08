/* eslint-disable react-hooks/exhaustive-deps */
import { useState, useEffect } from "react";
import { AiOutlineSearch, AiOutlineInfoCircle } from "react-icons/ai";
import axios from "axios";
import config from "../../config/config";
import "./SearchModal.scss";

const SearchModal = ({ isOpen, onClose }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isAdvanced, setIsAdvanced] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [priceRange, setPriceRange] = useState("");
  const [fuzzyThreshold, setFuzzyThreshold] = useState(0.6);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchTerm && !isAdvanced) {
        performSentimentSearch();
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [searchTerm, isAdvanced]);

  const performSentimentSearch = async () => {
    setIsLoading(true);
    setError("");

    try {
      const response = await axios.get(
        `${config.apiUrl}/api/sentiment-search/?q=${searchTerm}`
      );
      setSearchResults(response.data);
    } catch (err) {
      setError("Error fetching search results");
      console.error("Search error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const performFuzzySearch = async () => {
    setIsLoading(true);
    setError("");

    try {
      const params = new URLSearchParams();
      params.append("q", searchTerm);
      if (priceRange) params.append("price_range", priceRange);
      params.append("fuzzy_threshold", fuzzyThreshold);

      const response = await axios.get(
        `${config.apiUrl}/api/fuzzy-search/?${params.toString()}`
      );
      setSearchResults(response.data);
    } catch (err) {
      setError("Error fetching search results");
      console.error("Search error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAdvancedSearch = (e) => {
    e.preventDefault();
    if (searchTerm) {
      performFuzzySearch();
    }
  };

  const handleProductClick = (productId) => {
    window.location.href = `/product/${productId}`;
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="search-modal-overlay" onClick={onClose}>
      <div
        className="search-modal-content"
        onClick={(e) => e.stopPropagation()}>
        <button
          className="search-modal-close"
          onClick={onClose}
          aria-label="Close Search Modal">
          ✕
        </button>

        <div className="search-modal-header">
          <h2>Search Products</h2>
          <div className="search-mode-info">
            {!isAdvanced && searchResults.length > 0 && (
              <div className="sentiment-info-tooltip">
                <button
                  className="info-icon"
                  type="button"
                  title="How Sentiment Analysis Works">
                  <AiOutlineInfoCircle />
                </button>
                <div className="tooltip-content">
                  <strong>Multi-Source Sentiment Analysis:</strong>
                  <p>Score = (Positive - Negative) / Total Words</p>
                  <p>
                    <small>📊 Analyzed from 5 sources:</small>
                    <br />
                    <small>👥 Opinions (40%) • 📝 Description (25%)</small>
                    <br />
                    <small>
                      🏷️ Name (15%) • 📋 Specs (12%) • 🗂️ Categories (8%)
                    </small>
                  </p>
                  <p>
                    <small>Range: -1.0 (negative) to +1.0 (positive)</small>
                  </p>
                  <p>
                    <small>
                      Source: Liu, B. (2012) - Sentiment Analysis and Opinion
                      Mining
                    </small>
                  </p>
                </div>
              </div>
            )}
            {isAdvanced && searchResults.length > 0 && (
              <div className="sentiment-info-tooltip">
                <button
                  className="info-icon"
                  type="button"
                  title="How Fuzzy Logic Works">
                  <AiOutlineInfoCircle />
                </button>
                <div className="tooltip-content">
                  <strong>Fuzzy Logic Inference System:</strong>
                  <p>🧠 Mamdani Fuzzy Inference (1975)</p>
                  <p>
                    <small>📐 Process:</small>
                    <br />
                    <small>1. Fuzzification: Crisp → Fuzzy Sets</small>
                    <br />
                    <small>2. Rule Evaluation: IF-THEN Rules</small>
                    <br />
                    <small>3. Aggregation: MAX Operator</small>
                    <br />
                    <small>4. Defuzzification: Centroid Method</small>
                  </p>
                  <p>
                    <small>🎯 Linguistic Variables:</small>
                    <br />
                    <small>• Name Match: very_low → very_high</small>
                    <br />
                    <small>• Category Match: poor → excellent</small>
                    <br />
                    <small>• Relevance: irrelevant → highly_relevant</small>
                  </p>
                  <p>
                    <small>
                      Source: Zadeh, L.A. (1965) - Fuzzy Sets Theory
                    </small>
                  </p>
                </div>
              </div>
            )}
            <button
              className="search-modal-toggle"
              onClick={() => setIsAdvanced(!isAdvanced)}>
              {isAdvanced ? "Sentiment Search" : "Fuzzy Logic Search"}
            </button>
          </div>
        </div>

        <form
          onSubmit={
            isAdvanced ? handleAdvancedSearch : (e) => e.preventDefault()
          }>
          <div className="search-modal-input-wrapper">
            <AiOutlineSearch className="search-modal-search-icon" />
            <input
              type="text"
              className="search-modal-input"
              placeholder={
                isAdvanced
                  ? "Search with fuzzy matching..."
                  : "Search products (sentiment-based)..."
              }
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              autoFocus
            />
          </div>

          {isAdvanced && (
            <div className="search-modal-advanced-options">
              <div className="search-modal-option">
                <label>Price Range Filter:</label>
                <select
                  value={priceRange}
                  onChange={(e) => setPriceRange(e.target.value)}
                  className="search-modal-select">
                  <option value="">All Price Ranges</option>
                  <option value="cheap">Cheap ({"<"} $100)</option>
                  <option value="medium">Medium ($100-$500)</option>
                  <option value="expensive">Expensive ({">"} $500)</option>
                </select>
              </div>

              <div className="search-modal-option">
                <label>Fuzzy Threshold:</label>
                <div className="search-modal-slider-wrapper">
                  <input
                    type="range"
                    min="0.3"
                    max="1.0"
                    step="0.1"
                    value={fuzzyThreshold}
                    onChange={(e) =>
                      setFuzzyThreshold(parseFloat(e.target.value))
                    }
                    className="search-modal-slider"
                  />
                  <span className="search-modal-slider-value">
                    {fuzzyThreshold.toFixed(1)}
                  </span>
                </div>
              </div>

              <button
                type="submit"
                className="search-modal-search-btn"
                disabled={!searchTerm}>
                Search with Fuzzy Logic
              </button>
            </div>
          )}
        </form>

        {isLoading && <div className="search-modal-loading">Searching...</div>}
        {error && <div className="search-modal-error">{error}</div>}

        <div className="search-modal-results">
          {searchResults.length > 0 ? (
            <div className="search-modal-results-list">
              {searchResults.map((product) => (
                <div
                  key={product.id}
                  className="search-modal-result-item"
                  onClick={() => handleProductClick(product.id)}>
                  {product.photos?.[0]?.path && (
                    <img
                      src={`${config.apiUrl}/media/${product.photos[0].path}`}
                      alt={product.name}
                      className="search-modal-result-image"
                    />
                  )}
                  <div className="search-modal-result-info">
                    <h3>{product.name}</h3>
                    <p className="search-modal-result-price">
                      ${product.price}
                    </p>
                    {isAdvanced && product.fuzzy_score && (
                      <div className="search-modal-fuzzy-logic">
                        <div className="fuzzy-main-score">
                          <strong>Fuzzy Logic Score:</strong>{" "}
                          {(product.fuzzy_score * 100).toFixed(0)}%
                        </div>
                        {product.fuzzy_relevance && (
                          <div className="fuzzy-inference-score">
                            <small>
                              🧠 Fuzzy Inference:{" "}
                              {(product.fuzzy_relevance * 100).toFixed(0)}%
                            </small>
                          </div>
                        )}
                        <div className="fuzzy-breakdown">
                          <small>
                            📝 Name: {(product.name_score * 100).toFixed(0)}% |
                            🗂️ Category:{" "}
                            {(product.category_score * 100).toFixed(0)}%
                          </small>
                        </div>
                      </div>
                    )}
                    {!isAdvanced && product.sentiment_score != null && (
                      <div className="search-modal-sentiment">
                        <div className="sentiment-score">
                          <strong>Sentiment Score:</strong>{" "}
                          {product.sentiment_score.toFixed(2)}
                          <span
                            className={`sentiment-badge ${
                              product.sentiment_score > 0.1
                                ? "positive"
                                : product.sentiment_score < -0.1
                                ? "negative"
                                : "neutral"
                            }`}>
                            {product.sentiment_score > 0.1
                              ? "😊 Positive"
                              : product.sentiment_score < -0.1
                              ? "😞 Negative"
                              : "😐 Neutral"}
                          </span>
                        </div>
                        {product.total_opinions > 0 && (
                          <div className="sentiment-details">
                            <span className="opinion-count">
                              📝 {product.total_opinions} opinion
                              {product.total_opinions !== 1 ? "s" : ""}
                            </span>
                            {(product.positive_count ||
                              product.negative_count ||
                              product.neutral_count) && (
                              <span className="opinion-breakdown">
                                👍 {product.positive_count || 0} | 👎{" "}
                                {product.negative_count || 0} | 😐{" "}
                                {product.neutral_count || 0}
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            searchTerm &&
            !isLoading && (
              <div className="search-modal-no-results">
                No products found for "{searchTerm}"
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchModal;
