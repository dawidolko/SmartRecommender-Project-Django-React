import React, { useState, useEffect } from "react";
import axios from "axios";
import "./CartPreview.scss";
import { AiOutlineClose } from "react-icons/ai";

const BASE_URL = "http://127.0.0.1:8000";

const CartPreview = () => {
  const [cart, setCart] = useState([]);
  const [showCart, setShowCart] = useState(false);
  const [products, setProducts] = useState({});

  useEffect(() => {
    const storedCart = JSON.parse(localStorage.getItem("cart")) || {};
    const formattedCart = Object.entries(storedCart).map(([productId, quantity]) => ({
      id: productId,
      quantity: quantity,
    }));
    setCart(formattedCart);
  }, []);

  useEffect(() => {
    if (cart.length === 0) return;

    const fetchProducts = async () => {
      try {
        const productIds = cart.map((item) => item.id).join(",");
        const response = await axios.get(`${BASE_URL}/api/products/?ids=${productIds}`);

        const productMap = {};
        response.data.forEach((product) => {
          productMap[product.id] = {
            ...product,
            image: product.photos?.[0]?.path
              ? `${BASE_URL}/media/${product.photos[0].path}`
              : "https://via.placeholder.com/150", // If product has no photos display placeholder
          };
        });

        setProducts(productMap);
      } catch (error) {
        console.error("Error with loading products:", error);
      }
    };

    fetchProducts();
  }, [cart]);

  const changeQuantity = (itemId, action) => {
    setCart((prevCart) => {
        const updatedCart = prevCart.map((item) =>
            item.id === itemId
                ? { ...item, quantity: action === "increase" ? item.quantity + 1 : Math.max(item.quantity - 1, 1) }
                : item
        );

        const storedCart = JSON.parse(localStorage.getItem("cart")) || {};
        updatedCart.forEach((item) => {
            storedCart[item.id] = item.quantity;
        });
        localStorage.setItem("cart", JSON.stringify(storedCart));

        return updatedCart;
    });
};

  const removeItem = (itemId) => {
    const storedCart = JSON.parse(localStorage.getItem("cart")) || {};
    delete storedCart[itemId];

    localStorage.setItem("cart", JSON.stringify(storedCart));

    setCart((prevCart) => prevCart.filter((item) => item.id !== itemId));
};


  return (
    <div className="cart-preview" onMouseEnter={() => setShowCart(true)} onMouseLeave={() => setShowCart(false)}>
      <div className="cart-icon">
        🛒 <span className="cart-count">{cart.reduce((acc, item) => acc + item.quantity, 0)}</span>
      </div>

      {showCart && (
        <div className="cart-dropdown">
          <h4>Cart ({cart.length})</h4>
          {cart.length > 0 ? (
            cart.map((item) => {
              const product = products[item.id];

              return product ? (
                <div key={item.id} className="cart-item">
                  <img src={product.image} alt={product.name} className="cart-item__img" />
                  <div className="cart-item__details">
                    <p>{product.name}</p>
                    <span>{product.price} $</span>
                    <div className="cart-item__actions">
                      <button onClick={() => changeQuantity(item.id, "decrease")}>-</button>
                      <span>{item.quantity}</span>
                      <button onClick={() => changeQuantity(item.id, "increase")}>+</button>
                    </div>
                  </div>
                  <AiOutlineClose className="cart-item__remove" onClick={() => removeItem(item.id)} />
                </div>
              ) : (
                <p key={item.id}>Loading...</p>
              );
            })
          ) : (
            <p>Cart is empty</p>
          )}
          <a href="/cart" className="cart-btn">Go To Cart</a>
        </div>
      )}
    </div>
  );
};

export default CartPreview;
