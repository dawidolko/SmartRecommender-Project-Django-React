import "./CartContent.scss";
import { useContext, useEffect, useState } from "react";
import { CartContext } from "../ShopContext/ShopContext";
import CartProduct from "./CartProduct";
import TotalAmount from "./TotalAmount";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import config from "../../config/config";

const CartContent = () => {
  const { items, totalAmount, removeFromCart } = useContext(CartContext);
  const [shopData, setShopData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get(`${config.apiUrl}/api/products/`);
        setShopData(response.data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };
    fetchProducts();
  }, []);

  useEffect(() => {
    localStorage.setItem("cart", JSON.stringify(items));
  }, [items]);

  return (
    <div className="cart container">
      {totalAmount() > 0 ? (
        <div className="cart__container">
          <table className="cart__table">
            <thead className="cart__thead">
              <tr className="cart__row">
                <th style={{ textAlign: "center" }}>Product</th>
                <th style={{ textAlign: "center" }}>Name</th>
                <th style={{ textAlign: "center" }}>Quantity</th>
                <th style={{ textAlign: "center" }}>Total Price</th>
                <th style={{ textAlign: "center" }}>Remove</th>
              </tr>
            </thead>
            <tbody>
              {shopData.map((product) => {
                if (items[product.id] > 0) {
                  return (
                    <CartProduct
                      key={product.id}
                      {...product}
                      removeItemFromCart={removeFromCart}
                    />
                  );
                }
                return null;
              })}
            </tbody>
          </table>
          <TotalAmount />
        </div>
      ) : (
        <div className="cart__empty">
          <h2 className="cart__empty-title">Your cart is empty</h2>
          <button className="cart__empty-btn" onClick={() => navigate("/shop")}>
            Go To Shopping
          </button>
        </div>
      )}
    </div>
  );
};

export default CartContent;
