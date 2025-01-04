import React from "react";

const FavoritesProduct = ({ product, onMoveToCart }) => {
  const { id, img, name } = product;

  return (
    <tr className="favorites__tr" key={id}>
      <td>
        <img className="favorites__img" src={img} alt={name} />
      </td>
      <td>{name}</td>
      <td>
        <button
          className="favorites__action-btn"
          onClick={() => onMoveToCart(id)}>
          Move to Cart
        </button>
      </td>
    </tr>
  );
};

export default FavoritesProduct;
