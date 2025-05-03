import React, { useEffect, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";

import Hero from "../components/Hero/Hero";

import AdminSidebar from "../components/AdminPanel/AdminSidebar";
import AdminHeader from "../components/AdminPanel/AdminHeader";
import AdminDashboard from "../components/AdminPanel/AdminDashboard";
import AdminProducts from "../components/AdminPanel/AdminProducts";
import AdminOrders from "../components/AdminPanel/AdminOrders";
import AdminUsers from "../components/AdminPanel/AdminUsers";
import AdminComplaints from "../components/AdminPanel/AdminComplaints";
import AdminAccount from "../components/AdminPanel/AdminAccount";
import AdminStatistics from "../components/AdminPanel/AdminStatistics";

import "../components/AdminPanel/AdminPanel.scss";

const AdminPanel = () => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (!user || user.role !== "admin") {
      navigate("/login", { replace: true });
    }
  }, [user, navigate]);

  if (!user || user.role !== "admin") {
    return null;
  }

  const getTitle = () => {
    switch (location.pathname) {
      case "/admin":
        return "Overview";
      case "/admin/products":
        return "Products";
      case "/admin/orders":
        return "Orders";
      case "/admin/users":
        return "Users";
      case "/admin/complaints":
        return "Complaints";
      case "/admin/account":
        return "Account Settings";
      case "/admin/statistics":
        return "Statistics";
      default:
        return "Admin Panel";
    }
  };

  return (
    <div className="admin-container">
      <Hero title="Panel Admin" cName="hero__img" />
      <div className="admin-panel">
        <AdminSidebar />
        <div className="admin-wrapper">
          <AdminHeader title={getTitle()} />
          <main className="admin-main">
            <Routes>
              <Route path="/" element={<AdminDashboard />} />
              <Route path="products" element={<AdminProducts />} />
              <Route path="orders" element={<AdminOrders />} />
              <Route path="users" element={<AdminUsers />} />
              <Route path="complaints" element={<AdminComplaints />} />
              <Route path="account" element={<AdminAccount />} />
              <Route path="statistics" element={<AdminStatistics />} />
              <Route
                path="*"
                element={
                  <div style={{ padding: "2rem" }}>
                    <h2>Not Found</h2>
                  </div>
                }
              />
            </Routes>
          </main>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;
