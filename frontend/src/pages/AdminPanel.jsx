import React, { useEffect, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";

import AnimatedPage from "../components/AnimatedPage/AnimatedPage";
import Hero from "../components/Hero/Hero";

import AdminSidebar from "../components/AdminPanel/AdminSidebar";
import AdminHeader from "../components/AdminPanel/AdminHeader";
import AdminDashboard from "../components/AdminPanel/AdminDashboard";
import AdminProducts from "../components/AdminPanel/AdminProducts";
import AdminOrders from "../components/AdminPanel/AdminOrders";
import AdminUsers from "../components/AdminPanel/AdminUsers";
import AdminComplaints from "../components/AdminPanel/AdminComplaints";

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

  // Function to get the title based on the current path
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
      default:
        return "Admin Panel";
    }
  };

  return (
    <AnimatedPage>
      <Hero title="Panel Admin" cName="hero__img" />
      <div className="admin-panel">
        <AdminSidebar />
        <div className="admin-wrapper">
          <AdminHeader title={getTitle()} />
          <main className="admin-main">
            <Routes>
              {/* AdminDashboard is the default route when visiting /admin */}
              <Route path="/" element={<AdminDashboard />} />
              {/* These are the routes for other sections like Products, Orders, etc. */}
              <Route path="products" element={<AdminProducts />} />
              <Route path="orders" element={<AdminOrders />} />
              <Route path="users" element={<AdminUsers />} />
              <Route path="complaints" element={<AdminComplaints />} />
              {/* Catch-all route for undefined paths */}
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
    </AnimatedPage>
  );
};

export default AdminPanel;
