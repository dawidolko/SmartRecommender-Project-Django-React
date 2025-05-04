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
  Briefcase,
  TrendingUp,
  AlertTriangle,
  Package,
  Users,
  BarChart2,
} from "lucide-react";
import { motion } from "framer-motion";
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

const AdminProbabilistic = () => {
  const [activeTab, setActiveTab] = useState("forecast");
  const [salesForecasts, setSalesForecasts] = useState([]);
  const [riskData, setRiskData] = useState([]);
  const [demandForecasts, setDemandForecasts] = useState([]);
  const [userInsights, setUserInsights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const token = localStorage.getItem("access");
    console.log("Token:", token ? "exists" : "missing");

    try {
      console.log("Fetching forecast data...");
      const forecastRes = await fetch("/api/sales-forecast/", {
        headers: { Authorization: `Bearer ${token}` },
      });

      console.log("Forecast response status:", forecastRes.status);

      if (!forecastRes.ok) {
        throw new Error(`HTTP error! status: ${forecastRes.status}`);
      }

      const forecast = await forecastRes.json();
      console.log("Forecast data:", forecast);

      console.log("Fetching risk data...");
      const riskRes = await fetch("/api/risk-dashboard/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const risk = await riskRes.json();
      console.log("Risk data:", risk);

      console.log("Fetching demand data...");
      const demandRes = await fetch("/api/product-demand/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const demand = await demandRes.json();
      console.log("Demand data:", demand);

      setSalesForecasts(forecast.forecasts || []);
      setRiskData(risk);
      setDemandForecasts(demand.demand_forecasts || []);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
      setLoading(false);
    }
  };

  const getForecastChartData = () => {
    if (!salesForecasts.length) {
      console.log("No sales forecasts data available");
      return {
        labels: [],
        datasets: [],
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

  if (loading) {
    return <div className="loading">Loading probabilistic data...</div>;
  }

  return (
    <div className="admin-probabilistic">
      <div className="probabilistic-tabs">
        <TabButton id="forecast" label="Sales Forecast" icon={TrendingUp} />
        <TabButton id="demand" label="Product Demand" icon={Package} />
        <TabButton id="risk" label="Risk Dashboard" icon={AlertTriangle} />
        <TabButton id="insights" label="User Insights" icon={Users} />
      </div>

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
              {salesForecasts.length > 0 ? (
                <Line
                  data={getForecastChartData()}
                  options={{ responsive: true }}
                />
              ) : (
                <div className="no-data">No forecast data available</div>
              )}
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
                  {salesForecasts.slice(0, 10).map((forecast, index) => (
                    <tr key={index}>
                      <td>{forecast.product.name}</td>
                      <td>
                        {new Date(forecast.forecast_date).toLocaleDateString()}
                      </td>
                      <td>{forecast.predicted_quantity}</td>
                      <td>
                        {forecast.confidence_interval[0]} -{" "}
                        {forecast.confidence_interval[1]}
                      </td>
                      <td>{forecast.historical_accuracy}%</td>
                    </tr>
                  ))}
                  {salesForecasts.length === 0 && (
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
                  {demandForecasts.slice(0, 15).map((demand, index) => (
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
                  ))}
                  {demandForecasts.length === 0 && (
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
                {riskData.high_risk_alerts?.map((alert, index) => (
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
                ))}
                {(!riskData.high_risk_alerts ||
                  riskData.high_risk_alerts.length === 0) && (
                  <div className="no-data">No high risk alerts</div>
                )}
              </div>
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
                <button className="view-details">View Details</button>
              </div>
              <div className="insight-card">
                <h3>Customer Segmentation</h3>
                <p>Segment users based on buying behavior</p>
                <button className="view-details">View Details</button>
              </div>
              <div className="insight-card">
                <h3>Churn Prediction</h3>
                <p>Identify customers at risk of churning</p>
                <button className="view-details">View Details</button>
              </div>
              <div className="insight-card">
                <h3>Product Recommendations</h3>
                <p>Personalized product recommendations</p>
                <button className="view-details">View Details</button>
              </div>
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default AdminProbabilistic;
