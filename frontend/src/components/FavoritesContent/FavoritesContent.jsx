import "./FavoritesContent.scss";
import { useContext, useEffect, useState } from "react";
import axios from "axios";
import { useFavorites } from "./FavoritesContext";
import { CartContext } from "../ShopContext/ShopContext";
import FavoritesProduct from "./FavoritesProduct";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import config from "../../config/config";
import { mockAPI } from "../../utils/mockData";
import DemoFallback from "../DemoFallback/DemoFallback";

const FavoritesContent = () => {
  const { favorites, removeFromFavorites } = useFavorites();
  const { addToCart } = useContext(CartContext);
  const [products, setProducts] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        if (config.useMockData) {
          const data = await mockAPI.getProducts();
          setProducts(data);
        } else {
          const response = await axios.get(`${config.apiUrl}/api/products/`);
          setProducts(response.data);
        }
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
      toast.success("Moved to Cart", {
        position: "top-center",
        autoClose: 3000,
        theme: "colored",
      });
    }
  };

  const handleRemoveFromFavorites = (productId) => {
    removeFromFavorites(productId);
    toast.success("Removed from Favorites", {
      position: "top-center",
      autoClose: 3000,
      theme: "colored",
    });
  };

  return (
    <div className="favorites container">
      {favorites.length > 0 && products.length > 0 ? (
        <div className="favorites__container">
          <table className="favorites__table">
            <thead className="favorites__thead">
              <tr className="favorites__row">
                <th style={{ textAlign: "center" }}>Product</th>
                <th style={{ textAlign: "center" }}>Name</th>
                <th style={{ textAlign: "center" }}>Action</th>
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
                      onRemoveFromFavorites={handleRemoveFromFavorites}
                    />
                  );
                }
                return null;
              })}
            </tbody>
          </table>
        </div>
      ) : (
        (() => {
          // Check if on GitHub Pages
          const isGitHubPages =
            typeof window !== "undefined" &&
            (window.location.hostname.includes("github.io") ||
              window.location.hostname.includes("project.dawidolko.pl") ||
              (!window.location.hostname.includes("localhost") &&
                !window.location.hostname.includes("127.0.0.1")));

          if (isGitHubPages) {
            return (
              <DemoFallback
                title="Favorites - Demo Mode"
                message="Favorites functionality requires database connectivity to save and manage your preferred items. This feature is not available in the static demo version."
              />
            );
          }

          // Show message if favorites has items but no product data loaded
          if (favorites.length > 0 && products.length === 0) {
            return (
              <div className="favorites__empty">
                <h2 className="favorites__empty-title">
                  Cannot load favorite products
                </h2>
                <p style={{ marginBottom: "2rem", color: "#666" }}>
                  Unable to connect to the server. Your {favorites.length}{" "}
                  favorite items are saved locally but cannot be displayed
                  without server connection.
                </p>
                <button
                  className="favorites__empty-btn"
                  onClick={() => navigate("/shop")}>
                  Go To Shopping
                </button>
              </div>
            );
          }

          return (
            <div className="favorites__empty">
              <h2 className="favorites__empty-title">
                Your Favorites are empty
              </h2>
              <button
                className="favorites__empty-btn"
                onClick={() => navigate("/shop")}>
                Go To Shopping
              </button>
            </div>
          );
        })()
      )}
    </div>
  );
};

export default FavoritesContent;
