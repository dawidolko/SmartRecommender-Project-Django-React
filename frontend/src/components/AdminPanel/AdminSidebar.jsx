import React, { useState, useEffect } from "react";
import { NavLink, useLocation } from "react-router-dom";
import {
  BarChart2,
  ShoppingBag,
  Users,
  ShoppingCart,
  List,
  ArrowLeft,
  LogOut,
  User,
  BarChart,
  TrendingUp,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import "./AdminPanel.scss";

const HamburgerMenuIcon = () => (
  <svg
    stroke="currentColor"
    fill="none"
    strokeWidth="2"
    viewBox="0 0 24 24"
    strokeLinecap="round"
    strokeLinejoin="round"
    height="1em"
    width="1em"
    xmlns="http://www.w3.org/2000/svg">
    <line x1="3" y1="12" x2="21" y2="12"></line>
    <line x1="3" y1="6" x2="21" y2="6"></line>
    <line x1="3" y1="18" x2="21" y2="18"></line>
  </svg>
);

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
  {
    name: "Statistics",
    icon: BarChart,
    color: "#3B82F6",
    href: "/admin/statistics",
  },
  {
    name: "Probabilistic",
    icon: TrendingUp,
    color: "#8B5CF6",
    href: "/admin/probabilistic",
  },
  {
    name: "Account",
    icon: User,
    color: "#EF4444",
    href: "/admin/account",
  },
];

const AdminSidebar = () => {
  const [isOpen, setIsOpen] = useState(true);
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const location = useLocation();

  useEffect(() => {
    const handleResize = () => {
      setWindowWidth(window.innerWidth);

      if (window.innerWidth <= 800) {
        setIsOpen(false);
      } else {
        setIsOpen(true);
      }
    };

    window.addEventListener("resize", handleResize);

    handleResize();

    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("loggedUser");
    window.location.href = "/login";
  };

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  const isMobile = windowWidth <= 800;

  const isLinkActive = (path) => {
    if (path === "/admin") {
      return location.pathname === "/admin";
    }
    return location.pathname.startsWith(path);
  };

  return (
    <motion.div
      className={`admin-aside ${
        isOpen ? "admin-aside--open" : "admin-aside--closed"
      }`}
      animate={{ width: isOpen && !isMobile ? 300 : 80 }}
      transition={{ duration: 0.3 }}>
      <div className="admin-aside__header">
        {isOpen && (
          <button
            className="admin-aside__toggle"
            onClick={toggleSidebar}
            aria-label="Toggle sidebar">
            <HamburgerMenuIcon />
          </button>
        )}
        <AnimatePresence>
          {isOpen && !isMobile && (
            <motion.div
              className="admin-aside__title"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}>
              <div className="admin-aside__title-content">SmartRecommender</div>
            </motion.div>
          )}
        </AnimatePresence>

        {!isOpen && (
          <button
            className="admin-aside__toggle-collapsed"
            onClick={toggleSidebar}
            aria-label="Expand sidebar">
            <HamburgerMenuIcon />
          </button>
        )}
      </div>
      <nav className="admin-aside__nav">
        <ul className="admin-aside__list">
          {SIDEBAR_ITEMS.map((item) => (
            <li key={item.href}>
              <NavLink
                to={item.href}
                className={
                  isLinkActive(item.href)
                    ? "admin-aside__link admin-aside__link--active"
                    : "admin-aside__link"
                }
                end>
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
