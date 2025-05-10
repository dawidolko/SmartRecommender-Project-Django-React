import React, { useState, useEffect } from "react";
import { Line, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import {
  TrendingUp,
  AlertTriangle,
  Package,
  Users,
  BarChart2,
  ChevronLeft,
  ChevronRight,
  X,
} from "lucide-react";
import { motion } from "framer-motion";
import config from "../../config/config";
import "./AdminProbabilistic.scss";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="modal-close" onClick={onClose}>
            <X size={24} />
          </button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
};

const AdminProbabilistic = () => {
  const [activeTab, setActiveTab] = useState("forecast");
  const [salesForecasts, setSalesForecasts] = useState([]);
  const [riskData, setRiskData] = useState({
    high_risk_alerts: [],
    risk_overview: {},
  });
  const [demandForecasts, setDemandForecasts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [modalContent, setModalContent] = useState(null);
  const [modalTitle, setModalTitle] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(5);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const token = localStorage.getItem("access");
    setLoading(true);
    setError(null);

    try {
      const forecastRes = await fetch(`${config.apiUrl}/api/sales-forecast/`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!forecastRes.ok) {
        throw new Error(`HTTP error! status: ${forecastRes.status}`);
      }

      const forecast = await forecastRes.json();

      const riskRes = await fetch(`${config.apiUrl}/api/risk-dashboard/`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      const risk = await riskRes.json();

      const demandRes = await fetch(`${config.apiUrl}/api/product-demand/`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      const demand = await demandRes.json();

      setSalesForecasts(forecast.forecasts || []);
      setRiskData(risk || { high_risk_alerts: [], risk_overview: {} });
      setDemandForecasts(demand.demand_forecasts || []);
      setLoading(false);
    } catch (error) {
      setError(error.message);
      setLoading(false);
    }
  };

  const getForecastChartData = () => {
    if (!salesForecasts.length) {
      return {
        labels: ["No Data"],
        datasets: [
          {
            label: "Predicted Quantity",
            data: [0],
            borderColor: "rgb(75, 192, 192)",
            tension: 0.1,
            fill: false,
          },
        ],
      };
    }

    const labels = salesForecasts.map((f) =>
      new Date(f.forecast_date).toLocaleDateString()
    );
    const predicted = salesForecasts.map((f) => f.predicted_quantity);
    const lower = salesForecasts.map((f) => f.confidence_interval[0]);
    const upper = salesForecasts.map((f) => f.confidence_interval[1]);

    return {
      labels,
      datasets: [
        {
          label: "Predicted Quantity",
          data: predicted,
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1,
          fill: false,
        },
        {
          label: "Lower Bound",
          data: lower,
          borderColor: "rgba(255, 99, 132, 0.5)",
          borderDash: [5, 5],
          fill: false,
        },
        {
          label: "Upper Bound",
          data: upper,
          borderColor: "rgba(255, 99, 132, 0.5)",
          borderDash: [5, 5],
          fill: false,
        },
      ],
    };
  };

  const getRiskChartData = () => {
    if (
      !riskData.risk_overview ||
      Object.keys(riskData.risk_overview).length === 0
    ) {
      return {
        labels: ["No Data"],
        datasets: [
          {
            label: "Risk Items",
            data: [0],
            backgroundColor: "rgba(255, 99, 132, 0.5)",
          },
        ],
      };
    }

    const riskTypes = Object.keys(riskData.risk_overview || {});
    const riskCounts = riskTypes.map(
      (type) => riskData.risk_overview[type]?.length || 0
    );

    return {
      labels: riskTypes.map((type) => type.replace("_", " ").toUpperCase()),
      datasets: [
        {
          label: "Risk Items",
          data: riskCounts,
          backgroundColor: [
            "rgba(255, 99, 132, 0.5)",
            "rgba(54, 162, 235, 0.5)",
            "rgba(255, 206, 86, 0.5)",
            "rgba(75, 192, 192, 0.5)",
          ],
        },
      ],
    };
  };

  const TabButton = ({ id, label, icon: Icon }) => (
    <button
      className={`tab-button ${activeTab === id ? "active" : ""}`}
      onClick={() => setActiveTab(id)}>
      <Icon size={20} />
      <span>{label}</span>
    </button>
  );

  const showModal = (title, content) => {
    setModalTitle(title);
    setModalContent(content);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setModalContent(null);
    setModalTitle("");
  };

  const handleInsightView = async (insightType) => {
    const token = localStorage.getItem("access");
    try {
      let modalContent = null;

      switch (insightType) {
        case "purchase_patterns":
          const patternsRes = await fetch(
            `${config.apiUrl}/api/admin-purchase-patterns/`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
              },
            }
          );
          const patternsData = await patternsRes.json();

          if (
            !patternsData.purchase_patterns ||
            patternsData.purchase_patterns.length === 0
          ) {
            modalContent = (
              <div className="insight-modal-content">
                <h3>No Purchase Patterns Data Available</h3>
                <p>There are no purchase patterns recorded in the system.</p>
              </div>
            );
          } else {
            modalContent = (
              <div className="insight-modal-content">
                <h3>Purchase Patterns Analysis</h3>
                <div className="patterns-list">
                  {patternsData.purchase_patterns
                    .slice(0, 5)
                    .map((userData, idx) => (
                      <div key={idx} className="user-patterns">
                        <h4 className="user-patterns-name">
                          User: {userData.user.email}
                        </h4>
                        <div className="patterns-grid">
                          {userData.patterns.map((pattern, index) => (
                            <div key={index} className="pattern-item">
                              <p>
                                <strong>Category:</strong> {pattern.category}
                              </p>
                              <p>
                                <strong>Purchase Frequency:</strong>{" "}
                                {pattern.purchase_frequency}/month
                              </p>
                              <p>
                                <strong>Average Order Value:</strong> $
                                {pattern.average_order_value}
                              </p>
                              <p>
                                <strong>Preferred Time:</strong>{" "}
                                {pattern.preferred_time}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                </div>
                <div className="summary">
                  <p>Total Users: {patternsData.summary.total_users}</p>
                  <p>Total Patterns: {patternsData.summary.total_patterns}</p>
                </div>
              </div>
            );
          }
          showModal("PURCHASE PATTERNS", modalContent);
          break;

        case "customer_segmentation":
          modalContent = (
            <div className="insight-modal-content">
              <h3>Customer Segmentation Overview</h3>
              <div className="segments-list">
                <div className="segment-item">
                  <h4>High Value Customers</h4>
                  <p>Customers with lifetime value above $500</p>
                </div>
                <div className="segment-item">
                  <h4>Frequent Shoppers</h4>
                  <p>Customers making 5+ purchases per month</p>
                </div>
                <div className="segment-item">
                  <h4>At-Risk Customers</h4>
                  <p>Customers with high churn probability</p>
                </div>
              </div>
            </div>
          );
          showModal("CUSTOMER SEGMENTATION", modalContent);
          break;

        case "churn_prediction":
          const churnRes = await fetch(
            `${config.apiUrl}/api/admin-churn-prediction/`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
              },
            }
          );
          const churnData = await churnRes.json();

          if (
            !churnData.churn_predictions ||
            churnData.churn_predictions.length === 0
          ) {
            modalContent = (
              <div className="insight-modal-content">
                <h3>No Churn Prediction Data Available</h3>
                <p>There are no customer churn risks recorded in the system.</p>
              </div>
            );
          } else {
            modalContent = (
              <div className="insight-modal-content">
                <h3>Churn Prediction Analysis</h3>
                <div className="summary-stats">
                  <div className="stat-item">
                    <span>High Risk:</span> {churnData.summary.high_risk_users}
                  </div>
                  <div className="stat-item">
                    <span>Medium Risk:</span>{" "}
                    {churnData.summary.medium_risk_users}
                  </div>
                  <div className="stat-item">
                    <span>Low Risk:</span> {churnData.summary.low_risk_users}
                  </div>
                </div>
                <div className="churn-list">
                  {churnData.churn_predictions.map((prediction, index) => (
                    <div key={index} className="churn-item">
                      <p>
                        <strong>Customer:</strong> {prediction.user_name}
                      </p>
                      <p>
                        <strong>Risk Level:</strong>{" "}
                        {(prediction.risk_score * 100).toFixed(0)}%
                      </p>
                      <p>
                        <strong>Confidence:</strong>{" "}
                        {(prediction.confidence * 100).toFixed(0)}%
                      </p>
                      <p>
                        <strong>Mitigation:</strong> {prediction.mitigation}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            );
          }
          showModal("CHURN PREDICTION", modalContent);
          break;

        case "product_recommendations":
          const recRes = await fetch(
            `${config.apiUrl}/api/admin-product-recommendations/`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
              },
            }
          );
          const recData = await recRes.json();

          if (
            !recData.user_recommendations ||
            recData.user_recommendations.length === 0
          ) {
            modalContent = (
              <div className="insight-modal-content">
                <h3>No Product Recommendations Available</h3>
                <p>
                  There are no product recommendations generated in the system.
                </p>
              </div>
            );
          } else {
            modalContent = (
              <div className="insight-modal-content">
                <h3>Product Recommendations</h3>
                <div className="recommendations-list">
                  {recData.user_recommendations
                    .slice(0, 5)
                    .map((userData, idx) => (
                      <div key={idx} className="user-recommendations">
                        <h4 className="user-recommendations-name">
                          User: {userData.user.email}
                        </h4>
                        <div className="recommendations-grid">
                          {userData.recommendations.map((rec, index) => (
                            <div key={index} className="recommendation-item">
                              <p>
                                <strong>Product:</strong> {rec.product}
                              </p>
                              <p>
                                <strong>Purchase Probability:</strong>{" "}
                                {(rec.probability * 100).toFixed(0)}%
                              </p>
                              <p>
                                <strong>Confidence:</strong>{" "}
                                {(rec.confidence * 100).toFixed(0)}%
                              </p>
                              {rec.price && (
                                <p>
                                  <strong>Price:</strong> $
                                  {rec.price.toFixed(2)}
                                </p>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            );
          }
          showModal("PRODUCT RECOMMENDATIONS", modalContent);
          break;

        default:
          break;
      }
    } catch (error) {
      showModal("Error", <p>Failed to fetch insight data: {error.message}</p>);
    }
  };

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentAlerts = riskData.high_risk_alerts?.slice(
    indexOfFirstItem,
    indexOfLastItem
  );

  const totalPages = Math.ceil(
    (riskData.high_risk_alerts?.length || 0) / itemsPerPage
  );

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  if (loading) {
    return <div className="loading-spinner"></div>;
  }

  if (error) {
    return (
      <div className="error">
        <h2>Error loading data:</h2>
        <p>{error}</p>
        <button onClick={fetchData} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="admin-probabilistic">
      <div className="probabilistic-tabs">
        <TabButton id="forecast" label="Sales Forecast" icon={TrendingUp} />
        <TabButton id="demand" label="Product Demand" icon={Package} />
        <TabButton id="risk" label="Risk Dashboard" icon={AlertTriangle} />
        <TabButton id="insights" label="User Insights" icon={Users} />
      </div>

      <Modal isOpen={isModalOpen} onClose={closeModal} title={modalTitle}>
        {modalContent}
      </Modal>

      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="tab-content">
        {activeTab === "forecast" && (
          <div className="forecast-section">
            <div className="forecast-header">
              <h2>Sales Forecasting</h2>
              <div className="summary-cards">
                <div className="summary-card">
                  <h3>Total Predicted Units</h3>
                  <p>
                    {salesForecasts.length > 0
                      ? salesForecasts.reduce(
                          (acc, curr) => acc + curr.predicted_quantity,
                          0
                        )
                      : 0}
                  </p>
                </div>
                <div className="summary-card">
                  <h3>Forecast Period</h3>
                  <p>30 days</p>
                </div>
              </div>
            </div>

            <div className="chart-container">
              <Line
                data={getForecastChartData()}
                options={{ responsive: true }}
              />
            </div>

            <div className="forecast-table">
              <h3>Detailed Forecast</h3>
              <table>
                <thead>
                  <tr>
                    <th>Product</th>
                    <th>Date</th>
                    <th>Predicted Quantity</th>
                    <th>Confidence Range</th>
                    <th>Accuracy</th>
                  </tr>
                </thead>
                <tbody>
                  {salesForecasts.length > 0 ? (
                    salesForecasts.slice(0, 10).map((forecast, index) => (
                      <tr key={index}>
                        <td>{forecast.product.name}</td>
                        <td>
                          {new Date(
                            forecast.forecast_date
                          ).toLocaleDateString()}
                        </td>
                        <td>{forecast.predicted_quantity}</td>
                        <td>
                          {forecast.confidence_interval[0]} -{" "}
                          {forecast.confidence_interval[1]}
                        </td>
                        <td>{forecast.historical_accuracy}%</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="5" style={{ textAlign: "center" }}>
                        No data available
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === "demand" && (
          <div className="demand-section">
            <div className="demand-header">
              <h2>Product Demand Forecasting</h2>
              <div className="alerts">
                {demandForecasts.some(
                  (d) => d.expected_demand > d.reorder_point
                ) && (
                  <div className="alert alert-warning">
                    <AlertTriangle />
                    <span>Some products need reordering</span>
                  </div>
                )}
              </div>
            </div>

            <div className="demand-table">
              <table>
                <thead>
                  <tr>
                    <th>Product</th>
                    <th>Period</th>
                    <th>Expected Demand</th>
                    <th>Reorder Point</th>
                    <th>Suggested Stock</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {demandForecasts.length > 0 ? (
                    demandForecasts.slice(0, 15).map((demand, index) => (
                      <tr key={index}>
                        <td>{demand.product.name}</td>
                        <td>{demand.forecast_period}</td>
                        <td>{demand.expected_demand}</td>
                        <td>{demand.reorder_point}</td>
                        <td>{demand.suggested_stock_level}</td>
                        <td>
                          {demand.expected_demand > demand.reorder_point ? (
                            <span className="status-warning">Reorder Soon</span>
                          ) : (
                            <span className="status-ok">OK</span>
                          )}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="6" style={{ textAlign: "center" }}>
                        No data available
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === "risk" && (
          <div className="risk-section">
            <div className="risk-overview">
              <h2>Risk Dashboard</h2>
              <div className="risk-summary">
                <div className="risk-stat">
                  <h3>Total Risk Items</h3>
                  <p>{riskData.high_risk_alerts?.length || 0}</p>
                </div>
                <div className="risk-stat">
                  <h3>Critical Risks</h3>
                  <p>
                    {riskData.high_risk_alerts?.filter(
                      (r) => r.risk_score > 0.8
                    ).length || 0}
                  </p>
                </div>
              </div>
            </div>

            <div className="risk-charts">
              <div className="chart-container">
                <Bar data={getRiskChartData()} options={{ responsive: true }} />
              </div>
            </div>

            <div className="risk-alerts">
              <h3>High Risk Alerts</h3>
              <div className="alerts-list">
                {currentAlerts?.length > 0 ? (
                  currentAlerts.map((alert, index) => (
                    <div key={index} className="alert-item">
                      <div className="alert-header">
                        <span className="alert-type">{alert.risk_type}</span>
                        <span
                          className={`risk-score score-${Math.floor(
                            alert.risk_score * 10
                          )}`}>
                          Risk: {(alert.risk_score * 100).toFixed(0)}%
                        </span>
                      </div>
                      <div className="alert-body">
                        <p>
                          <strong>Entity:</strong> {alert.entity_name}
                        </p>
                        <p>
                          <strong>Mitigation:</strong> {alert.mitigation}
                        </p>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="no-data">No high risk alerts</div>
                )}
              </div>

              {riskData.high_risk_alerts?.length > itemsPerPage && (
                <div className="pagination-container">
                  <div className="pagination-info">
                    <p className="pagination-text2">
                      Displaying {indexOfFirstItem + 1} to{" "}
                      {Math.min(
                        indexOfLastItem,
                        riskData.high_risk_alerts.length
                      )}{" "}
                      of {riskData.high_risk_alerts.length} alerts
                    </p>
                  </div>
                  <div className="pagination-controls">
                    <button
                      onClick={() => paginate(currentPage - 1)}
                      disabled={currentPage === 1}
                      className={`pagination-button ${
                        currentPage === 1 ? "disabled" : ""
                      }`}>
                      <ChevronLeft size={16} />
                      <span>&lt;</span>
                    </button>
                    {Array.from({ length: totalPages })
                      .map((_, index) => (
                        <button
                          key={index}
                          onClick={() => paginate(index + 1)}
                          className={`pagination-number ${
                            currentPage === index + 1 ? "active" : ""
                          }`}>
                          {index + 1}
                        </button>
                      ))
                      .slice(
                        Math.max(0, currentPage - 3),
                        Math.min(totalPages, currentPage + 2)
                      )}
                    <button
                      onClick={() => paginate(currentPage + 1)}
                      disabled={currentPage >= totalPages}
                      className={`pagination-button ${
                        currentPage >= totalPages ? "disabled" : ""
                      }`}>
                      <ChevronRight size={16} />
                      <span>&gt;</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === "insights" && (
          <div className="insights-section">
            <div className="insights-header">
              <h2>User Behavior Insights</h2>
              <button className="insights-refresh" onClick={fetchData}>
                <BarChart2 />
                Refresh Data
              </button>
            </div>

            <div className="insights-grid">
              <div className="insight-card">
                <h3>Purchase Patterns</h3>
                <p>Analyzing user purchase behavior across categories</p>
                <button
                  className="view-details"
                  onClick={() => handleInsightView("purchase_patterns")}>
                  View Details
                </button>
              </div>
              <div className="insight-card">
                <h3>Customer Segmentation</h3>
                <p>Segment users based on buying behavior</p>
                <button
                  className="view-details"
                  onClick={() => handleInsightView("customer_segmentation")}>
                  View Details
                </button>
              </div>
              <div className="insight-card">
                <h3>Churn Prediction</h3>
                <p>Identify customers at risk of churning</p>
                <button
                  className="view-details"
                  onClick={() => handleInsightView("churn_prediction")}>
                  View Details
                </button>
              </div>
              <div className="insight-card">
                <h3>Product Recommendations</h3>
                <p>Personalized product recommendations</p>
                <button
                  className="view-details"
                  onClick={() => handleInsightView("product_recommendations")}>
                  View Details
                </button>
              </div>
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default AdminProbabilistic;
