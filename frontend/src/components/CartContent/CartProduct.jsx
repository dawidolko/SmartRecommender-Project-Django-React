import React, { useContext } from "react";
import { CartContext } from "../ShopContext/ShopContext";
import { AiOutlinePlus, AiOutlineMinus } from "react-icons/ai";
import shopData from "../ShopContent/ShopData"; // Importujemy dane z shopData

const CartProduct = ({ id, name, price }) => {
  const { items, addToCart, removeFromCart, singleProductAmount } =
    useContext(CartContext);

  // Znajdź produkt po id z shopData
  const product = shopData.find((product) => product.id === id);
  const img = product ? product.imgs[0] : ""; // Pobierz zdjęcie z imgs[0]
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
