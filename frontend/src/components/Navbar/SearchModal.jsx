/* eslint-disable react-hooks/exhaustive-deps */
import { useState, useEffect } from "react";
import { AiOutlineClose, AiOutlineSearch } from "react-icons/ai";
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
        <button className="search-modal-close" onClick={onClose}>
          <AiOutlineClose />
        </button>

        <div className="search-modal-header">
          <h2>Search Products</h2>
          <button
            className="search-modal-toggle"
            onClick={() => setIsAdvanced(!isAdvanced)}>
            {isAdvanced ? "Sentiment Search" : "Fuzzy Search"}
          </button>
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
                      <div className="search-modal-score">
                        Fuzzy Match: {(product.fuzzy_score * 100).toFixed(0)}%
                      </div>
                    )}
                    {!isAdvanced && product.sentiment_score != null && (
                      <div className="search-modal-sentiment">
                        Sentiment Score: {product.sentiment_score.toFixed(2)}
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
