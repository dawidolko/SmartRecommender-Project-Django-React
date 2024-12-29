import React, { useContext } from "react";
import { CartContext } from "../ShopContext/ShopContext";
import { AiOutlinePlus, AiOutlineMinus } from "react-icons/ai";

const CartProduct = ({ id, img, name, price }) => {
  const { items, addToCart, removeFromCart, singleProductAmount } =
    useContext(CartContext);
  const itemQuantity = items[id];
  const totalProductAmount = singleProductAmount(id);

  return (
    <tr className="cart__tr" key={id}>
      <td>
        <img className="cart__img" src={img} alt={name} />
      </td>
      <td className="cart__name">{name}</td>
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
        $
        {typeof totalProductAmount === "number"
          ? totalProductAmount.toFixed(2)
          : "0.00"}
      </td>
    </tr>
  );
};

export default CartProduct;
