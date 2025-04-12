import React, { useEffect, useState } from "react";
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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true, position: "top" },
    },
  };

  useEffect(() => {
    const token = localStorage.getItem("access");

    const ordersRequest = axios.get(`${config.apiUrl}/api/orders/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const clientStatsRequest = axios.get(`${config.apiUrl}/api/client-stats/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    Promise.all([ordersRequest, clientStatsRequest])
      .then(([ordersRes, clientStatsRes]) => {
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

        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
        setError("Failed to fetch data. Please try again.");
        setLoading(false);
      });
  }, [baseOptions]);

  if (loading) {
    return <div style={{ padding: "2rem" }}>Loading stats...</div>;
  }
  if (error) {
    return <div style={{ padding: "2rem", color: "red" }}>{error}</div>;
  }

  return (
    <div className="container client-dashboard">
      <h1>Client Dashboard</h1>

      <div className="row mt-4">
        <div className="col-md-6">
          <div
            className="small-box bg-primary"
            style={{ cursor: "pointer" }}
            onClick={() => navigate("/client/orders")}>
            <div className="inner">
              <h3>
                <CountUp end={purchasedItems} duration={1.5} />
              </h3>
              <p>Purchased Items</p>
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div
            className="small-box bg-danger"
            style={{ cursor: "pointer" }}
            onClick={() => navigate("/client/complaints")}>
            <div className="inner">
              <h3>
                <CountUp end={complaints} duration={1.5} />
              </h3>
              <p>Complaints</p>
            </div>
          </div>
        </div>
      </div>

      <div className="order-summary my-4">
        <h2>Order Summary</h2>
        <div className="row">
          <div className="col-md-6">
            <div className="summary-box">
              <p className="summary-title">Orders This Month</p>
              <h3>
                <CountUp end={orderSummary.ordersThisMonth} duration={1.5} />
              </h3>
            </div>
          </div>
          <div className="col-md-6">
            <div className="summary-box">
              <p className="summary-title">Average Order Value</p>
              <h3>${orderSummary.avgOrderValue.toFixed(2)}</h3>
            </div>
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
          <div className="recommendation-card">
            <img src="https://placehold.co/250" alt="Recommendation" />
            <p>Product Name</p>
          </div>
          <div className="recommendation-card">
            <img src="https://placehold.co/250" alt="Recommendation" />
            <p>Product Name</p>
          </div>
          <div className="recommendation-card">
            <img src="https://placehold.co/250" alt="Recommendation" />
            <p>Product Name</p>
          </div>
          <div className="recommendation-card">
            <img src="https://placehold.co/250" alt="Recommendation" />
            <p>Product Name</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClientDashboard;
