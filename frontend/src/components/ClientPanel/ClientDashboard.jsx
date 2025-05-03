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
    const recommendedProductsRequest = axios.get(
      `${config.apiUrl}/api/recommended-products/`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    Promise.all([ordersRequest, clientStatsRequest, recommendedProductsRequest])
      .then(([ordersRes, clientStatsRes, recommendedProductsRes]) => {
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

        setRecommendedProducts(recommendedProductsRes.data.slice(0, 4));

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
        <h2>Recommended For You</h2>
        <div className="recommendations-grid">
          {recommendedProducts.slice(0, 4).map((product, index) => (
            <div
              className="recommendation-card"
              key={index}
              onClick={() => handleProductClick(product.id)}
              style={{ cursor: "pointer" }}>
              <img
                src={`${config.apiUrl}/media/${
                  product.photos[0]?.path || "https://placehold.co/250"
                }`}
                alt={product.name}
              />
              <p>{product.name}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ClientDashboard;
