import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import "./CartPreview.scss";
import { AiOutlineClose, AiOutlineShopping } from "react-icons/ai";
import { Link } from "react-router-dom";
import config from "../../config/config";
import { CartContext } from "../ShopContext/ShopContext";

const BASE_URL = `${config.apiUrl}`;

const CartPreview = () => {
  const { items, totalCartItems } = useContext(CartContext);
  const [showCart, setShowCart] = useState(false);
  const [products, setProducts] = useState({});

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
  }, [items]);

  const changeQuantity = (itemId, action) => {
    if (action === "increase") {
      items[itemId] = (items[itemId] || 0) + 1;
    } else if (action === "decrease") {
      if (items[itemId] === 1) {
        removeItem(itemId);
      } else {
        items[itemId] -= 1;
      }
    }
  };

  const removeItem = (itemId) => {
    delete items[itemId];
  };

  return (
    <div
      className="cart-preview"
      onMouseEnter={() => setShowCart(true)}
      onMouseLeave={() => setShowCart(false)}>
      <div className="cart-icon">
        <AiOutlineShopping />
        <span className="cart-count">{totalCartItems()}</span>
      </div>
      {showCart && (
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
                      <Link
                        to={`/product/${product.id}`}
                        className="cart-item__name">
                        <p>{product.name}</p>
                      </Link>
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
