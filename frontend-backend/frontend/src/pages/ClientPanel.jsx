import React from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import ClientSidebar from "../components/ClientPanel/ClientSidebar";
import ClientDashboard from "../components/ClientPanel/ClientDashboard";
import ClientOrders from "../components/ClientPanel/ClientOrders";
import ClientComplaints from "../components/ClientPanel/ClientComplaints";
import ClientAccount from "../components/ClientPanel/ClientAccount";
import "../components/ClientPanel/ClientPanel.scss";

const ClientPanel = () => {
  const navigate = useNavigate();
  const storedUser = localStorage.getItem("loggedUser");
  const user = storedUser ? JSON.parse(storedUser) : null;

  if (!user || user.role !== "client") {
    navigate("/login");
    return null;
  }

  return (
    <div className="client-panel">
      <ClientSidebar />
      <div className="client-wrapper">
        <div className="client-header">
          <h1 className="client-header__title">Welcome, {user.first_name}</h1>
        </div>
        <main className="client-main">
          <Routes>
            <Route path="/" element={<ClientDashboard />} />
            <Route path="/orders" element={<ClientOrders />} />
            <Route path="/complaints" element={<ClientComplaints />} />
            <Route path="/account" element={<ClientAccount />} />
            <Route
              path="*"
              element={<div style={{ padding: "2rem" }}>Page Not Found</div>}
            />
          </Routes>
        </main>
      </div>
    </div>
  );
};

export default ClientPanel;
