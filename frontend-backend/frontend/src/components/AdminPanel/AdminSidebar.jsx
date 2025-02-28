import React, { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  FiHome,
  FiBox,
  FiUsers,
  FiShoppingCart,
  FiList,
  FiArrowLeft,
  FiLogOut,
  FiMenu,
} from "react-icons/fi";
import "./AdminPanel.scss";

const AdminSidebar = () => {
  const [isOpen, setIsOpen] = useState(true);
  const navigate = useNavigate();

  const handleLogout = () => {
    // Remove authentication token and user data from localStorage
    localStorage.removeItem("access");
    localStorage.removeItem("loggedUser");
    navigate("/login", { replace: true });
    window.location.reload();
  };

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <aside
      className={`admin-aside ${
        isOpen ? "admin-aside--open" : "admin-aside--closed"
      }`}
    >
      <div className="admin-aside__header">
        <button className="admin-aside__toggle" onClick={toggleSidebar}>
          <FiMenu />
        </button>
        {isOpen && <div className="admin-aside__title">SmartRecommender</div>}
      </div>
      <nav className="admin-aside__nav">
        <div className="admin-aside__desc">Admin Panel</div>
        <ul className="admin-aside__list">
          <li>
            <NavLink
              to="/admin"
              className={({ isActive }) =>
                "admin-aside__link " +
                (isActive ? "admin-aside__link--active" : "")
              }
              end
            >
              <FiHome className="admin-aside__link-icon" />
              {isOpen && <span>Home</span>}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/admin/orders"
              className={({ isActive }) =>
                "admin-aside__link " +
                (isActive ? "admin-aside__link--active" : "")
              }
            >
              <FiShoppingCart className="admin-aside__link-icon" />
              {isOpen && <span>Orders</span>}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/admin/products"
              className={({ isActive }) =>
                "admin-aside__link " +
                (isActive ? "admin-aside__link--active" : "")
              }
            >
              <FiBox className="admin-aside__link-icon" />
              {isOpen && <span>Products</span>}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/admin/customers"
              className={({ isActive }) =>
                "admin-aside__link " +
                (isActive ? "admin-aside__link--active" : "")
              }
            >
              <FiUsers className="admin-aside__link-icon" />
              {isOpen && <span>Customers</span>}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/admin/complaints"
              className={({ isActive }) =>
                "admin-aside__link " +
                (isActive ? "admin-aside__link--active" : "")
              }
            >
              <FiList className="admin-aside__link-icon" />
              {isOpen && <span>Complaints</span>}
            </NavLink>
          </li>
          <li>
            <a href="/" className="admin-aside__link">
              <FiArrowLeft className="admin-aside__link-icon" />
              {isOpen && <span>Back to page</span>}
            </a>
          </li>
          <br />
          <li>
            <button
              className="admin-aside__link admin-aside__link--logout"
              onClick={handleLogout}
            >
              <FiLogOut className="admin-aside__link-icon" />
              {isOpen && <span>Logout</span>}
            </button>
          </li>
        </ul>
      </nav>
    </aside>
  );
};

export default AdminSidebar;
