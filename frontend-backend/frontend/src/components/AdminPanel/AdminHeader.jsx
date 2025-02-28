import React, { useState, useEffect } from "react";
import "./AdminPanel.scss";

const AdminHeader = () => {
  const [user, setUser] = useState(null);
  const avatarUrl = "http://127.0.0.1:8000/media/avatar.svg";

  useEffect(() => {
    const storedUser = localStorage.getItem("loggedUser");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const displayName = user
    ? (user.first_name || user.last_name) 
      ? `${user.first_name ?? ""} ${user.last_name ?? ""}`.trim()
      : user.username || user.email
    : null;

  return (
    <header className="admin-header">
      <p className="admin-header__title">Final project for engineering work</p>
      <div className="admin-header__user">
        <img className="admin-header__user-av" src={avatarUrl} alt="avatar" />
        {user && (
          <span className="admin-header__user-hello">
            Hello, {displayName}
          </span>
        )}
      </div>
    </header>
  );
};

export default AdminHeader;
