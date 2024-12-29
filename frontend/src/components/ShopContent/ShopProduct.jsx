import React, { useContext, useState } from "react";
import { CartContext } from "../ShopContext/ShopContext";
import { useFavorites } from "../FavoritesContent/FavoritesContext";
import { AiOutlineHeart, AiFillHeart } from "react-icons/ai";

const ShopProduct = (props) => {
  const { id, img, name, price, isNew } = props;
  const { items, addToCart } = useContext(CartContext);
  const { addToFavorites, removeFromFavorites, isFavorite } = useFavorites();
  const itemsInfo = items[id];
  const [favorite, setFavorite] = useState(isFavorite(id));

  const handleFavoriteToggle = () => {
    if (favorite) {
      removeFromFavorites(id);
    } else {
      addToFavorites({ id, img, name, price });
    }
    setFavorite(!favorite);
  };

  return (
    <div className="shop__product" key={id}>
      {/* Obrazek wraz z etykietą i przyciskiem ulubionych */}
      <div className="shop__image">
        {isNew && <span className="shop__label">NEW</span>}
        <img className="shop__img" src={img} alt={name} />

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
      </div>

      <div className="shop__content">
        <p className="shop__name">{name}</p>
        <p className="shop__price">${price}</p>
        <button className="shop__btn" onClick={() => addToCart(id)}>
          Add To Cart {itemsInfo > 0 && <span>( {itemsInfo} )</span>}
        </button>
      </div>
    </div>
  );
};

export default ShopProduct;
