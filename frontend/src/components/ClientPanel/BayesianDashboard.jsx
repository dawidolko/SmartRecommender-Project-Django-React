import React, { useState, useEffect, useRef } from "react";
import { Line, Pie, Bar, Radar, Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  BarElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { 
  TrendingUp, 
  Target, 
  Activity, 
  Brain, 
  BarChart3, 
  PieChart, 
  Radar as RadarIcon,
  AlertTriangle,
  Info,
  Eye,
  Settings
} from "react-feather";
import "./BayesianDashboard.scss";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  BarElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend,
  Filler
);

const BayesianDashboard = ({
  categoryPreferences = {},
  churnRisk = 0.25,
  behavioralInsights = [],
  recommendations = [],
  confidenceIntervals = {},
  title = "Bayesian Analysis Dashboard",
  onInsightClick = null,
}) => {
  const [activeView, setActiveView] = useState("overview");
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [hoveredElement, setHoveredElement] = useState(null);
  const [animationEnabled, setAnimationEnabled] = useState(true);
  const chartRefs = {
    radar: useRef(null),
    gauge: useRef(null),
    behavioral: useRef(null),
    confidence: useRef(null),
  };

  // Default data for demonstration if no props provided
  const defaultCategoryPreferences = {
    "Electronics": 0.85,
    "Books": 0.72,
    "Clothing": 0.68,
    "Home & Garden": 0.45,
    "Sports": 0.63,
    "Beauty": 0.54
  };

  const defaultBehavioralInsights = [
    {
      name: "Price Sensitivity",
      score: 0.76,
      confidence: 0.89,
      description: "Moderate price sensitivity with preference for value deals",
      trend: "increasing"
    },
    {
      name: "Brand Loyalty",
      score: 0.62,
      confidence: 0.82,
      description: "Shows moderate brand loyalty patterns",
      trend: "stable"
    },
    {
      name: "Seasonal Behavior",
      score: 0.91,
      confidence: 0.94,
      description: "Strong seasonal shopping patterns detected",
      trend: "seasonal"
    },
    {
      name: "Impulse Buying",
      score: 0.34,
      confidence: 0.71,
      description: "Low impulse buying tendency",
      trend: "decreasing"
    }
  ];

  const defaultConfidenceIntervals = {
    "Next Purchase": { lower: 0.65, upper: 0.89, mean: 0.77 },
    "Category Switch": { lower: 0.23, upper: 0.51, mean: 0.37 },
    "Churn Risk": { lower: 0.18, upper: 0.32, mean: 0.25 },
    "Price Sensitivity": { lower: 0.68, upper: 0.84, mean: 0.76 }
  };

  // Use props or defaults
  const categoryData = Object.keys(categoryPreferences).length > 0 ? categoryPreferences : defaultCategoryPreferences;
  const behaviorData = behavioralInsights.length > 0 ? behavioralInsights : defaultBehavioralInsights;
  const confidenceData = Object.keys(confidenceIntervals).length > 0 ? confidenceIntervals : defaultConfidenceIntervals;

  // Color schemes
  const colors = {
    primary: "#0066cc",
    secondary: "#4caf50",
    accent: "#ff9800",
    danger: "#f44336",
    warning: "#ff9800",
    info: "#2196f3",
    success: "#4caf50",
    gradient: {
      primary: ["#0066cc", "#4d94ff"],
      secondary: ["#4caf50", "#81c784"],
      accent: ["#ff9800", "#ffb74d"],
      danger: ["#f44336", "#e57373"]
    }
  };

  // Generate radar chart data for category preferences
  const getRadarChartData = () => {
    const categories = Object.keys(categoryData);
    const values = Object.values(categoryData);

    return {
      labels: categories,
      datasets: [
        {
          label: "Category Preference Probability",
          data: values,
          backgroundColor: "rgba(0, 102, 204, 0.2)",
          borderColor: colors.primary,
          borderWidth: 2,
          pointBackgroundColor: colors.primary,
          pointBorderColor: "#ffffff",
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
          fill: true,
        },
        {
          label: "Market Average",
          data: categories.map(() => 0.5), // Baseline comparison
          backgroundColor: "rgba(117, 117, 117, 0.1)",
          borderColor: "#757575",
          borderWidth: 1,
          borderDash: [5, 5],
          pointBackgroundColor: "#757575",
          pointBorderColor: "#ffffff",
          pointBorderWidth: 1,
          pointRadius: 4,
          fill: true,
        }
      ],
    };
  };

  // Generate gauge chart data for churn risk
  const getGaugeChartData = () => {
    const riskLevel = churnRisk;
    const remaining = 1 - riskLevel;

    let riskColor = colors.success;
    let riskLabel = "Low Risk";

    if (riskLevel > 0.7) {
      riskColor = colors.danger;
      riskLabel = "High Risk";
    } else if (riskLevel > 0.4) {
      riskColor = colors.warning;
      riskLabel = "Medium Risk";
    }

    return {
      labels: [riskLabel, "Safe Zone"],
      datasets: [
        {
          data: [riskLevel * 100, remaining * 100],
          backgroundColor: [riskColor, "#e0e0e0"],
          borderWidth: 0,
          cutout: "70%",
          rotation: -90,
          circumference: 180,
        }
      ],
    };
  };

  // Generate behavioral insights bar chart
  const getBehavioralInsightsChart = () => {
    const labels = behaviorData.map(item => item.name);
    const scores = behaviorData.map(item => item.score);
    const confidences = behaviorData.map(item => item.confidence);

    return {
      labels: labels,
      datasets: [
        {
          label: "Behavioral Score",
          data: scores,
          backgroundColor: colors.gradient.primary[0],
          borderColor: colors.primary,
          borderWidth: 1,
          borderRadius: 8,
          borderSkipped: false,
        },
        {
          label: "Confidence Level",
          data: confidences,
          backgroundColor: colors.gradient.secondary[0],
          borderColor: colors.secondary,
          borderWidth: 1,
          borderRadius: 8,
          borderSkipped: false,
        }
      ],
    };
  };

  // Generate confidence intervals chart
  const getConfidenceIntervalsChart = () => {
    const labels = Object.keys(confidenceData);
    const means = labels.map(key => confidenceData[key].mean);
    const lowerBounds = labels.map(key => confidenceData[key].lower);
    const upperBounds = labels.map(key => confidenceData[key].upper);

    return {
      labels: labels,
      datasets: [
        {
          label: "Mean",
          data: means,
          backgroundColor: colors.primary,
          borderColor: colors.primary,
          borderWidth: 2,
          type: 'line',
          pointRadius: 6,
          pointHoverRadius: 8,
        },
        {
          label: "Lower Bound",
          data: lowerBounds,
          backgroundColor: "rgba(0, 102, 204, 0.3)",
          borderColor: "rgba(0, 102, 204, 0.5)",
          borderWidth: 1,
          fill: false,
        },
        {
          label: "Upper Bound",
          data: upperBounds,
          backgroundColor: "rgba(0, 102, 204, 0.3)",
          borderColor: "rgba(0, 102, 204, 0.5)",
          borderWidth: 1,
          fill: '-1',
        }
      ],
    };
  };

  // Chart options
  const radarOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Category Preference Analysis',
        font: { size: 16, weight: 'bold' }
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const value = (context.parsed.r * 100).toFixed(1);
            return `${context.dataset.label}: ${value}%`;
          }
        }
      }
    },
    scales: {
      r: {
        beginAtZero: true,
        max: 1,
        ticks: {
          stepSize: 0.2,
          callback: (value) => `${(value * 100).toFixed(0)}%`
        },
        grid: {
          color: "#e0e0e0",
        },
        pointLabels: {
          font: { size: 12, weight: '500' }
        }
      }
    },
    animation: {
      duration: animationEnabled ? 1500 : 0,
      easing: 'easeInOutCubic'
    }
  };

  const gaugeOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Churn Risk Assessment',
        font: { size: 16, weight: 'bold' }
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            if (context.label === "Safe Zone") return null;
            return `Churn Risk: ${context.parsed.toFixed(1)}%`;
          }
        }
      }
    },
    animation: {
      duration: animationEnabled ? 2000 : 0,
      easing: 'easeOutBounce'
    }
  };

  const behavioralOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Behavioral Insights Analysis',
        font: { size: 16, weight: 'bold' }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 1,
        ticks: {
          callback: (value) => `${(value * 100).toFixed(0)}%`
        }
      }
    },
    animation: {
      duration: animationEnabled ? 1200 : 0,
      delay: (context) => context.dataIndex * 100
    }
  };

  const confidenceOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Prediction Confidence Intervals',
        font: { size: 16, weight: 'bold' }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 1,
        ticks: {
          callback: (value) => `${(value * 100).toFixed(0)}%`
        }
      }
    },
    animation: {
      duration: animationEnabled ? 1500 : 0
    }
  };

  // Tab component
  const TabButton = ({ id, label, icon: Icon, count }) => (
    <button
      className={`tab-button ${activeView === id ? "active" : ""}`}
      onClick={() => setActiveView(id)}
      onMouseEnter={() => setHoveredElement(id)}
      onMouseLeave={() => setHoveredElement(null)}>
      <Icon size={20} />
      <span>{label}</span>
      {count && <span className="tab-count">{count}</span>}
    </button>
  );

  // Handle chart interactions
  const handleChartClick = (event, elements, chartType) => {
    if (elements.length > 0 && onInsightClick) {
      const elementIndex = elements[0].index;
      let clickedData = null;

      switch (chartType) {
        case 'radar':
          const categories = Object.keys(categoryData);
          clickedData = {
            type: 'category',
            name: categories[elementIndex],
            value: Object.values(categoryData)[elementIndex]
          };
          break;
        case 'behavioral':
          clickedData = {
            type: 'behavioral',
            ...behaviorData[elementIndex]
          };
          break;
        default:
          break;
      }

      if (clickedData) {
        onInsightClick(clickedData);
      }
    }
  };

  // Get risk level info
  const getRiskLevelInfo = () => {
    if (churnRisk < 0.3) {
      return {
        level: "Low Risk",
        color: colors.success,
        icon: Target,
        message: "Customer shows strong engagement and loyalty patterns",
        recommendations: [
          "Continue current engagement strategies",
          "Introduce premium features or loyalty programs",
          "Use as reference for similar customer segments"
        ]
      };
    } else if (churnRisk < 0.7) {
      return {
        level: "Medium Risk",
        color: colors.warning,
        icon: AlertTriangle,
        message: "Customer shows some signs of disengagement",
        recommendations: [
          "Implement targeted retention campaigns",
          "Offer personalized deals and recommendations",
          "Increase communication frequency with relevant content"
        ]
      };
    } else {
      return {
        level: "High Risk",
        color: colors.danger,
        icon: AlertTriangle,
        message: "Customer shows strong indicators of potential churn",
        recommendations: [
          "Immediate intervention required",
          "Offer significant incentives to retain",
          "Personal outreach from customer success team"
        ]
      };
    }
  };

  const riskInfo = getRiskLevelInfo();

  return (
    <div className="bayesian-dashboard">
      <div className="dashboard-header">
        <div className="header-content">
          <div className="header-title">
            <Brain size={28} />
            <h1>{title}</h1>
          </div>
          <div className="header-controls">
            <button
              className={`control-button ${animationEnabled ? 'active' : ''}`}
              onClick={() => setAnimationEnabled(!animationEnabled)}
              title="Toggle animations">
              <Activity size={16} />
              <span>Animate</span>
            </button>
          </div>
        </div>
        <p className="dashboard-description">
          Advanced Bayesian analysis providing probabilistic insights into customer behavior, preferences, and risk assessment.
        </p>
      </div>

      <div className="dashboard-tabs">
        <TabButton
          id="overview"
          label="Overview"
          icon={Eye}
          count={Object.keys(categoryData).length}
        />
        <TabButton
          id="preferences"
          label="Preferences"
          icon={RadarIcon}
        />
        <TabButton
          id="risk"
          label="Churn Risk"
          icon={AlertTriangle}
        />
        <TabButton
          id="behavior"
          label="Behavior"
          icon={BarChart3}
          count={behaviorData.length}
        />
        <TabButton
          id="confidence"
          label="Confidence"
          icon={TrendingUp}
        />
      </div>

      <div className="tab-content">
        {activeView === "overview" && (
          <div className="overview-section">
            <div className="overview-grid">
              <div className="overview-card radar-preview">
                <div className="card-header">
                  <RadarIcon size={20} />
                  <h3>Category Preferences</h3>
                </div>
                <div className="chart-container small">
                  <Radar
                    data={getRadarChartData()}
                    options={{
                      ...radarOptions,
                      plugins: { ...radarOptions.plugins, title: { display: false } }
                    }}
                  />
                </div>
                <div className="card-footer">
                  <span>Top preference: {Object.keys(categoryData)[0]}</span>
                  <button onClick={() => setActiveView('preferences')}>View Details</button>
                </div>
              </div>

              <div className="overview-card gauge-preview">
                <div className="card-header">
                  <riskInfo.icon size={20} />
                  <h3>Churn Risk</h3>
                </div>
                <div className="gauge-display">
                  <div className="gauge-value" style={{ color: riskInfo.color }}>
                    {(churnRisk * 100).toFixed(1)}%
                  </div>
                  <div className="gauge-label">{riskInfo.level}</div>
                </div>
                <div className="card-footer">
                  <span>{riskInfo.message}</span>
                  <button onClick={() => setActiveView('risk')}>View Analysis</button>
                </div>
              </div>

              <div className="overview-card insights-preview">
                <div className="card-header">
                  <BarChart3 size={20} />
                  <h3>Key Insights</h3>
                </div>
                <div className="insights-list">
                  {behaviorData.slice(0, 3).map((insight, idx) => (
                    <div key={idx} className="insight-item">
                      <span className="insight-name">{insight.name}</span>
                      <div className="insight-bar">
                        <div
                          className="insight-fill"
                          style={{
                            width: `${insight.score * 100}%`,
                            backgroundColor: colors.primary
                          }}
                        />
                        <span className="insight-value">{(insight.score * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="card-footer">
                  <button onClick={() => setActiveView('behavior')}>View All Insights</button>
                </div>
              </div>
            </div>

            <div className="summary-cards">
              <div className="summary-card">
                <div className="summary-icon" style={{ backgroundColor: colors.primary + '20', color: colors.primary }}>
                  <Target size={24} />
                </div>
                <div className="summary-content">
                  <h4>Prediction Accuracy</h4>
                  <div className="summary-value">
                    {(Object.values(confidenceData).reduce((sum, item) => sum + item.mean, 0) / Object.keys(confidenceData).length * 100).toFixed(1)}%
                  </div>
                  <p>Average model confidence</p>
                </div>
              </div>

              <div className="summary-card">
                <div className="summary-icon" style={{ backgroundColor: colors.secondary + '20', color: colors.secondary }}>
                  <TrendingUp size={24} />
                </div>
                <div className="summary-content">
                  <h4>Engagement Level</h4>
                  <div className="summary-value">
                    {behaviorData.find(item => item.name === "Brand Loyalty")?.score ? 
                      (behaviorData.find(item => item.name === "Brand Loyalty").score * 100).toFixed(0) + '%' : 
                      'N/A'}
                  </div>
                  <p>Customer loyalty score</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeView === "preferences" && (
          <div className="preferences-section">
            <div className="section-header">
              <h2>Category Preference Analysis</h2>
              <p>Bayesian analysis of customer preferences across different product categories</p>
            </div>

            <div className="preferences-content">
              <div className="chart-section">
                <div className="chart-container">
                  <Radar
                    ref={chartRefs.radar}
                    data={getRadarChartData()}
                    options={{
                      ...radarOptions,
                      onClick: (event, elements) => handleChartClick(event, elements, 'radar')
                    }}
                  />
                </div>
              </div>

              <div className="preferences-details">
                <h3>Category Breakdown</h3>
                <div className="category-list">
                  {Object.entries(categoryData)
                    .sort(([,a], [,b]) => b - a)
                    .map(([category, probability], idx) => (
                    <div
                      key={idx}
                      className={`category-item ${selectedCategory === category ? 'selected' : ''}`}
                      onClick={() => setSelectedCategory(selectedCategory === category ? null : category)}>
                      <div className="category-info">
                        <span className="category-name">{category}</span>
                        <span className="category-rank">#{idx + 1}</span>
                      </div>
                      <div className="probability-display">
                        <div className="probability-bar">
                          <div
                            className="probability-fill"
                            style={{
                              width: `${probability * 100}%`,
                              backgroundColor: `hsl(${120 * probability}, 70%, 50%)`
                            }}
                          />
                        </div>
                        <span className="probability-value">{(probability * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  ))}
                </div>

                {selectedCategory && (
                  <div className="category-details">
                    <h4>Analysis: {selectedCategory}</h4>
                    <div className="detail-stats">
                      <div className="stat">
                        <span className="stat-label">Preference Score</span>
                        <span className="stat-value">{(categoryData[selectedCategory] * 100).toFixed(1)}%</span>
                      </div>
                      <div className="stat">
                        <span className="stat-label">Market Position</span>
                        <span className="stat-value">
                          {categoryData[selectedCategory] > 0.7 ? 'High' : 
                           categoryData[selectedCategory] > 0.4 ? 'Medium' : 'Low'}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeView === "risk" && (
          <div className="risk-section">
            <div className="section-header">
              <h2>Churn Risk Assessment</h2>
              <p>Bayesian probability model for customer retention prediction</p>
            </div>

            <div className="risk-content">
              <div className="gauge-section">
                <div className="chart-container gauge-container">
                  <Doughnut
                    ref={chartRefs.gauge}
                    data={getGaugeChartData()}
                    options={gaugeOptions}
                  />
                  <div className="gauge-overlay">
                    <div className="gauge-center">
                      <span className="gauge-percentage" style={{ color: riskInfo.color }}>
                        {(churnRisk * 100).toFixed(1)}%
                      </span>
                      <span className="gauge-label">Risk Level</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="risk-analysis">
                <div className="risk-info-card" style={{ borderLeftColor: riskInfo.color }}>
                  <div className="risk-header">
                    <riskInfo.icon size={24} style={{ color: riskInfo.color }} />
                    <h3 style={{ color: riskInfo.color }}>{riskInfo.level}</h3>
                  </div>
                  <p className="risk-message">{riskInfo.message}</p>
                </div>

                <div className="recommendations-card">
                  <h4>Recommended Actions</h4>
                  <ul className="recommendations-list">
                    {riskInfo.recommendations.map((recommendation, idx) => (
                      <li key={idx} className="recommendation-item">
                        <Info size={16} />
                        <span>{recommendation}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="risk-factors">
                  <h4>Contributing Factors</h4>
                  <div className="factors-grid">
                    <div className="factor-item">
                      <span className="factor-label">Purchase Frequency</span>
                      <div className="factor-impact low">Low Impact</div>
                    </div>
                    <div className="factor-item">
                      <span className="factor-label">Engagement Score</span>
                      <div className="factor-impact medium">Medium Impact</div>
                    </div>
                    <div className="factor-item">
                      <span className="factor-label">Support Interactions</span>
                      <div className="factor-impact high">High Impact</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeView === "behavior" && (
          <div className="behavior-section">
            <div className="section-header">
              <h2>Behavioral Insights Analysis</h2>
              <p>Deep learning insights into customer behavioral patterns and tendencies</p>
            </div>

            <div className="behavior-content">
              <div className="chart-section">
                <div className="chart-container">
                  <Bar
                    ref={chartRefs.behavioral}
                    data={getBehavioralInsightsChart()}
                    options={{
                      ...behavioralOptions,
                      onClick: (event, elements) => handleChartClick(event, elements, 'behavioral')
                    }}
                  />
                </div>
              </div>

              <div className="insights-grid">
                {behaviorData.map((insight, idx) => (
                  <div key={idx} className="insight-card">
                    <div className="insight-header">
                      <h4>{insight.name}</h4>
                      <div className={`trend-indicator ${insight.trend}`}>
                        {insight.trend === 'increasing' && '↗️'}
                        {insight.trend === 'decreasing' && '↘️'}
                        {insight.trend === 'stable' && '➡️'}
                        {insight.trend === 'seasonal' && '🔄'}
                      </div>
                    </div>
                    
                    <div className="insight-metrics">
                      <div className="metric">
                        <span className="metric-label">Score</span>
                        <span className="metric-value">{(insight.score * 100).toFixed(0)}%</span>
                      </div>
                      <div className="metric">
                        <span className="metric-label">Confidence</span>
                        <span className="metric-value">{(insight.confidence * 100).toFixed(0)}%</span>
                      </div>
                    </div>

                    <p className="insight-description">{insight.description}</p>

                    <div className="insight-visualization">
                      <div className="mini-bar">
                        <div
                          className="mini-bar-fill"
                          style={{
                            width: `${insight.score * 100}%`,
                            backgroundColor: colors.primary
                          }}
                        />
                      </div>
                      <div className="confidence-indicator">
                        <div
                          className="confidence-fill"
                          style={{
                            width: `${insight.confidence * 100}%`,
                            backgroundColor: colors.secondary
                          }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeView === "confidence" && (
          <div className="confidence-section">
            <div className="section-header">
              <h2>Prediction Confidence Intervals</h2>
              <p>Statistical confidence bounds for Bayesian model predictions</p>
            </div>

            <div className="confidence-content">
              <div className="chart-section">
                <div className="chart-container">
                  <Line
                    ref={chartRefs.confidence}
                    data={getConfidenceIntervalsChart()}
                    options={confidenceOptions}
                  />
                </div>
              </div>

              <div className="confidence-details">
                <h3>Statistical Summary</h3>
                <div className="confidence-grid">
                  {Object.entries(confidenceData).map(([key, interval], idx) => (
                    <div key={idx} className="confidence-card">
                      <h4>{key}</h4>
                      <div className="interval-display">
                        <div className="interval-bar">
                          <div className="interval-range">
                            <div
                              className="range-fill"
                              style={{
                                left: `${interval.lower * 100}%`,
                                width: `${(interval.upper - interval.lower) * 100}%`
                              }}
                            />
                            <div
                              className="mean-indicator"
                              style={{ left: `${interval.mean * 100}%` }}
                            />
                          </div>
                        </div>
                        <div className="interval-values">
                          <span className="lower">{(interval.lower * 100).toFixed(1)}%</span>
                          <span className="mean">{(interval.mean * 100).toFixed(1)}%</span>
                          <span className="upper">{(interval.upper * 100).toFixed(1)}%</span>
                        </div>
                      </div>
                      <div className="confidence-width">
                        Confidence Width: {((interval.upper - interval.lower) * 100).toFixed(1)}%
                      </div>
                    </div>
                  ))}
                </div>

                <div className="model-info">
                  <h4>Model Information</h4>
                  <div className="model-stats">
                    <div className="model-stat">
                      <span className="stat-label">Average Confidence</span>
                      <span className="stat-value">
                        {(Object.values(confidenceData).reduce((sum, item) => sum + (item.upper - item.lower), 0) / Object.keys(confidenceData).length * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="model-stat">
                      <span className="stat-label">Model Accuracy</span>
                      <span className="stat-value">87.3%</span>
                    </div>
                    <div className="model-stat">
                      <span className="stat-label">Data Points</span>
                      <span className="stat-value">1,247</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BayesianDashboard;