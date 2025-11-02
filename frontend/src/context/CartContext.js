import { createContext, useState, useEffect } from "react";

/**
 * CartContext - Shopping cart state management
 *
 * Provides global shopping cart state using React Context API.
 * Manages cart items with localStorage persistence.
 *
 * Features:
 *   - Cart persistence across sessions (localStorage)
 *   - Add/remove products
 *   - Quantity management
 *   - Automatic cart loading on mount
 *
 * Context Values:
 *   - cart: Array of cart items [{id, name, price, quantity, photos}, ...]
 *   - fetchCart(): Load cart from localStorage
 *   - updateCart(newCart): Update cart state and persist to localStorage
 *   - addToCart(product): Add product or increment quantity
 *   - removeFromCart(itemId): Remove item from cart
 *
 * Cart Item Structure:
 *   {
 *     id: number,
 *     name: string,
 *     price: number,
 *     quantity: number,
 *     photos: array,
 *     ...other product fields
 *   }
 *
 * @context
 */
export const CartContext = createContext();

/**
 * CartProvider Component
 *
 * Wraps application with shopping cart context provider.
 * Automatically loads cart from localStorage on mount.
 *
 * @component
 * @param {Object} props
 * @param {React.ReactNode} props.children - Child components
 * @returns {React.ReactElement} Context provider with cart state
 */
export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState([]);

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = () => {
    const storedCart = localStorage.getItem("cart");
    if (storedCart) {
      setCart(JSON.parse(storedCart));
    }
  };

  const updateCart = (newCart) => {
    setCart(newCart);
    localStorage.setItem("cart", JSON.stringify(newCart));
  };

  const addToCart = (product) => {
    const existingItem = cart.find((item) => item.id === product.id);

    if (existingItem) {
      const updatedCart = cart.map((item) =>
        item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
      );
      updateCart(updatedCart);
    } else {
      updateCart([...cart, { ...product, quantity: 1 }]);
    }
  };

  const removeFromCart = (itemId) => {
    const updatedCart = cart.filter((item) => item.id !== itemId);
    updateCart(updatedCart);
  };

  return (
    <CartContext.Provider
      value={{ cart, fetchCart, updateCart, addToCart, removeFromCart }}>
      {children}
    </CartContext.Provider>
  );
};
