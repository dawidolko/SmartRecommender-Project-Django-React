import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AiOutlineHeart, AiFillHeart } from "react-icons/ai";
import { useFavorites } from "../FavoritesContent/FavoritesContext";
import { CartContext } from "../ShopContext/ShopContext";
import { toast } from "react-toastify";
import config from "../../config/config";

const ProductSliderItem = ({
  id,
  photos,
  name,
  price,
  old_price,
  categories,
}) => {
  const { addToFavorites, removeFromFavorites, isFavorite } = useFavorites();
  const { items, addToCart } = useContext(CartContext);
  const favorite = isFavorite(id);
  const itemsInfo = items ? items[id] : 0;

  const navigate = useNavigate();

  const handleBoxClick = () => {
    navigate(`/product/${id}`);
  };

  const toggleFavorite = (e) => {
    e.stopPropagation();
    if (favorite) {
      removeFromFavorites(id);
      toast.success("Removed from Favorites", {
        position: "top-center",
        autoClose: 3000,
        theme: "colored",
      });
    } else {
      addToFavorites({
        id,
        img: photos?.[0]?.path
          ? `${config.apiUrl}/media/${photos[0].path}`
          : "https://via.placeholder.com/150",
        name,
        price,
      });
      toast.success("Added to Favorites", {
        position: "top-center",
        autoClose: 3000,
        theme: "colored",
      });
    }
  };

  const handleAddToCart = (e) => {
    e.stopPropagation();
    addToCart(id);
    toast.success("Added to Cart", {
      position: "top-center",
      autoClose: 3000,
      theme: "colored",
    });
  };

  const imageUrl = photos?.[0]?.path
    ? `${config.apiUrl}/media/${photos[0].path}`
    : "https://via.placeholder.com/150";

  return (
    <div className="sliderItem" onClick={handleBoxClick}>
      <div className="sliderItem__image-container">
        <img
          src={imageUrl}
          alt={name}
          className="sliderItem__img"
          onClick={(e) => e.stopPropagation()}
        />
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

      <div className="sliderItem__content">
        <h3 className="sliderItem__name">{name}</h3>
        <div className="sliderItem__prices">
          {old_price && (
            <p className="sliderItem__price--discounted">
              ${parseFloat(old_price).toFixed(2)}
            </p>
          )}
          <p className="sliderItem__price">${parseFloat(price).toFixed(2)}</p>
        </div>
        <button className="sliderItem__btn" onClick={handleAddToCart}>
          ADD TO CART {itemsInfo > 0 && <span>({itemsInfo})</span>}
        </button>
      </div>
    </div>
  );
};

export default ProductSliderItem;
