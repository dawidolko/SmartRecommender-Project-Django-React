import React, { useState, useEffect, useRef } from "react";
import { Line, Pie, Scatter } from "react-chartjs-2";
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
  ScatterController,
} from "chart.js";
import { TrendingUp, Target, GitBranch, Activity } from "react-feather";
import "./MarkovVisualization.scss";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  ScatterController
);

const MarkovVisualization = ({
  transitionMatrix = [],
  states = [],
  probabilities = [],
  currentState = null,
  title = "Markov Chain Visualization",
  onStateClick = null,
}) => {
  const [selectedState, setSelectedState] = useState(currentState);
  const [hoveredTransition, setHoveredTransition] = useState(null);
  const [activeView, setActiveView] = useState("network");
  const chartRef = useRef(null);

  useEffect(() => {
    if (states.length === 0) {
      const defaultStates = [
        "Electronics",
        "Books",
        "Clothing",
        "Home & Garden",
      ];
      const defaultMatrix = [
        [0.4, 0.2, 0.3, 0.1],
        [0.15, 0.5, 0.25, 0.1],
        [0.2, 0.1, 0.6, 0.1],
        [0.25, 0.15, 0.2, 0.4],
      ];
    }
  }, [states]);

  const processTransitionData = () => {
    if (!transitionMatrix.length || !states.length) return null;

    const transitions = [];
    const nodePositions = generateNodePositions(states.length);

    transitionMatrix.forEach((row, fromIndex) => {
      row.forEach((probability, toIndex) => {
        if (probability > 0.05) {
          transitions.push({
            from: fromIndex,
            to: toIndex,
            probability: probability,
            fromState: states[fromIndex],
            toState: states[toIndex],
            fromPos: nodePositions[fromIndex],
            toPos: nodePositions[toIndex],
          });
        }
      });
    });

    return { transitions, nodePositions };
  };

  const generateNodePositions = (nodeCount) => {
    const positions = [];
    const centerX = 50;
    const centerY = 50;
    const radius = 30;

    for (let i = 0; i < nodeCount; i++) {
      const angle = (2 * Math.PI * i) / nodeCount - Math.PI / 2;
      positions.push({
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
      });
    }

    return positions;
  };

  const createNetworkData = () => {
    const data = processTransitionData();
    if (!data) return null;

    const { transitions, nodePositions } = data;

    const nodeDataset = {
      label: "States",
      data: nodePositions.map((pos, index) => ({
        x: pos.x,
        y: pos.y,
        state: states[index],
        index: index,
        isSelected: selectedState === index,
        isCurrent: currentState === index,
      })),
      backgroundColor: nodePositions.map((_, index) => {
        if (currentState === index) return "#dc3545";
        if (selectedState === index) return "#007bff";
        return "#28a745";
      }),
      borderColor: nodePositions.map((_, index) => {
        if (currentState === index) return "#a71e2a";
        if (selectedState === index) return "#0056b3";
        return "#1e7e34";
      }),
      borderWidth: 3,
      pointRadius: nodePositions.map((_, index) => {
        if (currentState === index || selectedState === index) return 12;
        return 10;
      }),
      showLine: false,
    };

    return {
      datasets: [nodeDataset],
      transitions: transitions,
    };
  };

  const createTransitionChart = () => {
    if (!transitionMatrix.length || selectedState === null) return null;

    const selectedRow = transitionMatrix[selectedState];

    return {
      labels: states,
      datasets: [
        {
          label: `Transition Probabilities from ${states[selectedState]}`,
          data: selectedRow,
          backgroundColor: [
            "#007bff",
            "#28a745",
            "#ffc107",
            "#dc3545",
            "#6f42c1",
            "#17a2b8",
            "#fd7e14",
            "#e83e8c",
          ],
          borderColor: [
            "#0056b3",
            "#1e7e34",
            "#d39e00",
            "#a71e2a",
            "#59359a",
            "#0f5257",
            "#d76100",
            "#b8306f",
          ],
          borderWidth: 2,
          hoverOffset: 10,
        },
      ],
    };
  };

  const networkOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        text: "State Transition Network",
        font: { size: 16, weight: "bold" },
        color: "#333",
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            const point = context.parsed;
            const dataPoint = context.dataset.data[context.dataIndex];
            return `State: ${dataPoint.state}`;
          },
        },
      },
    },
    scales: {
      x: {
        display: false,
        min: 0,
        max: 100,
      },
      y: {
        display: false,
        min: 0,
        max: 100,
      },
    },
    onHover: (event, activeElements) => {
      if (activeElements.length > 0) {
        const element = activeElements[0];
        const index = element.index;
        setHoveredTransition(index);
      } else {
        setHoveredTransition(null);
      }
    },
    onClick: (event, activeElements) => {
      if (activeElements.length > 0) {
        const element = activeElements[0];
        const index = element.index;
        setSelectedState(index);
        if (onStateClick) {
          onStateClick(states[index], index);
        }
      }
    },
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "right",
        labels: { font: { size: 12 } },
      },
      title: {
        display: true,
        text:
          selectedState !== null
            ? `Transition Probabilities from ${states[selectedState]}`
            : "Select a state to view transitions",
        font: { size: 14, weight: "bold" },
        color: "#333",
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            const percentage = (context.parsed * 100).toFixed(1);
            return `${context.label}: ${percentage}%`;
          },
        },
      },
    },
  };

  const networkData = createNetworkData();
  const transitionData = createTransitionChart();

  const renderTransitionArrows = () => {
    const data = processTransitionData();
    if (!data || activeView !== "network") return null;

    const { transitions } = data;

    return (
      <div className="markov-network-overlay">
        <svg className="transition-arrows" width="100%" height="100%">
          {transitions.map((transition, index) => {
            const opacity = hoveredTransition === transition.from ? 1 : 0.6;
            const strokeWidth = selectedState === transition.from ? 3 : 2;
            const color =
              selectedState === transition.from ? "#007bff" : "#666";

            const x1 = `${transition.fromPos.x}%`;
            const y1 = `${transition.fromPos.y}%`;
            const x2 = `${transition.toPos.x}%`;
            const y2 = `${transition.toPos.y}%`;

            return (
              <g key={`transition-${index}`}>
                <line
                  x1={x1}
                  y1={y1}
                  x2={x2}
                  y2={y2}
                  stroke={color}
                  strokeWidth={strokeWidth}
                  opacity={opacity}
                  markerEnd="url(#arrowhead)"
                />
                <text
                  x={`${(transition.fromPos.x + transition.toPos.x) / 2}%`}
                  y={`${(transition.fromPos.y + transition.toPos.y) / 2}%`}
                  fill={color}
                  fontSize="12"
                  textAnchor="middle"
                  dy="0.3em"
                  opacity={opacity}
                  className="transition-probability-label">
                  {transition.probability.toFixed(2)}
                </text>
              </g>
            );
          })}
          <defs>
            <marker
              id="arrowhead"
              markerWidth="10"
              markerHeight="7"
              refX="9"
              refY="3.5"
              orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#666" />
            </marker>
          </defs>
        </svg>
      </div>
    );
  };

  return (
    <div className="markov-visualization">
      <div className="markov-header">
        <h2 className="markov-title">
          <GitBranch className="markov-icon" />
          {title}
        </h2>

        <div className="markov-controls">
          <button
            className={`control-btn ${
              activeView === "network" ? "active" : ""
            }`}
            onClick={() => setActiveView("network")}>
            <Target size={16} />
            Network View
          </button>
          <button
            className={`control-btn ${
              activeView === "transitions" ? "active" : ""
            }`}
            onClick={() => setActiveView("transitions")}
            disabled={selectedState === null}>
            <Activity size={16} />
            Transitions
          </button>
        </div>
      </div>

      <div className="markov-content">
        {activeView === "network" && (
          <div className="markov-network-container">
            <div className="chart-container">
              {networkData && (
                <>
                  <Scatter
                    ref={chartRef}
                    data={networkData}
                    options={networkOptions}
                  />
                  {renderTransitionArrows()}
                </>
              )}
            </div>

            <div className="state-legend">
              <h4>State Legend</h4>
              <div className="legend-items">
                {states.map((state, index) => (
                  <div
                    key={index}
                    className={`legend-item ${
                      selectedState === index ? "selected" : ""
                    } ${currentState === index ? "current" : ""}`}
                    onClick={() => setSelectedState(index)}>
                    <div
                      className="legend-color"
                      style={{
                        backgroundColor:
                          currentState === index
                            ? "#dc3545"
                            : selectedState === index
                            ? "#007bff"
                            : "#28a745",
                      }}
                    />
                    <span className="legend-text">{state}</span>
                    {currentState === index && (
                      <span className="current-badge">Current</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeView === "transitions" && (
          <div className="markov-transitions-container">
            <div className="chart-container">
              {transitionData ? (
                <Pie data={transitionData} options={pieOptions} />
              ) : (
                <div className="no-data-message">
                  <Target size={48} />
                  <p>
                    Select a state from the network view to see transition
                    probabilities
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      <div className="markov-stats">
        <h4>Statistics</h4>
        <div className="stats-grid">
          <div className="stat-item">
            <TrendingUp className="stat-icon" />
            <div className="stat-content">
              <span className="stat-label">Total States</span>
              <span className="stat-value">{states.length}</span>
            </div>
          </div>

          {selectedState !== null && (
            <div className="stat-item">
              <Target className="stat-icon" />
              <div className="stat-content">
                <span className="stat-label">Selected State</span>
                <span className="stat-value">{states[selectedState]}</span>
              </div>
            </div>
          )}

          {currentState !== null && (
            <div className="stat-item">
              <Activity className="stat-icon" />
              <div className="stat-content">
                <span className="stat-label">Current State</span>
                <span className="stat-value">{states[currentState]}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MarkovVisualization;
