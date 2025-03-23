import { useEffect, useState } from "react";
import axios from "axios";
import { BarChart2, ShoppingBag, Users, Zap } from "lucide-react";
import { motion } from "framer-motion";

import Header from "../components/common/Header";
import StatCard from "../components/common/StatCard";
import SalesOverviewChart from "../components/overview/SalesOverviewChart";
import CategoryDistributionChart from "../components/overview/CategoryDistributionChart";
import SalesChannelChart from "../components/overview/SalesChannelChart";

const OverviewPage = () => {
  const [dashboardStats, setDashboardStats] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("access");
    axios
      .get("http://127.0.0.1:8000/api/admin-dashboard-stats/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setDashboardStats(res.data);
      })
      .catch((error) => {
        console.error("Error fetching dashboard stats:", error);
      });
  }, []);

  const salesOverviewData = dashboardStats
    ? dashboardStats.trend.labels.map((label, index) => ({
        name: label,
        sales: dashboardStats.trend.data[index],
      }))
    : null;

  const categoryData = dashboardStats
    ? dashboardStats.category_distribution.labels.map((label, index) => ({
        name: label,
        value: dashboardStats.category_distribution.data[index],
      }))
    : null;

  return (
    <div className="flex-1 overflow-auto relative z-10">
      <Header title="Overview" />

      <main className="max-w-7xl mx-auto py-6 px-4 lg:px-8">
        {/* STATS */}
        <motion.div
          className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          <StatCard
            name="Total Sales"
            icon={Zap}
            value={dashboardStats ? `$${dashboardStats.totalSales}` : "$0"}
            color="#6366F1"
          />
          <StatCard
            name="New Users"
            icon={Users}
            value={dashboardStats ? dashboardStats.newUsers : "0"}
            color="#8B5CF6"
          />
          <StatCard
            name="Total Products"
            icon={ShoppingBag}
            value={dashboardStats ? dashboardStats.totalProducts : "0"}
            color="#EC4899"
          />
          <StatCard
            name="Conversion Rate"
            icon={BarChart2}
            value={dashboardStats ? dashboardStats.conversionRate : "0%"}
            color="#10B981"
          />
        </motion.div>

        {/* CHARTS */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <SalesOverviewChart data={salesOverviewData} />
          <CategoryDistributionChart data={categoryData} />
          <SalesChannelChart data={dashboardStats ? dashboardStats.sales_channels : null} />
        </div>
      </main>
    </div>
  );
};

export default OverviewPage;
