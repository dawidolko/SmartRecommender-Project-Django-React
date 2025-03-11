import React, { useContext } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import ClientSidebar from "../components/ClientPanel/ClientSidebar";
import ClientDashboard from "../components/ClientPanel/ClientDashboard";
import ClientOrders from "../components/ClientPanel/ClientOrders";
import ClientOrderDetail from "../components/ClientPanel/ClientOrderDetail";
import ClientComplaints from "../components/ClientPanel/ClientComplaints";
import ClientComplaintDetail from "../components/ClientPanel/ClientComplaintDetail";
import ClientAccount from "../components/ClientPanel/ClientAccount";
import "../components/ClientPanel/ClientPanel.scss";

const ClientPanel = () => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

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
            <Route index element={<ClientDashboard />} />
            <Route path="orders" element={<ClientOrders />} />
            <Route path="orders/:id" element={<ClientOrderDetail />} />
            <Route path="complaints" element={<ClientComplaints />} />
            <Route path="complaints/:id" element={<ClientComplaintDetail />} />
            <Route path="account" element={<ClientAccount />} />
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
