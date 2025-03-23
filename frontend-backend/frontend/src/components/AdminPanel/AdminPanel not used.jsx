import React, { useEffect } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import AdminSidebar from "./AdminSidebar";
import AdminHeader from "./AdminHeader";
import AdminDashboard from "./AdminDashboard";
import AdminProducts from "./AdminProducts";
import AdminOrders from "./AdminOrders";
import AdminCustomers from "./AdminCustomers";
import AdminComplaints from "./AdminComplaints";
import "./AdminPanel.scss";

const AdminPanel = () => {
  const navigate = useNavigate();
  const storedUser = localStorage.getItem("loggedUser");
  const user = storedUser ? JSON.parse(storedUser) : null;

  // Redirect to login if the user is not an admin
  useEffect(() => {
    if (!user || user.role !== "admin") {
      navigate("/login");
    }
  }, [user, navigate]);

  if (!user || user.role !== "admin") {
    return null;
  }

  return (
    <div className="admin-panel">
      <AdminSidebar />
      <div className="admin-wrapper">
        <AdminHeader />
        <main className="admin-main">
          <Routes>
            <Route path="/" element={<AdminDashboard />} />
            <Route path="/products" element={<AdminProducts />} />
            <Route path="/orders" element={<AdminOrders />} />
            <Route path="/customers" element={<AdminCustomers />} />
            <Route path="/complaints" element={<AdminComplaints />} />
          </Routes>
        </main>
      </div>
    </div>
  );
};

export default AdminPanel;
