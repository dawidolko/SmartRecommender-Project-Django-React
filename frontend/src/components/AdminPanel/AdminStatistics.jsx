import React, { useEffect, useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import {
  BarChart2,
  ShoppingBag,
  DollarSign,
  Users,
  Star,
  ShoppingCart,
  TrendingUp,
  List,
} from "lucide-react";
import StatCard from "./StatCard";
import config from "../../config/config";
import { toast } from "react-toastify";
import "./AdminPanel.scss";

const AdminStatistics = () => {
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalSales: 0,
    topSelling: 0,
    totalUsers: 0,
    totalOpinions: 0,
    averageRating: 0,
    topCategoryName: "",
    topTagName: "",
    churnRate: "0%",
    conversionRate: "0%",
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        `${config.apiUrl}/api/admin-dashboard-stats/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setStats({
        totalProducts: res.data.totalProducts || 0,
        totalSales: res.data.totalSales || 0,
        topSelling: res.data.topSelling || 0,
        totalUsers: res.data.clients || 0,
        totalOpinions: res.data.totalOpinions || 0,
        averageRating: res.data.averageRating || 0,
        topCategoryName: res.data.topCategoryName || "",
        topTagName: res.data.topTagName || "",
        churnRate: res.data.churnRate || "0%",
        conversionRate: res.data.conversionRate || "0%",
      });
      setLoading(false);
    } catch (err) {
      console.error("Error fetching statistics:", err);
      toast.error("Failed to fetch statistics. Please try again.");
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading-spinner"></div>;
  }

  return (
    <div className="admin-content">
      <div className="stat_Cards">
        <StatCard
          name="All Products"
          icon={ShoppingBag}
          value={stats.totalProducts}
          color="#8B5CF6"
        />
        <StatCard
          name="Best Selling"
          icon={TrendingUp}
          value={stats.topSelling}
          color="#10B981"
        />
        <StatCard
          name="Total Sales"
          icon={DollarSign}
          value={`$${stats.totalSales.toLocaleString("en-US", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}`}
          color="#EF4444"
        />
        <StatCard
          name="All Users"
          icon={Users}
          value={stats.totalUsers}
          color="#F59E0B"
        />
      </div>

      <div className="stat_Cards">
        <StatCard
          name="All Opinions"
          icon={Star}
          value={stats.totalOpinions}
          color="#6366F1"
        />
        <StatCard
          name="Average Rating"
          icon={BarChart2}
          value={stats.averageRating.toFixed(1)}
          color="#10B981"
        />
        <StatCard
          name="Top Category"
          icon={ShoppingCart}
          value={stats.topCategoryName || "—"}
          color="#F59E0B"
        />
        <StatCard
          name="Top Tag"
          icon={List}
          value={stats.topTagName || "—"}
          color="#EF4444"
        />
      </div>

      <motion.div
        className="admin-statistics-container"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}>
        <div className="admin-statistics-card">
          <h2 className="admin-statistics-title">Statistics Overview</h2>
          <div className="admin-statistics-content">
            <p>
              This page provides a summary of key performance indicators for
              your store.
            </p>
            <p>
              Monitor sales trends, customer engagement, and product performance
              all in one place.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default AdminStatistics;
