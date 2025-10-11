import React, { useState, useEffect } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  FiArrowLeft,
  FiHome,
  FiShoppingCart,
  FiList,
  FiUser,
  FiLogOut,
  FiMenu,
  FiBarChart2,
  FiCpu,
} from "react-icons/fi";
import "./ClientPanel.scss";

const ClientSidebar = () => {
  const [isOpen, setIsOpen] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 900) {
        setIsOpen(false);
      } else {
        setIsOpen(true);
      }
    };

    handleResize();
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
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
              to="/client"
              className={({ isActive }) =>
                "client-aside__link " +
                (isActive ? "client-aside__link--active" : "")
              }
              end>
              <FiHome className="client-aside__link-icon icon-dashboard" />
              {isOpen && <span>Dashboard</span>}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/client/orders"
              className={({ isActive }) =>
                "client-aside__link " +
                (isActive ? "client-aside__link--active" : "")
              }>
              <FiShoppingCart className="client-aside__link-icon icon-orders" />
              {isOpen && <span>My Orders</span>}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/client/probabilistic"
              className={({ isActive }) =>
                "client-aside__link " +
                (isActive ? "client-aside__link--active" : "")
              }>
              <FiBarChart2 className="client-aside__link-icon icon-probabilistic" />
              {isOpen && <span>Smart Recommendations</span>}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/client/fuzzy-logic"
              className={({ isActive }) =>
                "client-aside__link " +
                (isActive ? "client-aside__link--active" : "")
              }>
              <FiCpu className="client-aside__link-icon icon-fuzzy" />
              {isOpen && <span>Fuzzy Logic</span>}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/client/complaints"
              className={({ isActive }) =>
                "client-aside__link " +
                (isActive ? "client-aside__link--active" : "")
              }>
              <FiList className="client-aside__link-icon icon-complaints" />
              {isOpen && <span>Complaints</span>}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/client/account"
              className={({ isActive }) =>
                "client-aside__link " +
                (isActive ? "client-aside__link--active" : "")
              }>
              <FiUser className="client-aside__link-icon icon-account" />
              {isOpen && <span>Account</span>}
            </NavLink>
          </li>
          <li>
            <button
              className="client-aside__link client-aside__link--back"
              onClick={() => navigate("/")}>
              <FiArrowLeft className="client-aside__link-icon" />
              {isOpen && <span>Back to page</span>}
            </button>
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
