/**
 * ClientDashboard Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Client panel dashboard displaying personalized analytics, statistics,
 * and product recommendations based on user's purchase history.
 *
 * Features:
 *   - Purchase statistics (total items, complaints, orders this month)
 *   - Average order value calculation
 *   - Order trends line chart (monthly spending)
 *   - Category distribution pie chart (spending by category)
 *   - Personalized product recommendations (3 algorithms)
 *   - Algorithm selection preview:
 *     * Collaborative Filtering - Based on similar users
 *     * Content-Based Filtering - Based on product attributes
 *     * Fuzzy Logic - Based on fuzzy user profile
 *   - Animated counters (CountUp effect)
 *   - Responsive chart sizing
 *   - Product quick view and navigation
 *
 * Dashboard Metrics:
 *   1. Purchased Items Count - Total products bought by user
 *   2. Complaints Count - Total complaints filed
 *   3. Orders This Month - Number of orders in current month
 *   4. Average Order Value - Mean spending per order
 *
 * Charts:
 *   1. Order Trends (Line Chart):
 *      - X-axis: Months (formatted as "MMM yyyy")
 *      - Y-axis: Total spending (PLN)
 *      - Shows spending patterns over time
 *
 *   2. Category Distribution (Pie Chart):
 *      - Shows percentage of spending per category
 *      - Helps users understand their purchase preferences
 *      - Color-coded segments
 *
 * Recommendations:
 *   - Fetches user's active algorithm preference
 *   - Displays top 6 recommended products
 *   - Shows algorithm name in title
 *   - Clicking product navigates to detail page
 *
 * State Management:
 *   - purchasedItems: Total items purchased
 *   - complaints: Complaint count
 *   - orderSummary: {ordersThisMonth, avgOrderValue}
 *   - orderTrendsData: Chart.js data for line chart
 *   - categoryDistributionData: Chart.js data for pie chart
 *   - recommendedProducts: Array of product recommendations
 *   - currentAlgorithm: Active recommendation algorithm
 *   - loading: Loading state for async operations
 *   - error: Error message if API fails
 *
 * API Endpoints:
 *   - GET /api/orders/ - Fetch user's orders
 *   - GET /api/client-stats/ - Fetch dashboard statistics
 *   - GET /api/recommendation-settings/ - Get user's algorithm preference
 *   - GET /api/recommendation-preview/?algorithm={alg} - Get recommendations
 *
 * Calculations:
 *   - Average Order Value = Σ(order totals) / count(orders)
 *   - Category Spending = Σ(product prices) grouped by category
 *   - Monthly Trends = Σ(order values) grouped by month
 *
 * @component
 * @returns {React.ReactElement} Client dashboard with analytics and recommendations
 */
/* eslint-disable react-hooks/exhaustive-deps */
import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import CountUp from "react-countup";
import { Line, Pie } from "react-chartjs-2";
import "chart.js/auto";
import { format } from "date-fns";
import { useNavigate } from "react-router-dom";
import "./ClientDashboard.scss";
import config from "../../config/config";

const ClientDashboard = () => {
  const [purchasedItems, setPurchasedItems] = useState(0);
  const [complaints, setComplaints] = useState(0);
  const [orderSummary, setOrderSummary] = useState({
    ordersThisMonth: 0,
    avgOrderValue: 0,
  });
  const [orderTrendsData, setOrderTrendsData] = useState(null);
  const [categoryDistributionData, setCategoryDistributionData] =
    useState(null);
  const [chartOptions, setChartOptions] = useState(null);
  const [recommendedProducts, setRecommendedProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [, setCurrentAlgorithm] = useState("collaborative");
  const [recommendationTitle, setRecommendationTitle] = useState(
    "Recommended For You (Collaborative Filtering)"
  );
  const dataFetchedRef = useRef(false);

  const navigate = useNavigate();

  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true, position: "top" },
    },
  };

  useEffect(() => {
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    const token = localStorage.getItem("access");

    const ordersRequest = axios.get(`${config.apiUrl}/api/orders/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const clientStatsRequest = axios.get(`${config.apiUrl}/api/client-stats/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const algorithmRequest = axios.get(
      `${config.apiUrl}/api/recommendation-settings/`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    const fetchingAlgorithm = algorithmRequest
      .then((response) => {
        const algorithm = response.data.active_algorithm || "collaborative";
        setCurrentAlgorithm(algorithm);

        if (algorithm === "collaborative") {
          setRecommendationTitle(
            "Recommended For You (Collaborative Filtering)"
          );
        } else if (algorithm === "content_based") {
          setRecommendationTitle("Recommended For You (Content-Based)");
        } else if (algorithm === "fuzzy_logic") {
          setRecommendationTitle("Recommended For You (Fuzzy Logic)");
        } else {
          setRecommendationTitle("Recommended For You");
        }

        return axios.get(
          `${config.apiUrl}/api/recommendation-preview/?algorithm=${algorithm}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
      })
      .catch((error) => {
        console.error("Error fetching algorithm:", error);
        setCurrentAlgorithm("collaborative");
        setRecommendationTitle("Recommended For You (Collaborative Filtering)");

        return axios.get(
          `${config.apiUrl}/api/recommendation-preview/?algorithm=collaborative`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
      });

    Promise.all([ordersRequest, clientStatsRequest, fetchingAlgorithm])
      .then(async ([ordersRes, clientStatsRes, recommendedProductsRes]) => {
        const orders = ordersRes.data;

        const trendsMap = {};
        orders.forEach((order) => {
          const monthLabel = format(new Date(order.date_order), "MMM yyyy");
          trendsMap[monthLabel] = (trendsMap[monthLabel] || 0) + 1;
        });

        const trendArray = Object.entries(trendsMap);
        trendArray.sort(([labelA], [labelB]) => {
          const dateA = new Date(labelA);
          const dateB = new Date(labelB);
          return dateA - dateB;
        });

        const sortedLabels = trendArray.map(([label]) => label);
        const sortedData = trendArray.map(([, count]) => count);

        const maxTrend = Math.max(...sortedData, 0);
        const dynamicMax = maxTrend + 2;

        const orderTrends = {
          labels: sortedLabels,
          datasets: [
            {
              label: "Orders",
              data: sortedData,
              fill: false,
              borderColor: "rgba(75,192,192,1)",
            },
          ],
        };
        setOrderTrendsData(orderTrends);

        const dynamicOptions = {
          ...baseOptions,
          scales: {
            y: {
              min: 0,
              max: dynamicMax,
              ticks: { stepSize: 1, precision: 0 },
            },
          },
        };
        setChartOptions(dynamicOptions);

        const currentMonth = format(new Date(), "MMM yyyy");
        const ordersThisMonth = orders.filter(
          (order) =>
            format(new Date(order.date_order), "MMM yyyy") === currentMonth
        ).length;
        const totalValue = orders.reduce(
          (sum, order) => sum + (order.total || 0),
          0
        );
        const avgOrderValue =
          orders.length > 0 ? totalValue / orders.length : 0;
        setOrderSummary({ ordersThisMonth, avgOrderValue });

        const stats = clientStatsRes.data;
        setPurchasedItems(stats.purchased_items);
        setComplaints(stats.complaints);

        const catDist = stats.category_distribution;
        const catChart = {
          labels: catDist.labels,
          datasets: [
            {
              data: catDist.data,
              backgroundColor: [
                "#007bff",
                "#28a745",
                "#ffc107",
                "#dc3545",
                "#6f42c1",
                "#17a2b8",
              ],
            },
          ],
        };
        setCategoryDistributionData(catChart);

        let products = [];
        if (
          recommendedProductsRes.data &&
          recommendedProductsRes.data.length > 0
        ) {
          products = recommendedProductsRes.data.slice(0, 4);
        }

        if (products.length === 0) {
          try {
            const fallbackResponse = await axios.get(
              `${config.apiUrl}/api/recommended-products/`,
              {
                headers: { Authorization: `Bearer ${token}` },
              }
            );
            products = fallbackResponse.data.slice(0, 4);
          } catch (err) {
            console.error("Error fetching fallback recommendations:", err);
          }
        }

        setRecommendedProducts(products);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
        setError("Failed to fetch data. Please try again.");
        setLoading(false);

        localStorage.removeItem("access");
        navigate("/");
        window.location.reload();
      });
  }, []);

  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === "recommendationAlgorithm") {
        setCurrentAlgorithm(e.newValue || "collaborative");
        fetchRecommendedProducts(e.newValue || "collaborative");
      }
    };

    const handleCustomEvent = (e) => {
      if (e.detail && e.detail.algorithm) {
        setCurrentAlgorithm(e.detail.algorithm);
        fetchRecommendedProducts(e.detail.algorithm);
      }
    };

    window.addEventListener("storage", handleStorageChange);
    window.addEventListener("algorithmChanged", handleCustomEvent);

    return () => {
      window.removeEventListener("storage", handleStorageChange);
      window.removeEventListener("algorithmChanged", handleCustomEvent);
    };
  }, []);

  const fetchRecommendedProducts = async (algorithm) => {
    const token = localStorage.getItem("access");
    if (!token) return;

    try {
      const response = await axios.get(
        `${config.apiUrl}/api/recommendation-preview/?algorithm=${algorithm}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      let products = [];
      if (response.data && response.data.length > 0) {
        products = response.data.slice(0, 4);
      }

      if (products.length === 0) {
        try {
          const fallbackResponse = await axios.get(
            `${config.apiUrl}/api/recommended-products/`,
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          products = fallbackResponse.data.slice(0, 4);
        } catch (err) {
          console.error("Error fetching fallback recommendations:", err);
        }
      }

      setRecommendedProducts(products);

      if (algorithm === "collaborative") {
        setRecommendationTitle("Recommended For You (Collaborative Filtering)");
      } else if (algorithm === "content_based") {
        setRecommendationTitle("Recommended For You (Content-Based)");
      } else if (algorithm === "fuzzy_logic") {
        setRecommendationTitle("Recommended For You (Fuzzy Logic)");
      } else {
        setRecommendationTitle("Recommended For You");
      }
    } catch (err) {
      console.error("Error fetching recommended products:", err);

      try {
        const fallbackResponse = await axios.get(
          `${config.apiUrl}/api/recommended-products/`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        setRecommendedProducts(fallbackResponse.data.slice(0, 4));
      } catch (fallbackErr) {
        console.error("Error fetching fallback recommendations:", fallbackErr);
        setRecommendedProducts([]);
      }

      setRecommendationTitle("Recommended For You");
    }
  };

  if (loading) {
    return <div className="loading-spinner"></div>;
  }
  if (error) {
    return <div style={{ padding: "2rem", color: "red" }}>{error}</div>;
  }

  const handleProductClick = (productId) => {
    navigate(`/product/${productId}`);
  };

  return (
    <div className="container client-dashboard">
      <h1>Client Dashboard</h1>

      <div className="row mt-4">
        <div className="col-md-6 margin-bottom-4">
          <div
            className="small-box bg-primary"
            style={{ cursor: "pointer" }}
            onClick={() => navigate("/client/orders")}>
            <div className="inner">
              <h3 className="font-size-4">
                <CountUp end={purchasedItems} duration={1.5} />
              </h3>
              <p className="summary-title">Purchased Items</p>
            </div>
          </div>
        </div>
        <div className="col-md-6 margin-bottom-4">
          <div
            className="small-box bg-danger"
            style={{ cursor: "pointer" }}
            onClick={() => navigate("/client/complaints")}>
            <div className="inner">
              <h3 className="font-size-4">
                <CountUp end={complaints} duration={1.5} />
              </h3>
              <p className="summary-title">Complaints</p>
            </div>
          </div>
        </div>
        <div className="col-md-6 margin-bottom-4">
          <div className="small-box bg-success">
            <h3 className="font-size-4">
              <CountUp end={orderSummary.ordersThisMonth} duration={1.5} />
            </h3>
            <p className="summary-title">Orders This Month</p>
          </div>
        </div>
        <div className="col-md-6 margin-bottom-4">
          <div className="small-box bg-info">
            <h3 className="font-size-4">
              ${orderSummary.avgOrderValue.toFixed(2)}
            </h3>
            <p className="summary-title">Average Order Value</p>
          </div>
        </div>
      </div>

      <div className="dashboard-charts my-4">
        <div className="order-trends-chart">
          <h2>Order Trends</h2>
          <div className="chart-container">
            {orderTrendsData && chartOptions ? (
              <Line data={orderTrendsData} options={chartOptions} />
            ) : (
              <p>No order trends data available.</p>
            )}
          </div>
        </div>
        <div className="category-distribution-chart">
          <h2 className="mt-4">Category Distribution</h2>
          <div className="chart-container">
            {categoryDistributionData ? (
              <Pie data={categoryDistributionData} options={baseOptions} />
            ) : (
              <p>No category distribution data available.</p>
            )}
          </div>
        </div>
      </div>

      <div className="dashboard-recommendations my-4">
        <h2>{recommendationTitle}</h2>
        <div className="recommendations-grid">
          {recommendedProducts && recommendedProducts.length > 0 ? (
            recommendedProducts.map((product, index) => (
              <div
                className="recommendation-card"
                key={index}
                onClick={() => handleProductClick(product.id)}
                style={{ cursor: "pointer" }}>
                <img
                  src={`${config.apiUrl}/media/${
                    product.photos && product.photos[0]?.path
                      ? product.photos[0].path
                      : "placeholder.jpg"
                  }`}
                  alt={product.name}
                  onError={(e) => {
                    e.target.src = "https://placehold.co/250";
                  }}
                />
                <p>{product.name}</p>
              </div>
            ))
          ) : (
            <div className="loading-spinner"></div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ClientDashboard;
