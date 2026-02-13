import React, { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import {
  Code,
  Brain,
  MessageSquare,
  Link2,
  Grid,
  Sparkles,
  TrendingUp,
} from "lucide-react";
import config from "../../config/config";
import { toast } from "react-toastify";
import "./AdminPanel.scss";

/**
 * AdminDebug Component
 *
 * Comprehensive debugging interface for SmartRecommender's recommendation algorithms.
 * Provides detailed diagnostic information, performance metrics, and algorithm visualization
 * for all recommendation strategies implemented in the system.
 *
 * Supported Algorithms:
 *   1. Collaborative Filtering (CF) - Adjusted Cosine Similarity (Sarwar et al., 2001)
 *      Formula: sim(i,j) = Σ(R_u,i - R̄_u)(R_u,j - R̄_u) / √[Σ(R_u,i - R̄_u)² × Σ(R_u,j - R̄_u)²]
 *
 *   2. Sentiment Analysis - TextBlob polarity scoring
 *      Formula: sentiment = (positive_words - negative_words) / total_words
 *
 *   3. Content-Based Filtering - TF-IDF + Cosine Similarity
 *      Formula: cos(θ) = (A · B) / (||A|| × ||B||)
 *
 *   4. Association Rules - Apriori Algorithm (Agrawal & Srikant, 1994)
 *      Metrics: Support, Confidence, Lift
 *
 *   5. Fuzzy Logic - Membership functions + Defuzzification
 *      Methods: Triangular, Trapezoidal, Gaussian membership
 *
 *   6. Probabilistic Models - Naive Bayes, Markov Chains
 *      Formulas: P(A|B) = P(B|A)P(A) / P(B)
 *
 * Features:
 *   - Real-time algorithm diagnostics
 *   - Matrix visualization and statistics
 *   - Performance metrics tracking
 *   - Cache monitoring
 *   - Interactive debugging tools
 *   - Modal views for detailed data
 *   - Pagination for large datasets
 *
 * @component
 * @returns {React.ReactElement} Admin debug dashboard with tabbed interface
 */
const AdminDebug = () => {
  // ============================================================================
  // STATE MANAGEMENT
  // ============================================================================

  /** @type {[string, Function]} Active debugging tab/method */
  const [activeMethod, setActiveMethod] = useState("collaborative");

  /** @type {[Object|null, Function]} Collaborative filtering debug data */
  const [cfDebugData, setCfDebugData] = useState(null);

  /** @type {[Object|null, Function]} Sentiment analysis debug data */
  const [sentimentDebugData, setSentimentDebugData] = useState(null);

  /** @type {[Object|null, Function]} Detailed sentiment data for specific product */
  const [sentimentDetailData, setSentimentDetailData] = useState(null);

  /** @type {[Object|null, Function]} Association rules debug data */
  const [associationDebugData, setAssociationDebugData] = useState(null);

  /** @type {[Object|null, Function]} Content-based filtering debug data */
  const [contentBasedDebugData, setContentBasedDebugData] = useState(null);

  /** @type {[Object|null, Function]} Fuzzy logic debug data */
  const [fuzzyLogicDebugData, setFuzzyLogicDebugData] = useState(null);

  /** @type {[Object|null, Function]} Probabilistic models debug data */
  const [probabilisticDebugData, setProbabilisticDebugData] = useState(null);

  /** @type {[string, Function]} Selected product ID for detail views */
  const [selectedProductId, setSelectedProductId] = useState("");

  /** @type {[string, Function]} Selected user ID for detail views */
  const [selectedUserId, setSelectedUserId] = useState("");

  /** @type {[Array, Function]} List of all products */
  const [users, setUsers] = useState([]);

  /** @type {[Array, Function]} List of all users */
  const [products, setProducts] = useState([]);

  /** @type {[boolean, Function]} Loading state for async operations */
  const [loading, setLoading] = useState(false);

  // Modal state for all similarities view
  /** @type {[boolean, Function]} Modal visibility toggle */
  const [showAllSimilaritiesModal, setShowAllSimilaritiesModal] =
    useState(false);

  /** @type {[Array, Function]} All CF similarities data */
  const [allSimilarities, setAllSimilarities] = useState([]);

  /** @type {[boolean, Function]} Loading state for similarities fetch */
  const [allSimilaritiesLoading, setAllSimilaritiesLoading] = useState(false);

  /** @type {[number, Function]} Current page number for pagination */
  const [similaritiesPage, setSimilaritiesPage] = useState(1);

  /** @const {number} Items per page in similarities modal */
  const similaritiesPerPage = 50;

  // ============================================================================
  // LIFECYCLE HOOKS
  // ============================================================================

  /**
   * Initialize component by fetching reference data (products and users).
   * Runs once on component mount.
   */
  useEffect(() => {
    fetchProducts();
    fetchUsers();
  }, []);

  /**
   * Handle tab switching and fetch appropriate debug data.
   * Resets selections and fetches new data when active method changes.
   */
  useEffect(() => {
    setSelectedProductId("");
    setSelectedUserId("");
    setSentimentDetailData(null);
    setAssociationDebugData(null);
    setContentBasedDebugData(null);
    setFuzzyLogicDebugData(null);
    setProbabilisticDebugData(null);

    if (activeMethod === "collaborative") {
      fetchCFDebug();
    } else if (activeMethod === "sentiment") {
      fetchSentimentDebug();
    } else if (activeMethod === "content") {
      fetchContentBasedDebug();
    } else if (activeMethod === "fuzzy") {
      fetchFuzzyLogicDebug();
    } else if (activeMethod === "probabilistic") {
      fetchProbabilisticDebug();
    }
  }, [activeMethod]);

  // ============================================================================
  // DATA FETCHING FUNCTIONS
  // ============================================================================

  /**
   * Fetch all products from the database.
   * Used for dropdown selections and reference data.
   *
   * @async
   * @function fetchProducts
   * @returns {Promise<void>}
   */
  const fetchProducts = async () => {
    try {
      const token = localStorage.getItem("access");
      const res = await axios.get(`${config.apiUrl}/api/products/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setProducts(res.data.results || res.data || []);
    } catch (err) {
      console.error("Error fetching products:", err);
    }
  };

  /**
   * Fetch all users from the database.
   * Used for dropdown selections and reference data.
   *
   * @async
   * @function fetchUsers
   * @returns {Promise<void>}
   */
  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem("access");
      const res = await axios.get(`${config.apiUrl}/api/users/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers(res.data || []);
    } catch (err) {
      console.error("Error fetching users:", err);
    }
  };

  /**
   * Fetch Collaborative Filtering debug information.
   *
   * Retrieves detailed CF algorithm diagnostics including:
   *   - User-product interaction matrix statistics
   *   - Similarity computation results
   *   - Top 10 similar product pairs
   *   - Cache status
   *   - System health indicators
   *
   * Algorithm: Adjusted Cosine Similarity (Sarwar et al., 2001)
   * Formula: sim(i,j) = Σ_u∈U(R_u,i - R̄_u)(R_u,j - R̄_u) / √[Σ_u∈U(R_u,i - R̄_u)² × Σ_u∈U(R_u,j - R̄_u)²]
   *
   * @async
   * @function fetchCFDebug
   * @returns {Promise<void>}
   */
  const fetchCFDebug = async () => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        `${config.apiUrl}/api/collaborative-filtering-debug/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );
      setCfDebugData(res.data);
    } catch (err) {
      console.error("Error fetching CF debug:", err);
      toast.error("Failed to fetch Collaborative Filtering debug data.");
    } finally {
      setLoading(false);
    }
  };

  /**
   * Fetch all Collaborative Filtering similarities from database.
   *
   * Retrieves complete list of product-product similarities computed using
   * Adjusted Cosine Similarity algorithm. Used for detailed analysis and
   * modal view with pagination.
   *
   * Features:
   *   - Fetches up to 10,000 similarity records
   *   - Formats data for modal table display
   *   - Handles empty results gracefully
   *   - Provides user feedback via toasts
   *
   * @async
   * @function fetchAllSimilarities
   * @returns {Promise<void>}
   */
  const fetchAllSimilarities = async () => {
    setAllSimilaritiesLoading(true);
    const token = localStorage.getItem("access");
    try {
      // Fetch all collaborative filtering similarities from dedicated endpoint
      const res = await axios.get(
        `${config.apiUrl}/api/all-collaborative-similarities/?limit=10000`,
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );

      // Format data for modal table structure
      const formattedSimilarities = res.data.results
        ? res.data.results.map((sim) => ({
            product1_id: sim.product1?.id,
            product1_name: sim.product1?.name || "Unknown Product",
            product2_id: sim.product2?.id,
            product2_name: sim.product2?.name || "Unknown Product",
            score: sim.similarity_score,
          }))
        : [];

      setAllSimilarities(formattedSimilarities);

      if (formattedSimilarities.length === 0) {
        toast.info("No collaborative similarities found in database.");
      }
    } catch (err) {
      console.error("Error fetching all similarities:", err);
      toast.error("Failed to fetch all similarities.");
      setAllSimilarities([]);
    } finally {
      setAllSimilaritiesLoading(false);
    }
  };

  /**
   * Open modal displaying all CF similarities.
   *
   * Triggers data fetch if not already loaded. Modal displays paginated
   * table of all product-product similarity scores.
   *
   * @function openAllSimilaritiesModal
   * @returns {void}
   */
  const openAllSimilaritiesModal = () => {
    setShowAllSimilaritiesModal(true);
    if (allSimilarities.length === 0) {
      fetchAllSimilarities();
    }
  };

  /**
   * Close similarities modal and reset pagination.
   *
   * @function closeAllSimilaritiesModal
   * @returns {void}
   */
  const closeAllSimilaritiesModal = () => {
    setShowAllSimilaritiesModal(false);
    setSimilaritiesPage(1);
  };

  const fetchSentimentDebug = async () => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        `${config.apiUrl}/api/sentiment-analysis-debug/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );
      setSentimentDebugData(res.data);
    } catch (err) {
      console.error("Error fetching Sentiment debug:", err);
      toast.error("Failed to fetch Sentiment Analysis debug data.");
    } finally {
      setLoading(false);
    }
  };

  const fetchSentimentDetailDebug = async (productId) => {
    if (!productId) return;
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        `${config.apiUrl}/api/sentiment-product-debug/?product_id=${productId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );
      setSentimentDetailData(res.data);
    } catch (err) {
      console.error("Error fetching Sentiment detail debug:", err);
      toast.error("Failed to fetch detailed sentiment analysis.");
    } finally {
      setLoading(false);
    }
  };

  const fetchAssociationDebug = async (productId) => {
    if (!productId) return;
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        `${config.apiUrl}/api/product-association-debug/?product_id=${productId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );
      setAssociationDebugData(res.data);
    } catch (err) {
      console.error("Error fetching Association debug:", err);
      toast.error("Failed to fetch Association Rules debug data.");
    } finally {
      setLoading(false);
    }
  };

  const fetchContentBasedDebug = async (productId = null) => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      const url = productId
        ? `${config.apiUrl}/api/content-based-debug/?product_id=${productId}`
        : `${config.apiUrl}/api/content-based-debug/`;
      const res = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setContentBasedDebugData(res.data);
    } catch (err) {
      console.error("Error fetching Content-Based debug:", err);
      toast.error("Failed to fetch Content-Based Filtering debug data.");
    } finally {
      setLoading(false);
    }
  };

  const fetchFuzzyLogicDebug = async (productId = null, userId = null) => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      let url = `${config.apiUrl}/api/fuzzy-logic-debug/?`;
      if (productId) url += `product_id=${productId}&`;
      if (userId) url += `user_id=${userId}`;

      const res = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setFuzzyLogicDebugData(res.data);
    } catch (err) {
      console.error("Error fetching Fuzzy Logic debug:", err);
      toast.error("Failed to fetch Fuzzy Logic debug data.");
    } finally {
      setLoading(false);
    }
  };

  const fetchProbabilisticDebug = async (productId = null, userId = null) => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      let url = `${config.apiUrl}/api/probabilistic-debug/?`;
      if (productId) url += `product_id=${productId}&`;
      if (userId) url += `user_id=${userId}`;

      const res = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setProbabilisticDebugData(res.data);
    } catch (err) {
      console.error("Error fetching Probabilistic debug:", err);
      toast.error("Failed to fetch Probabilistic Models debug data.");
    } finally {
      setLoading(false);
    }
  };

  const handleProductSelect = (e) => {
    const productId = e.target.value;
    setSelectedProductId(productId);
    if (productId) {
      if (activeMethod === "sentiment") {
        fetchSentimentDetailDebug(productId);
      } else if (activeMethod === "association") {
        fetchAssociationDebug(productId);
      } else if (activeMethod === "content") {
        fetchContentBasedDebug(productId);
      } else if (activeMethod === "fuzzy") {
        fetchFuzzyLogicDebug(productId, selectedUserId);
      } else if (activeMethod === "probabilistic") {
        fetchProbabilisticDebug(productId, selectedUserId);
      }
    }
  };

  const handleUserSelect = (e) => {
    const userId = e.target.value;
    setSelectedUserId(userId);
    if (activeMethod === "fuzzy") {
      fetchFuzzyLogicDebug(selectedProductId, userId);
    } else if (activeMethod === "probabilistic") {
      fetchProbabilisticDebug(selectedProductId, userId);
    }
  };

  return (
    <div className="debug-container">
      <motion.div
        className="debug-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}>
        <h1 className="debug-title">
          <Code className="debug-icon" />
          Debug Tools - ML Methods Inspector
        </h1>
        <p className="debug-description">
          Inspect internal workings of all 7 machine learning methods used in
          SmartRecommender.
        </p>
      </motion.div>

      <motion.div
        className="method-selector"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}>
        <button
          className={`method-tab ${
            activeMethod === "collaborative" ? "active" : ""
          }`}
          onClick={() => setActiveMethod("collaborative")}>
          <Brain className="tab-icon" />
          Collaborative Filtering
        </button>
        <button
          className={`method-tab ${
            activeMethod === "sentiment" ? "active" : ""
          }`}
          onClick={() => setActiveMethod("sentiment")}>
          <MessageSquare className="tab-icon" />
          Sentiment Analysis
        </button>
        <button
          className={`method-tab ${
            activeMethod === "association" ? "active" : ""
          }`}
          onClick={() => setActiveMethod("association")}>
          <Link2 className="tab-icon" />
          Association Rules
        </button>
        <button
          className={`method-tab ${activeMethod === "content" ? "active" : ""}`}
          onClick={() => setActiveMethod("content")}>
          <Grid className="tab-icon" />
          Content-Based
        </button>
        <button
          className={`method-tab ${activeMethod === "fuzzy" ? "active" : ""}`}
          onClick={() => setActiveMethod("fuzzy")}>
          <Sparkles className="tab-icon" />
          Fuzzy Logic
        </button>
        <button
          className={`method-tab ${
            activeMethod === "probabilistic" ? "active" : ""
          }`}
          onClick={() => setActiveMethod("probabilistic")}>
          <TrendingUp className="tab-icon" />
          Probabilistic
        </button>
      </motion.div>

      <motion.div
        className="debug-content"
        key={activeMethod}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3 }}>
        {loading ? (
          <div className="debug-loading">Loading debug data...</div>
        ) : (
          <>
            {activeMethod === "collaborative" && (
              <div className="debug-section cf-debug">
                <h2 className="section-title">
                  Collaborative Filtering Debug Information
                </h2>

                {cfDebugData ? (
                  <>
                    {cfDebugData.algorithm && (
                      <div className="debug-card">
                        <h3>Algorithm</h3>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Name:</span>
                            <span className="value">
                              {cfDebugData.algorithm}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Formula:</span>
                            <span className="value">{cfDebugData.formula}</span>
                          </div>
                          <div className="info-row">
                            <span className="label">Status:</span>
                            <span className="value success">
                              {cfDebugData.status}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {cfDebugData.database_stats && (
                      <div className="debug-card">
                        <h3>Database Statistics</h3>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Total Users:</span>
                            <span className="value">
                              {cfDebugData.database_stats.total_users}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Total Products:</span>
                            <span className="value">
                              {cfDebugData.database_stats.total_products}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Total Order Items:</span>
                            <span className="value">
                              {cfDebugData.database_stats.total_order_items}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Users with Purchases:</span>
                            <span className="value">
                              {cfDebugData.database_stats.users_with_purchases}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Total Purchases:</span>
                            <span className="value">
                              {cfDebugData.database_stats.total_purchases}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {cfDebugData.matrix_info && (
                      <div className="debug-card">
                        <h3>User-Product Matrix</h3>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Shape:</span>
                            <span className="value">
                              {cfDebugData.matrix_info.shape}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Total Cells:</span>
                            <span className="value">
                              {cfDebugData.matrix_info.total_cells}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Non-Zero Cells:</span>
                            <span className="value">
                              {cfDebugData.matrix_info.non_zero_cells}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Sparsity:</span>
                            <span className="value">
                              {cfDebugData.matrix_info.sparsity_percentage}%
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {cfDebugData.similarity_matrix_info && (
                      <div className="debug-card">
                        <h3>Similarity Matrix</h3>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Expected Shape:</span>
                            <span className="value">
                              {
                                cfDebugData.similarity_matrix_info
                                  .expected_shape
                              }
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Total Possible Pairs:</span>
                            <span className="value">
                              {
                                cfDebugData.similarity_matrix_info
                                  .total_possible_pairs
                              }
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Saved Similarities:</span>
                            <span className="value">
                              {
                                cfDebugData.similarity_matrix_info
                                  .saved_similarities
                              }
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Percentage Saved:</span>
                            <span className="value">
                              {
                                cfDebugData.similarity_matrix_info
                                  .percentage_saved
                              }
                              %
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Threshold:</span>
                            <span className="value">
                              {cfDebugData.similarity_matrix_info.threshold}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {cfDebugData.cache_info && (
                      <div className="debug-card">
                        <h3>Cache</h3>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Status:</span>
                            <span className="value success">
                              {cfDebugData.cache_info.status}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Cached Value:</span>
                            <span className="value">
                              {cfDebugData.cache_info.cached_value}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Timeout:</span>
                            <span className="value">
                              {cfDebugData.cache_info.timeout}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {cfDebugData.top_10_similarities &&
                      cfDebugData.top_10_similarities.length > 0 && (
                        <div className="debug-card">
                          <h3>Top 10 Similar Product Pairs</h3>
                          <div className="similarities-table">
                            <table>
                              <thead>
                                <tr>
                                  <th>Rank</th>
                                  <th>Product 1</th>
                                  <th>Product 2</th>
                                  <th>Score</th>
                                </tr>
                              </thead>
                              <tbody>
                                {cfDebugData.top_10_similarities.map(
                                  (sim, index) => (
                                    <tr key={index}>
                                      <td>{index + 1}</td>
                                      <td>{sim.product1_name}</td>
                                      <td>{sim.product2_name}</td>
                                      <td className="similarity-value">
                                        {sim.score.toFixed(4)}
                                      </td>
                                    </tr>
                                  ),
                                )}
                              </tbody>
                            </table>
                          </div>
                          <button
                            className="view-all-btn"
                            onClick={openAllSimilaritiesModal}
                            style={{ marginTop: "10px" }}>
                            View All Similarities
                          </button>
                        </div>
                      )}

                    {cfDebugData.sample_user_vector && (
                      <div className="debug-card">
                        <h3>
                          Sample User Vector (User #
                          {cfDebugData.sample_user_vector.user_id})
                        </h3>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Total Purchases:</span>
                            <span className="value">
                              {cfDebugData.sample_user_vector.total_purchases}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Vector Length:</span>
                            <span className="value">
                              {cfDebugData.sample_user_vector.vector_length}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}
                  </>
                ) : (
                  <div className="debug-card">
                    <p className="no-data">Loading...</p>
                  </div>
                )}
              </div>
            )}

            {activeMethod === "sentiment" && (
              <div className="debug-section sentiment-debug">
                <h2 className="section-title">
                  Sentiment Analysis Debug Information
                </h2>

                {sentimentDebugData ? (
                  <>
                    {sentimentDebugData.total_sentiments > 0 && (
                      <div className="debug-card">
                        <h3>Sentiment Distribution</h3>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Total Sentiments:</span>
                            <span className="value">
                              {sentimentDebugData.total_sentiments}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Positive:</span>
                            <span className="value success">
                              {sentimentDebugData.positive_count} (
                              {sentimentDebugData.positive_percentage}%)
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Negative:</span>
                            <span className="value error">
                              {sentimentDebugData.negative_count} (
                              {sentimentDebugData.negative_percentage}%)
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Neutral:</span>
                            <span className="value">
                              {sentimentDebugData.neutral_count} (
                              {sentimentDebugData.neutral_percentage}%)
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {sentimentDebugData.top_positive &&
                      sentimentDebugData.top_positive.length > 0 && (
                        <div className="debug-card">
                          <h3>Top Products by Positive Sentiment</h3>
                          <div className="sentiment-table">
                            <table>
                              <thead>
                                <tr>
                                  <th>Rank</th>
                                  <th>Product</th>
                                  <th>Avg Sentiment</th>
                                  <th>Total Reviews</th>
                                </tr>
                              </thead>
                              <tbody>
                                {sentimentDebugData.top_positive.map(
                                  (item, index) => (
                                    <tr key={index}>
                                      <td>{index + 1}</td>
                                      <td>{item.product_name}</td>
                                      <td className="sentiment-positive">
                                        {item.avg_sentiment.toFixed(2)}
                                      </td>
                                      <td>{item.review_count}</td>
                                    </tr>
                                  ),
                                )}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      )}

                    {sentimentDebugData.top_negative &&
                      sentimentDebugData.top_negative.length > 0 && (
                        <div className="debug-card">
                          <h3>Top Products by Negative Sentiment</h3>
                          <div className="sentiment-table">
                            <table>
                              <thead>
                                <tr>
                                  <th>Rank</th>
                                  <th>Product</th>
                                  <th>Avg Sentiment</th>
                                  <th>Total Reviews</th>
                                </tr>
                              </thead>
                              <tbody>
                                {sentimentDebugData.top_negative.map(
                                  (item, index) => (
                                    <tr key={index}>
                                      <td>{index + 1}</td>
                                      <td>{item.product_name}</td>
                                      <td className="sentiment-negative">
                                        {item.avg_sentiment.toFixed(2)}
                                      </td>
                                      <td>{item.review_count}</td>
                                    </tr>
                                  ),
                                )}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      )}

                    <div className="debug-card">
                      <h3>Detailed Product Sentiment Analysis</h3>
                      <div className="product-selector">
                        <select
                          className="product-select"
                          value={selectedProductId}
                          onChange={handleProductSelect}>
                          <option value="">
                            -- Select a Product for Detailed Analysis --
                          </option>
                          {products.map((product) => (
                            <option key={product.id} value={product.id}>
                              {product.name}
                            </option>
                          ))}
                        </select>
                      </div>
                    </div>

                    {selectedProductId && sentimentDetailData && (
                      <>
                        <div className="debug-card">
                          <h3>Product: {sentimentDetailData.product_name}</h3>
                          <div className="debug-info">
                            <div className="info-row">
                              <span className="label">Product ID:</span>
                              <span className="value">
                                {sentimentDetailData.product_id}
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Final Score:</span>
                              <span
                                className={`value ${
                                  sentimentDetailData.final_calculation
                                    .final_score > 0.1
                                    ? "success"
                                    : sentimentDetailData.final_calculation
                                          .final_score < -0.1
                                      ? "error"
                                      : ""
                                }`}>
                                {
                                  sentimentDetailData.final_calculation
                                    .final_score
                                }
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Final Category:</span>
                              <span
                                className={`value ${
                                  sentimentDetailData.final_calculation
                                    .final_category === "Positive"
                                    ? "success"
                                    : sentimentDetailData.final_calculation
                                          .final_category === "Negative"
                                      ? "error"
                                      : ""
                                }`}>
                                {
                                  sentimentDetailData.final_calculation
                                    .final_category
                                }
                              </span>
                            </div>
                          </div>
                        </div>

                        <div className="debug-card">
                          <h3>Multi-Source Analysis Breakdown</h3>
                          <div className="sources-breakdown">
                            <div className="source-item">
                              <h4>
                                Opinions (
                                {
                                  sentimentDetailData.multi_source_analysis
                                    .opinions.weight
                                }
                                )
                              </h4>
                              <div className="debug-info">
                                <div className="info-row">
                                  <span className="label">Count:</span>
                                  <span className="value">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .opinions.count
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Average Score:</span>
                                  <span className="value">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .opinions.average_score
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Contribution:</span>
                                  <span className="value success">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .opinions.contribution_to_final
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Formula:</span>
                                  <span className="value formula-text">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .opinions.formula
                                    }
                                  </span>
                                </div>
                              </div>
                            </div>

                            <div className="source-item">
                              <h4>
                                Description (
                                {
                                  sentimentDetailData.multi_source_analysis
                                    .description.weight
                                }
                                )
                              </h4>
                              <div className="debug-info">
                                <div className="info-row">
                                  <span className="label">Score:</span>
                                  <span className="value">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .description.score
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Category:</span>
                                  <span className="value">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .description.category
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Contribution:</span>
                                  <span className="value success">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .description.contribution_to_final
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Positive Words:</span>
                                  <span className="value">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .description.positive_words
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Negative Words:</span>
                                  <span className="value">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .description.negative_words
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Formula:</span>
                                  <span className="value formula-text">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .description.formula
                                    }
                                  </span>
                                </div>
                              </div>
                            </div>

                            <div className="source-item">
                              <h4>
                                Product Name (
                                {
                                  sentimentDetailData.multi_source_analysis.name
                                    .weight
                                }
                                )
                              </h4>
                              <div className="debug-info">
                                <div className="info-row">
                                  <span className="label">Text:</span>
                                  <span className="value">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .name.text
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Score:</span>
                                  <span className="value">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .name.score
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Contribution:</span>
                                  <span className="value success">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .name.contribution_to_final
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Formula:</span>
                                  <span className="value formula-text">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .name.formula
                                    }
                                  </span>
                                </div>
                              </div>
                            </div>

                            <div className="source-item">
                              <h4>
                                Specifications (
                                {
                                  sentimentDetailData.multi_source_analysis
                                    .specifications.weight
                                }
                                )
                              </h4>
                              <div className="debug-info">
                                <div className="info-row">
                                  <span className="label">Count:</span>
                                  <span className="value">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .specifications.count
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Combined Score:</span>
                                  <span className="value">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .specifications.combined_score
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Contribution:</span>
                                  <span className="value success">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .specifications.contribution_to_final
                                    }
                                  </span>
                                </div>
                              </div>
                            </div>

                            <div className="source-item">
                              <h4>
                                Categories (
                                {
                                  sentimentDetailData.multi_source_analysis
                                    .categories.weight
                                }
                                )
                              </h4>
                              <div className="debug-info">
                                <div className="info-row">
                                  <span className="label">Text:</span>
                                  <span className="value">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .categories.text
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Score:</span>
                                  <span className="value">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .categories.score
                                    }
                                  </span>
                                </div>
                                <div className="info-row">
                                  <span className="label">Contribution:</span>
                                  <span className="value success">
                                    {
                                      sentimentDetailData.multi_source_analysis
                                        .categories.contribution_to_final
                                    }
                                  </span>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>

                        <div className="debug-card">
                          <h3>Final Calculation</h3>
                          <div className="debug-info">
                            <div className="info-row">
                              <span className="label">Formula:</span>
                              <span className="value formula-text">
                                {sentimentDetailData.final_calculation.formula}
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Calculation:</span>
                              <span className="value formula-text">
                                {
                                  sentimentDetailData.final_calculation
                                    .calculation
                                }
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Final Score:</span>
                              <span className="value success">
                                {
                                  sentimentDetailData.final_calculation
                                    .final_score
                                }
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Final Category:</span>
                              <span className="value">
                                {
                                  sentimentDetailData.final_calculation
                                    .final_category
                                }
                              </span>
                            </div>
                          </div>
                        </div>

                        {sentimentDetailData.multi_source_analysis.opinions
                          .sample_details &&
                          sentimentDetailData.multi_source_analysis.opinions
                            .sample_details.length > 0 && (
                            <div className="debug-card">
                              <h3>Sample Opinion Analysis</h3>
                              {sentimentDetailData.multi_source_analysis.opinions.sample_details.map(
                                (opinion, index) => (
                                  <div key={index} className="opinion-detail">
                                    <h4>Opinion #{opinion.opinion_id}</h4>
                                    <p className="opinion-text">
                                      {opinion.opinion_excerpt}
                                    </p>
                                    <div className="debug-info">
                                      <div className="info-row">
                                        <span className="label">
                                          Positive Words:
                                        </span>
                                        <span className="value success">
                                          {
                                            opinion.calculation
                                              .positive_words_found
                                          }
                                        </span>
                                      </div>
                                      <div className="info-row">
                                        <span className="label">
                                          Negative Words:
                                        </span>
                                        <span className="value error">
                                          {
                                            opinion.calculation
                                              .negative_words_found
                                          }
                                        </span>
                                      </div>
                                      <div className="info-row">
                                        <span className="label">
                                          Total Words:
                                        </span>
                                        <span className="value">
                                          {opinion.calculation.total_words}
                                        </span>
                                      </div>
                                      <div className="info-row">
                                        <span className="label">Formula:</span>
                                        <span className="value formula-text">
                                          {opinion.calculation.formula}
                                        </span>
                                      </div>
                                      <div className="info-row">
                                        <span className="label">Score:</span>
                                        <span className="value">
                                          {opinion.calculation.sentiment_score}
                                        </span>
                                      </div>
                                      <div className="info-row">
                                        <span className="label">Category:</span>
                                        <span className="value">
                                          {opinion.calculation.category}
                                        </span>
                                      </div>
                                    </div>
                                  </div>
                                ),
                              )}
                            </div>
                          )}

                        {sentimentDetailData.lexicon_info && (
                          <div className="debug-card">
                            <h3>Sentiment Lexicon Information</h3>
                            <div className="debug-info">
                              <div className="info-row">
                                <span className="label">
                                  Positive Words Count:
                                </span>
                                <span className="value success">
                                  {
                                    sentimentDetailData.lexicon_info
                                      .positive_words_count
                                  }
                                </span>
                              </div>
                              <div className="info-row">
                                <span className="label">
                                  Negative Words Count:
                                </span>
                                <span className="value error">
                                  {
                                    sentimentDetailData.lexicon_info
                                      .negative_words_count
                                  }
                                </span>
                              </div>
                              <div className="info-row">
                                <span className="label">
                                  Examples (Positive):
                                </span>
                                <span className="value">
                                  {sentimentDetailData.lexicon_info.examples_positive.join(
                                    ", ",
                                  )}
                                </span>
                              </div>
                              <div className="info-row">
                                <span className="label">
                                  Examples (Negative):
                                </span>
                                <span className="value">
                                  {sentimentDetailData.lexicon_info.examples_negative.join(
                                    ", ",
                                  )}
                                </span>
                              </div>
                            </div>
                          </div>
                        )}

                        {sentimentDetailData.source && (
                          <div className="debug-card">
                            <h3>Scientific Reference</h3>
                            <p className="reference-text">
                              {sentimentDetailData.source}
                            </p>
                          </div>
                        )}
                      </>
                    )}

                    {sentimentDebugData.total_sentiments === 0 &&
                      (!sentimentDebugData.top_positive ||
                        sentimentDebugData.top_positive.length === 0) &&
                      (!sentimentDebugData.top_negative ||
                        sentimentDebugData.top_negative.length === 0) && (
                        <div className="debug-card">
                          <p className="no-data">
                            No sentiment analysis data available.
                          </p>
                        </div>
                      )}
                  </>
                ) : (
                  <div className="debug-card">
                    <p className="no-data">Loading...</p>
                  </div>
                )}
              </div>
            )}

            {activeMethod === "association" && (
              <div className="debug-section association-debug">
                <h2 className="section-title">
                  Association Rules Debug Information
                </h2>

                <div className="debug-card">
                  <h3>Select Product to Inspect</h3>
                  <div className="product-selector">
                    <select
                      className="product-select"
                      value={selectedProductId}
                      onChange={handleProductSelect}>
                      <option value="">-- Select a Product --</option>
                      {products.map((product) => (
                        <option key={product.id} value={product.id}>
                          {product.name}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {associationDebugData && (
                  <>
                    <div className="debug-card">
                      <h3>Product: {associationDebugData.product.name}</h3>
                      <div className="debug-info">
                        <div className="info-row">
                          <span className="label">Product ID:</span>
                          <span className="value">
                            {associationDebugData.product.id}
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Product Support:</span>
                          <span className="value success">
                            {(
                              associationDebugData.statistics.product_support *
                              100
                            ).toFixed(2)}
                            %
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">
                            Transactions with This Product:
                          </span>
                          <span className="value">
                            {
                              associationDebugData.statistics
                                .transactions_with_product
                            }
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Rules for This Product:</span>
                          <span className="value">
                            {
                              associationDebugData.statistics
                                .rules_for_this_product
                            }
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="debug-card">
                      <h3>Database Statistics</h3>
                      <div className="debug-info">
                        <div className="info-row">
                          <span className="label">All Orders in Database:</span>
                          <span className="value">
                            {associationDebugData.statistics.all_orders_in_db}
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Single Product Orders:</span>
                          <span className="value">
                            {
                              associationDebugData.statistics
                                .single_product_orders
                            }
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Multi-Product Orders:</span>
                          <span className="value success">
                            {
                              associationDebugData.statistics
                                .multi_product_orders
                            }
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Total Rules in System:</span>
                          <span className="value">
                            {
                              associationDebugData.statistics
                                .total_rules_in_system
                            }
                          </span>
                        </div>
                      </div>
                      {associationDebugData.statistics.note && (
                        <p className="info-note">
                          {associationDebugData.statistics.note}
                        </p>
                      )}
                    </div>

                    {associationDebugData.algorithm_behavior && (
                      <div className="debug-card">
                        <h3>Algorithm Behavior</h3>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Filtering:</span>
                            <span className="value">
                              {
                                associationDebugData.algorithm_behavior
                                  .filtering
                              }
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Reason:</span>
                            <span className="value">
                              {associationDebugData.algorithm_behavior.reason}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Impact:</span>
                            <span className="value">
                              {associationDebugData.algorithm_behavior.impact}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {associationDebugData.top_associations &&
                      associationDebugData.top_associations.length > 0 && (
                        <div className="debug-card">
                          <h3>Top 10 Association Rules for This Product</h3>
                          <div className="associations-table">
                            <table>
                              <thead>
                                <tr>
                                  <th>Rank</th>
                                  <th>Product</th>
                                  <th>Support</th>
                                  <th>Confidence</th>
                                  <th>Lift</th>
                                </tr>
                              </thead>
                              <tbody>
                                {associationDebugData.top_associations.map(
                                  (assoc, index) => (
                                    <tr key={index}>
                                      <td>{index + 1}</td>
                                      <td>{assoc.product_2.name}</td>
                                      <td className="metric-value">
                                        {(assoc.metrics.support * 100).toFixed(
                                          2,
                                        )}
                                        %
                                      </td>
                                      <td className="metric-value">
                                        {(
                                          assoc.metrics.confidence * 100
                                        ).toFixed(1)}
                                        %
                                      </td>
                                      <td className="metric-value success">
                                        {assoc.metrics.lift.toFixed(2)}x
                                      </td>
                                    </tr>
                                  ),
                                )}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      )}

                    {associationDebugData.top_associations &&
                      associationDebugData.top_associations.length > 0 && (
                        <div className="debug-card">
                          <h3>Detailed Rule Analysis</h3>
                          {associationDebugData.top_associations
                            .slice(0, 3)
                            .map((assoc, index) => (
                              <div key={index} className="rule-detail">
                                <h4>
                                  Rule #{index + 1}:{" "}
                                  {associationDebugData.product.name} →{" "}
                                  {assoc.product_2.name}
                                </h4>
                                <div className="debug-info">
                                  <div className="info-row">
                                    <span className="label">
                                      Support Formula:
                                    </span>
                                    <span className="value formula-text">
                                      {
                                        assoc.formula_verification
                                          .support_formula
                                      }
                                    </span>
                                  </div>
                                  <div className="info-row">
                                    <span className="label">
                                      Confidence Formula:
                                    </span>
                                    <span className="value formula-text">
                                      {
                                        assoc.formula_verification
                                          .confidence_formula
                                      }
                                    </span>
                                  </div>
                                  <div className="info-row">
                                    <span className="label">Lift Formula:</span>
                                    <span className="value formula-text">
                                      {assoc.formula_verification.lift_formula}
                                    </span>
                                  </div>
                                  <div className="info-row interpretation">
                                    <span className="label">Support:</span>
                                    <span className="value">
                                      {assoc.interpretation.support}
                                    </span>
                                  </div>
                                  <div className="info-row interpretation">
                                    <span className="label">Confidence:</span>
                                    <span className="value">
                                      {assoc.interpretation.confidence}
                                    </span>
                                  </div>
                                  <div className="info-row interpretation">
                                    <span className="label">Lift:</span>
                                    <span className="value">
                                      {assoc.interpretation.lift}
                                    </span>
                                  </div>
                                </div>
                              </div>
                            ))}
                        </div>
                      )}

                    <div className="debug-card">
                      <h3>Association Rules (Formulas)</h3>
                      <div className="formulas">
                        <div className="formula-card">
                          <h4>Support</h4>
                          <p className="formula-text">
                            Support(A, B) = P(A ∩ B) = Transactions with both /
                            Total transactions
                          </p>
                          <p className="formula-explanation">
                            Measures how frequently both products appear
                            together in transactions.
                          </p>
                        </div>
                        <div className="formula-card">
                          <h4>Confidence</h4>
                          <p className="formula-text">
                            Confidence(A → B) = P(B|A) = Support(A, B) /
                            Support(A)
                          </p>
                          <p className="formula-explanation">
                            Probability of buying B when A is purchased.
                          </p>
                        </div>
                        <div className="formula-card">
                          <h4>Lift</h4>
                          <p className="formula-text">
                            Lift(A → B) = Confidence(A → B) / Support(B)
                          </p>
                          <p className="formula-explanation">
                            How many times more likely B is purchased with A
                            compared to random chance.
                          </p>
                        </div>
                      </div>
                    </div>

                    {associationDebugData.references && (
                      <div className="debug-card">
                        <h3>Scientific References</h3>
                        <ul className="references-list">
                          {associationDebugData.references.map((ref, index) => (
                            <li key={index}>{ref}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </>
                )}

                {!associationDebugData && selectedProductId && (
                  <div className="debug-card">
                    <p className="no-data">
                      Loading association rules for selected product...
                    </p>
                  </div>
                )}

                {!selectedProductId && (
                  <div className="debug-card">
                    <p className="no-data">
                      Please select a product to view its association rules.
                    </p>
                  </div>
                )}
              </div>
            )}

            {activeMethod === "content" && (
              <div className="debug-section cb-debug">
                <h2 className="section-title">
                  Content-Based Filtering Debug Information
                </h2>

                <div className="product-selector-card">
                  <label htmlFor="product-select">
                    Select Product to Analyze:
                  </label>
                  <select
                    id="product-select"
                    value={selectedProductId}
                    onChange={handleProductSelect}
                    className="product-dropdown">
                    <option value="">-- Select a Product --</option>
                    {products.map((product) => (
                      <option key={product.id} value={product.id}>
                        {product.name} (ID: {product.id})
                      </option>
                    ))}
                  </select>
                </div>

                {contentBasedDebugData ? (
                  <>
                    <div className="debug-card">
                      <h3>Algorithm</h3>
                      <div className="debug-info">
                        <div className="info-row">
                          <span className="label">Name:</span>
                          <span className="value">
                            {contentBasedDebugData.algorithm}
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Formula:</span>
                          <span className="value">
                            {contentBasedDebugData.formula}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="debug-card">
                      <h3>Database Statistics</h3>
                      <div className="debug-info">
                        <div className="info-row">
                          <span className="label">Total Products:</span>
                          <span className="value">
                            {
                              contentBasedDebugData.database_stats
                                .total_products
                            }
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Saved Similarities:</span>
                          <span className="value">
                            {
                              contentBasedDebugData.database_stats
                                .saved_similarities
                            }
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Percentage Saved:</span>
                          <span className="value">
                            {
                              contentBasedDebugData.database_stats
                                .percentage_saved
                            }
                            %
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Threshold:</span>
                          <span className="value">
                            {contentBasedDebugData.database_stats.threshold *
                              100}
                            %
                          </span>
                        </div>
                      </div>
                      <p className="description">
                        {contentBasedDebugData.database_stats.description}
                      </p>
                    </div>

                    <div className="debug-card">
                      <h3>Feature Weights</h3>
                      <div className="debug-info">
                        <div className="info-row">
                          <span className="label">Category:</span>
                          <span className="value">
                            {contentBasedDebugData.feature_weights.category *
                              100}
                            %
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Tag:</span>
                          <span className="value">
                            {contentBasedDebugData.feature_weights.tag * 100}%
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Price:</span>
                          <span className="value">
                            {contentBasedDebugData.feature_weights.price * 100}%
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Keywords:</span>
                          <span className="value">
                            {contentBasedDebugData.feature_weights.keywords *
                              100}
                            %
                          </span>
                        </div>
                      </div>
                      <p className="description">
                        {contentBasedDebugData.feature_weights.description}
                      </p>
                    </div>

                    {contentBasedDebugData.selected_product && (
                      <>
                        <div className="debug-card">
                          <h3>Selected Product</h3>
                          <div className="debug-info">
                            <div className="info-row">
                              <span className="label">Name:</span>
                              <span className="value">
                                {contentBasedDebugData.selected_product.name}
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">ID:</span>
                              <span className="value">
                                {contentBasedDebugData.selected_product.id}
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Price:</span>
                              <span className="value">
                                {contentBasedDebugData.selected_product.price}{" "}
                                PLN
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Price Category:</span>
                              <span className="value">
                                {
                                  contentBasedDebugData.selected_product
                                    .price_category
                                }
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Categories:</span>
                              <span className="value">
                                {contentBasedDebugData.selected_product.categories.join(
                                  ", ",
                                )}
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Tags:</span>
                              <span className="value">
                                {contentBasedDebugData.selected_product.tags.join(
                                  ", ",
                                )}
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Keywords:</span>
                              <span className="value">
                                {contentBasedDebugData.selected_product.keywords.join(
                                  ", ",
                                )}
                              </span>
                            </div>
                          </div>
                        </div>

                        <div className="debug-card">
                          <h3>
                            Feature Vector (
                            {contentBasedDebugData.feature_vector.vector_length}{" "}
                            features)
                          </h3>
                          <div className="debug-info">
                            {Object.entries(
                              contentBasedDebugData.feature_vector.features,
                            ).map(([key, value]) => (
                              <div key={key} className="info-row">
                                <span className="label">{key}:</span>
                                <span className="value">
                                  {value.toFixed(3)}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>

                        {contentBasedDebugData.similar_products &&
                          contentBasedDebugData.similar_products.count > 0 && (
                            <div className="debug-card">
                              <h3>
                                Top{" "}
                                {contentBasedDebugData.similar_products.count}{" "}
                                Similar Products
                              </h3>
                              <div className="table-container">
                                <table className="debug-table">
                                  <thead>
                                    <tr>
                                      <th>#</th>
                                      <th>Product Name</th>
                                      <th>Similarity Score</th>
                                      <th>Price</th>
                                      <th>Categories</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {contentBasedDebugData.similar_products.top_10.map(
                                      (sim, idx) => (
                                        <tr key={idx}>
                                          <td>{idx + 1}</td>
                                          <td>{sim.product_2.name}</td>
                                          <td>
                                            <strong>
                                              {(
                                                sim.similarity_score * 100
                                              ).toFixed(2)}
                                              %
                                            </strong>
                                          </td>
                                          <td>{sim.product_2.price} PLN</td>
                                          <td>
                                            {sim.product_2.categories.join(
                                              ", ",
                                            )}
                                          </td>
                                        </tr>
                                      ),
                                    )}
                                  </tbody>
                                </table>
                              </div>

                              <h4
                                style={{
                                  marginTop: "2rem",
                                  marginBottom: "1rem",
                                }}>
                                Detailed Calculations (Top 3)
                              </h4>
                              {contentBasedDebugData.similar_products.top_10
                                .slice(0, 3)
                                .map((sim, idx) => (
                                  <div
                                    key={idx}
                                    className="debug-card"
                                    style={{ marginBottom: "1rem" }}>
                                    <h3>
                                      #{idx + 1} {sim.product_2.name}
                                    </h3>
                                    <div className="debug-info">
                                      <div className="info-row">
                                        <span className="label">Formula:</span>
                                        <span className="value">
                                          {sim.calculation.formula}
                                        </span>
                                      </div>
                                      <div className="info-row">
                                        <span className="label">
                                          Dot Product:
                                        </span>
                                        <span className="value">
                                          {sim.calculation.dot_product}
                                        </span>
                                      </div>
                                      <div className="info-row">
                                        <span className="label">
                                          Norm Product 1:
                                        </span>
                                        <span className="value">
                                          {sim.calculation.norm_product1}
                                        </span>
                                      </div>
                                      <div className="info-row">
                                        <span className="label">
                                          Norm Product 2:
                                        </span>
                                        <span className="value">
                                          {sim.calculation.norm_product2}
                                        </span>
                                      </div>
                                      <div className="info-row">
                                        <span className="label">
                                          Verification:
                                        </span>
                                        <span
                                          className={`value ${
                                            sim.calculation.stored_vs_calculated
                                              .match
                                              ? "success"
                                              : "error"
                                          }`}>
                                          Stored:{" "}
                                          {
                                            sim.calculation.stored_vs_calculated
                                              .stored
                                          }{" "}
                                          | Calculated:{" "}
                                          {
                                            sim.calculation.stored_vs_calculated
                                              .calculated
                                          }
                                          {sim.calculation.stored_vs_calculated
                                            .match
                                            ? " ✓"
                                            : " ✗"}
                                        </span>
                                      </div>
                                    </div>

                                    {Object.keys(sim.common_features).length >
                                      0 && (
                                      <>
                                        <h4
                                          style={{
                                            marginTop: "1rem",
                                            marginBottom: "0.5rem",
                                          }}>
                                          Common Features (
                                          {sim.common_features_count} total)
                                        </h4>
                                        <div className="table-container">
                                          <table className="debug-table">
                                            <thead>
                                              <tr>
                                                <th>Feature</th>
                                                <th>Product 1 Value</th>
                                                <th>Product 2 Value</th>
                                              </tr>
                                            </thead>
                                            <tbody>
                                              {Object.entries(
                                                sim.common_features,
                                              ).map(([feat, vals]) => (
                                                <tr key={feat}>
                                                  <td>
                                                    <strong>{feat}</strong>
                                                  </td>
                                                  <td>{vals.product1_value}</td>
                                                  <td>{vals.product2_value}</td>
                                                </tr>
                                              ))}
                                            </tbody>
                                          </table>
                                        </div>
                                      </>
                                    )}
                                  </div>
                                ))}
                            </div>
                          )}
                      </>
                    )}

                    {!selectedProductId &&
                      contentBasedDebugData.top_10_global_similarities && (
                        <div className="debug-card">
                          <h3>Top 10 Global Similarities</h3>
                          <div className="table-container">
                            <table className="debug-table">
                              <thead>
                                <tr>
                                  <th>#</th>
                                  <th>Product 1</th>
                                  <th>Product 2</th>
                                  <th>Similarity Score</th>
                                </tr>
                              </thead>
                              <tbody>
                                {contentBasedDebugData.top_10_global_similarities.map(
                                  (sim, idx) => (
                                    <tr key={idx}>
                                      <td>{idx + 1}</td>
                                      <td>
                                        {sim.product1_name}
                                        <span className="id-badge">
                                          ID: {sim.product1_id}
                                        </span>
                                      </td>
                                      <td>
                                        {sim.product2_name}
                                        <span className="id-badge">
                                          ID: {sim.product2_id}
                                        </span>
                                      </td>
                                      <td>
                                        <strong>
                                          {(sim.score * 100).toFixed(2)}%
                                        </strong>
                                      </td>
                                    </tr>
                                  ),
                                )}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      )}

                    <div className="debug-card">
                      <h3>Computation Status</h3>
                      <div className="debug-info">
                        <div className="info-row">
                          <span className="label">Can Compute:</span>
                          <span
                            className={`value ${
                              contentBasedDebugData.computation_status
                                .can_compute
                                ? "success"
                                : "error"
                            }`}>
                            {contentBasedDebugData.computation_status
                              .can_compute
                              ? "✅ Yes"
                              : "❌ No"}
                          </span>
                        </div>
                      </div>
                      <div className="issues-list">
                        {contentBasedDebugData.computation_status.issues.map(
                          (issue, idx) => (
                            <p
                              key={idx}
                              className={
                                issue.includes("✅") ? "success" : "warning"
                              }>
                              {issue}
                            </p>
                          ),
                        )}
                      </div>
                    </div>
                  </>
                ) : (
                  <div className="debug-card">
                    <p className="no-data">
                      {loading
                        ? "Loading content-based debug data..."
                        : "No content-based debug data available."}
                    </p>
                  </div>
                )}
              </div>
            )}
          </>
        )}

        {activeMethod === "fuzzy" && (
          <div className="debug-section fuzzy-debug">
            <h2 className="section-title">
              Fuzzy Logic Inference System Debug
            </h2>

            <div className="product-selector-card">
              <label>Select User Profile:</label>
              <select
                value={selectedUserId}
                onChange={handleUserSelect}
                className="product-select">
                <option value="">Default Profile (Guest)</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.username} (ID: {user.id})
                  </option>
                ))}
              </select>
            </div>

            <div className="product-selector-card">
              <label>Select Product to Analyze (Optional):</label>
              <select
                value={selectedProductId}
                onChange={handleProductSelect}
                className="product-select">
                <option value="">None (Show Top 10 Products)</option>
                {products.map((product) => (
                  <option key={product.id} value={product.id}>
                    {product.name}
                  </option>
                ))}
              </select>
            </div>

            {fuzzyLogicDebugData ? (
              <>
                <div className="debug-card">
                  <h3>Algorithm Information</h3>
                  <div className="debug-info">
                    <div className="info-row">
                      <span className="label">Name:</span>
                      <span className="value">
                        {fuzzyLogicDebugData.algorithm}
                      </span>
                    </div>
                    <div className="info-row">
                      <span className="label">Description:</span>
                      <span className="value">
                        {fuzzyLogicDebugData.description}
                      </span>
                    </div>
                  </div>
                </div>

                {fuzzyLogicDebugData.user_profile && (
                  <div className="debug-card">
                    <h3>User Profile</h3>
                    <div className="debug-info">
                      <div className="info-row">
                        <span className="label">User:</span>
                        <span className="value">
                          {fuzzyLogicDebugData.user_profile.username}
                          {fuzzyLogicDebugData.user_profile.user_id && (
                            <span className="id-badge">
                              ID: {fuzzyLogicDebugData.user_profile.user_id}
                            </span>
                          )}
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">Profile Type:</span>
                        <span className="value">
                          {fuzzyLogicDebugData.user_profile.profile_type}
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">Price Sensitivity:</span>
                        <span className="value">
                          {fuzzyLogicDebugData.user_profile.price_sensitivity} -{" "}
                          {
                            fuzzyLogicDebugData.user_profile
                              .price_sensitivity_label
                          }
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">Tracked Categories:</span>
                        <span className="value">
                          {
                            fuzzyLogicDebugData.user_profile
                              .total_categories_tracked
                          }
                        </span>
                      </div>
                    </div>

                    <h4 style={{ marginTop: "1rem" }}>Category Interests</h4>
                    <div className="debug-info">
                      {Object.entries(
                        fuzzyLogicDebugData.user_profile.category_interests ||
                          {},
                      ).map(([cat, interest]) => (
                        <div className="info-row" key={cat}>
                          <span className="label">{cat}:</span>
                          <span className="value">{interest}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {fuzzyLogicDebugData.membership_functions && (
                  <div className="debug-card">
                    <h3>Membership Functions</h3>

                    <h4>Price Functions</h4>
                    <div className="debug-info">
                      {Object.entries(
                        fuzzyLogicDebugData.membership_functions.price,
                      ).map(([key, func]) => (
                        <div key={key} style={{ marginBottom: "0.8rem" }}>
                          <div className="info-row">
                            <span className="label">{key.toUpperCase()}:</span>
                            <span className="value">{func.range}</span>
                          </div>
                          <p className="description">{func.description}</p>
                        </div>
                      ))}
                    </div>

                    <h4 style={{ marginTop: "1rem" }}>Quality Functions</h4>
                    <div className="debug-info">
                      {Object.entries(
                        fuzzyLogicDebugData.membership_functions.quality,
                      ).map(([key, func]) => (
                        <div key={key} style={{ marginBottom: "0.8rem" }}>
                          <div className="info-row">
                            <span className="label">{key.toUpperCase()}:</span>
                            <span className="value">{func.range}</span>
                          </div>
                          <p className="description">{func.description}</p>
                        </div>
                      ))}
                    </div>

                    <h4 style={{ marginTop: "1rem" }}>Popularity Functions</h4>
                    <div className="debug-info">
                      {Object.entries(
                        fuzzyLogicDebugData.membership_functions.popularity,
                      ).map(([key, func]) => (
                        <div key={key} style={{ marginBottom: "0.8rem" }}>
                          <div className="info-row">
                            <span className="label">{key.toUpperCase()}:</span>
                            <span className="value">{func.range}</span>
                          </div>
                          <p className="description">{func.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {fuzzyLogicDebugData.fuzzy_rules && (
                  <div className="debug-card">
                    <h3>
                      Fuzzy Rule Base ({fuzzyLogicDebugData.fuzzy_rules.length}{" "}
                      rules)
                    </h3>
                    {fuzzyLogicDebugData.fuzzy_rules.map((rule, idx) => (
                      <div
                        key={idx}
                        className="calculation-card"
                        style={{ marginBottom: "1rem" }}>
                        <h5>{rule.name}</h5>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Condition:</span>
                            <span className="value">{rule.condition}</span>
                          </div>
                          <div className="info-row">
                            <span className="label">Consequence:</span>
                            <span className="value">{rule.consequence}</span>
                          </div>
                          <p className="description">{rule.interpretation}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {fuzzyLogicDebugData.selected_product && (
                  <>
                    <div className="debug-card">
                      <h3>Selected Product</h3>
                      <div className="debug-info">
                        <div className="info-row">
                          <span className="label">ID:</span>
                          <span className="value">
                            {fuzzyLogicDebugData.selected_product.id}
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Name:</span>
                          <span className="value">
                            {fuzzyLogicDebugData.selected_product.name}
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Price:</span>
                          <span className="value">
                            {fuzzyLogicDebugData.selected_product.price} PLN
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Rating:</span>
                          <span className="value">
                            {fuzzyLogicDebugData.selected_product.rating}
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">View Count:</span>
                          <span className="value">
                            {fuzzyLogicDebugData.selected_product.view_count}
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Categories:</span>
                          <span className="value">
                            {fuzzyLogicDebugData.selected_product.categories.join(
                              ", ",
                            )}
                          </span>
                        </div>
                      </div>
                    </div>

                    {fuzzyLogicDebugData.fuzzification && (
                      <div className="debug-card">
                        <h3>Fuzzification - Membership Degrees</h3>

                        <h4>
                          Price: {fuzzyLogicDebugData.fuzzification.price.value}{" "}
                          PLN
                        </h4>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Cheap:</span>
                            <span className="value">
                              μ ={" "}
                              {fuzzyLogicDebugData.fuzzification.price.cheap}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Medium:</span>
                            <span className="value">
                              μ ={" "}
                              {fuzzyLogicDebugData.fuzzification.price.medium}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Expensive:</span>
                            <span className="value">
                              μ ={" "}
                              {
                                fuzzyLogicDebugData.fuzzification.price
                                  .expensive
                              }
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Dominant:</span>
                            <span className="value success">
                              <strong>
                                {fuzzyLogicDebugData.fuzzification.price.dominant.toUpperCase()}
                              </strong>
                            </span>
                          </div>
                        </div>

                        <h4 style={{ marginTop: "1rem" }}>
                          Quality:{" "}
                          {fuzzyLogicDebugData.fuzzification.quality.value}
                        </h4>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Low:</span>
                            <span className="value">
                              μ ={" "}
                              {fuzzyLogicDebugData.fuzzification.quality.low}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Medium:</span>
                            <span className="value">
                              μ ={" "}
                              {fuzzyLogicDebugData.fuzzification.quality.medium}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">High:</span>
                            <span className="value">
                              μ ={" "}
                              {fuzzyLogicDebugData.fuzzification.quality.high}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Dominant:</span>
                            <span className="value success">
                              <strong>
                                {fuzzyLogicDebugData.fuzzification.quality.dominant.toUpperCase()}
                              </strong>
                            </span>
                          </div>
                        </div>

                        <h4 style={{ marginTop: "1rem" }}>
                          Popularity:{" "}
                          {fuzzyLogicDebugData.fuzzification.popularity.value}{" "}
                          views
                        </h4>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Low:</span>
                            <span className="value">
                              μ ={" "}
                              {fuzzyLogicDebugData.fuzzification.popularity.low}
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Medium:</span>
                            <span className="value">
                              μ ={" "}
                              {
                                fuzzyLogicDebugData.fuzzification.popularity
                                  .medium
                              }
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">High:</span>
                            <span className="value">
                              μ ={" "}
                              {
                                fuzzyLogicDebugData.fuzzification.popularity
                                  .high
                              }
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Dominant:</span>
                            <span className="value success">
                              <strong>
                                {fuzzyLogicDebugData.fuzzification.popularity.dominant.toUpperCase()}
                              </strong>
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {fuzzyLogicDebugData.category_matching && (
                      <div className="debug-card">
                        <h3>Category Matching</h3>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Max Match:</span>
                            <span className="value success">
                              <strong>
                                {
                                  fuzzyLogicDebugData.category_matching
                                    .max_match
                                }
                              </strong>
                            </span>
                          </div>
                        </div>
                        <p className="description">
                          {fuzzyLogicDebugData.category_matching.explanation}
                        </p>

                        <h4 style={{ marginTop: "1rem" }}>Category Details</h4>
                        <div className="debug-info">
                          {Object.entries(
                            fuzzyLogicDebugData.category_matching
                              .category_details || {},
                          ).map(([cat, match]) => (
                            <div className="info-row" key={cat}>
                              <span className="label">{cat}:</span>
                              <span className="value">{match}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {fuzzyLogicDebugData.inference && (
                      <div className="debug-card">
                        <h3>Fuzzy Inference - Rule Activations</h3>
                        <div className="debug-info">
                          {Object.entries(
                            fuzzyLogicDebugData.inference.rule_activations ||
                              {},
                          ).map(([rule, activation]) => (
                            <div className="info-row" key={rule}>
                              <span className="label">{rule}:</span>
                              <span className="value">
                                <strong>{activation}</strong>
                              </span>
                            </div>
                          ))}
                        </div>

                        <h4 style={{ marginTop: "1.5rem" }}>Defuzzification</h4>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Method:</span>
                            <span className="value">
                              {
                                fuzzyLogicDebugData.inference
                                  .defuzzification_method
                              }
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Final Fuzzy Score:</span>
                            <span className="value success">
                              <strong>
                                {
                                  fuzzyLogicDebugData.inference
                                    .final_fuzzy_score
                                }
                              </strong>
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Percentage:</span>
                            <span className="value success">
                              <strong>
                                {fuzzyLogicDebugData.inference.final_percentage}
                                %
                              </strong>
                            </span>
                          </div>
                        </div>

                        <p
                          className="description"
                          style={{ marginTop: "1rem" }}>
                          {
                            fuzzyLogicDebugData.inference.calculation
                              .description
                          }
                        </p>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Weighted Sum:</span>
                            <span className="value">
                              {
                                fuzzyLogicDebugData.inference.calculation
                                  .weighted_sum
                              }
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Weight Sum:</span>
                            <span className="value">
                              {
                                fuzzyLogicDebugData.inference.calculation
                                  .weight_sum
                              }
                            </span>
                          </div>
                        </div>
                      </div>
                    )}
                  </>
                )}

                {fuzzyLogicDebugData.top_products && !selectedProductId && (
                  <div className="debug-card">
                    <h3>
                      Top {fuzzyLogicDebugData.top_products.count} Products by
                      Fuzzy Score
                    </h3>
                    <p className="description">
                      {fuzzyLogicDebugData.top_products.description}
                    </p>

                    <div className="table-container">
                      <table className="debug-table">
                        <thead>
                          <tr>
                            <th>#</th>
                            <th>Product Name</th>
                            <th>Price</th>
                            <th>Rating</th>
                            <th>Fuzzy Score</th>
                            <th>Percentage</th>
                            <th>Category Match</th>
                            <th>Categories</th>
                          </tr>
                        </thead>
                        <tbody>
                          {fuzzyLogicDebugData.top_products.products.map(
                            (prod, idx) => (
                              <tr key={prod.id}>
                                <td>{idx + 1}</td>
                                <td>{prod.name}</td>
                                <td>{prod.price} PLN</td>
                                <td>{prod.rating}</td>
                                <td>
                                  <strong>{prod.fuzzy_score}</strong>
                                </td>
                                <td>
                                  <strong>{prod.fuzzy_percentage}%</strong>
                                </td>
                                <td>{prod.category_match}</td>
                                <td>{prod.categories.join(", ")}</td>
                              </tr>
                            ),
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {fuzzyLogicDebugData.system_stats && (
                  <div className="debug-card">
                    <h3>System Statistics</h3>
                    <div className="debug-info">
                      <div className="info-row">
                        <span className="label">Total Products:</span>
                        <span className="value">
                          {fuzzyLogicDebugData.system_stats.total_products}
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">Total Rules:</span>
                        <span className="value">
                          {fuzzyLogicDebugData.system_stats.total_rules}
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">
                          Membership Function Types:
                        </span>
                        <span className="value">
                          {
                            fuzzyLogicDebugData.system_stats
                              .membership_function_types
                          }
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">Defuzzification Method:</span>
                        <span className="value">
                          {
                            fuzzyLogicDebugData.system_stats
                              .defuzzification_method
                          }
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="debug-card">
                <p className="no-data">
                  {loading
                    ? "Loading fuzzy logic debug data..."
                    : "No fuzzy logic debug data available."}
                </p>
              </div>
            )}
          </div>
        )}

        {activeMethod === "probabilistic" && (
          <div className="debug-section probabilistic-debug">
            <h2 className="section-title">
              Probabilistic Models Debug Information
            </h2>

            <div className="product-selector-card">
              <label>Select User to Analyze:</label>
              <select
                value={selectedUserId}
                onChange={handleUserSelect}
                className="product-select">
                <option value="">Select User...</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.username} (ID: {user.id})
                  </option>
                ))}
              </select>
            </div>

            <div className="product-selector-card">
              <label>Select Product to Analyze (Optional):</label>
              <select
                value={selectedProductId}
                onChange={handleProductSelect}
                className="product-select">
                <option value="">None</option>
                {products.map((product) => (
                  <option key={product.id} value={product.id}>
                    {product.name}
                  </option>
                ))}
              </select>
            </div>

            {probabilisticDebugData ? (
              <>
                <div className="debug-card">
                  <h3>Algorithm Information</h3>
                  <div className="debug-info">
                    <div className="info-row">
                      <span className="label">Name:</span>
                      <span className="value">
                        {probabilisticDebugData.algorithm}
                      </span>
                    </div>
                    <div className="info-row">
                      <span className="label">Description:</span>
                      <span className="value">
                        {probabilisticDebugData.description}
                      </span>
                    </div>
                  </div>
                </div>

                {probabilisticDebugData.markov_chain && (
                  <div className="debug-card">
                    <h3>Markov Chain Model</h3>
                    <div className="debug-info">
                      <div className="info-row">
                        <span className="label">Order:</span>
                        <span className="value">
                          {probabilisticDebugData.markov_chain.order}
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">
                          Total States (Categories):
                        </span>
                        <span className="value">
                          {probabilisticDebugData.markov_chain.total_states}
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">Total Transitions:</span>
                        <span className="value">
                          {
                            probabilisticDebugData.markov_chain
                              .total_transitions
                          }
                        </span>
                      </div>
                    </div>

                    <h4 style={{ marginTop: "1.5rem" }}>Top 10 Transitions</h4>
                    <div className="similarities-table">
                      <table>
                        <thead>
                          <tr>
                            <th>#</th>
                            <th>From Category</th>
                            <th>To Category</th>
                            <th>Probability</th>
                            <th>Count</th>
                          </tr>
                        </thead>
                        <tbody>
                          {probabilisticDebugData.markov_chain.top_transitions.map(
                            (trans, idx) => (
                              <tr key={idx}>
                                <td>{idx + 1}</td>
                                <td>{trans.from}</td>
                                <td>{trans.to}</td>
                                <td>
                                  <strong>
                                    {(trans.probability * 100).toFixed(2)}%
                                  </strong>
                                </td>
                                <td>{trans.count}</td>
                              </tr>
                            ),
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {probabilisticDebugData.naive_bayes_purchase && (
                  <div className="debug-card">
                    <h3>Naive Bayes - Purchase Prediction</h3>
                    <div className="debug-info">
                      <div className="info-row">
                        <span className="label">Trained:</span>
                        <span
                          className={`value ${
                            probabilisticDebugData.naive_bayes_purchase.trained
                              ? "success"
                              : "error"
                          }`}>
                          {probabilisticDebugData.naive_bayes_purchase.trained
                            ? "✅ Yes"
                            : "❌ No"}
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">Number of Features:</span>
                        <span className="value">
                          {
                            probabilisticDebugData.naive_bayes_purchase
                              .num_features
                          }
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">Classes:</span>
                        <span className="value">
                          {probabilisticDebugData.naive_bayes_purchase.classes.join(
                            ", ",
                          )}
                        </span>
                      </div>
                    </div>

                    <h4 style={{ marginTop: "1rem" }}>Class Priors</h4>
                    <div className="debug-info">
                      {Object.entries(
                        probabilisticDebugData.naive_bayes_purchase
                          .class_priors,
                      ).map(([cls, prob]) => (
                        <div className="info-row" key={cls}>
                          <span className="label">Class {cls}:</span>
                          <span className="value">{prob}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {probabilisticDebugData.naive_bayes_churn && (
                  <div className="debug-card">
                    <h3>Naive Bayes - Churn Prediction</h3>
                    <div className="debug-info">
                      <div className="info-row">
                        <span className="label">Trained:</span>
                        <span
                          className={`value ${
                            probabilisticDebugData.naive_bayes_churn.trained
                              ? "success"
                              : "error"
                          }`}>
                          {probabilisticDebugData.naive_bayes_churn.trained
                            ? "✅ Yes"
                            : "❌ No"}
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">Number of Features:</span>
                        <span className="value">
                          {
                            probabilisticDebugData.naive_bayes_churn
                              .num_features
                          }
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">Classes:</span>
                        <span className="value">
                          {probabilisticDebugData.naive_bayes_churn.classes.join(
                            ", ",
                          )}
                        </span>
                      </div>
                    </div>

                    <h4 style={{ marginTop: "1rem" }}>Class Priors</h4>
                    <div className="debug-info">
                      {Object.entries(
                        probabilisticDebugData.naive_bayes_churn.class_priors,
                      ).map(([cls, prob]) => (
                        <div className="info-row" key={cls}>
                          <span className="label">Class {cls}:</span>
                          <span className="value">{prob}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {probabilisticDebugData.user_analysis &&
                  !probabilisticDebugData.user_analysis.error && (
                    <>
                      <div className="debug-card">
                        <h3>User Analysis</h3>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">User:</span>
                            <span className="value">
                              {probabilisticDebugData.user_analysis.username}
                              <span className="id-badge">
                                ID:{" "}
                                {probabilisticDebugData.user_analysis.user_id}
                              </span>
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Total Orders:</span>
                            <span className="value">
                              {
                                probabilisticDebugData.user_analysis
                                  .total_orders
                              }
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Total Spent:</span>
                            <span className="value">
                              {probabilisticDebugData.user_analysis.total_spent}{" "}
                              PLN
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Avg Order Value:</span>
                            <span className="value">
                              {
                                probabilisticDebugData.user_analysis
                                  .avg_order_value
                              }{" "}
                              PLN
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">
                              Days Since Last Order:
                            </span>
                            <span className="value">
                              {
                                probabilisticDebugData.user_analysis
                                  .days_since_last_order
                              }
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">
                              Last Category Purchased:
                            </span>
                            <span className="value">
                              {
                                probabilisticDebugData.user_analysis
                                  .last_category
                              }
                            </span>
                          </div>
                        </div>

                        <h4 style={{ marginTop: "1rem" }}>
                          Purchase Sequence (Last 10)
                        </h4>
                        <p className="description">
                          {probabilisticDebugData.user_analysis.purchase_sequence.join(
                            " → ",
                          )}
                        </p>
                      </div>

                      {probabilisticDebugData.user_analysis
                        .markov_predictions &&
                        probabilisticDebugData.user_analysis.markov_predictions
                          .length > 0 && (
                          <div className="debug-card">
                            <h3>Next Purchase Predictions (Markov Chain)</h3>
                            <div className="similarities-table">
                              <table>
                                <thead>
                                  <tr>
                                    <th>#</th>
                                    <th>Predicted Category</th>
                                    <th>Probability</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {probabilisticDebugData.user_analysis.markov_predictions.map(
                                    (pred, idx) => (
                                      <tr key={idx}>
                                        <td>{idx + 1}</td>
                                        <td>{pred.category}</td>
                                        <td>
                                          <strong>
                                            {(pred.probability * 100).toFixed(
                                              2,
                                            )}
                                            %
                                          </strong>
                                        </td>
                                      </tr>
                                    ),
                                  )}
                                </tbody>
                              </table>
                            </div>
                          </div>
                        )}

                      <div className="debug-card">
                        <h3>User Behavior Predictions (Naive Bayes)</h3>

                        <h4>Purchase Probability</h4>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Active Buyer:</span>
                            <span className="value success">
                              <strong>
                                {(
                                  probabilisticDebugData.user_analysis
                                    .purchase_probability.active_buyer * 100
                                ).toFixed(2)}
                                %
                              </strong>
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Inactive:</span>
                            <span className="value">
                              {(
                                probabilisticDebugData.user_analysis
                                  .purchase_probability.inactive * 100
                              ).toFixed(2)}
                              %
                            </span>
                          </div>
                        </div>

                        <h4 style={{ marginTop: "1.5rem" }}>
                          Churn Probability
                        </h4>
                        <div className="debug-info">
                          <div className="info-row">
                            <span className="label">Will Churn:</span>
                            <span
                              className={`value ${
                                probabilisticDebugData.user_analysis
                                  .churn_probability.will_churn > 0.5
                                  ? "error"
                                  : ""
                              }`}>
                              <strong>
                                {(
                                  probabilisticDebugData.user_analysis
                                    .churn_probability.will_churn * 100
                                ).toFixed(2)}
                                %
                              </strong>
                            </span>
                          </div>
                          <div className="info-row">
                            <span className="label">Will Stay:</span>
                            <span
                              className={`value ${
                                probabilisticDebugData.user_analysis
                                  .churn_probability.will_stay > 0.5
                                  ? "success"
                                  : ""
                              }`}>
                              {(
                                probabilisticDebugData.user_analysis
                                  .churn_probability.will_stay * 100
                              ).toFixed(2)}
                              %
                            </span>
                          </div>
                        </div>
                      </div>
                    </>
                  )}

                {probabilisticDebugData.product_analysis &&
                  !probabilisticDebugData.product_analysis.error && (
                    <div className="debug-card">
                      <h3>Product Analysis</h3>
                      <div className="debug-info">
                        <div className="info-row">
                          <span className="label">Product:</span>
                          <span className="value">
                            {
                              probabilisticDebugData.product_analysis
                                .product_name
                            }
                            <span className="id-badge">
                              ID:{" "}
                              {
                                probabilisticDebugData.product_analysis
                                  .product_id
                              }
                            </span>
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Category:</span>
                          <span className="value">
                            {probabilisticDebugData.product_analysis.category}
                          </span>
                        </div>
                      </div>

                      <h4 style={{ marginTop: "1.5rem" }}>
                        Next Likely Categories
                      </h4>
                      <div className="similarities-table">
                        <table>
                          <thead>
                            <tr>
                              <th>#</th>
                              <th>Category</th>
                              <th>Probability</th>
                              <th>Count</th>
                            </tr>
                          </thead>
                          <tbody>
                            {probabilisticDebugData.product_analysis.next_likely_categories.map(
                              (cat, idx) => (
                                <tr key={idx}>
                                  <td>{idx + 1}</td>
                                  <td>{cat.category}</td>
                                  <td>
                                    <strong>
                                      {(cat.probability * 100).toFixed(2)}%
                                    </strong>
                                  </td>
                                  <td>{cat.count}</td>
                                </tr>
                              ),
                            )}
                          </tbody>
                        </table>
                      </div>

                      {probabilisticDebugData.product_analysis
                        .predicted_next_products &&
                        probabilisticDebugData.product_analysis
                          .predicted_next_products.length > 0 && (
                          <>
                            <h4 style={{ marginTop: "1.5rem" }}>
                              Predicted Next Products
                            </h4>
                            <div className="similarities-table">
                              <table>
                                <thead>
                                  <tr>
                                    <th>Product Name</th>
                                    <th>Category</th>
                                    <th>Price</th>
                                    <th>Transition Probability</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {probabilisticDebugData.product_analysis.predicted_next_products.map(
                                    (prod, idx) => (
                                      <tr key={idx}>
                                        <td>{prod.name}</td>
                                        <td>{prod.category}</td>
                                        <td>{prod.price} PLN</td>
                                        <td>
                                          <strong>
                                            {(
                                              prod.transition_probability * 100
                                            ).toFixed(2)}
                                            %
                                          </strong>
                                        </td>
                                      </tr>
                                    ),
                                  )}
                                </tbody>
                              </table>
                            </div>
                          </>
                        )}
                    </div>
                  )}

                {probabilisticDebugData.system_stats && (
                  <div className="debug-card">
                    <h3>System Statistics</h3>
                    <div className="debug-info">
                      <div className="info-row">
                        <span className="label">Total Users Analyzed:</span>
                        <span className="value">
                          {
                            probabilisticDebugData.system_stats
                              .total_users_analyzed
                          }
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">Total Categories:</span>
                        <span className="value">
                          {probabilisticDebugData.system_stats.total_categories}
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">Markov Chain Trained:</span>
                        <span
                          className={`value ${
                            probabilisticDebugData.system_stats.markov_trained
                              ? "success"
                              : "error"
                          }`}>
                          {probabilisticDebugData.system_stats.markov_trained
                            ? "✅ Yes"
                            : "❌ No"}
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">
                          Naive Bayes Purchase Trained:
                        </span>
                        <span
                          className={`value ${
                            probabilisticDebugData.system_stats
                              .naive_bayes_purchase_trained
                              ? "success"
                              : "error"
                          }`}>
                          {probabilisticDebugData.system_stats
                            .naive_bayes_purchase_trained
                            ? "✅ Yes"
                            : "❌ No"}
                        </span>
                      </div>
                      <div className="info-row">
                        <span className="label">
                          Naive Bayes Churn Trained:
                        </span>
                        <span
                          className={`value ${
                            probabilisticDebugData.system_stats
                              .naive_bayes_churn_trained
                              ? "success"
                              : "error"
                          }`}>
                          {probabilisticDebugData.system_stats
                            .naive_bayes_churn_trained
                            ? "✅ Yes"
                            : "❌ No"}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="debug-card">
                <p className="no-data">
                  {loading
                    ? "Loading probabilistic debug data..."
                    : "No probabilistic debug data available."}
                </p>
              </div>
            )}
          </div>
        )}
      </motion.div>

      {showAllSimilaritiesModal && (
        <div className="modal-overlay" onClick={closeAllSimilaritiesModal}>
          <div
            className="modal-content-large"
            onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>All Product Similarities ({allSimilarities.length})</h2>
              <button
                className="common-modal-close modal-close"
                onClick={closeAllSimilaritiesModal}>
                ×
              </button>
            </div>
            <div className="modal-body-rules">
              {allSimilaritiesLoading ? (
                <div className="loading-spinner"></div>
              ) : (
                <>
                  <div className="rules-table-container">
                    <table className="rules-table">
                      <thead>
                        <tr>
                          <th>Rank</th>
                          <th>Product 1</th>
                          <th>Product 2</th>
                          <th>Similarity Score</th>
                        </tr>
                      </thead>
                      <tbody>
                        {allSimilarities
                          .slice(
                            (similaritiesPage - 1) * similaritiesPerPage,
                            similaritiesPage * similaritiesPerPage,
                          )
                          .map((sim, index) => (
                            <tr
                              key={`sim-${index}-${sim.product1_name}-${sim.product2_name}`}>
                              <td>
                                {(similaritiesPage - 1) * similaritiesPerPage +
                                  index +
                                  1}
                              </td>
                              <td>{sim.product1_name}</td>
                              <td>{sim.product2_name}</td>
                              <td>{sim.score.toFixed(4)}</td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                  <div className="pagination">
                    <button
                      onClick={() =>
                        setSimilaritiesPage((p) => Math.max(1, p - 1))
                      }
                      disabled={similaritiesPage === 1}>
                      Previous
                    </button>
                    <span>
                      Page {similaritiesPage} of{" "}
                      {Math.ceil(allSimilarities.length / similaritiesPerPage)}
                    </span>
                    <button
                      onClick={() =>
                        setSimilaritiesPage((p) =>
                          Math.min(
                            Math.ceil(
                              allSimilarities.length / similaritiesPerPage,
                            ),
                            p + 1,
                          ),
                        )
                      }
                      disabled={
                        similaritiesPage >=
                        Math.ceil(allSimilarities.length / similaritiesPerPage)
                      }>
                      Next
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDebug;
