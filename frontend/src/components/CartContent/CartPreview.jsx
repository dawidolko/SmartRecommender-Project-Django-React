import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import "./CartPreview.scss";
import { AiOutlineClose, AiOutlineShopping } from "react-icons/ai";
import { Link, useNavigate } from "react-router-dom";
import config from "../../config/config";
import { CartContext } from "../ShopContext/ShopContext";

const BASE_URL = `${config.apiUrl}`;

const CartPreview = () => {
  const { items, totalCartItems, addToCart, removeFromCart } =
    useContext(CartContext);
  const [showCart, setShowCart] = useState(false);
  const [products, setProducts] = useState({});
  const [isMobile, setIsMobile] = useState(window.innerWidth < 640);
  const navigate = useNavigate();

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 640);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  useEffect(() => {
    if (totalCartItems() === 0) return;

    const fetchProducts = async () => {
      try {
        const productIds = Object.keys(items).join(",");
        const response = await axios.get(
          `${BASE_URL}/api/products/?ids=${productIds}`
        );
        const productMap = {};
        response.data.forEach((product) => {
          productMap[product.id] = {
            ...product,
            image: product.photos?.[0]?.path
              ? `${BASE_URL}/media/${product.photos[0].path}`
              : "https://via.placeholder.com/150",
          };
        });
        setProducts(productMap);
      } catch (error) {
        console.error("Error with loading products:", error);
      }
    };

    fetchProducts();
  }, [items, totalCartItems]);

  const changeQuantity = (itemId, action) => {
    if (action === "increase") {
      addToCart(itemId);
    } else if (action === "decrease") {
      removeFromCart(itemId);
    }
  };

  const removeItem = (itemId) => {
    const quantity = items[itemId] || 0;
    for (let i = 0; i < quantity; i++) {
      removeFromCart(itemId);
    }
  };

  const handleCartClick = () => {
    if (isMobile) {
      navigate("/cart");
    }
  };

  const handleMouseEnter = () => {
    if (!isMobile) {
      setShowCart(true);
    }
  };

  const handleMouseLeave = () => {
    if (!isMobile) {
      setShowCart(false);
    }
  };

  return (
    <div
      className="cart-preview"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={handleCartClick}>
      <div className="cart-icon">
        <AiOutlineShopping />
        <span className="cart-count">{totalCartItems()}</span>
      </div>
      {!isMobile && showCart && (
        <div className="cart-dropdown">
          <h4>Cart ({totalCartItems()})</h4>
          {totalCartItems() > 0 ? (
            Object.entries(items).map(([itemId, quantity]) => {
              if (quantity > 0) {
                const product = products[itemId];
                return product ? (
                  <div key={itemId} className="cart-item">
                    <img
                      src={product.image}
                      alt={product.name}
                      className="cart-item__img"
                    />
                    <div className="cart-item__details">
                      <p className="cart-item__name">{product.name}</p>
                      <span>{product.price} $</span>
                      <div className="cart-item__actions">
                        <button
                          onClick={() => changeQuantity(itemId, "decrease")}>
                          -
                        </button>
                        <span>{quantity}</span>
                        <button
                          onClick={() => changeQuantity(itemId, "increase")}>
                          +
                        </button>
                      </div>
                    </div>
                    <AiOutlineClose
                      className="cart-item__remove"
                      onClick={() => removeItem(itemId)}
                    />
                  </div>
                ) : (
                  <div key={itemId} className="loading-spinner"></div>
                );
              }
              return null;
            })
          ) : (
            <p>Cart is empty</p>
          )}
          <Link to="/cart" className="cart-btn">
            Go To Cart
          </Link>
        </div>
      )}
    </div>
  );
};

export default CartPreview;
