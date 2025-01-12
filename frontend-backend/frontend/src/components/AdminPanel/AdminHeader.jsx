import React, { useEffect, useState } from "react";
import axios from "axios";
import "./AdminPanel.scss";

const AdminHeader = () => {
  const [user, setUser] = useState(null);
  const avatarUrl = "http://127.0.0.1:8000/media/avatar.svg";

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/me/")
      .then((res) => setUser(res.data))
      .catch((err) => console.error("Error fetching user data:", err));
  }, []);

  return (
    <header className="admin-header">
      <p className="admin-header__title">Final project for engineering work</p>
      <div className="admin-header__user">
        <img className="admin-header__user-av" src={avatarUrl} alt="avatar" />
        {user && (
          <span className="admin-header__user-hello">
            Hello, {user.first_name} {user.last_name}
          </span>
        )}
      </div>
    </header>
  );
};

export default AdminHeader;
