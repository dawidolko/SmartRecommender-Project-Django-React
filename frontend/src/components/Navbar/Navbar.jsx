import "./Navbar.scss";
import { Link, NavLink } from "react-router-dom";
import { useEffect, useState, useContext } from "react";
import { GiHamburgerMenu } from "react-icons/gi";
import { AiOutlineClose, AiOutlineHeart } from "react-icons/ai";
import { FaShoppingCart, FaUserCircle } from "react-icons/fa";
import { CartContext } from "../ShopContext/ShopContext";
import { useFavorites } from "../FavoritesContent/FavoritesContext";

const Navbar = ({ categories = [] }) => {
  const { totalCartItems } = useContext(CartContext);
  const { favorites } = useFavorites();

  const [isOpen, setIsOpen] = useState(false);
  const [navBgc, setNavBgc] = useState(false);
  const [showCategories, setShowCategories] = useState(false);
  const [searchInput, setSearchInput] = useState("");
  const [loggedUser, setLoggedUser] = useState(null);
  const [showUserDropdown, setShowUserDropdown] = useState(false);

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

  const handleUserIconClick = () => {
    if (loggedUser) {
      setShowUserDropdown(!showUserDropdown);
    } else {
      window.location.href = "/login";
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("loggedUser");
    setLoggedUser(null);
    setShowUserDropdown(false);
    window.location.href = "/";
  };

  const handleCategoryHover = () => setShowCategories(true);
  const handleCategoryLeave = () => setShowCategories(false);

  return (
    <nav className={navBgc ? "navbar navbar__bgc" : "navbar"}>
      <div className="navbar__container container">
        <Link to="/" className="navbar__logo">
          <p className="navbar__logo-text"></p>
        </Link>

        {/* Pasek wyszukiwania */}
        <div className="navbar__search">
          <input
            type="text"
            placeholder="Search products..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
          />
          <button className="navbar__search-button">Search</button>
        </div>

        {/* Nawigacja */}
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

          {/* Kategorie */}
          <li
            className="navbar__categories"
            onMouseEnter={handleCategoryHover}
            onMouseLeave={handleCategoryLeave}>
            <span className="navbar__link">CATEGORIES</span>
            {showCategories && (
              <div className="navbar__dropdown">
                {categories.map((category, index) => (
                  <Link
                    key={index}
                    to={`/shop/${category}`}
                    className="navbar__dropdown-item"
                    onClick={closeNav}>
                    {category}
                  </Link>
                ))}
              </div>
            )}
          </li>

          {/* Ikony */}
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
            <NavLink
              className="navbar__cart-link"
              to="/cart"
              onClick={closeNav}>
              <div className="navbar__cart">
                <span className="navbar__quantity">{totalCartItems()}</span>
                <FaShoppingCart className="navbar__basket" />
              </div>
            </NavLink>

            {/* Ikona ludzika */}
            <div
              className="navbar__user"
              onClick={() => {
                closeNav();
                handleUserIconClick();
              }}>
              <FaUserCircle className="navbar__user-icon" />
              {loggedUser && showUserDropdown && (
                <div className="navbar__user-dropdown">
                  <button onClick={handleLogout} className="navbar__logoutBtn">
                    Log out
                  </button>
                </div>
              )}
            </div>
          </li>
        </ul>

        {/* Ikona hamburgera */}
        <div className="navbar__hamburger" onClick={handleClick}>
          {isOpen ? <AiOutlineClose /> : <GiHamburgerMenu />}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
