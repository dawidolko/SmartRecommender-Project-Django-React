import React, { useContext } from "react";
import { CartContext } from "../ShopContext/ShopContext";
import { AiOutlinePlus, AiOutlineMinus, AiOutlineClose } from "react-icons/ai";
import config from "../../config/config";
import { Link } from "react-router-dom";
import { PLACEHOLDER_IMAGE } from "../../utils/mockData";

const CartProduct = ({ id, name, price, photos, removeItemFromCart }) => {
  const { items, addToCart, removeFromCart } = useContext(CartContext);

  const img = config.useMockData
    ? PLACEHOLDER_IMAGE
    : photos?.[0]?.path
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
      <td className="cart__img-cell">
        <img className="cart__img" src={img} alt={name} />
      </td>
      <td className="cart__name">
        <Link to={`/product/${id}`} className="cart__product-name">
          {name}
        </Link>
      </td>
      <td className="cart__action">
        <button
          className="cart__action-btn"
          onClick={() => removeFromCart(id)}
          aria-label={`Decrease quantity of ${name}`}>
          <AiOutlineMinus className="cart__action-icon" />
        </button>
        <span className="cart__action-quantity">{itemQuantity}</span>
        <button
          className="cart__action-btn"
          onClick={() => addToCart(id)}
          aria-label={`Increase quantity of ${name}`}>
          <AiOutlinePlus className="cart__action-icon" />
        </button>
      </td>
      <td className="cart__total">
        ${totalProductAmount ? totalProductAmount.toFixed(2) : "0.00"}
      </td>
      <td className="cart__remove">
        <button className="cart__remove-btn" onClick={handleRemoveItem}>
          <AiOutlineClose />
        </button>
      </td>
    </tr>
  );
};

export default CartProduct;
