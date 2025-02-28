import React, { useEffect, useState } from "react";
import axios from "axios";
import CountUp from "react-countup";
import { Line, Pie } from "react-chartjs-2";
import "chart.js/auto"; // Required for Chart.js v3+
import { format } from "date-fns";
import "./ClientDashboard.scss";

const ClientDashboard = () => {
  const [purchasedItems, setPurchasedItems] = useState(0);
  const [complaints, setComplaints] = useState(0);
  const [orderSummary, setOrderSummary] = useState({
    ordersThisMonth: 0,
    avgOrderValue: 0,
  });
  const [orderTrendsData, setOrderTrendsData] = useState(null);
  const [categoryDistributionData, setCategoryDistributionData] = useState(null);
  const [chartOptions, setChartOptions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true, position: "top" },
      title: { display: true, text: "Order Trends" },
    },
  };

  useEffect(() => {
    const token = localStorage.getItem("access");
    axios
      .get("http://127.0.0.1:8000/api/orders/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        const orders = res.data;

        const totalPurchased = orders.reduce((sum, order) => {
          if (order.order_products && Array.isArray(order.order_products)) {
            return sum + order.order_products.reduce((s, op) => s + (op.quantity || 0), 0);
          }
          return sum;
        }, 0);
        setPurchasedItems(totalPurchased);

        const totalComplaints = orders.reduce((sum, order) => {
          return sum + (order.complaints ? order.complaints.length : 0);
        }, 0);
        setComplaints(totalComplaints);

        const trendsMap = {};
        orders.forEach((order) => {
          const monthLabel = format(new Date(order.date_order), "MMM yyyy");
          const orderTotal = order.order_products && Array.isArray(order.order_products)
            ? order.order_products.reduce((s, op) => s + (op.quantity || 0), 0)
            : 0;
          trendsMap[monthLabel] = (trendsMap[monthLabel] || 0) + orderTotal;
        });
        const trendLabels = Object.keys(trendsMap);
        const trendData = Object.values(trendsMap);
        const maxTrend = Math.max(...trendData, 0);
        const dynamicMax = maxTrend + 2;
        const orderTrends = {
          labels: trendLabels,
          datasets: [
            {
              label: "Purchased Items",
              data: trendData,
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

        const categoryMap = {};
        orders.forEach((order) => {
          if (order.order_products && Array.isArray(order.order_products)) {
            order.order_products.forEach((op) => {
              const cat = op.product__categories__name || op.product.categories?.[0]?.name; 
              if (cat) {
                categoryMap[cat] = (categoryMap[cat] || 0) + (op.quantity || 0);
              }
            });
          }
        });
        const categoriesArray = Object.entries(categoryMap).map(([category, count]) => ({ category, count }));
        categoriesArray.sort((a, b) => b.count - a.count);
        const top5 = categoriesArray.slice(0, 5);
        const othersSum = categoriesArray.slice(5).reduce((sum, item) => sum + item.count, 0);
        const categoryLabels = top5.map((item) => item.category);
        const categoryData = top5.map((item) => item.count);
        if (othersSum > 0) {
          categoryLabels.push("Others");
          categoryData.push(othersSum);
        }
        const categoryDistribution = {
          labels: categoryLabels,
          datasets: [
            {
              data: categoryData,
              backgroundColor: ["#007bff", "#28a745", "#ffc107", "#dc3545", "#6f42c1", "#17a2b8"],
            },
          ],
        };
        setCategoryDistributionData(categoryDistribution);

        const currentMonth = format(new Date(), "MMM yyyy");
        const ordersThisMonth = orders.filter(
          (order) => format(new Date(order.date_order), "MMM yyyy") === currentMonth
        ).length;
        const totalValue = orders.reduce((sum, order) => sum + (order.total || 0), 0);
        const avgOrderValue = orders.length > 0 ? totalValue / orders.length : 0;
        setOrderSummary({ ordersThisMonth, avgOrderValue });

        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching orders:", err);
        setError("Failed to fetch data. Please try again.");
        setLoading(false);
      });
  }, []);

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
          <div className="small-box bg-primary">
            <div className="inner">
              <h3>
                <CountUp end={purchasedItems} duration={1.5} />
              </h3>
              <p>Purchased Items</p>
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div className="small-box bg-danger">
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
        <h2>Order Trends</h2>
        <div className="chart-container" style={{ height: "300px" }}>
          {orderTrendsData && chartOptions ? (
            <Line data={orderTrendsData} options={chartOptions} />
          ) : (
            <p>No order trends data available.</p>
          )}
        </div>
        <h2 className="mt-4">Category Distribution</h2>
        <div className="chart-container" style={{ height: "300px" }}>
          {categoryDistributionData ? (
            <Pie data={categoryDistributionData} options={baseOptions} />
          ) : (
            <p>No category distribution data available.</p>
          )}
        </div>
      </div>

      <div className="dashboard-recommendations my-4">
        <h2>Recommended For You</h2>
        <div className="recommendations-grid">
          <div className="recommendation-card">
            <img src="https://placehold.co/150" alt="Recommendation" />
            <p>Product Name</p>
          </div>
          <div className="recommendation-card">
            <img src="https://placehold.co/150" alt="Recommendation" />
            <p>Product Name</p>
          </div>
          <div className="recommendation-card">
            <img src="https://placehold.co/150" alt="Recommendation" />
            <p>Product Name</p>
          </div>
          <div className="recommendation-card">
            <img src="https://placehold.co/150" alt="Recommendation" />
            <p>Product Name</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClientDashboard;