import "./Navbar.scss";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useEffect, useState, useContext } from "react";
import { GiHamburgerMenu } from "react-icons/gi";
import { AiOutlineClose, AiOutlineHeart } from "react-icons/ai";
import { FaUserCircle } from "react-icons/fa";
import { CartContext } from "../ShopContext/ShopContext";
import { useFavorites } from "../FavoritesContent/FavoritesContext";
import CartPreview from "../CartContent/CartPreview";
import axios from "axios";

const Navbar = () => {
  useContext(CartContext);
  const { favorites } = useFavorites();
  const navigate = useNavigate();

  const [isOpen, setIsOpen] = useState(false);
  const [navBgc, setNavBgc] = useState(false);
  const [searchInput, setSearchInput] = useState("");
  useState(false);
  const [loggedUser, setLoggedUser] = useState(null);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const [categories, setCategories] = useState([]);

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

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/categories/")
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

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      navigate(`/search/${searchInput}`);
      setSearchInput("");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("loggedUser");
    setLoggedUser(null);
    setShowUserDropdown(false);
    window.location.href = "/login";
  };

  // Ustal prefiks panelu w zależności od roli
  const panelPrefix =
    loggedUser && loggedUser.role === "admin" ? "/admin" : "/client";

  const getUserRedirect = () => {
    if (loggedUser) {
      return panelPrefix;
    }
    return "/login";
  };

  return (
    <nav className={navBgc ? "navbar navbar__bgc" : "navbar"}>
      <div className="navbar__container container">
        <Link to="/" className="navbar__logo">
          <p className="navbar__logo-text"></p>
        </Link>
        <div className="navbar__search-wrapper">
          <form className="search-bar" onSubmit={handleSearchSubmit}>
            <input
              type="search"
              name="search"
              placeholder="Search products..."
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              required
            />
            <button className="search-btn" type="submit">
              <span>Search</span>
            </button>
          </form>
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
          <li
            className="navbar__categories"
            onMouseEnter={() => setIsOpen(true)}
            onMouseLeave={() => setIsOpen(false)}>
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
                  <p className="navbar__main-category-name">
                    {mainCategory.toUpperCase()}
                  </p>
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
                </div>
              ))}
            </div>
          </li>
          {/* User Icon i dropdown */}
          <li className="navbar__icons">
            <div
              className="navbar__user"
              onMouseEnter={handleUserIconHover}
              onMouseLeave={handleUserIconLeave}
              style={{ cursor: "pointer" }}>
              <FaUserCircle
                className="navbar__user-icon"
                onClick={() => (window.location.href = getUserRedirect())}
              />
              {showUserDropdown && (
                <div className="navbar__user-dropdown">
                  {loggedUser ? (
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
                      <Link to={panelPrefix} className="navbar__dropdown-link">
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
    </nav>
  );
};

export default Navbar;
