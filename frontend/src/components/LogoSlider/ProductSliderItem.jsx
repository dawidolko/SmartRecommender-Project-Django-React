import React from "react";
import { useNavigate } from "react-router-dom";
import { AiOutlineHeart, AiFillHeart } from "react-icons/ai";
import { useFavorites } from "../FavoritesContent/FavoritesContext";

const ProductSliderItem = ({ id, imgs, name, price }) => {
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
        img: imgs?.[0],
        name,
        price,
      });
    }
  };

  return (
    <div className="sliderItem" onClick={handleBoxClick}>
      <img
        src={imgs && imgs[0]}
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
