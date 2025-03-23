import React, { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

const AdminHeader = ({ title }) => {
  const { user } = useContext(AuthContext);

  const displayName = user
    ? (user.first_name || user.last_name)
      ? `${user.first_name ?? ""} ${user.last_name ?? ""}`.trim()
      : user.username || user.email
    : null;

  return (
    <header className="bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg border-b border-gray-700">
      <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
        {/* Tytuł projektu */}
        <h1 className="text-2xl font-semibold text-gray-100">{title}</h1>
        {/* Dane użytkownika */}
        {user && (
          <div className="flex items-center">
            
            <span className="text-gray-100">Witaj, {displayName}</span>
          </div>
        )}
      </div>
    </header>
  );
};

export default AdminHeader;