import "./FavoritesContent.scss";
import shopData from "../ShopContent/ShopData";
import { useContext } from "react";
import { useFavorites } from "./FavoritesContext";
import { CartContext } from "../ShopContext/ShopContext";
import FavoritesProduct from "./FavoritesProduct";
import { useNavigate } from "react-router-dom";

const FavoritesContent = () => {
  const { favorites, removeFromFavorites } = useFavorites();
  const { addToCart } = useContext(CartContext);
  const navigate = useNavigate();

  const handleMoveToCart = (productId) => {
    const product = shopData.find((item) => item.id === productId);
    if (product) {
      addToCart(product.id);
      removeFromFavorites(product.id);
    }
  };

  return (
    <div className="favorites container">
      {favorites.length > 0 ? (
        <div className="favorites__container">
          <table className="favorites__table">
            <thead className="favorites__thead">
              <tr className="favorites__row">
                <th>Product</th>
                <th>Name</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {favorites.map((product) => (
                <FavoritesProduct
                  key={product.id}
                  product={product}
                  onMoveToCart={handleMoveToCart}
                />
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="favorites__empty">
          <h2 className="favorites__empty-title">Your Favorites are empty</h2>
          <button
            className="favorites__empty-btn"
            onClick={() => navigate("/shop")}>
            Go To Shopping
          </button>
        </div>
      )}
    </div>
  );
};

export default FavoritesContent;
