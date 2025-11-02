/**
 * Navbar Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Main navigation bar component with responsive design, user authentication,
 * and dynamic category menu.
 *
 * Features:
 *   - Responsive hamburger menu for mobile devices
 *   - Dynamic background color on scroll
 *   - User authentication state display
 *   - User dropdown menu (Profile/Admin Panel/Logout)
 *   - Shopping cart preview with item count
 *   - Favorites counter with heart icon
 *   - Search modal integration
 *   - Category dropdown menu
 *   - Sticky navigation on scroll
 *   - Role-based menu items (client vs admin)
 *
 * Navigation Links:
 *   - Home - Main landing page
 *   - Shop - Product catalog with categories
 *   - About - Company information
 *   - Blog - Articles and news
 *   - FAQ - Frequently asked questions
 *   - Contact - Contact form
 *   - Cart - Shopping cart page
 *   - Favorites - Saved products
 *
 * User Menu (Authenticated):
 *   - Client Panel - Order history, recommendations, insights
 *   - Admin Panel - Product/order/user management (admin only)
 *   - Logout - Clear session and redirect
 *
 * State Management:
 *   - isOpen: Mobile menu toggle state
 *   - navBgc: Background color change on scroll
 *   - showUserDropdown: User menu dropdown visibility
 *   - categories: Product categories from API
 *   - searchModalOpen: Search modal visibility
 *   - user: Current authenticated user from AuthContext
 *   - favorites: Favorites count from FavoritesContext
 *   - cart items: From CartContext
 *
 * API Endpoints:
 *   - GET /api/categories/ - Fetch product categories
 *
 * Authentication:
 *   - Reads user from localStorage on mount
 *   - Displays login/register or user icon based on auth state
 *   - Logout clears access token and user data
 *
 * @component
 * @returns {React.ReactElement} Navigation bar with responsive menu
 */
import "./Navbar.scss";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useState, useEffect, useContext } from "react";
import { GiHamburgerMenu } from "react-icons/gi";
import {
  AiOutlineClose,
  AiOutlineHeart,
  AiOutlineSearch,
} from "react-icons/ai";
import { FaUserCircle } from "react-icons/fa";
import { useFavorites } from "../FavoritesContent/FavoritesContext";
import CartPreview from "../CartContent/CartPreview";
import SearchModal from "./SearchModal";
import axios from "axios";
import config from "../../config/config";
import { CartContext } from "../ShopContext/ShopContext";
import { AuthContext } from "../../context/AuthContext";

const Navbar = () => {
  const { favorites } = useFavorites();
  useContext(CartContext);
  const { user, setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const [isOpen, setIsOpen] = useState(false);
  const [navBgc, setNavBgc] = useState(false);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const [categories, setCategories] = useState([]);
  const [showModal, setShowModal] = useState(true);
  const [searchModalOpen, setSearchModalOpen] = useState(false);

  useEffect(() => {
    const savedUser = localStorage.getItem("loggedUser");
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, [setUser]);

  useEffect(() => {
    const changeBgc = () => {
      setNavBgc(window.scrollY > 10);
    };
    window.addEventListener("scroll", changeBgc);
    return () => {
      window.removeEventListener("scroll", changeBgc);
    };
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 0 && showModal) {
        setShowModal(false);
      }
    };
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, [showModal]);

  useEffect(() => {
    axios
      .get(`${config.apiUrl}/api/categories/`)
      .then((res) => setCategories(res.data))
      .catch((err) => console.error("Error fetching categories:", err));
  }, []);

  const handleClick = () => setIsOpen(!isOpen);
  const closeNav = () => setIsOpen(false);

  const handleUserIconHover = () => {
    setShowUserDropdown(true);
  };

  const handleUserIconLeave = () => {
    setShowUserDropdown(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("loggedUser");
    window.location.href = "/login";
  };

  const panelPrefix = user && user.role === "admin" ? "/admin" : "/client";

  const closeModal = () => setShowModal(false);

  return (
    <>
      <nav className={navBgc ? "navbar navbar__bgc" : "navbar"}>
        {showModal && (
          <div className="modal">
            <div className="modal__content">
              <p className="modal__text">
                Want to feel the magic of technology? Check out our products.
                Save up to $100!
              </p>
              <div className="modal__actions">
                <button
                  className="modal__button"
                  onClick={() => navigate("/shop")}>
                  View products
                </button>
                <AiOutlineClose className="modal__close" onClick={closeModal} />
              </div>
            </div>
          </div>
        )}
        <div className="navbar__logo-wrapper">
          <Link to="/" className="header__logo">
            <p className="header__logo-text"></p>
          </Link>
        </div>
        <div className="navbar__main__section">
          <div className="navbar__container container nav_con">
            <Link to="/" className="header__logo__display">
              <p className="header__logo-text"></p>
            </Link>
            <div className="navbar__section">
              <div
                className="navbar__user"
                onMouseEnter={handleUserIconHover}
                onMouseLeave={handleUserIconLeave}
                style={{ cursor: "pointer" }}>
                <FaUserCircle
                  className="navbar__user-icon"
                  onClick={() => setShowUserDropdown(!showUserDropdown)}
                />
                {showUserDropdown && (
                  <div className="navbar__user-dropdown">
                    {user ? (
                      <>
                        <Link
                          to={`${panelPrefix}/account`}
                          className="navbar__dropdown-link">
                          Your Account
                        </Link>
                        <Link
                          to={`${panelPrefix}/orders`}
                          className="navbar__dropdown-link">
                          Orders
                        </Link>
                        <Link
                          to={panelPrefix}
                          className="navbar__dropdown-link">
                          Go to Panel
                        </Link>
                        <button
                          onClick={handleLogout}
                          className="navbar__logoutBtn">
                          Logout
                        </button>
                      </>
                    ) : (
                      <>
                        <Link to="/login" className="navbar__dropdown-link">
                          Login
                        </Link>
                        <Link to="/signup" className="navbar__dropdown-link">
                          Register
                        </Link>
                      </>
                    )}
                  </div>
                )}
              </div>
              <div className="navbar__search-wrapper">
                <button
                  className="search-icon"
                  onClick={() => setSearchModalOpen(true)}>
                  <AiOutlineSearch />
                </button>
              </div>
            </div>
            <ul
              className={
                isOpen ? "navbar__links navbar__links-active" : "navbar__links"
              }>
              <li>
                <NavLink className="navbar__link" to="/" onClick={closeNav}>
                  HOME
                </NavLink>
              </li>
              <li>
                <NavLink
                  className="navbar__link"
                  to="/about"
                  onClick={closeNav}>
                  ABOUT
                </NavLink>
              </li>
              <li>
                <NavLink className="navbar__link" to="/shop" onClick={closeNav}>
                  SHOP
                </NavLink>
              </li>
              <li>
                <NavLink className="navbar__link" to="/faq" onClick={closeNav}>
                  FAQ
                </NavLink>
              </li>
              <li>
                <NavLink className="navbar__link" to="/blog" onClick={closeNav}>
                  BLOG
                </NavLink>
              </li>
              <li className="navbar__categories">
                <p className="navbar__link">CATEGORY</p>
                <div className={`navbar__dropdown ${isOpen ? "active" : ""}`}>
                  {Object.entries(
                    categories.reduce((acc, category) => {
                      const [main, sub] = category.name.split(".");
                      if (!acc[main]) acc[main] = [];
                      if (sub) acc[main].push(sub);
                      return acc;
                    }, {})
                  ).map(([mainCategory, subCategories]) => (
                    <div
                      key={mainCategory}
                      className="navbar__main-category"
                      onMouseEnter={(e) => {
                        e.currentTarget.classList.add("hover");
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.classList.remove("hover");
                      }}>
                      <NavLink
                        to={`/category/${mainCategory}`}
                        className="navbar__main-category-name"
                        onClick={closeNav}>
                        {mainCategory.toUpperCase()}
                      </NavLink>
                      {subCategories.length > 0 && (
                        <div className="navbar__subcategories">
                          {subCategories.map((subCategory) => (
                            <NavLink
                              key={subCategory}
                              to={`/category/${mainCategory}.${subCategory}`}
                              className="navbar__dropdown-item"
                              onClick={closeNav}>
                              {subCategory}
                            </NavLink>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </li>
              <li className="navbar__icons">
                <NavLink
                  className="navbar__favorites-link"
                  to="/favorites"
                  onClick={closeNav}>
                  <div className="navbar__favorites">
                    <span className="navbar__quantity">{favorites.length}</span>
                    <AiOutlineHeart className="navbar__heart" />
                  </div>
                </NavLink>
                <CartPreview />
              </li>
            </ul>
            <div className="navbar__hamburger" onClick={handleClick}>
              {isOpen ? <AiOutlineClose /> : <GiHamburgerMenu />}
            </div>
          </div>
        </div>
      </nav>

      <SearchModal
        isOpen={searchModalOpen}
        onClose={() => setSearchModalOpen(false)}
      />
    </>
  );
};

export default Navbar;
