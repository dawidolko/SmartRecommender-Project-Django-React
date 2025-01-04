import "./Navbar.scss";
import { Link, NavLink } from "react-router-dom";
import { useEffect, useState, useContext } from "react";
import { GiHamburgerMenu } from "react-icons/gi";
import {
  AiOutlineClose,
  AiOutlineHeart,
  AiOutlineSearch,
} from "react-icons/ai";
import { FaShoppingCart, FaUserCircle } from "react-icons/fa";
import { CartContext } from "../ShopContext/ShopContext";
import { useFavorites } from "../FavoritesContent/FavoritesContext";
import accountData from "../panelLogin/AccountData";

const Navbar = ({ categories = [] }) => {
  const { totalCartItems } = useContext(CartContext);
  const { favorites } = useFavorites();

  const [isOpen, setIsOpen] = useState(false);
  const [navBgc, setNavBgc] = useState(false);
  const [searchInput, setSearchInput] = useState("");
  const [showSearch, setShowSearch] = useState(false);
  const [loggedUser, setLoggedUser] = useState(null);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const [showCartDropdown, setShowCartDropdown] = useState(false);

  useEffect(() => {
    const savedUser = localStorage.getItem("loggedUser");
    if (savedUser) {
      setLoggedUser(JSON.parse(savedUser));
    }
  }, []);

  useEffect(() => {
    const changeBgc = () => {
      setNavBgc(window.scrollY > 10);
    };
    window.addEventListener("scroll", changeBgc);
    return () => {
      window.removeEventListener("scroll", changeBgc);
    };
  }, []);

  const handleClick = () => setIsOpen(!isOpen);
  const closeNav = () => setIsOpen(false);

  const handleUserIconHover = () => {
    setShowUserDropdown(true);
  };

  const handleUserIconLeave = () => {
    setShowUserDropdown(false);
  };

  const handleCartHover = () => {
    setShowCartDropdown(true);
  };

  const handleCartLeave = () => {
    setShowCartDropdown(false);
  };

  const toggleSearch = () => setShowSearch(!showSearch);

  const handleLogout = () => {
    localStorage.removeItem("loggedUser");
    setLoggedUser(null);
    setShowUserDropdown(false);
    window.location.href = "/";
  };

  const getUserRedirect = () => {
    if (loggedUser) {
      const user = accountData.find((user) => user.email === loggedUser.email);
      if (user) {
        return user.role === "Admin" ? "/admin" : "/client";
      }
    }
    return "/login";
  };

  return (
    <nav className={navBgc ? "navbar navbar__bgc" : "navbar"}>
      <div className="navbar__container container">
        <div className="navbar__search-wrapper">
          <button className="navbar__search-icon" onClick={toggleSearch}>
            <AiOutlineSearch />
          </button>
          {showSearch && (
            <div className="navbar__search">
              <input
                type="text"
                placeholder="Search products..."
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
              />
              <button className="navbar__search-button">Search</button>
            </div>
          )}
        </div>
        <Link to="/" className="navbar__logo">
          <p className="navbar__logo-text"></p>
        </Link>

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
            <NavLink className="navbar__link" to="/about" onClick={closeNav}>
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
            <NavLink
              className="navbar__link"
              to="/categories"
              onClick={closeNav}>
              CATEGORIES
            </NavLink>
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

            <div
              className="navbar__cart"
              onMouseEnter={handleCartHover}
              onMouseLeave={handleCartLeave}
              onClick={() => (window.location.href = "/cart")}
              style={{ cursor: "pointer" }}>
              <span className="navbar__quantity">{totalCartItems()}</span>
              <FaShoppingCart className="navbar__basket" />
              {showCartDropdown && (
                <div className="navbar__cart-dropdown">
                  {totalCartItems() === 0 ? (
                    <p>Your cart is empty.</p>
                  ) : (
                    <p>You have {totalCartItems()} items in your cart.</p>
                  )}
                  <Link to="/cart" className="navbar__cart-button">
                    Go to cart
                  </Link>
                </div>
              )}
            </div>

            <div
              className="navbar__user"
              onMouseEnter={handleUserIconHover}
              onMouseLeave={handleUserIconLeave}
              onClick={() => (window.location.href = getUserRedirect())}
              style={{ cursor: "pointer" }}>
              <FaUserCircle className="navbar__user-icon" />
              {showUserDropdown && (
                <div className="navbar__user-dropdown">
                  <Link to="/account" className="navbar__dropdown-link">
                    Your Account
                  </Link>
                  <Link to="/orders" className="navbar__dropdown-link">
                    Orders
                  </Link>
                  <Link to="/settings" className="navbar__dropdown-link">
                    Settings
                  </Link>
                  <button onClick={handleLogout} className="navbar__logoutBtn">
                    Logout
                  </button>
                </div>
              )}
            </div>
          </li>
        </ul>

        <div className="navbar__hamburger" onClick={handleClick}>
          {isOpen ? <AiOutlineClose /> : <GiHamburgerMenu />}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
