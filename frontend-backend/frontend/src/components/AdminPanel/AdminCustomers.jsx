import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Users as UsersIcon, UserPlus, UserCheck, UserX, Trash2 } from "lucide-react";
import axios from "axios";
import StatCard from "./StatCard";
import UserGrowthChart from "./UserGrowthChart";
import UserDemographicsChart from "./UserDemographicsChart";
import "./AdminPanel.scss";


const AdminCustomers = () => {
  const [customers, setCustomers] = useState([]);
  const [stats, setStats] = useState({
    totalCustomers: 0,
    newCustomersToday: 0,
    activeCustomers: 0,
    churnRate: "0%",
  });
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredCustomers, setFilteredCustomers] = useState(customers);

  useEffect(() => {
    fetchCustomers();
    fetchCustomerStats();
  }, []);

  useEffect(() => {
    const filtered = customers.filter(
      (customer) =>
        customer.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (customer.username && customer.username.toLowerCase().includes(searchTerm.toLowerCase()))
    );
    setFilteredCustomers(filtered);
  }, [customers, searchTerm]);

  const fetchCustomers = async () => {
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/users/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setCustomers(res.data);
    } catch (err) {
      console.error("Error fetching customers:", err);
    }
  };

  const fetchCustomerStats = async () => {
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/admin-dashboard-stats/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setStats({
        totalCustomers: res.data.totalCustomers || 0,
        newCustomersToday: res.data.newCustomersToday || 0,
        activeCustomers: res.data.activeCustomers || 0,
        churnRate: res.data.churnRate || "0%",
      });
    } catch (err) {
      console.error("Error fetching customer stats:", err);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleDelete = async (userId) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;
    const token = localStorage.getItem("access");
    try {
      await axios.delete(`http://127.0.0.1:8000/api/users/${userId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchCustomers();
    } catch (error) {
      console.error("Error deleting user:", error);
    }
  };

  return (
    <div className="flex-1 overflow-auto relative z-10">
      <main className="max-w-7xl mx-auto py-6 px-4 lg:px-8">
        {/* Statystyki klientów */}
        <motion.div
          className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          <StatCard
            name="Total Customers"
            icon={UsersIcon}
            value={stats.totalCustomers.toLocaleString()}
            color="#6366F1"
          />
          <StatCard
            name="New Customers Today"
            icon={UserPlus}
            value={stats.newCustomersToday}
            color="#10B981"
          />
          <StatCard
            name="Active Customers"
            icon={UserCheck}
            value={stats.activeCustomers.toLocaleString()}
            color="#F59E0B"
          />
          <StatCard
            name="Churn Rate"
            icon={UserX}
            value={stats.churnRate}
            color="#EF4444"
          />
        </motion.div>

        {/* Tabela klientów */}
        <motion.div
          className="bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-100">Customers</h2>
            <div className="relative">
              <input
                type="text"
                placeholder="Search customers..."
                className="bg-gray-700 text-white placeholder-gray-400 rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={searchTerm}
                onChange={handleSearch}
              />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-700">
              <thead>
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Username
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {filteredCustomers.map((cust) => (
                  <motion.tr
                    key={cust.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.3 }}
                    className="hover:bg-gray-700"
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{cust.id}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{cust.email}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{cust.username || cust.nickname || "--"}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                      <button
                        onClick={() => handleDelete(cust.id)}
                        className="text-red-400 hover:text-red-300 inline-flex items-center"
                      >
                        <Trash2 size={16} className="mr-1" />
                        Delete
                      </button>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>

        {/* Wykresy */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          <UserGrowthChart />
          <UserDemographicsChart />
        </div>
      </main>
    </div>
  );
};

export default AdminCustomers;
