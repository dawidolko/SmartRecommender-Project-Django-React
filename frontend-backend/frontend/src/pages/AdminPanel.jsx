import React from "react";
import { Routes, Route, useNavigate } from "react-router-dom";

import AnimatedPage from "../components/AnimatedPage/AnimatedPage";
import Hero from "../components/Hero/Hero";

import AdminSidebar from "../components/AdminPanel/AdminSidebar";
import AdminHeader from "../components/AdminPanel/AdminHeader";
import AdminDashboard from "../components/AdminPanel/AdminDashboard";
import AdminProducts from "../components/AdminPanel/AdminProducts";
import AdminOrders from "../components/AdminPanel/AdminOrders";
import AdminCustomers from "../components/AdminPanel/AdminCustomers";
import AdminComplaints from "../components/AdminPanel/AdminComplaints";

import "../components/AdminPanel/AdminPanel.scss";

const AdminPanel = () => {
  const navigate = useNavigate();

  const storedUser = localStorage.getItem("loggedUser");
  let user = null;
  if (storedUser) {
    user = JSON.parse(storedUser);
  }

  if (!user || user.role !== "admin") {
    navigate("/login");
    return null;
  }

  return (
    <AnimatedPage>
      <Hero title="Panel Admin" cName="hero__img" />

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
