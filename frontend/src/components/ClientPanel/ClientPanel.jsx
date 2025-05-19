import { useContext } from "react";
import { Navigate, Outlet } from "react-router-dom";
import ClientSidebar from "./ClientSidebar";
import "./ClientPanel.scss";
import { AuthContext } from "../../context/AuthContext";

const ClientPanel = () => {
  const { user, token } = useContext(AuthContext);

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (token && !user) {
    return <div className="loading-spinner"></div>;
  }

  if (user.role !== "client") {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="client-panel">
      <ClientSidebar />
      <div className="client-wrapper">
        <main className="client-main">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default ClientPanel;
