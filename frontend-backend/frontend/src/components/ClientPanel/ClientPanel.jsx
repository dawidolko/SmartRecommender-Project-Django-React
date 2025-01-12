import React from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import ClientSidebar from "./ClientSidebar";
import ClientDashboard from "./ClientDashboard";
import ClientOrders from "./ClientOrders";
import ClientComplaints from "./ClientComplaints";
import ClientAccount from "./ClientAccount";
import "./ClientPanel.scss";

const ClientPanel = () => {
  const navigate = useNavigate();

  const storedUser = localStorage.getItem("loggedUser");
  let user = null;
  if (storedUser) {
    user = JSON.parse(storedUser);
  }

  if (!user || user.role !== "client") {
    navigate("/login");
    return null;
  }

  return (
    <div className="client-panel">
      <ClientSidebar />
      <div className="client-wrapper">
        <main className="client-main">
          <Routes>
            <Route path="/" element={<ClientDashboard />} />
            <Route path="/orders" element={<ClientOrders />} />
            <Route path="/complaints" element={<ClientComplaints />} />
            <Route path="/account" element={<ClientAccount />} />
          </Routes>
        </main>
      </div>
    </div>
  );
};

export default ClientPanel;
