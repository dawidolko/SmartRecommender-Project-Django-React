import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import ClientSidebar from "./ClientSidebar";
import ClientDashboard from "./ClientDashboard";
import ClientOrders from "./ClientOrders";
import ClientComplaints from "./ClientComplaints";
import ClientAccount from "./ClientAccount";
import "./ClientPanel.scss";

const ClientPanel = () => {
  console.log("[ClientPanel] Component rendered");

  const storedUser = localStorage.getItem("loggedUser");
  let user = null;
  if (storedUser) {
    try {
      user = JSON.parse(storedUser);
    } catch (error) {
      console.error("[ClientPanel] Error parsing user data:", error);
    }
  }

  console.log("[ClientPanel] User data:", user);

  if (!user || user.role !== "client") {
    console.warn("[ClientPanel] Unauthorized access, redirecting...");
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="client-panel">
      <ClientSidebar />
      <div className="client-wrapper">
        <main className="client-main">
          <Routes>
            <Route path="/" element={<ClientDashboard />} />
            <Route path="orders" element={<ClientOrders />} />
            <Route path="complaints" element={<ClientComplaints />} />
            <Route path="account" element={<ClientAccount />} />
          </Routes>
        </main>
      </div>
    </div>
  );
};

export default ClientPanel;
