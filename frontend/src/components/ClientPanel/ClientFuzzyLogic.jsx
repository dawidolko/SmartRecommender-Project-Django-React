import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Cpu, Layers, Settings, X } from "react-feather";
import config from "../../config/config";
import "./ClientProbabilistic.scss";

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

const ClientFuzzyLogic = () => {
  const [activeTab, setActiveTab] = useState("recommendations");
  const [recommendationsData, setRecommendationsData] = useState([]);
  const [userProfile, setUserProfile] = useState({});
  const [fuzzySystem, setFuzzySystem] = useState({});
  const [ruleExplanations, setRuleExplanations] = useState([]);
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
      const response = await fetch(
        `${config.apiUrl}/api/fuzzy-logic-recommendations/?limit=10&debug=true`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch fuzzy logic recommendations");
      }

      const data = await response.json();

      const enhancedRecommendations = (data.recommendations || []).map(
        (rec) => {
          const imageUrl =
            rec.product.photos &&
            rec.product.photos[0] &&
            rec.product.photos[0].path
              ? `${config.apiUrl}/media/${rec.product.photos[0].path}`
              : null;

          return {
            ...rec.product,
            fuzzy_score: rec.fuzzy_score,
            category_match: rec.category_match,
            rule_activations: rec.rule_activations,
            image_url: imageUrl,
          };
        }
      );

      setRecommendationsData(enhancedRecommendations);
      setUserProfile(data.user_profile || {});
      setFuzzySystem(data.fuzzy_system || {});
      setRuleExplanations(data.rule_explanations || []);
      setLoading(false);
    } catch (error) {
      setError(error.message);
      setLoading(false);
    }
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

  const handleViewRuleDetails = (product) => {
    const modalContent = (
      <div className="rule-details">
        <h3>Fuzzy Rule Activations for {product.name}</h3>
        <p className="product-info">
          <strong>Fuzzy Score:</strong> {product.fuzzy_score.toFixed(3)} <br />
          <strong>Category Match:</strong> {product.category_match.toFixed(3)}
        </p>

        <h4>Rule Activations:</h4>
        <div className="rule-list">
          {Object.entries(product.rule_activations || {}).map(
            ([ruleName, activation], idx) => (
              <div key={idx} className="rule-item">
                <div className="rule-name">{ruleName}</div>
                <div className="rule-bar-container">
                  <div
                    className="rule-bar-fill"
                    style={{
                      width: `${activation * 100}%`,
                      backgroundColor:
                        activation > 0.7
                          ? "#28a745"
                          : activation > 0.3
                          ? "#ffc107"
                          : "#dc3545",
                    }}></div>
                  <span className="rule-activation-value">
                    {activation.toFixed(3)}
                  </span>
                </div>
              </div>
            )
          )}
        </div>

        <div className="rule-explanation-section">
          <h4>How Rules Work:</h4>
          <p>
            Each rule evaluates the product using <strong>fuzzy logic</strong>.
            Rules use <strong>T-norms</strong> (min) for AND conditions and{" "}
            <strong>T-conorms</strong> (max) for OR conditions. The final score
            is computed using weighted average defuzzification (Mamdani-style).
          </p>
        </div>
      </div>
    );
    showModal("FUZZY RULE DETAILS", modalContent);
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
          label="Fuzzy Recommendations"
          icon={Cpu}
        />
        <TabButton id="profile" label="User Profile" icon={Layers} />
        <TabButton id="rules" label="Fuzzy Rules" icon={Settings} />
      </div>

      <Modal isOpen={isModalOpen} onClose={closeModal} title={modalTitle}>
        {modalContent}
      </Modal>

      <div className="tab-content">
        {activeTab === "recommendations" && (
          <div className="recommendations-section">
            <div className="section-header">
              <h2>Fuzzy Logic Recommendations</h2>
              <p>
                Products selected using <strong>fuzzy logic</strong> to model
                uncertainty in your preferences. Each product is scored using{" "}
                <strong>membership functions</strong> and{" "}
                <strong>fuzzy inference rules</strong>.
              </p>
            </div>

            <div className="recommendations-list">
              <h3>Recommended Products</h3>
              <div className="products-grid">
                {recommendationsData.map((product, idx) => (
                  <div key={idx} className="product-card-wrapper">
                    <Link
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
                          <div className="fuzzy-scores">
                            <div className="score-item">
                              <span className="score-label">Fuzzy Score:</span>
                              <div className="score-bar">
                                <div
                                  className="score-fill"
                                  style={{
                                    width: `${product.fuzzy_score * 100}%`,
                                  }}></div>
                                <span>
                                  {(product.fuzzy_score * 100).toFixed(1)}%
                                </span>
                              </div>
                            </div>
                            <div className="score-item">
                              <span className="score-label">
                                Category Match:
                              </span>
                              <div className="score-bar">
                                <div
                                  className="score-fill secondary"
                                  style={{
                                    width: `${product.category_match * 100}%`,
                                  }}></div>
                                <span>
                                  {(product.category_match * 100).toFixed(1)}%
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </Link>
                    <button
                      className="view-rules-button"
                      onClick={() => handleViewRuleDetails(product)}>
                      View Rule Activations
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === "profile" && (
          <div className="profile-section">
            <div className="section-header">
              <h2>Your Fuzzy User Profile</h2>
              <p>
                Your profile is built using <strong>fuzzy logic</strong> to
                model uncertainty and imprecision in your shopping preferences.
              </p>
            </div>

            <div className="profile-cards">
              <div className="profile-card">
                <div className="card-header">
                  <h3>Profile Type</h3>
                </div>
                <div className="card-body">
                  <p className="highlight">
                    {userProfile.profile_type || "Unknown"}
                  </p>
                  <p className="subtext">
                    {userProfile.profile_type === "authenticated"
                      ? "Based on your purchase history"
                      : "Based on your browsing session"}
                  </p>
                </div>
              </div>

              <div className="profile-card">
                <div className="card-header">
                  <h3>Price Sensitivity</h3>
                </div>
                <div className="card-body">
                  <div className="sensitivity-display">
                    <div className="sensitivity-bar">
                      <div
                        className="sensitivity-fill"
                        style={{
                          width: `${
                            (userProfile.price_sensitivity || 0.5) * 100
                          }%`,
                        }}></div>
                    </div>
                    <span className="sensitivity-value">
                      {((userProfile.price_sensitivity || 0.5) * 100).toFixed(
                        0
                      )}
                      %
                    </span>
                  </div>
                  <p className="subtext">
                    {userProfile.price_sensitivity > 0.7
                      ? "Highly price-sensitive (prefers budget options)"
                      : userProfile.price_sensitivity < 0.3
                      ? "Low price sensitivity (prefers premium products)"
                      : "Moderate price sensitivity"}
                  </p>
                </div>
              </div>
            </div>

            <div className="category-interests">
              <h3>Your Favorite Categories</h3>
              <p className="explanation">
                These categories are ranked based on your shopping behavior. The
                bar shows your interest level from 0% (no interest) to 100%
                (highest interest).
              </p>
              <div className="interests-list">
                {(userProfile.top_interests || []).map(
                  ([category, degree], idx) => (
                    <div key={idx} className="interest-item">
                      <div className="interest-header">
                        <span className="category-name">{category}</span>
                        <span className="interest-percentage">
                          {(degree * 100).toFixed(0)}%
                        </span>
                      </div>
                      <div className="interest-bar">
                        <div
                          className="interest-fill"
                          style={{ width: `${degree * 100}%` }}></div>
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === "rules" && (
          <div className="rules-section">
            <div className="section-header">
              <h2>How Recommendations Are Made</h2>
              <p>
                Our system uses <strong>6 intelligent rules</strong> to find the
                best products for you. Each rule looks at different aspects like
                price, quality, and category match.
              </p>
            </div>

            <div className="rules-list">
              {ruleExplanations.map((rule, idx) => (
                <div key={idx} className="rule-card">
                  <div className="rule-header">
                    <span className="rule-number">Rule {idx + 1}</span>
                    <h3>{rule.rule}</h3>
                  </div>
                  <div className="rule-body">
                    <div className="rule-explanation">
                      <p className="rule-interpretation">
                        {rule.interpretation}
                      </p>
                    </div>
                    <div className="rule-details">
                      <div className="rule-detail-item">
                        <span className="detail-label">When:</span>
                        <span className="detail-value">{rule.condition}</span>
                      </div>
                      <div className="rule-detail-item">
                        <span className="detail-label">Then:</span>
                        <span className="detail-value">{rule.consequence}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="fuzzy-logic-explanation">
              <h3>How It Works Behind the Scenes</h3>
              <div className="explanation-grid">
                <div className="explanation-card">
                  <div className="explanation-icon">1</div>
                  <h4>Analyze Product</h4>
                  <p>
                    We look at price, quality ratings, and popularity for each
                    product.
                  </p>
                </div>
                <div className="explanation-card">
                  <div className="explanation-icon">2</div>
                  <h4>Apply Rules</h4>
                  <p>
                    Each of the 5 rules evaluates how well the product matches
                    your preferences.
                  </p>
                </div>
                <div className="explanation-card">
                  <div className="explanation-icon">3</div>
                  <h4>Calculate Score</h4>
                  <p>
                    All rule results are combined to create a final
                    recommendation score.
                  </p>
                </div>
                <div className="explanation-card">
                  <div className="explanation-icon">4</div>
                  <h4>Rank Products</h4>
                  <p>
                    Products with the highest scores are shown first in your
                    recommendations.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClientFuzzyLogic;
