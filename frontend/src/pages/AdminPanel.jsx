import { useEffect, useContext, useMemo } from "react";
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
import AdminProbabilistic from "../components/AdminPanel/AdminProbabilistic";

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

  const getTitle = useMemo(() => {
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
      case "/admin/probabilistic":
        return "Probabilistic Analytics";
      default:
        return "Admin Panel";
    }
  }, [location.pathname]);

  const displayName = useMemo(() => {
    if (!user) return null;
    if (user.first_name || user.last_name) {
      return `${user.first_name ?? ""} ${user.last_name ?? ""}`.trim();
    }
    return user.username || user.email || "Admin";
  }, [user]);

  if (!user || user.role !== "admin") {
    return null;
  }

  return (
    <div className="admin-container">
      <Hero title="Panel Admin" cName="hero__img" />
      <AdminHeader title={getTitle} />
      <div className="admin-panel">
        <AdminSidebar />
        <div className="admin-wrapper">
          <div className="welcome-text">
            <span className="text-gray-100 name-span">
              Welcome, {displayName}
            </span>
          </div>
          <main className="admin-main">
            <Routes>
              <Route path="/" element={<AdminDashboard />} />
              <Route path="products" element={<AdminProducts />} />
              <Route path="orders" element={<AdminOrders />} />
              <Route path="users" element={<AdminUsers />} />
              <Route path="complaints" element={<AdminComplaints />} />
              <Route path="account" element={<AdminAccount />} />
              <Route path="statistics" element={<AdminStatistics />} />
              <Route path="probabilistic" element={<AdminProbabilistic />} />
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
