import React, { useState, useEffect } from "react";
import { NavLink } from "react-router-dom";
import {
  BarChart2,
  ShoppingBag,
  Users,
  ShoppingCart,
  List,
  ArrowLeft,
  LogOut,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import "./AdminPanel.scss";

const SIDEBAR_ITEMS = [
  { name: "Dashboard", icon: BarChart2, color: "#6366f1", href: "/admin" },
  {
    name: "Products",
    icon: ShoppingBag,
    color: "#8B5CF6",
    href: "/admin/products",
  },
  { name: "Users", icon: Users, color: "#EC4899", href: "/admin/users" },
  {
    name: "Orders",
    icon: ShoppingCart,
    color: "#F59E0B",
    href: "/admin/orders",
  },
  {
    name: "Complaints",
    icon: List,
    color: "#10B981",
    href: "/admin/complaints",
  },
];

const AdminSidebar = () => {
  const [isOpen] = useState(true);
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("loggedUser");
    window.location.href = "/login";
  };

  const isMobile = windowWidth <= 800;

  return (
    <motion.div
      className={`admin-aside ${
        isMobile
          ? "admin-aside--closed"
          : isOpen
          ? "admin-aside--open"
          : "admin-aside--closed"
      }`}
      style={{ width: isMobile ? "80px" : isOpen ? "300px" : "80px" }}
      animate={{ width: isOpen && !isMobile ? 300 : isMobile ? 80 : 300 }}
      transition={{ duration: 0.3 }}>
      <div className="admin-aside__header">
        {/* <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setIsOpen(!isOpen)}
          className="admin-aside__toggle">
          <Menu size={24} />
        </motion.button> */}
        <AnimatePresence>
          {isOpen && !isMobile && (
            <motion.div
              className="admin-aside__title"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}>
              SmartRecommender
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      <nav className="admin-aside__nav">
        <ul className="admin-aside__list">
          {SIDEBAR_ITEMS.map((item) => (
            <li key={item.href}>
              <NavLink
                to={item.href}
                className={({ isActive }) =>
                  `admin-aside__link ${
                    isActive ? "admin-aside__link--active" : ""
                  }`
                }>
                <item.icon
                  size={20}
                  style={{ color: item.color, minWidth: "20px" }}
                />
                <AnimatePresence>
                  {isOpen && !isMobile && (
                    <motion.span
                      initial={{ opacity: 0, width: 0 }}
                      animate={{ opacity: 1, width: "auto" }}
                      exit={{ opacity: 0, width: 0 }}
                      transition={{ duration: 0.2 }}>
                      {item.name}
                    </motion.span>
                  )}
                </AnimatePresence>
              </NavLink>
            </li>
          ))}
          <li>
            <a href="/" className="admin-aside__link">
              <ArrowLeft size={20} style={{ minWidth: "20px" }} />
              {isOpen && !isMobile && <span>Back to page</span>}
            </a>
          </li>
          <li>
            <button
              className="admin-aside__link admin-aside__link--logout"
              onClick={handleLogout}>
              <LogOut size={20} style={{ minWidth: "20px" }} />
              {isOpen && !isMobile && <span>Logout</span>}
            </button>
          </li>
        </ul>
      </nav>
    </motion.div>
  );
};

export default AdminSidebar;
