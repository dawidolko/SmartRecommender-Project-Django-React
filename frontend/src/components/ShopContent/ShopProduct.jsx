import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { CartContext } from "../ShopContext/ShopContext";
import { useFavorites } from "../FavoritesContent/FavoritesContext";
import { AiOutlineHeart, AiFillHeart, AiOutlineSearch } from "react-icons/ai";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const ShopProduct = (props) => {
  const { id, imgs, name, price, old_price, category } = props;
  const { items, addToCart } = useContext(CartContext);
  const { addToFavorites, removeFromFavorites, isFavorite } = useFavorites();
  const itemsInfo = items ? items[id] : 0;

  const [favorite, setFavorite] = useState(isFavorite(id));
  const [isImageEnlarged, setIsImageEnlarged] = useState(false);

  const navigate = useNavigate();

  const handleBoxClick = () => {
    if (!isImageEnlarged) {
      navigate(`/product/${id}`);
    }
  };

  const handleFavoriteToggle = (e) => {
    e.stopPropagation();
    if (favorite) {
      removeFromFavorites(id);
      toast.success("Removed from Favorites", {
        position: "top-center",
        autoClose: 3000,
        theme: "colored",
      });
    } else {
      addToFavorites({ id, img: imgs[0], name, price });
      toast.success("Added to Favorites", {
        position: "top-center",
        autoClose: 3000,
        theme: "colored",
      });
    }
    setFavorite(!favorite);
  };

  const handleImageEnlarge = (e) => {
    e.stopPropagation();
    setIsImageEnlarged(true);
  };

  const closeImageOverlay = (e) => {
    e.stopPropagation();
    setIsImageEnlarged(false);
  };

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      closeImageOverlay(e);
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

  const handleNameClick = (e) => {
    e.stopPropagation();
    if (!isImageEnlarged) {
      navigate(`/product/${id}`);
    }
  };

  return (
    <>
      <div className="shop__product" key={id} onClick={handleBoxClick}>
        <div className="shop__image" onClick={(e) => e.stopPropagation()}>
          <img
            className="shop__img"
            src={imgs[0]}
            alt={name}
            onClick={handleImageEnlarge}
          />
          <button
            className="shop__favorite-btn"
            onClick={handleFavoriteToggle}
            aria-label={
              favorite ? "Remove from Favorites" : "Add to Favorites"
            }>
            {favorite ? (
              <AiFillHeart className="shop__favorite-icon shop__favorite-icon--active" />
            ) : (
              <AiOutlineHeart className="shop__favorite-icon" />
            )}
          </button>
          <button
            className="shop__image-enlarge-btn"
            onClick={handleImageEnlarge}
            aria-label="Enlarge Image">
            <AiOutlineSearch className="shop__image-enlarge-icon" />
          </button>
        </div>

        <div className="shop__content" onClick={(e) => e.stopPropagation()}>
          <p className="shop__category__main">{`CATEGORY: ${category
            .replace(".", " > ")
            .toUpperCase()}`}</p>

          <p className="shop__name" onClick={handleNameClick}>
            {name}
          </p>

          <div className="shop__prices">
            {old_price && (
              <p className="shop__price--discounted">
                ${parseFloat(old_price).toFixed(2)}
              </p>
            )}
            <p className="shop__price">${parseFloat(price).toFixed(2)}</p>
          </div>

          <button className="shop__btn" onClick={handleAddToCart}>
            Add To Cart {itemsInfo > 0 && <span>( {itemsInfo} )</span>}
          </button>
        </div>
      </div>

      {isImageEnlarged && (
        <div className="common-shop-image-overlay" onClick={handleOverlayClick}>
          <div className="common-shop-image-overlay__content">
            <button
              className="common-shop-image-overlay__close"
              onClick={closeImageOverlay}
              aria-label="Close Image">
              ×
            </button>
            <img
              className="common-shop-image-overlay__image"
              src={imgs[0]}
              alt={name}
            />
          </div>
        </div>
      )}
    </>
  );
};

export default ShopProduct;
