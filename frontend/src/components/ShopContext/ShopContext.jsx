import { createContext, useEffect, useState } from "react";
import axios from "axios";

export const CartContext = createContext(null);

const getStoredCart = () => {
  const storedCart = localStorage.getItem("cart");
  return storedCart ? JSON.parse(storedCart) : {};
};

const ShopContext = (props) => {
  const [items, setItems] = useState(getStoredCart());
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/products/");
        setProducts(response.data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };

    fetchProducts();
  }, []);

  useEffect(() => {
    localStorage.setItem("cart", JSON.stringify(items));
  }, [items]);

  const addToCart = (itemId) => {
    setItems((prev) => ({ ...prev, [itemId]: (prev[itemId] || 0) + 1 }));
  };

  const removeFromCart = (itemId) => {
    setItems((prev) => ({
      ...prev,
      [itemId]: Math.max((prev[itemId] || 0) - 1, 0),
    }));
  };

  const totalAmount = () => {
    return Object.entries(items).reduce((total, [itemId, quantity]) => {
      const product = products.find((product) => product.id === Number(itemId));
      return product ? total + product.price * quantity : total;
    }, 0);
  };

  const totalCartItems = () => {
    return Object.values(items).reduce((sum, quantity) => sum + quantity, 0);
  };

  const singleProductAmount = (itemId) => {
    const product = products.find((product) => product.id === Number(itemId));
    return product ? items[itemId] * product.price : 0;
  };

  const resetCart = () => {
    setItems({});
  };

  const contextValue = {
    items,
    addToCart,
    removeFromCart,
    totalAmount,
    totalCartItems,
    singleProductAmount,
    resetCart,
  };

  return (
    <CartContext.Provider value={contextValue}>
      {props.children}
    </CartContext.Provider>
  );
};

export default ShopContext;
