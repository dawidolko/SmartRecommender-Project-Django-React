import React from "react";
import { X } from "lucide-react";
import "./ProbabilisticModal.scss";

const ProbabilisticModal = ({ isOpen, onClose, title, type, data }) => {
  if (!isOpen) return null;

  const renderModalContent = () => {
    switch (type) {
      case "purchase_patterns":
        if (
          !data ||
          !data.recommendations ||
          data.recommendations.length === 0
        ) {
          return (
            <div className="modal-no-data">
              <p>No purchase patterns data available.</p>
              <p>
                This may be because there are no recent purchase patterns to
                analyze.
              </p>
            </div>
          );
        }

        return (
          <div className="purchase-patterns-content">
            <h3>Purchase Patterns Analysis</h3>
            <div className="patterns-grid">
              {data.recommendations.map((pattern, index) => (
                <div key={index} className="pattern-card">
                  <h4>Category: {pattern.category || "Unknown"}</h4>
                  <div className="pattern-details">
                    <p>
                      <strong>Purchase Frequency:</strong>{" "}
                      {pattern.purchase_frequency || 0} times/month
                    </p>
                    <p>
                      <strong>Average Order Value:</strong> $
                      {pattern.average_order_value || 0}
                    </p>
                    <p>
                      <strong>Next Purchase Likely:</strong>{" "}
                      {pattern.next_purchase_likely || "Unknown"}
                    </p>
                  </div>
                </div>
              ))}
            </div>
            {data.user_insights && (
              <div className="user-insights">
                <h4>User Insights</h4>
                <p>
                  <strong>Most Active Category:</strong>{" "}
                  {data.user_insights.most_active_category || "None"}
                </p>
                <p>
                  <strong>Preferred Shopping Time:</strong>{" "}
                  {data.user_insights.preferred_shopping_time || "Unknown"}
                </p>
              </div>
            )}
          </div>
        );

      case "customer_segmentation":
        return (
          <div className="customer-segmentation-content">
            <h3>Customer Segmentation Overview</h3>
            <div className="segments-grid">
              <div className="segment-card">
                <h4>High Value Customers</h4>
                <p>Customers with lifetime value above $500</p>
                <div className="segment-stats">
                  <p>
                    <strong>Percentage:</strong> 15%
                  </p>
                  <p>
                    <strong>Average Order Value:</strong> $250
                  </p>
                </div>
              </div>
              <div className="segment-card">
                <h4>Frequent Shoppers</h4>
                <p>Customers making 5+ purchases per month</p>
                <div className="segment-stats">
                  <p>
                    <strong>Percentage:</strong> 25%
                  </p>
                  <p>
                    <strong>Loyalty Rate:</strong> 85%
                  </p>
                </div>
              </div>
              <div className="segment-card">
                <h4>At-Risk Customers</h4>
                <p>Customers with high churn probability</p>
                <div className="segment-stats">
                  <p>
                    <strong>Percentage:</strong> 10%
                  </p>
                  <p>
                    <strong>Risk Level:</strong> 75%+
                  </p>
                </div>
              </div>
              <div className="segment-card">
                <h4>Occasional Shoppers</h4>
                <p>Customers shopping 1-2 times per month</p>
                <div className="segment-stats">
                  <p>
                    <strong>Percentage:</strong> 50%
                  </p>
                  <p>
                    <strong>Engagement Rate:</strong> 40%
                  </p>
                </div>
              </div>
            </div>
          </div>
        );

      case "churn_prediction":
        if (
          !data ||
          !data.high_risk_alerts ||
          data.high_risk_alerts.length === 0
        ) {
          return (
            <div className="modal-no-data">
              <p>No churn predictions available.</p>
              <p>All customers appear to be at low risk of churning.</p>
            </div>
          );
        }

        const churnAlerts = data.high_risk_alerts.filter(
          (alert) => alert.risk_type === "customer_churn"
        );

        if (churnAlerts.length === 0) {
          return (
            <div className="modal-no-data">
              <p>No customer churn risks found.</p>
              <p>All customers appear to be engaged and active.</p>
            </div>
          );
        }

        return (
          <div className="churn-prediction-content">
            <h3>Churn Prediction Analysis</h3>
            <div className="churn-grid">
              {churnAlerts.map((alert, index) => (
                <div key={index} className="churn-card">
                  <h4>Customer: {alert.entity_name}</h4>
                  <div className="churn-details">
                    <p>
                      <strong>Risk Level:</strong>{" "}
                      {(alert.risk_score * 100).toFixed(0)}%
                    </p>
                    <p>
                      <strong>Confidence:</strong>{" "}
                      {(alert.confidence * 100).toFixed(0)}%
                    </p>
                    <div className="mitigation-actions">
                      <h5>Recommended Actions:</h5>
                      <p>
                        {alert.mitigation || "No specific actions recommended"}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );

      case "product_recommendations":
        if (!data || !data.predictions || data.predictions.length === 0) {
          return (
            <div className="modal-no-data">
              <p>No product recommendations available.</p>
              <p>No purchase probability data found for current user.</p>
            </div>
          );
        }

        return (
          <div className="product-recommendations-content">
            <h3>Product Recommendations</h3>
            <div className="recommendations-grid">
              {data.predictions.map((product, index) => (
                <div key={index} className="recommendation-card">
                  <h4>{product.name || "Unknown Product"}</h4>
                  <div className="recommendation-details">
                    <p>
                      <strong>Purchase Probability:</strong>{" "}
                      {product.purchase_probability || 0}%
                    </p>
                    <p>
                      <strong>Confidence Level:</strong>{" "}
                      {product.confidence || 0}%
                    </p>
                    <p>
                      <strong>Price:</strong> ${product.price || "N/A"}
                    </p>
                  </div>
                </div>
              ))}
            </div>
            {data.message && (
              <p className="recommendation-message">{data.message}</p>
            )}
          </div>
        );

      default:
        return <div className="modal-no-data">Data type not recognized</div>;
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="modal-close" onClick={onClose}>
            <X size={24} />
          </button>
        </div>
        <div className="modal-body">{renderModalContent()}</div>
      </div>
    </div>
  );
};

export default ProbabilisticModal;
