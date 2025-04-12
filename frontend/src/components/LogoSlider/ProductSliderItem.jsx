import React from "react";
import { useNavigate } from "react-router-dom";
import { AiOutlineHeart, AiFillHeart } from "react-icons/ai";
import { useFavorites } from "../FavoritesContent/FavoritesContext";

const ProductSliderItem = ({ id, photos, name, price }) => {
  const { addToFavorites, removeFromFavorites, isFavorite } = useFavorites();
  const favorite = isFavorite(id);

  const navigate = useNavigate();

  const handleBoxClick = () => {
    navigate(`/product/${id}`);
  };

  const toggleFavorite = (e) => {
    e.stopPropagation();
    if (favorite) {
      removeFromFavorites(id);
    } else {
      addToFavorites({
        id,
        img: photos?.[0]?.path
          ? `http://localhost:8000/media/${photos[0].path}`
          : "https://via.placeholder.com/150",
        name,
        price,
      });
    }
  };

  const imageUrl = photos?.[0]?.path
    ? `http://localhost:8000/media/${photos[0].path}`
    : "https://via.placeholder.com/150";

  return (
    <div className="sliderItem" onClick={handleBoxClick}>
      <img
        src={imageUrl}
        alt={name}
        className="sliderItem__img"
        onClick={(e) => e.stopPropagation()}
      />
      <h3 className="sliderItem__name">{name}</h3>
      <p className="sliderItem__price">${price}</p>

      <button
        className="sliderItem__btn-fav"
        onClick={toggleFavorite}
        aria-label="Toggle Favorite">
        {favorite ? (
          <AiFillHeart style={{ color: "red", fontSize: "1.8rem" }} />
        ) : (
          <AiOutlineHeart style={{ fontSize: "1.8rem" }} />
        )}
      </button>
    </div>
  );
};

export default ProductSliderItem;
