import React, { useContext, useState } from "react";
import { CartContext } from "../ShopContext/ShopContext";
import { useFavorites } from "../FavoritesContent/FavoritesContext";
import { AiOutlineHeart, AiFillHeart, AiOutlineSearch } from "react-icons/ai";

const ShopProduct = (props) => {
  const { id, imgs, name, price, category, isNew } = props;
  const { items, addToCart } = useContext(CartContext); // Sprawdzamy, czy dodanie do koszyka działa dla wszystkich produktów.
  const { addToFavorites, removeFromFavorites, isFavorite } = useFavorites();
  const itemsInfo = items[id];
  const [favorite, setFavorite] = useState(isFavorite(id));
  const [isImageEnlarged, setIsImageEnlarged] = useState(false);

  const handleFavoriteToggle = () => {
    if (favorite) {
      removeFromFavorites(id);
    } else {
      addToFavorites({ id, img: imgs[0], name, price });
    }
    setFavorite(!favorite);
  };

  const handleImageEnlarge = () => {
    setIsImageEnlarged(true);
  };

  const closeImageOverlay = () => {
    setIsImageEnlarged(false);
  };

  const discountedPrice = parseFloat(price) + 10.0;

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      closeImageOverlay();
    }
  };

  // Funkcja obsługująca dodawanie produktów do koszyka
  const handleAddToCart = () => {
    addToCart(id);
  };

  return (
    <div className="shop__product" key={id}>
      <div className="shop__image">
        {isNew && <span className="shop__label">NEW</span>}
        <img
          className="shop__img"
          src={imgs[0]}
          alt={name}
          onClick={handleImageEnlarge} // Zrobienie obrazu klikalnym
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

      <div className="shop__content">
        <p className="shop__category">CATEGORY: {category.toUpperCase()}</p>
        <p className="shop__name">{name}</p>
        <div className="shop__prices">
          <p className="shop__price--discounted">
            ${discountedPrice.toFixed(2)}
          </p>
          <p className="shop__price">${price}</p>
        </div>
        <button className="shop__btn" onClick={handleAddToCart}>
          Add To Cart {itemsInfo > 0 && <span>( {itemsInfo} )</span>}
        </button>
      </div>

      {/* Image Overlay */}
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
