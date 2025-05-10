import React, { useState, useEffect } from "react";
import { Line, Pie } from "react-chartjs-2";
import { Link } from "react-router-dom";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import {
  TrendingUp,
  ShoppingBag,
  Clock,
  Heart,
  X,
  Calendar,
} from "react-feather";
import config from "../../config/config";
import "./ClientProbabilistic.scss";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
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

const ClientProbabilistic = () => {
  const [activeTab, setActiveTab] = useState("recommendations");
  const [recommendationsData, setRecommendationsData] = useState([]);
  const [shoppingProfile, setShoppingProfile] = useState({});
  const [seasonalTips, setSeasonalTips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [modalContent, setModalContent] = useState(null);
  const [modalTitle, setModalTitle] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const token = localStorage.getItem("access");
    setLoading(true);
    setError(null);

    try {
      const insightsRes = await fetch(
        `${config.apiUrl}/api/my-shopping-insights/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!insightsRes.ok) {
        throw new Error(`HTTP error! status: ${insightsRes.status}`);
      }

      const insightsData = await insightsRes.json();

      const enhancedRecommendations = (
        insightsData.personalized_suggestions || []
      ).map((product) => {
        const imageUrl =
          product.photos && product.photos[0] && product.photos[0].path
            ? `${config.apiUrl}/media/${product.photos[0].path}`
            : null;

        return {
          ...product,
          image_url: product.image_url || imageUrl || null,
        };
      });

      setRecommendationsData(enhancedRecommendations);
      setShoppingProfile(insightsData.your_shopping_profile || {});
      setSeasonalTips(insightsData.recommendations?.seasonal_tips || []);
      setLoading(false);
    } catch (error) {
      setError(error.message);
      setLoading(false);
    }
  };

  const getRecommendationsChartData = () => {
    if (!recommendationsData.length) {
      return {
        labels: ["No Data"],
        datasets: [
          {
            data: [1],
            backgroundColor: ["#e0e0e0"],
          },
        ],
      };
    }

    return {
      labels: recommendationsData.map((r) => r.name),
      datasets: [
        {
          data: recommendationsData.map((r) => r.match_score),
          backgroundColor: [
            "rgba(255, 99, 132, 0.6)",
            "rgba(54, 162, 235, 0.6)",
            "rgba(255, 206, 86, 0.6)",
            "rgba(75, 192, 192, 0.6)",
            "rgba(153, 102, 255, 0.6)",
          ],
          borderWidth: 1,
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

  const handleViewMore = (type) => {
    const token = localStorage.getItem("access");

    switch (type) {
      case "shopping_profile":
        fetch(`${config.apiUrl}/api/purchase-prediction/`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        })
          .then((res) => res.json())
          .then((data) => {
            const modalContent = (
              <div className="profile-details">
                <h3>Your Shopping Profile</h3>
                <p>
                  Based on your purchase history and browsing patterns, our
                  system has built a probabilistic profile of your shopping
                  preferences.
                </p>

                <div className="profile-stats">
                  <div className="stat-item">
                    <h4>Favorite Category</h4>
                    <p>
                      {shoppingProfile.favorite_category || "Not enough data"}
                    </p>
                  </div>
                  <div className="stat-item">
                    <h4>Best Time to Shop</h4>
                    <p>{shoppingProfile.best_shopping_time || "Anytime"}</p>
                  </div>
                  <div className="stat-item">
                    <h4>Potential Savings</h4>
                    <p>{shoppingProfile.savings_potential || "Unknown"}</p>
                  </div>
                </div>

                <h3>Product Preferences</h3>
                <div className="product-preferences">
                  {data.predictions?.map((item, idx) => (
                    <div key={idx} className="preference-item">
                      <p>
                        <strong>{item.name}</strong>
                      </p>
                      <div className="probability-bar">
                        <div
                          className="probability-fill"
                          style={{
                            width: `${item.purchase_probability}%`,
                          }}></div>
                        <span>{item.purchase_probability}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
            showModal("YOUR SHOPPING PROFILE", modalContent);
          })
          .catch((error) => {
            showModal(
              "Error",
              <p>Failed to load profile details: {error.message}</p>
            );
          });
        break;

      case "seasonal_trends":
        fetch(`${config.apiUrl}/api/personalized-recommendations/`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        })
          .then((res) => res.json())
          .then((data) => {
            const modalContent = (
              <div className="seasonal-trends">
                <h3>Your Seasonal Shopping Patterns</h3>
                <p>
                  Our probability models have analyzed your shopping patterns
                  throughout different seasons.
                </p>

                <div className="seasonal-insights">
                  <h4>Seasonal Insights</h4>
                  <ul className="seasonal-tips">
                    {seasonalTips.map((tip, idx) => (
                      <li key={idx}>{tip}</li>
                    ))}
                  </ul>
                </div>

                <div className="recommended-categories">
                  <h4>Recommended Categories This Season</h4>
                  <div className="category-list">
                    {data.recommendations?.slice(0, 3).map((rec, idx) => (
                      <div key={idx} className="category-item">
                        <h5>{rec.category}</h5>
                        <p>
                          Purchase Frequency: {rec.purchase_frequency}/month
                        </p>
                        <p>Next Purchase: {rec.next_purchase_likely}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
            showModal("SEASONAL TRENDS", modalContent);
          })
          .catch((error) => {
            showModal(
              "Error",
              <p>Failed to load seasonal trends: {error.message}</p>
            );
          });
        break;

      default:
        break;
    }
  };

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
    <div className="client-probabilistic">
      <div className="probabilistic-tabs">
        <TabButton
          id="recommendations"
          label="Personal Recommendations"
          icon={Heart}
        />
        <TabButton id="profile" label="Shopping Profile" icon={ShoppingBag} />
        <TabButton id="timing" label="Purchase Timing" icon={Clock} />
        <TabButton id="trends" label="Seasonal Trends" icon={TrendingUp} />
      </div>

      <Modal isOpen={isModalOpen} onClose={closeModal} title={modalTitle}>
        {modalContent}
      </Modal>

      <div className="tab-content">
        {activeTab === "recommendations" && (
          <div className="recommendations-section">
            <div className="section-header">
              <h2>Your Personalized Recommendations</h2>
              <p>
                Based on your purchasing patterns and preferences, we've
                selected these items for you.
              </p>
            </div>
            <div className="recommendations-chart">
              <div className="chart-container">
                <h3>Match Score</h3>
                <Pie
                  data={getRecommendationsChartData()}
                  options={{
                    responsive: true,
                    plugins: {
                      legend: {
                        position: "bottom",
                      },
                    },
                  }}
                />
              </div>
            </div>
            <div className="recommendations-list">
              <h3>Recommended Products</h3>
              <div className="products-grid">
                {recommendationsData.map((product, idx) => (
                  <Link
                    key={idx}
                    to={`/product/${product.id}`}
                    className="product-card-link">
                    <div className="product-card">
                      <div className="product-image">
                        {product.image_url ? (
                          <img src={product.image_url} alt={product.name} />
                        ) : (
                          <div className="placeholder-image">
                            {product.name.substring(0, 2).toUpperCase()}
                          </div>
                        )}
                      </div>
                      <div className="product-details">
                        <h4>{product.name}</h4>
                        <p className="product-price">${product.price}</p>
                        <div className="match-score">
                          <div className="score-label">Match Score:</div>
                          <div className="score-bar">
                            <div
                              className="score-fill"
                              style={{
                                width: `${product.match_score}%`,
                              }}></div>
                            <span>{product.match_score}%</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === "profile" && (
          <div className="profile-section">
            <div className="section-header">
              <h2>Your Shopping Profile</h2>
              <p>
                Our probabilistic models have analyzed your shopping behavior to
                create your unique profile.
              </p>
            </div>

            <div className="profile-cards">
              <div className="profile-card">
                <div className="card-header">
                  <h3>Favorite Category</h3>
                </div>
                <div className="card-body">
                  <p className="highlight">
                    {shoppingProfile.favorite_category || "Not enough data yet"}
                  </p>
                  <p className="subtext">
                    Based on your purchase frequency and volume
                  </p>
                </div>
              </div>

              <div className="profile-card">
                <div className="card-header">
                  <h3>Best Shopping Time</h3>
                </div>
                <div className="card-body">
                  <p className="highlight">
                    {shoppingProfile.best_shopping_time || "Any time"}
                  </p>
                  <p className="subtext">
                    When you typically make your purchases
                  </p>
                </div>
              </div>

              <div className="profile-card">
                <div className="card-header">
                  <h3>Potential Savings</h3>
                </div>
                <div className="card-body">
                  <p className="highlight">
                    {shoppingProfile.savings_potential ||
                      "Calculate your potential"}
                  </p>
                  <p className="subtext">
                    By optimizing your shopping timing and patterns
                  </p>
                </div>
              </div>
            </div>

            <div className="view-more-container">
              <button
                className="view-more-button"
                onClick={() => handleViewMore("shopping_profile")}>
                View Detailed Analysis
              </button>
            </div>
          </div>
        )}

        {activeTab === "timing" && (
          <div className="timing-section">
            <div className="section-header">
              <h2>Optimal Purchase Timing</h2>
              <p>
                Let our probabilistic models help you decide when to purchase
                for the best deals and availability.
              </p>
            </div>

            <div className="timing-insights">
              <div className="timing-card">
                <div className="card-header">
                  <h3>Best Day to Shop</h3>
                </div>
                <div className="card-body">
                  <div className="days-chart">
                    {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map(
                      (day, idx) => (
                        <div
                          key={idx}
                          className={`day-bar ${
                            idx === 2 || idx === 5 ? "highlight" : ""
                          }`}
                          style={{ height: `${30 + Math.random() * 40}px` }}>
                          <span className="day-label">{day}</span>
                        </div>
                      )
                    )}
                  </div>
                  <p className="timing-recommendation">
                    Our model suggests <strong>Wednesday</strong> and{" "}
                    <strong>Saturday</strong> as ideal shopping days based on
                    your habits.
                  </p>
                </div>
              </div>

              <div className="timing-card">
                <div className="card-header">
                  <h3>Purchase Frequency</h3>
                </div>
                <div className="card-body">
                  <div className="frequency-display">
                    <div className="frequency-value">
                      <span className="large-number">1.8</span>
                      <span className="unit">times/month</span>
                    </div>
                  </div>
                  <p className="timing-recommendation">
                    You typically shop <strong>once every 16 days</strong>,
                    which is your natural purchase cycle.
                  </p>
                </div>
              </div>
            </div>

            <div className="next-purchase-prediction">
              <h3>Next Purchase Prediction</h3>
              <div className="prediction-content">
                <div className="prediction-icon">
                  <Calendar size={48} />
                </div>
                <div className="prediction-details">
                  <p className="prediction-date">May 14, 2025</p>
                  <p className="prediction-explanation">
                    Based on your past purchase patterns, our probabilistic
                    model predicts your next purchase will be around this date.
                    The likelihood of this prediction is 75%.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "trends" && (
          <div className="trends-section">
            <div className="section-header">
              <h2>Your Seasonal Shopping Patterns</h2>
              <p>
                Discover how your shopping behavior changes throughout the year.
              </p>
            </div>

            <div className="seasonal-advice">
              <h3>Seasonal Shopping Tips</h3>
              <ul className="tips-list">
                {seasonalTips.map((tip, idx) => (
                  <li key={idx} className="tip-item">
                    <span className="tip-icon">💡</span>
                    <span className="tip-text">{tip}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="seasonal-chart">
              <h3>Your Shopping Volume by Month</h3>
              <div className="chart-container">
                <Line
                  data={{
                    labels: [
                      "Jan",
                      "Feb",
                      "Mar",
                      "Apr",
                      "May",
                      "Jun",
                      "Jul",
                      "Aug",
                      "Sep",
                      "Oct",
                      "Nov",
                      "Dec",
                    ],
                    datasets: [
                      {
                        label: "Purchase Volume",
                        data: [5, 3, 4, 6, 8, 7, 6, 9, 8, 10, 12, 15],
                        borderColor: "rgb(75, 192, 192)",
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                        fill: true,
                      },
                    ],
                  }}
                  options={{ responsive: true }}
                />
              </div>
            </div>

            <div className="view-more-container">
              <button
                className="view-more-button"
                onClick={() => handleViewMore("seasonal_trends")}>
                View Detailed Analysis
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClientProbabilistic;
