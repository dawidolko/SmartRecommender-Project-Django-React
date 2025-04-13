import React, { useContext } from "react";
import { CartContext } from "../ShopContext/ShopContext";
import { AiOutlinePlus, AiOutlineMinus, AiOutlineClose } from "react-icons/ai";
import config from "../../config/config";
import { Link } from "react-router-dom";

const CartProduct = ({ id, name, price, photos, removeItemFromCart }) => {
  const { items, addToCart, removeFromCart } = useContext(CartContext);

  const img = photos?.[0]?.path
    ? `${config.apiUrl}/media/${photos[0].path}`
    : "https://via.placeholder.com/150";

  const itemQuantity = items[id];
  const totalProductAmount = price * itemQuantity;

  const handleRemoveItem = () => {
    for (let i = 0; i < itemQuantity; i++) {
      removeFromCart(id);
    }
  };

  return (
    <tr className="cart__tr" key={id}>
      <td
        style={{
          display: "flex",
          justifyContent: "center",
          paddingBottom: "50px",
        }}>
        <img className="cart__img" src={img} alt={name} />
      </td>
      <td style={{ textAlign: "center" }} className="cart__name">
        <Link to={`/product/${id}`} className="cart__product-name">
          {name}
        </Link>
      </td>
      <td
        className="cart__action"
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          paddingBottom: "50px",
        }}>
        <button
          className="cart__action-btn"
          onClick={() => removeFromCart(id)}
          aria-label={`Decrease quantity of ${name}`}
          style={{ margin: "0 5px" }}>
          <AiOutlineMinus className="cart__action-icon" />
        </button>
        <span className="cart__action-quantity" style={{ margin: "0 10px" }}>
          {itemQuantity}
        </span>
        <button
          className="cart__action-btn"
          onClick={() => addToCart(id)}
          aria-label={`Increase quantity of ${name}`}
          style={{ margin: "0 5px" }}>
          <AiOutlinePlus className="cart__action-icon" />
        </button>
      </td>
      <td style={{ textAlign: "center" }} className="cart__total">
        ${totalProductAmount ? totalProductAmount.toFixed(2) : "0.00"}
      </td>
      <td style={{ textAlign: "center" }} className="cart__remove">
        <button className="cart__remove-btn" onClick={handleRemoveItem}>
          <AiOutlineClose />
        </button>
      </td>
    </tr>
  );
};

export default CartProduct;
