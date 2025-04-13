import React from "react";
import config from "../../config/config";
import { Link } from "react-router-dom";
import { AiOutlineClose } from "react-icons/ai";

const FavoritesProduct = ({ product, onMoveToCart, onRemoveFromFavorites }) => {
  const { id, photos, name } = product;
  const imageUrl = photos?.[0]?.path
    ? `${config.apiUrl}/media/${photos[0].path}`
    : "https://via.placeholder.com/150";

  return (
    <tr className="favorites__tr" key={id}>
      <td
        className="favorites__td"
        style={{ display: "flex", justifyContent: "center" }}>
        <img className="favorites__img" src={imageUrl} alt={name} />
      </td>
      <td className="favorites__td">
        <Link to={`/product/${id}`} className="favorites__product-name">
          {name}
        </Link>
      </td>
      <td className="favorites__td">
        <button
          className="favorites__action-btn"
          onClick={() => onMoveToCart(id)}>
          Move to Cart
        </button>
        <button
          className="favorites__remove-btn"
          onClick={() => onRemoveFromFavorites(id)}>
          <AiOutlineClose />
        </button>
      </td>
    </tr>
  );
};

export default FavoritesProduct;
