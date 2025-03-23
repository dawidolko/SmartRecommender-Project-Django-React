import React, { useEffect, useState } from "react";
import axios from "axios";
import { BarChart2, ShoppingBag, Users, Zap } from "lucide-react";
import { motion } from "framer-motion";

import StatCard from "./StatCard";
import SalesOverviewChart from "./SalesOverviewChart";
import CategoryDistributionChart from "./CategoryDistributionChart";
import SalesChannelChart from "./SalesChannelChart";

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

    // Pobieranie statystyk ogólnych
    axios
      .get("http://127.0.0.1:8000/api/admin-stats/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        console.log("Admin Stats:", res.data);
        setStats({
          totalSales: res.data.totalSales || res.data.orders * 100,
          newUsers: res.data.newUsers || res.data.clients,
          totalProducts: res.data.totalProducts || res.data.products,
          conversionRate: res.data.conversionRate || `${((res.data.orders / res.data.clients) * 100 || 0).toFixed(1)}%`,
        });
      })
      .catch((error) => {
        console.error("Error fetching admin stats:", error);
      });

    axios
      .get("http://127.0.0.1:8000/api/admin-dashboard-stats/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        console.log("Dashboard Stats:", res.data);
        setDashboardData({
          trend: res.data.trend || { labels: [], data: [], y_axis_max: 0 },
          category_distribution: res.data.category_distribution || { labels: [], data: [] },
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
    return <div style={{ padding: "2rem" }}>Loading dashboard...</div>;
  }

  return (
    <div className="flex-1 overflow-auto relative z-10">
      <main className="max-w-7xl mx-auto py-6 px-4 lg:px-8">
        {/* Statystyki */}
        <motion.div
          className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          <StatCard name="Total Sales" icon={Zap} value={`$${stats.totalSales.toLocaleString()}`} color="#6366F1" />
          <StatCard name="New Users" icon={Users} value={stats.newUsers.toLocaleString()} color="#8B5CF6" />
          <StatCard name="Total Products" icon={ShoppingBag} value={stats.totalProducts.toLocaleString()} color="#EC4899" />
          <StatCard name="Conversion Rate" icon={BarChart2} value={stats.conversionRate} color="#10B981" />
        </motion.div>

        {/* Wykresy */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <SalesOverviewChart data={dashboardData.trend} />
          <CategoryDistributionChart data={dashboardData.category_distribution} />
          <SalesChannelChart data={dashboardData.sales_channels} />
        </div>
      </main>
    </div>
  );
};

export default AdminDashboard;