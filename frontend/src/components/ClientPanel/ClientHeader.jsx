import React, { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

const ClientHeader = ({ title }) => {
  useContext(AuthContext);

  return (
    <header className="bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg border-b border-gray-700">
      <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <h1 className="admin-top-header">{title}</h1>
      </div>
    </header>
  );
};

export default ClientHeader;
