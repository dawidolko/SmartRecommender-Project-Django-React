import React from "react";

const FavoritesProduct = ({ product, onMoveToCart }) => {
  const { id, photos, name } = product;
  const imageUrl = photos?.[0]?.path
    ? `http://localhost:8000/media/${photos[0].path}`
    : "https://via.placeholder.com/150";

  return (
    <tr className="favorites__tr" key={id}>
      <td>
        <img className="favorites__img" src={imageUrl} alt={name} />
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
