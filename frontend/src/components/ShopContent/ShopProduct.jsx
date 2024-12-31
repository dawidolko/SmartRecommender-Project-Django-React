import React, { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { CartContext } from "../ShopContext/ShopContext";
import { useFavorites } from "../FavoritesContent/FavoritesContext";
import { AiOutlineHeart, AiFillHeart, AiOutlineSearch } from "react-icons/ai";

const ShopProduct = (props) => {
  const { id, imgs, name, price, category, isNew } = props;
  const { items, addToCart } = useContext(CartContext);
  const { addToFavorites, removeFromFavorites, isFavorite } = useFavorites();
  const itemsInfo = items[id];

  const [favorite, setFavorite] = useState(isFavorite(id));
  const [isImageEnlarged, setIsImageEnlarged] = useState(false);
  const [oldPrice, setOldPrice] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    const difference = Math.floor(Math.random() * 51);
    if (difference > 0) {
      setOldPrice(parseFloat(price) + difference);
    }
  }, [price]);

  const handleBoxClick = () => {
    if (!isImageEnlarged) {
      navigate(`/product/${id}`);
    }
  };

  const handleFavoriteToggle = (e) => {
    e.stopPropagation();
    if (favorite) {
      removeFromFavorites(id);
    } else {
      addToFavorites({ id, img: imgs[0], name, price });
    }
    setFavorite(!favorite);
  };

  const handleImageEnlarge = (e) => {
    e.stopPropagation();
    setIsImageEnlarged(true);
  };

  const closeImageOverlay = () => {
    setIsImageEnlarged(false);
  };

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      closeImageOverlay();
    }
  };

  const handleAddToCart = (e) => {
    e.stopPropagation();
    // Ensure that the same product can only be added once and adjust the quantity
    addToCart(id);
  };

  const handleNameClick = (e) => {
    e.stopPropagation();
    if (!isImageEnlarged) {
      navigate(`/product/${id}`);
    }
  };

  return (
    <div className="shop__product" key={id} onClick={handleBoxClick}>
      <div className="shop__image" onClick={(e) => e.stopPropagation()}>
        {isNew && <span className="shop__label">NEW</span>}
        <img
          className="shop__img"
          src={imgs[0]}
          alt={name}
          onClick={handleImageEnlarge}
        />
        <button
          className="shop__favorite-btn"
          onClick={handleFavoriteToggle}
          aria-label={favorite ? "Remove from Favorites" : "Add to Favorites"}>
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
        <p className="shop__category">{`CATEGORY: ${category.toUpperCase()}`}</p>

        <p className="shop__name" onClick={handleNameClick}>
          {name}
        </p>

        <div className="shop__prices">
          {oldPrice && (
            <p className="shop__price--discounted">${oldPrice.toFixed(2)}</p>
          )}
          <p className="shop__price">${price}</p>
        </div>

        <button className="shop__btn" onClick={handleAddToCart}>
          Add To Cart {itemsInfo > 0 && <span>( {itemsInfo} )</span>}
        </button>
      </div>

      {isImageEnlarged && (
        <div className="image-overlay" onClick={handleOverlayClick}>
          <button
            className="close-btn"
            onClick={closeImageOverlay}
            aria-label="Close Image">
            X
          </button>
          <img className="overlay-image" src={imgs[0]} alt={name} />
        </div>
      )}
    </div>
  );
};

export default ShopProduct;
