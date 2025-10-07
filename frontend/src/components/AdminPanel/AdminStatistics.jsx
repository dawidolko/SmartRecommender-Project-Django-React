import React, { useEffect, useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import {
  BarChart2,
  ShoppingBag,
  DollarSign,
  Users,
  Star,
  ShoppingCart,
  TrendingUp,
  List,
  Link2,
  RefreshCw,
  Code,
} from "lucide-react";
import StatCard from "./StatCard";
import config from "../../config/config";
import { toast } from "react-toastify";
import "./AdminPanel.scss";

const AdminStatistics = () => {
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalSales: 0,
    topSelling: 0,
    totalUsers: 0,
    totalOpinions: 0,
    averageRating: 0,
    topCategoryName: "",
    topTagName: "",
    churnRate: "0%",
    conversionRate: "0%",
  });
  const [loading, setLoading] = useState(false);
  const [currentAlgorithm, setCurrentAlgorithm] = useState(null);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState(null);
  const [recommendationPreview, setRecommendationPreview] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [associationRules, setAssociationRules] = useState([]);
  const [associationLoading, setAssociationLoading] = useState(false);
  const [isUpdatingRules, setIsUpdatingRules] = useState(false);
  const [algorithmStatus, setAlgorithmStatus] = useState(null);

  useEffect(() => {
    fetchStats();
    fetchRecommendationSettings();
    fetchAssociationRules();
    fetchAlgorithmStatus();

    const checkAndGenerateRules = async () => {
      const token = localStorage.getItem("access");
      try {
        const res = await axios.get(`${config.apiUrl}/api/association-rules/`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!res.data.rules || res.data.rules.length === 0) {
          axios
            .post(
              `${config.apiUrl}/api/update-association-rules/`,
              {
                min_support: 0.005, // 0.5%
                min_confidence: 0.05, // 5%
                min_lift: 1.0,
              },
              {
                headers: { Authorization: `Bearer ${token}` },
              }
            )
            .then(() => {
              fetchAssociationRules();
            })
            .catch((err) => {
              console.error("❌ Failed to auto-generate rules:", err);
            });
        }
      } catch (err) {
        console.error("Error checking association rules:", err);
      }
    };

    setTimeout(checkAndGenerateRules, 1000);
  }, []);

  useEffect(() => {
    if (currentAlgorithm) {
      fetchRecommendationPreview(currentAlgorithm);
    }
  }, [currentAlgorithm]);

  const fetchStats = async () => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        `${config.apiUrl}/api/admin-dashboard-stats/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setStats({
        totalProducts: res.data.totalProducts || 0,
        totalSales: res.data.totalSales || 0,
        topSelling: res.data.topSelling || 0,
        totalUsers: res.data.clients || 0,
        totalOpinions: res.data.totalOpinions || 0,
        averageRating: res.data.averageRating || 0,
        topCategoryName: res.data.topCategoryName || "",
        topTagName: res.data.topTagName || "",
        churnRate: res.data.churnRate || "0%",
        conversionRate: res.data.conversionRate || "0%",
      });
      setLoading(false);
    } catch (err) {
      console.error("Error fetching statistics:", err);
      toast.error("Failed to fetch statistics. Please try again.");
      setLoading(false);
    }
  };

  const fetchAlgorithmStatus = async () => {
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        `${config.apiUrl}/api/recommendation-algorithm-status/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setAlgorithmStatus(res.data);
    } catch (err) {
      console.error("Error fetching algorithm status:", err);
    }
  };

  const fetchRecommendationSettings = async () => {
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        `${config.apiUrl}/api/recommendation-settings/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      const algorithm = res.data.active_algorithm || "collaborative";
      setCurrentAlgorithm(algorithm);
      setSelectedAlgorithm(algorithm);
    } catch (err) {
      console.error("Error fetching recommendation settings:", err);
      setCurrentAlgorithm("collaborative");
      setSelectedAlgorithm("collaborative");
    }
  };

  const fetchRecommendationPreview = async (algorithm) => {
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        `${config.apiUrl}/api/recommendation-preview/?algorithm=${algorithm}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setRecommendationPreview(res.data);
    } catch (err) {
      console.error("Error fetching recommendation preview:", err);
    }
  };

  const fetchAssociationRules = async (bypassCache = false) => {
    setAssociationLoading(true);
    const token = localStorage.getItem("access");
    try {
      const cacheBuster = bypassCache ? `?t=${Date.now()}` : "";
      const res = await axios.get(
        `${config.apiUrl}/api/association-rules/${cacheBuster}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      setAssociationRules(res.data.rules ? res.data.rules.slice(0, 10) : []);

      if (res.data.total_rules !== undefined) {
      }

      if (!res.data.rules || res.data.rules.length === 0) {
        console.warn(
          "⚠️ No association rules found. Click 'Update Rules' to generate them."
        );
      }
    } catch (err) {
      console.error("Error fetching association rules:", err);
      toast.error("Failed to fetch association rules.");
    } finally {
      setAssociationLoading(false);
    }
  };

  const updateAssociationRules = async () => {
    setIsUpdatingRules(true);
    const token = localStorage.getItem("access");
    try {
      const res = await axios.post(
        `${config.apiUrl}/api/update-association-rules/`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (res.data.rules_created === 0) {
        toast.warning(
          `⚠️ No association rules created! Current transactions: ${res.data.total_transactions}`,
          { autoClose: 8000 }
        );
      } else {
        toast.success(
          `✅ Successfully created ${res.data.rules_created} association rules from ${res.data.total_transactions} transactions!`,
          { autoClose: 5000 }
        );
      }

      fetchAssociationRules(true);
    } catch (err) {
      console.error("Error updating association rules:", err);
      const errorMsg =
        err.response?.data?.error || "Failed to update association rules.";
      toast.error(errorMsg);
    } finally {
      setIsUpdatingRules(false);
    }
  };

  const handleAlgorithmChange = (algorithm) => {
    setSelectedAlgorithm(algorithm);
  };

  const handleApplyAlgorithm = async () => {
    if (isProcessing) return;

    setTimeout(() => {
      window.location.reload();
    }, 1000);

    const token = localStorage.getItem("access");
    setIsProcessing(true);
    try {
      const res = await axios.post(
        `${config.apiUrl}/api/recommendation-settings/`,
        { algorithm: selectedAlgorithm },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (res.data.success) {
        toast.success(
          `${selectedAlgorithm} algorithm applied successfully! This will be used across the website.`
        );
        setCurrentAlgorithm(selectedAlgorithm);

        const processRes = await axios.post(
          `${config.apiUrl}/api/process-recommendations/`,
          { algorithm: selectedAlgorithm },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        if (processRes.data.success) {
          toast.success("Recommendations processed successfully!");
        }
      }
    } catch (err) {
      console.error("Error updating recommendation settings:", err);
      toast.error("Failed to update recommendation settings.");
      setIsProcessing(false);
    }
  };

  const hasChanges = currentAlgorithm !== selectedAlgorithm;

  if (loading && currentAlgorithm === null) {
    return <div className="loading-spinner"></div>;
  }

  return (
    <div className="admin-content">
      <div className="stat_Cards">
        <StatCard
          name="All Products"
          icon={ShoppingBag}
          value={stats.totalProducts}
          color="#8B5CF6"
          variant="first"
        />
        <StatCard
          name="Best Selling"
          icon={TrendingUp}
          value={stats.topSelling}
          color="#10B981"
          variant="third"
        />
        <StatCard
          name="Total Sales"
          icon={DollarSign}
          value={`$${stats.totalSales.toLocaleString("en-US", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}`}
          color="#EF4444"
          variant="second"
        />
        <StatCard
          name="All Users"
          icon={Users}
          value={stats.totalUsers}
          color="#F59E0B"
          variant="fourth"
        />
      </div>

      <div className="stat_Cards">
        <StatCard
          name="All Opinions"
          icon={Star}
          value={stats.totalOpinions}
          color="#6366F1"
          variant="fifth"
        />
        <StatCard
          name="Average Rating"
          icon={BarChart2}
          value={stats.averageRating.toFixed(1)}
          color="#10B981"
          variant="sixth"
        />
        <StatCard
          name="Top Category"
          icon={ShoppingCart}
          value={stats.topCategoryName || "—"}
          color="#F59E0B"
          variant="seventh"
        />
        <StatCard
          name="Top Tag"
          icon={List}
          value={stats.topTagName || "—"}
          color="#EF4444"
          variant="eighth"
        />
      </div>

      <motion.div
        className="admin-statistics-container"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}>
        <div className="admin-statistics-card">
          <h2 className="admin-statistics-title">Statistics Overview</h2>
          <div className="admin-statistics-content">
            <p>
              This page provides a summary of key performance indicators for
              your store.
            </p>
            <p>
              Monitor sales trends, customer engagement, and product performance
              all in one place.
            </p>
          </div>
        </div>
      </motion.div>

      {algorithmStatus && (
        <motion.div
          className="algorithm-status-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}>
          <div className="algorithm-status-card">
            <div className="algorithm-status-header">
              <h2 className="algorithm-status-title">
                <Code className="algorithm-status-icon" />
                Implementation Status
              </h2>
            </div>
            <div className="algorithm-status-content">
              <p className="algorithm-status-description">
                Overview of recommendation algorithm implementations:
              </p>
              <div className="algorithms-grid">
                {Object.entries(algorithmStatus.algorithms).map(
                  ([key, algo]) => (
                    <div key={key} className="algorithm-item">
                      <h4 className="algorithm-name">
                        {key === "content_based"
                          ? "Content-Based Filtering"
                          : "Collaborative Filtering"}
                      </h4>
                      <div className="algorithm-details">
                        <p>
                          <strong>Implementation:</strong> {algo.implementation}
                        </p>
                        <p>
                          <strong>Similarities:</strong> {algo.similarity_count}
                        </p>
                        <p>
                          <strong>Description:</strong> {algo.description}
                        </p>
                      </div>
                      <div
                        className={`implementation-badge ${
                          algo.implementation.includes("Custom")
                            ? "custom"
                            : "library"
                        }`}>
                        {algo.implementation.includes("Custom")
                          ? "Manual Implementation"
                          : "Library Implementation"}
                      </div>
                    </div>
                  )
                )}
              </div>
              <div className="custom-implementations">
                <h4>Custom Manual Implementations:</h4>
                <div className="custom-methods">
                  {algorithmStatus.custom_implementations.map(
                    (method, index) => (
                      <span key={index} className="custom-method-badge">
                        {method.replace("_", " ").toUpperCase()}
                      </span>
                    )
                  )}
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      <motion.div
        className="association-rules-section"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}>
        <div className="association-rules-card">
          <div className="association-rules-header">
            <h2 className="association-rules-title">
              <Link2 className="association-rules-icon" />
              Association Rules Management
              <span className="custom-implementation-badge">
                Custom Apriori
              </span>
            </h2>
            <button
              className="update-rules-btn"
              onClick={updateAssociationRules}
              disabled={isUpdatingRules}>
              <RefreshCw
                className={`icon ${isUpdatingRules ? "rotating" : ""}`}
              />
              {isUpdatingRules ? "Updating..." : "Update Rules"}
            </button>
          </div>

          <div className="association-rules-content">
            <p className="association-rules-description">
              Association rules help identify products frequently bought
              together. These rules power the "Frequently Bought Together"
              recommendations in the shopping cart.{" "}
              <strong>
                Using custom manual Apriori algorithm implementation with real
                formulas from scientific literature (Agrawal & Srikant 1994).
              </strong>
            </p>

            {associationLoading ? (
              <div className="association-rules-loading">
                Loading association rules...
              </div>
            ) : associationRules.length > 0 ? (
              <div className="association-rules-table">
                <table>
                  <thead>
                    <tr>
                      <th>Product 1</th>
                      <th>Product 2</th>
                      <th>Support</th>
                      <th>Confidence</th>
                      <th>Lift</th>
                    </tr>
                  </thead>
                  <tbody>
                    {associationRules.map((rule, index) => (
                      <tr key={rule.id || index}>
                        <td>{rule.product_1.name}</td>
                        <td>{rule.product_2.name}</td>
                        <td>{(rule.support * 100).toFixed(1)}%</td>
                        <td>{(rule.confidence * 100).toFixed(1)}%</td>
                        <td>{rule.lift.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="association-rules-empty">
                No association rules found. Click "Update Rules" to generate
                them using custom Apriori algorithm.
              </div>
            )}
          </div>
        </div>
      </motion.div>

      {currentAlgorithm !== null && (
        <motion.div
          className="recommendation-control-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}>
          <div className="recommendation-card">
            <h2 className="recommendation-title">Recommendation System</h2>
            <div className="recommendation-controls">
              <div className="algorithm-selection">
                <label className="algorithm-label">Select Algorithm:</label>
                <div className="algorithm-options">
                  <label className="radio-label">
                    <input
                      type="radio"
                      value="collaborative"
                      checked={selectedAlgorithm === "collaborative"}
                      onChange={() => handleAlgorithmChange("collaborative")}
                      disabled={isProcessing}
                    />
                    Collaborative Filtering (CF) - Library Implementation
                  </label>
                  <label className="radio-label">
                    <input
                      type="radio"
                      value="content_based"
                      checked={selectedAlgorithm === "content_based"}
                      onChange={() => handleAlgorithmChange("content_based")}
                      disabled={isProcessing}
                    />
                    Content-Based Filtering (CBF) -{" "}
                    <strong>Custom Manual Implementation</strong>
                  </label>
                </div>
              </div>
              <div className="algorithm-actions">
                <button
                  className="btn-primary"
                  onClick={handleApplyAlgorithm}
                  disabled={isProcessing || !hasChanges}
                  style={{
                    opacity: !hasChanges && !isProcessing ? 0.5 : 1,
                    cursor:
                      !hasChanges && !isProcessing ? "not-allowed" : "pointer",
                  }}>
                  {isProcessing ? "Processing..." : "Apply Algorithm"}
                </button>
              </div>
            </div>
          </div>

          <div className="recommendation-preview">
            <h3 className="preview-title">
              {currentAlgorithm === "collaborative"
                ? "Collaborative Filtering Preview (Library)"
                : "Content-Based Filtering Preview (Custom Manual)"}
            </h3>
            <div className="preview-content">
              {recommendationPreview.length > 0 ? (
                <div className="preview-products">
                  {recommendationPreview.map((product) => (
                    <Link
                      to={`/product/${product.id}`}
                      className="preview-product-link"
                      key={product.id}>
                      <div className="preview-product">
                        {product.photos?.[0]?.path && (
                          <img
                            src={`${config.apiUrl}/media/${product.photos[0].path}`}
                            alt={product.name}
                            className="preview-product-image"
                          />
                        )}
                        <div className="preview-product-info">
                          <h4>{product.name}</h4>
                          <p>${product.price}</p>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              ) : (
                <p className="preview-empty">
                  No recommendations available. Click "Apply Algorithm" to
                  generate.
                </p>
              )}
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default AdminStatistics;
