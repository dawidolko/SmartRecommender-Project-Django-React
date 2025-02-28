import React, { useContext } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import ClientSidebar from "./ClientSidebar";
import ClientDashboard from "./ClientDashboard";
import ClientOrders from "./ClientOrders";
import ClientComplaints from "./ClientComplaints";
import ClientAccount from "./ClientAccount";
import "./ClientPanel.scss";
import { AuthContext } from "../../context/AuthContext";

const ClientPanel = () => {
  const { user, token } = useContext(AuthContext);

  // Jeśli nie ma tokenu – użytkownik nie jest zalogowany, przekieruj
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Jeśli token jest, ale user jeszcze nie został zdekodowany, wyświetl loader
  if (token && !user) {
    return <div>Loading...</div>;
  }

  // Gdy mamy już usera, sprawdzamy jego rolę
  if (user.role !== "client") {
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
