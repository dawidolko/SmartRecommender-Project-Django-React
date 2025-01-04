import "./FavoritesContent.scss";
import { useContext, useEffect, useState } from "react";
import axios from "axios";
import { useFavorites } from "./FavoritesContext";
import { CartContext } from "../ShopContext/ShopContext";
import FavoritesProduct from "./FavoritesProduct";
import { useNavigate } from "react-router-dom";

const FavoritesContent = () => {
  const { favorites, removeFromFavorites } = useFavorites();
  const { addToCart } = useContext(CartContext);
  const [products, setProducts] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/products/");
        setProducts(response.data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };

    fetchProducts();
  }, []);

  const handleMoveToCart = (productId) => {
    const product = products.find((item) => item.id === productId);
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
              {favorites.map((fav) => {
                const product = products.find((p) => p.id === fav.id);
                if (product) {
                  return (
                    <FavoritesProduct
                      key={product.id}
                      product={product}
                      onMoveToCart={handleMoveToCart}
                    />
                  );
                }
                return null;
              })}
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
