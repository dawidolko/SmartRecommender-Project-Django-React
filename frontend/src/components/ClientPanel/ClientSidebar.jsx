import React, { useState, useEffect } from "react";
import { NavLink } from "react-router-dom";
import {
  FiHome,
  FiShoppingCart,
  FiList,
  FiUser,
  FiLogOut,
  FiMenu,
} from "react-icons/fi";
import "./ClientPanel.scss";

const ClientSidebar = () => {
  const [isOpen, setIsOpen] = useState(true);

  useEffect(() => {
    if (window.innerWidth < 576) {
      setIsOpen(false);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("loggedUser");
    window.location.href = "/login";
  };

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <aside
      className={`client-aside ${
        isOpen ? "client-aside--open" : "client-aside--closed"
      }`}>
      <div className="client-aside__header">
        <button className="client-aside__toggle" onClick={toggleSidebar}>
          <FiMenu />
        </button>
        {isOpen && <div className="client-aside__title">SmartRecommender</div>}
      </div>

      <nav className="client-aside__nav">
        <div className="client-aside__desc">Client Panel</div>
        <ul className="client-aside__list">
          <li>
            <NavLink
              to=""
              className={({ isActive }) =>
                "client-aside__link " +
                (isActive ? "client-aside__link--active" : "")
              }
              end>
              <FiHome className="client-aside__link-icon" />
              {isOpen && <span>Dashboard</span>}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="orders"
              className={({ isActive }) =>
                "client-aside__link " +
                (isActive ? "client-aside__link--active" : "")
              }>
              <FiShoppingCart className="client-aside__link-icon" />
              {isOpen && <span>My Orders</span>}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="complaints"
              className={({ isActive }) =>
                "client-aside__link " +
                (isActive ? "client-aside__link--active" : "")
              }>
              <FiList className="client-aside__link-icon" />
              {isOpen && <span>Complaints</span>}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="account"
              className={({ isActive }) =>
                "client-aside__link " +
                (isActive ? "client-aside__link--active" : "")
              }>
              <FiUser className="client-aside__link-icon" />
              {isOpen && <span>Account</span>}
            </NavLink>
          </li>
          <li>
            <button
              className="client-aside__link client-aside__link--logout"
              onClick={handleLogout}>
              <FiLogOut className="client-aside__link-icon" />
              {isOpen && <span>Logout</span>}
            </button>
          </li>
        </ul>
      </nav>
    </aside>
  );
};

export default ClientSidebar;
