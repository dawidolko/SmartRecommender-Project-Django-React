import React, { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Code, Brain, MessageSquare, Link2, Grid } from "lucide-react";
import config from "../../config/config";
import { toast } from "react-toastify";
import "./AdminPanel.scss";

const AdminDebug = () => {
  const [activeMethod, setActiveMethod] = useState("collaborative");
  const [cfDebugData, setCfDebugData] = useState(null);
  const [sentimentDebugData, setSentimentDebugData] = useState(null);
  const [sentimentDetailData, setSentimentDetailData] = useState(null);
  const [associationDebugData, setAssociationDebugData] = useState(null);
  const [contentBasedDebugData, setContentBasedDebugData] = useState(null);
  const [selectedProductId, setSelectedProductId] = useState("");
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProducts();
  }, []);

  useEffect(() => {
    setSelectedProductId("");
    setSentimentDetailData(null);
    setAssociationDebugData(null);
    setContentBasedDebugData(null);

    if (activeMethod === "collaborative") {
      fetchCFDebug();
    } else if (activeMethod === "sentiment") {
      fetchSentimentDebug();
    } else if (activeMethod === "content") {
      fetchContentBasedDebug();
    }
  }, [activeMethod]);

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

  const fetchCFDebug = async () => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        `${config.apiUrl}/api/collaborative-filtering-debug/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setCfDebugData(res.data);
    } catch (err) {
      console.error("Error fetching CF debug:", err);
      toast.error("Failed to fetch Collaborative Filtering debug data.");
    } finally {
      setLoading(false);
    }
  };

  const fetchSentimentDebug = async () => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        `${config.apiUrl}/api/sentiment-analysis-debug/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
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
        }
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
        }
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
      }
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
          Inspect internal workings of all 4 machine learning methods used in
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
          className={`method-tab ${
            activeMethod === "content" ? "active" : ""
          }`}
          onClick={() => setActiveMethod("content")}>
          <Grid className="tab-icon" />
          Content-Based
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
                                  )
                                )}
                              </tbody>
                            </table>
                          </div>
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
                                  )
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
                                  )
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
                                )
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
                                    ", "
                                  )}
                                </span>
                              </div>
                              <div className="info-row">
                                <span className="label">
                                  Examples (Negative):
                                </span>
                                <span className="value">
                                  {sentimentDetailData.lexicon_info.examples_negative.join(
                                    ", "
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
                                          2
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
                                  )
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
                            {contentBasedDebugData.database_stats.total_products}
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Saved Similarities:</span>
                          <span className="value">
                            {contentBasedDebugData.database_stats.saved_similarities}
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Percentage Saved:</span>
                          <span className="value">
                            {contentBasedDebugData.database_stats.percentage_saved}%
                          </span>
                        </div>
                        <div className="info-row">
                          <span className="label">Threshold:</span>
                          <span className="value">
                            {contentBasedDebugData.database_stats.threshold * 100}%
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
                            {contentBasedDebugData.feature_weights.category * 100}%
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
                            {contentBasedDebugData.feature_weights.keywords * 100}%
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
                                {contentBasedDebugData.selected_product.price} PLN
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Price Category:</span>
                              <span className="value">
                                {contentBasedDebugData.selected_product.price_category}
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Categories:</span>
                              <span className="value">
                                {contentBasedDebugData.selected_product.categories.join(", ")}
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Tags:</span>
                              <span className="value">
                                {contentBasedDebugData.selected_product.tags.join(", ")}
                              </span>
                            </div>
                            <div className="info-row">
                              <span className="label">Keywords:</span>
                              <span className="value">
                                {contentBasedDebugData.selected_product.keywords.join(", ")}
                              </span>
                            </div>
                          </div>
                        </div>

                        <div className="debug-card">
                          <h3>
                            Feature Vector ({contentBasedDebugData.feature_vector.vector_length} features)
                          </h3>
                          <div className="debug-info">
                            {Object.entries(contentBasedDebugData.feature_vector.features).map(([key, value]) => (
                              <div key={key} className="info-row">
                                <span className="label">{key}:</span>
                                <span className="value">{value.toFixed(3)}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        {contentBasedDebugData.similar_products && contentBasedDebugData.similar_products.count > 0 && (
                          <div className="debug-card">
                            <h3>
                              Top {contentBasedDebugData.similar_products.count} Similar Products
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
                                  {contentBasedDebugData.similar_products.top_10.map((sim, idx) => (
                                    <tr key={idx}>
                                      <td>{idx + 1}</td>
                                      <td>{sim.product_2.name}</td>
                                      <td>
                                        <strong>{(sim.similarity_score * 100).toFixed(2)}%</strong>
                                      </td>
                                      <td>{sim.product_2.price} PLN</td>
                                      <td>{sim.product_2.categories.join(", ")}</td>
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>

                            <div className="calculations-section">
                              <h4>Similarity Calculations</h4>
                              {contentBasedDebugData.similar_products.top_10.slice(0, 3).map((sim, idx) => (
                                <div key={idx} className="calculation-card">
                                  <h5>
                                    #{idx + 1} {sim.product_2.name}
                                  </h5>
                                  <div className="calculation-info">
                                    <p className="formula-text">{sim.calculation.formula}</p>
                                    <div className="calculation-details">
                                      <span>Dot Product: {sim.calculation.dot_product}</span>
                                      <span>Norm 1: {sim.calculation.norm_product1}</span>
                                      <span>Norm 2: {sim.calculation.norm_product2}</span>
                                    </div>
                                    <p className={`verification ${sim.calculation.stored_vs_calculated.match ? 'success' : 'error'}`}>
                                      Stored: {sim.calculation.stored_vs_calculated.stored} |
                                      Calculated: {sim.calculation.stored_vs_calculated.calculated}
                                      {sim.calculation.stored_vs_calculated.match ? ' ✓ Match' : ' ✗ Mismatch'}
                                    </p>
                                    {Object.keys(sim.common_features).length > 0 && (
                                      <div className="common-features-section">
                                        <p>
                                          <strong>Common Features ({sim.common_features_count} total):</strong>
                                        </p>
                                        <div className="features-list">
                                          {Object.entries(sim.common_features).map(([feat, vals]) => (
                                            <span key={feat} className="feature-badge">
                                              {feat}: {vals.product1_value} ↔ {vals.product2_value}
                                            </span>
                                          ))}
                                        </div>
                                      </div>
                                    )}
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </>
                    )}

                    {!selectedProductId && contentBasedDebugData.top_10_global_similarities && (
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
                              {contentBasedDebugData.top_10_global_similarities.map((sim, idx) => (
                                <tr key={idx}>
                                  <td>{idx + 1}</td>
                                  <td>
                                    {sim.product1_name}
                                    <span className="id-badge">ID: {sim.product1_id}</span>
                                  </td>
                                  <td>
                                    {sim.product2_name}
                                    <span className="id-badge">ID: {sim.product2_id}</span>
                                  </td>
                                  <td>
                                    <strong>{(sim.score * 100).toFixed(2)}%</strong>
                                  </td>
                                </tr>
                              ))}
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
                          <span className={`value ${contentBasedDebugData.computation_status.can_compute ? 'success' : 'error'}`}>
                            {contentBasedDebugData.computation_status.can_compute ? '✅ Yes' : '❌ No'}
                          </span>
                        </div>
                      </div>
                      <div className="issues-list">
                        {contentBasedDebugData.computation_status.issues.map((issue, idx) => (
                          <p key={idx} className={issue.includes('✅') ? 'success' : 'warning'}>
                            {issue}
                          </p>
                        ))}
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
      </motion.div>
    </div>
  );
};

export default AdminDebug;
