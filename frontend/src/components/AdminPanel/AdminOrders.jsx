/**
 * AdminOrders Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Admin panel component for order management and monitoring in the e-commerce system.
 * Provides comprehensive order tracking, status updates, and analytics dashboard.
 *
 * Features:
 *   - Real-time order list with status tracking
 *   - Order status management (Pending → Shipped → Delivered)
 *   - Search functionality (by order ID, status, date)
 *   - Sorting by multiple fields (ID, date, status, total)
 *   - Pagination (10 orders per page)
 *   - Order statistics dashboard:
 *     * Total orders count
 *     * Pending orders count
 *     * Shipped orders count
 *     * Delivered orders count
 *   - Order details view (expandable rows)
 *   - Product list per order
 *   - Order total calculation
 *   - Date formatting and display
 *
 * Order Status Flow:
 *   1. Pending - Initial state when order is created
 *   2. Shipped - Order has been dispatched
 *   3. Delivered - Order has been delivered to customer
 *
 * State Management:
 *   - orders: Array of all orders from database
 *   - stats: Dashboard statistics (total, pending, shipped, delivered)
 *   - filteredOrders: Orders after search/filter/sort operations
 *   - searchTerm: Current search query
 *   - sortField: Active sorting field (id, date_order, status, total)
 *   - sortDirection: Sort direction ('asc' or 'desc')
 *   - currentPage: Active pagination page
 *   - loading: Loading state for async operations
 *
 * API Endpoints:
 *   - GET /api/orders/ - Fetch all orders (admin only)
 *   - PUT /api/orders/:id/ - Update order status
 *   - DELETE /api/orders/:id/ - Delete order
 *
 * Calculations:
 *   - Order Total: Σ(product_price × quantity) for all products in order
 *   - Statistics: Real-time count aggregation by status
 *
 * @component
 * @returns {React.ReactElement} Admin orders management page with dashboard
 */
/* eslint-disable react-hooks/exhaustive-deps */
import React, { useEffect, useState, useCallback } from "react";
import { motion } from "framer-motion";
import {
  Search,
  ChevronLeft,
  ChevronRight,
  ChevronUp,
  ChevronDown,
  Package,
} from "lucide-react";
import axios from "axios";
import config from "../../config/config";
import StatCard from "./StatCard";
import "./AdminPanel.scss";

const AdminOrders = () => {
  const [orders, setOrders] = useState([]);
  const [stats, setStats] = useState({
    totalOrders: 0,
    pendingOrders: 0,
    shippedOrders: 0,
    deliveredOrders: 0,
  });

  const [searchTerm, setSearchTerm] = useState("");
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [sortField, setSortField] = useState("id");
  const [sortDirection, setSortDirection] = useState("desc");

  const [currentPage, setCurrentPage] = useState(1);
  const [ordersPerPage] = useState(10);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    await Promise.all([fetchOrders(), fetchOrderStats()]);
    setLoading(false);
  };

  const handleFilteringAndSorting = useCallback(() => {
    if (!orders.length) return;

    let data = [...orders];

    data = data.filter((order) => {
      if (!searchTerm) return true;

      const term = searchTerm.toLowerCase();
      const idMatch = order.id.toString().includes(term);
      const statusMatch = order.status?.toLowerCase().includes(term);

      const orderDate = formatDate(order.date_order);
      const dateMatch = orderDate.includes(term);

      return idMatch || statusMatch || dateMatch;
    });

    data.sort((a, b) => {
      let fieldA = a[sortField] || "";
      let fieldB = b[sortField] || "";

      if (sortField === "date_order") {
        fieldA = new Date(fieldA);
        fieldB = new Date(fieldB);
      } else if (typeof fieldA === "string") {
        fieldA = fieldA.toLowerCase();
        fieldB = fieldB.toLowerCase();
      }

      if (fieldA < fieldB) return sortDirection === "asc" ? -1 : 1;
      if (fieldA > fieldB) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });

    setFilteredOrders(data);
  }, [orders, searchTerm, sortField, sortDirection]);

  useEffect(() => {
    handleFilteringAndSorting();
  }, [handleFilteringAndSorting]);

  const handleSearch = (value) => {
    setSearchTerm(value);
    setCurrentPage(1);
  };

  const fetchOrders = async () => {
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(`${config.apiUrl}/api/orders/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setOrders(res.data);
      setFilteredOrders(res.data);
    } catch (err) {
      console.error("Error fetching orders:", err);
    }
  };

  const fetchOrderStats = async () => {
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(`${config.apiUrl}/api/orders/`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      const allOrders = res.data;
      const pending = allOrders.filter(
        (order) => order.status === "Pending"
      ).length;
      const shipped = allOrders.filter(
        (order) => order.status === "Shipped"
      ).length;
      const delivered = allOrders.filter(
        (order) => order.status === "Delivered"
      ).length;

      setStats({
        totalOrders: allOrders.length,
        pendingOrders: pending,
        shippedOrders: shipped,
        deliveredOrders: delivered,
      });
    } catch (err) {
      console.error("Error calculating order stats:", err);
    }
  };

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const renderSortIcon = (field) => {
    if (sortField !== field) return null;
    return sortDirection === "asc" ? (
      <ChevronUp size={14} />
    ) : (
      <ChevronDown size={14} />
    );
  };

  const getStatusClass = (status) => {
    switch (status) {
      case "Processing":
        return "status-processing";
      case "Shipped":
        return "status-shipped";
      case "Delivered":
        return "status-delivered";
      case "Cancelled":
        return "status-cancelled";
      case "Pending":
      default:
        return "status-pending";
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "";
    const date = new Date(dateString);
    return date
      .toLocaleString("en-GB", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      })
      .replace(",", "");
  };

  const indexOfLast = currentPage * ordersPerPage;
  const indexOfFirst = indexOfLast - ordersPerPage;
  const currentSlice = filteredOrders.slice(indexOfFirst, indexOfLast);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const nextPage = () => {
    if (currentPage < Math.ceil(filteredOrders.length / ordersPerPage)) {
      setCurrentPage(currentPage + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  if (loading) {
    return <div className="loading-spinner"></div>;
  }

  return (
    <div className="admin-content">
      <main className="admin-products">
        <motion.div
          className="stat_Cards"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}>
          <StatCard
            name="Total Orders"
            icon={Package}
            value={stats.totalOrders.toLocaleString()}
            color="#6366F1"
            variant="first"
          />
          <StatCard
            name="Pending Orders"
            icon={Package}
            value={stats.pendingOrders.toLocaleString()}
            color="#F59E0B"
            variant="fourth"
          />
          <StatCard
            name="Shipped Orders"
            icon={Package}
            value={stats.shippedOrders.toLocaleString()}
            color="#10B981"
            variant="third"
          />
          <StatCard
            name="Delivered Orders"
            icon={Package}
            value={stats.deliveredOrders.toLocaleString()}
            color="#EF4444"
            variant="second"
          />
        </motion.div>

        <motion.div
          className="product-table-container"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}>
          <div className="product-table-header">
            <h2>All Orders</h2>
            <div className="search-container">
              <input
                type="text"
                placeholder="Search orders... (ID, Status, Date)"
                onChange={(e) => handleSearch(e.target.value)}
                value={searchTerm}
              />
              <Search className="search-icon" size={18} />
            </div>
          </div>

          <div className="table-wrapper">
            <table className="product-table">
              <thead>
                <tr>
                  <th
                    onClick={() => handleSort("id")}
                    className="sortable-header"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>Order ID</span>
                      {renderSortIcon("id")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("date_order")}
                    className="sortable-header"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>Date</span>
                      {renderSortIcon("date_order")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("status")}
                    className="sortable-header"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>Status</span>
                      {renderSortIcon("status")}
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody>
                {currentSlice.length > 0 ? (
                  currentSlice.map((order) => (
                    <motion.tr
                      key={order.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.3 }}>
                      <td style={{ textAlign: "center" }}>{order.id}</td>
                      <td style={{ textAlign: "center" }}>
                        {formatDate(order.date_order)}
                      </td>
                      <td style={{ textAlign: "center" }}>
                        <span
                          className={`status-badge ${getStatusClass(
                            order.status
                          )}`}>
                          {order.status}
                        </span>
                      </td>
                    </motion.tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="3" className="no-results">
                      No orders found matching your search criteria
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {filteredOrders.length > 0 && (
            <div className="pagination-container">
              <div className="pagination-info">
                <p className="pagination-text">
                  Displaying {indexOfFirst + 1} to{" "}
                  {Math.min(indexOfLast, filteredOrders.length)} of{" "}
                  {filteredOrders.length} orders
                </p>
              </div>
              <div className="pagination-controls">
                <button
                  onClick={prevPage}
                  disabled={currentPage === 1}
                  className={`pagination-button ${
                    currentPage === 1 ? "disabled" : ""
                  }`}>
                  <ChevronLeft size={16} />
                  <span>&lt;</span>
                </button>
                {Array.from({
                  length: Math.ceil(filteredOrders.length / ordersPerPage),
                })
                  .map((_, index) => (
                    <button
                      key={index}
                      onClick={() => paginate(index + 1)}
                      className={`pagination-number ${
                        currentPage === index + 1 ? "active" : ""
                      }`}>
                      {index + 1}
                    </button>
                  ))
                  .slice(
                    Math.max(0, currentPage - 3),
                    Math.min(
                      Math.ceil(filteredOrders.length / ordersPerPage),
                      currentPage + 2
                    )
                  )}
                <button
                  onClick={nextPage}
                  disabled={
                    currentPage >=
                    Math.ceil(filteredOrders.length / ordersPerPage)
                  }
                  className={`pagination-button ${
                    currentPage >=
                    Math.ceil(filteredOrders.length / ordersPerPage)
                      ? "disabled"
                      : ""
                  }`}>
                  <ChevronRight size={16} />
                  <span>&gt;</span>
                </button>
              </div>
            </div>
          )}
        </motion.div>
      </main>
    </div>
  );
};

export default AdminOrders;
