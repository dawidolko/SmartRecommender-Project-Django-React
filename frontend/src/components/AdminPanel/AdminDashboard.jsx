import React, { useEffect, useState } from "react";
import axios from "axios";
import { BarChart2, ShoppingBag, Users, Zap } from "lucide-react";
import { motion } from "framer-motion";
import config from "../../config/config";
import StatCard from "./StatCard";
import SalesOverviewChart from "./SalesOverviewChart";
import CategoryDistributionChart from "./CategoryDistributionChart";

import "./AdminPanel.scss";

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    totalSales: 0,
    newUsers: 0,
    totalProducts: 0,
    conversionRate: "0%",
  });
  const [dashboardData, setDashboardData] = useState({
    trend: { labels: [], data: [], y_axis_max: 0 },
    category_distribution: { labels: [], data: [] },
    sales_channels: [],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access");

    axios
      .get(`${config.apiUrl}/api/admin-dashboard-stats/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setStats({
          totalSales: res.data.totalSales || 0,
          newUsers: res.data.newUsers || 0,
          totalProducts: res.data.totalProducts || 0,
          conversionRate: res.data.conversionRate || "0%",
        });
        setDashboardData({
          trend: res.data.trend || { labels: [], data: [], y_axis_max: 0 },
          category_distribution: res.data.category_distribution || {
            labels: [],
            data: [],
          },
          sales_channels: res.data.sales_channels || [],
        });
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching dashboard stats:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="loading-spinner"></div>;
  }

  return (
    <main style={{ width: "100%" }}>
      <motion.div
        className="stat_Cards"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}>
        <StatCard
          name="Total Sales"
          icon={Zap}
          value={`$${stats.totalSales.toLocaleString("pl-PL", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}`}
          color="#6366F1"
          variant="first"
        />
        <StatCard
          name="New Users"
          icon={Users}
          value={stats.newUsers.toLocaleString()}
          color="#8B5CF6"
          variant="second"
        />
        <StatCard
          name="Total Products"
          icon={ShoppingBag}
          value={stats.totalProducts.toLocaleString()}
          color="#EC4899"
          variant="third"
        />
        <StatCard
          name="Conversion Rate"
          icon={BarChart2}
          value={stats.conversionRate}
          color="#10B981"
          variant="fourth"
        />
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <SalesOverviewChart data={dashboardData.trend} />
        <CategoryDistributionChart
          category_distribution={dashboardData.category_distribution}
        />
      </div>
    </main>
  );
};

export default AdminDashboard;
