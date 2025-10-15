import React, { useContext, useEffect, useMemo } from "react";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import Hero from "../components/Hero/Hero";
import ClientSidebar from "../components/ClientPanel/ClientSidebar";
import ClientHeader from "../components/ClientPanel/ClientHeader";
import ClientDashboard from "../components/ClientPanel/ClientDashboard";
import ClientOrders from "../components/ClientPanel/ClientOrders";
import ClientComplaints from "../components/ClientPanel/ClientComplaints";
import ClientAccount from "../components/ClientPanel/ClientAccount";
import ClientProbabilistic from "../components/ClientPanel/ClientProbabilistic";
import ClientFuzzyLogic from "../components/ClientPanel/ClientFuzzyLogic";
import "../components/ClientPanel/ClientPanel.scss";

const ClientPanel = () => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (!user || user.role !== "client") {
      navigate("/login");
    }
  }, [user, navigate]);

  const getTitle = useMemo(() => {
    switch (location.pathname) {
      case "/client":
        return "Dashboard";
      case "/client/orders":
        return "My Orders";
      case "/client/complaints":
        return "My Complaints";
      case "/client/account":
        return "Account Settings";
      case "/client/probabilistic":
        return "Recommendations";
      default:
        return "Client Panel";
    }
  }, [location.pathname]);

  const displayName = useMemo(() => {
    if (!user) return null;
    if (user.first_name || user.last_name) {
      return `${user.first_name ?? ""} ${user.last_name ?? ""}`.trim();
    }
    return user.username || user.email || "Client";
  }, [user]);

  if (!user || user.role !== "client") {
    return null;
  }

  return (
    <div className="client-container">
      <Hero title="Panel Client" cName="hero__img" />
      <ClientHeader title={getTitle} />
      <div className="client-panel">
        <ClientSidebar />
        <div className="client-wrapper">
          <div className="welcome-text">
            <span className="text-gray-100 name-span">
              Welcome, {displayName}
            </span>
          </div>
          <main className="client-main">
            <Routes>
              <Route index element={<ClientDashboard />} />
              <Route path="orders" element={<ClientOrders />} />
              <Route path="complaints" element={<ClientComplaints />} />
              <Route path="account" element={<ClientAccount />} />
              <Route path="probabilistic" element={<ClientProbabilistic />} />
              <Route path="fuzzy-logic" element={<ClientFuzzyLogic />} />
              <Route
                path="*"
                element={<div style={{ padding: "2rem" }}>Page Not Found</div>}
              />
            </Routes>
          </main>
        </div>
      </div>
    </div>
  );
};

export default ClientPanel;
