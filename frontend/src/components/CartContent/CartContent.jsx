/**
 * CartContent Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Shopping cart page component that displays cart items, calculates totals,
 * and provides product recommendations based on cart contents.
 *
 * Features:
 *   - Display all items in shopping cart
 *   - Quantity management (increase/decrease/remove)
 *   - Real-time total amount calculation
 *   - Cart persistence in localStorage
 *   - "Frequently Bought Together" recommendations (Association Rules)
 *   - Image enlargement modal for product images
 *   - Checkout navigation
 *   - Empty cart state
 *
 * Recommendation Algorithm:
 *   - Uses Apriori Association Rules (backend)
 *   - Analyzes products currently in cart
 *   - Suggests products frequently bought together
 *   - Formula: If {A, B} in cart → Recommend {C} with confidence > 0.5
 *
 * State Management:
 *   - items: Cart items from CartContext (id → quantity mapping)
 *   - shopData: Full product catalog for displaying recommendations
 *   - recommendations: Products suggested based on cart contents
 *   - recommendationsLoading: Loading state for recommendations API
 *   - enlargedImage: Currently viewed enlarged product image
 *   - totalAmount: Calculated from CartContext
 *
 * API Endpoints:
 *   - GET /api/products/ - Fetch all products for recommendations
 *   - GET /api/frequently-bought-together/?product_ids[]={ids} - Get recommendations
 *
 * Cart Persistence:
 *   - Saves to localStorage on every cart change
 *   - Format: {"productId": quantity, ...}
 *   - Restores on component mount
 *
 * @component
 * @returns {React.ReactElement} Shopping cart page with recommendations
 */
/* eslint-disable react-hooks/exhaustive-deps */
import "./CartContent.scss";
import { useContext, useEffect, useState } from "react";
import { CartContext } from "../ShopContext/ShopContext";
import CartProduct from "./CartProduct";
import TotalAmount from "./TotalAmount";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import config from "../../config/config";

const CartContent = () => {
  const { items, totalAmount, removeFromCart, addToCart } =
    useContext(CartContext);
  const [shopData, setShopData] = useState([]);
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState([]);
  const [recommendationsLoading, setRecommendationsLoading] = useState(false);
  const [enlargedImage, setEnlargedImage] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get(`${config.apiUrl}/api/products/`);
        setShopData(response.data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };
    fetchProducts();
  }, []);

  useEffect(() => {
    localStorage.setItem("cart", JSON.stringify(items));
  }, [items]);

  useEffect(() => {
    if (Object.keys(items).length > 0) {
      fetchRecommendations();
    } else {
      setRecommendations([]);
    }
  }, [items]);

  const fetchRecommendations = async () => {
    setRecommendationsLoading(true);
    try {
      const productIds = Object.keys(items).filter((id) => items[id] > 0);
      if (productIds.length === 0) return;

      const params = new URLSearchParams();
      productIds.forEach((id) => params.append("product_ids[]", id));

      const response = await axios.get(
        `${config.apiUrl}/api/frequently-bought-together/?${params.toString()}`
      );

      if (!response.data || response.data.length === 0) {
        console.warn(
          "⚠️ No recommendations found for these products. Association rules may not be generated yet."
        );
      }

      setRecommendations(response.data);
    } catch (error) {
      console.error("❌ Error fetching cart recommendations:", error);
    } finally {
      setRecommendationsLoading(false);
    }
  };

  const handleAddToCart = (productId) => {
    addToCart(productId);
    toast.success("Added to Cart", {
      position: "top-center",
      autoClose: 3000,
      theme: "colored",
    });
  };

  const handleImageClick = (imageUrl, productName) => {
    setEnlargedImage({ url: imageUrl, name: productName });
  };

  const closeImageOverlay = () => {
    setEnlargedImage(null);
  };

  const handleProductClick = (productId) => {
    navigate(`/product/${productId}`);
  };

  return (
    <div className="cart container">
      {totalAmount() > 0 ? (
        <div className="cart__container">
          <table className="cart__table">
            <thead className="cart__thead">
              <tr className="cart__row">
                <th style={{ textAlign: "center" }}>Product</th>
                <th style={{ textAlign: "center" }}>Name</th>
                <th style={{ textAlign: "center" }}>Quantity</th>
                <th style={{ textAlign: "center" }}>Total Price</th>
                <th style={{ textAlign: "center" }}>Remove</th>
              </tr>
            </thead>
            <tbody>
              {shopData.map((product) => {
                if (items[product.id] > 0) {
                  return (
                    <CartProduct
                      key={product.id}
                      {...product}
                      removeItemFromCart={removeFromCart}
                    />
                  );
                }
                return null;
              })}
            </tbody>
          </table>

          {totalAmount() > 0 && recommendations.length > 0 && (
            <div className="cart__recommendations">
              <h3 className="cart__recommendations-title">
                Frequently Bought Together
              </h3>
              {recommendationsLoading ? (
                <div className="cart__recommendations-loading">Loading...</div>
              ) : (
                <div className="cart__recommendations-grid">
                  {recommendations.map((rec, index) => {
                    const imageUrl = `${config.apiUrl}/media/${rec.product.photos[0]?.path}`;
                    return (
                      <div key={index} className="cart__recommendation-item">
                        <img
                          src={imageUrl}
                          alt={rec.product.name}
                          className="cart__recommendation-image"
                          onClick={() =>
                            handleImageClick(imageUrl, rec.product.name)
                          }
                        />
                        <div className="cart__recommendation-info">
                          <h4
                            className="cart__recommendation-name"
                            onClick={() => handleProductClick(rec.product.id)}>
                            {rec.product.name}
                          </h4>
                          <p className="cart__recommendation-price">
                            ${rec.product.price}
                          </p>
                          <div className="cart__recommendation-stats">
                            <span className="stat-confidence">
                              Confidence: {(rec.confidence * 100).toFixed(0)}%
                            </span>
                            <span className="stat-lift">
                              Lift: {rec.lift.toFixed(2)}x
                            </span>
                            <span className="stat-support">
                              Support: {(rec.support * 100).toFixed(1)}%
                            </span>
                          </div>
                          <button
                            className="cart__recommendation-button"
                            onClick={() => handleAddToCart(rec.product.id)}>
                            Add to Cart
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {enlargedImage && (
            <div className="common-image-overlay" onClick={closeImageOverlay}>
              <div className="common-image-overlay__content">
                <button
                  className="common-close-button"
                  onClick={closeImageOverlay}
                  aria-label="Close image">
                  ×
                </button>
                <img
                  className="common-image-overlay__image"
                  src={enlargedImage.url}
                  alt={enlargedImage.name}
                />
              </div>
            </div>
          )}

          <TotalAmount />
        </div>
      ) : (
        <div className="cart__empty">
          <h2 className="cart__empty-title">Your cart is empty</h2>
          <button className="cart__empty-btn" onClick={() => navigate("/shop")}>
            Go To Shopping
          </button>
        </div>
      )}
    </div>
  );
};

export default CartContent;
