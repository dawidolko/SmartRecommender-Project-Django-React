import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";

const PublicRoute = ({ children }) => {
  const { user, token } = useContext(AuthContext);

  if (token && user) {
    const redirectPath = user.role === "admin" ? "/admin" : "/client";
    return <Navigate to={redirectPath} replace />;
  }

  return children;
};

export default PublicRoute;
