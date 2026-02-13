/**
 * ProductPage Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Detailed product page component displaying comprehensive product information,
 * images, specifications, reviews, and personalized recommendations.
 *
 * Features:
 *   - Product image gallery with enlargement modal
 *   - Image carousel navigation (left/right arrows)
 *   - Add to cart functionality
 *   - Add to favorites (heart icon toggle)
 *   - Product specifications table
 *   - User reviews and ratings
 *   - Average rating calculation with star display
 *   - Similar products carousel (same category)
 *   - Tabbed interface (Description, Specifications, Reviews)
 *   - User interaction tracking (view, add_to_cart, favorite)
 *   - Breadcrumb navigation
 *   - Stock status indicator
 *   - Price display with old price strikethrough
 *
 * Interaction Tracking:
 *   - Sends analytics events to backend for recommendation algorithms
 *   - Types: 'view', 'add_to_cart', 'favorite'
 *   - Used by Collaborative Filtering and User Profiling
 *
 * Similar Products Algorithm:
 *   - Fetches products from same main category
 *   - Excludes current product
 *   - Displays in carousel format
 *   - Helps users discover related products
 *
 * State Management:
 *   - product: Full product details from API
 *   - loading: Loading state for product data
 *   - favorite: Boolean indicating if product is in favorites
 *   - currentIndex: Active image in gallery
 *   - isImageEnlarged: Modal state for enlarged image view
 *   - similarProducts: Array of related products
 *   - activeTab: Current tab (description/specifications/reviews)
 *   - items: Cart items from CartContext
 *
 * API Endpoints:
 *   - GET /api/product/:id/ - Fetch product details
 *   - GET /api/products/?category={category} - Fetch similar products
 *   - POST /api/interaction/ - Log user interaction
 *
 * Reviews Calculation:
 *   - Average Rating = Σ(ratings) / count(reviews)
 *   - Star Display: Full stars, half stars, empty stars
 *   - Review Count: Total number of opinions
 *
 * @component
 * @returns {React.ReactElement} Product detail page with gallery and recommendations
 */
import React, { useState, useEffect, useContext, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { CartContext } from "../ShopContext/ShopContext";
import { useFavorites } from "../FavoritesContent/FavoritesContext";
import { AuthContext } from "../../context/AuthContext";
import { toast } from "react-toastify";
import {
  AiOutlineHeart,
  AiFillHeart,
  AiOutlineLeft,
  AiOutlineRight,
} from "react-icons/ai";
import { FaStar } from "react-icons/fa";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./ProductPage.scss";
import config from "../../config/config";
import { mockAPI } from "../../utils/mockData";
import axios from "axios";
import DemoFallback from "../DemoFallback/DemoFallback";

const ProductPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart, items } = useContext(CartContext);
  const { addToFavorites, removeFromFavorites, isFavorite } = useFavorites();
  const { logout } = useContext(AuthContext);

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [favorite, setFavorite] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isImageEnlarged, setIsImageEnlarged] = useState(false);
  const [similarProducts, setSimilarProducts] = useState([]);
  const [similarProductsLoading, setSimilarProductsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("description");

  const sendInteraction = useCallback(
    async (type) => {
      const token = localStorage.getItem("access");
      if (!token) {
        return;
      }

      try {
        await axios.post(
          `${config.apiUrl}/api/interaction/`,
          { product_id: id, interaction_type: type },
          { headers: { Authorization: `Bearer ${token}` } },
        );
      } catch (error) {
        if (error.response?.status !== 401) {
          console.error("Error sending interaction:", error);
        }
      }
    },
    [id],
  );

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        if (config.useMockData) {
          const data = await mockAPI.getProductById(id);
          if (!data) {
            toast.error("Product not found.", {
              position: "top-center",
            });
            navigate("/shop");
            return;
          }
          setProduct(data);
          setFavorite(isFavorite(data.id));
        } else {
          const response = await axios.get(
            `${config.apiUrl}/api/product/${id}/`,
          );
          setProduct(response.data);
          setFavorite(isFavorite(response.data.id));
          if (!config.useMockData) {
            sendInteraction("view");
          }
        }
      } catch (error) {
        console.error(error);
        toast.error("Error loading product details.", {
          position: "top-center",
        });
        if (
          error.message.includes("401") ||
          error.message.includes("unauthorized")
        ) {
          logout();
          navigate("/login");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id, isFavorite, logout, navigate, sendInteraction]);

  useEffect(() => {
    const fetchSimilarProducts = async () => {
      if (!product) return;

      setSimilarProductsLoading(true);
      try {
        if (config.useMockData) {
          const data = await mockAPI.getRelatedProducts(product.id, 10);
          setSimilarProducts(data);
        } else {
          if (!product.categories || product.categories.length === 0) {
            setSimilarProducts([]);
            setSimilarProductsLoading(false);
            return;
          }

          const fullCategory = product.categories[0];
          const mainCategory = fullCategory.split(".")[0];
          const token = localStorage.getItem("access");
          const headers = {};
          if (token) headers.Authorization = `Bearer ${token}`;

          const response = await axios.get(`${config.apiUrl}/api/products/`, {
            params: { category: mainCategory },
            headers: headers,
          });

          const filteredProducts = response.data.filter(
            (p) =>
              p.id !== product.id &&
              p.categories.some((cat) => cat.startsWith(mainCategory)),
          );
          const sortedProducts = filteredProducts.sort(
            () => 0.5 - Math.random(),
          );
          setSimilarProducts(sortedProducts.slice(0, 10));
        }
      } catch (error) {
        console.error("Error fetching similar products:", error);
        setSimilarProducts([]);
      } finally {
        setSimilarProductsLoading(false);
      }
    };

    if (product) fetchSimilarProducts();
  }, [product]);

  // Check if on GitHub Pages and no product found
  const isGitHubPages =
    typeof window !== "undefined" &&
    (window.location.hostname.includes("github.io") ||
      window.location.hostname.includes("project.dawidolko.pl") ||
      (!window.location.hostname.includes("localhost") &&
        !window.location.hostname.includes("127.0.0.1")));

  if (loading) return <div className="loading-spinner"></div>;

  if (!product) {
    if (isGitHubPages) {
      return (
        <DemoFallback
          title="Product Details - Demo Mode"
          message="Individual product pages require database connectivity to load product details, images, and specifications. This feature is not available in the static demo version."
        />
      );
    }
    return <h2>Product not found.</h2>;
  }

  const handleToggleFavorite = () => {
    if (favorite) {
      removeFromFavorites(product.id);
      toast.success("Removed from Favorites", { position: "top-center" });
    } else {
      addToFavorites({
        id: product.id,
        img: `${config.apiUrl}/media/${product.photos[0]?.path}`,
        name: product.name,
        price: product.price,
      });
      sendInteraction("favorite");
      toast.success("Added to Favorites", { position: "top-center" });
    }
    setFavorite(!favorite);
  };

  const handleAddToCart = () => {
    addToCart(product.id);
    sendInteraction("add_to_cart");
    toast.success("Added to Cart", { position: "top-center" });
  };

  const handlePrevImage = () => {
    if (!product.photos || product.photos.length === 0) return;
    setCurrentIndex((prev) =>
      prev === 0 ? product.photos.length - 1 : prev - 1,
    );
  };

  const handleNextImage = () => {
    if (!product.photos || product.photos.length === 0) return;
    setCurrentIndex((prev) =>
      prev === product.photos.length - 1 ? 0 : prev + 1,
    );
  };

  const handleImageEnlarge = () => setIsImageEnlarged(true);
  const closeImageOverlay = (e) => {
    if (e.target.className.includes("productPage__overlay"))
      setIsImageEnlarged(false);
  };

  const quantityInCart = items[product.id] || 0;

  const sliderSettings = {
    dots: true,
    infinite: similarProducts.length > 4,
    speed: 500,
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3000,
    responsive: [
      { breakpoint: 1200, settings: { slidesToShow: 3, slidesToScroll: 1 } },
      { breakpoint: 768, settings: { slidesToShow: 2, slidesToScroll: 1 } },
      { breakpoint: 480, settings: { slidesToShow: 1, slidesToScroll: 1 } },
    ],
  };

  const thumbnailSliderSettings = {
    dots: false,
    infinite: product?.photos?.length > 5,
    speed: 300,
    slidesToShow: 5,
    slidesToScroll: 1,
    focusOnSelect: true,
    arrows: true,
    swipeToSlide: true,
    responsive: [
      {
        breakpoint: 1500,
        settings: {
          slidesToShow: 4,
          slidesToScroll: 1,
          infinite: product?.photos?.length > 4,
          arrows: true,
        },
      },
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 4,
          slidesToScroll: 1,
          infinite: product?.photos?.length > 4,
          arrows: true,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
          infinite: product?.photos?.length > 3,
          arrows: true,
          swipeToSlide: true,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
          infinite: product?.photos?.length > 3,
          arrows: true,
          swipeToSlide: true,
        },
      },
    ],
  };

  const getSimpleCategory = (category) => category.split(".")[0];
  const getCurrentCategory = () =>
    product?.categories?.[0] ? getSimpleCategory(product.categories[0]) : "";

  const renderTabContent = () => {
    switch (activeTab) {
      case "description":
        return (
          <div className="productPage__tab-content">
            <div dangerouslySetInnerHTML={{ __html: product.description }} />
          </div>
        );
      case "specifications":
        return (
          <div className="productPage__tab-content">
            {product.specifications && product.specifications.length > 0 ? (
              <table className="productPage__specs-table">
                <tbody>
                  {product.specifications.map((spec, index) => (
                    <tr
                      key={`spec-${spec?.parameter_name ?? "param"}-${
                        spec?.specification ?? "value"
                      }-${index}`}>
                      <td className="productPage__specs-param">
                        {spec.parameter_name}
                      </td>
                      <td className="productPage__specs-value">
                        {spec.specification}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No specifications available for this product.</p>
            )}
          </div>
        );
      case "reviews":
        return (
          <div className="productPage__tab-content">
            {product.opinions && product.opinions.length > 0 ? (
              product.opinions.map((review) => (
                <div key={review.id} className="productPage__review">
                  <div className="productPage__review-header">
                    <span className="productPage__review-email">
                      {review.user_email}
                    </span>
                    <div className="productPage__review-stars">
                      {Array.from({ length: 5 }, (_, starIndex) => (
                        <FaStar
                          key={`star-${review.id}-${starIndex}`}
                          className={
                            starIndex < review.rating
                              ? "productPage__review-star--active"
                              : "productPage__review-star"
                          }
                        />
                      ))}
                    </div>
                  </div>
                  <p className="productPage__review-content">
                    {review.content}
                  </p>
                </div>
              ))
            ) : (
              <p className="productPage__no-data">
                No reviews yet for this product.
              </p>
            )}
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <section className="productPage">
      <div className="productPage__container">
        <button
          className="productPage__fav-btn"
          onClick={handleToggleFavorite}
          aria-label={favorite ? "Remove from favorites" : "Add to favorites"}>
          {favorite ? <AiFillHeart /> : <AiOutlineHeart />}
        </button>

        <div className="productPage__top-section">
          <div className="productPage__gallery">
            <div className="productPage__main-image-wrapper">
              <button
                onClick={handlePrevImage}
                aria-label="Previous Image"
                className="productPage__arrow productPage__arrow--prev">
                <AiOutlineLeft />
              </button>
              <img
                src={
                  product.photos && product.photos[currentIndex]
                    ? `${config.apiUrl}/media/${product.photos[currentIndex].path}`
                    : "/placeholder.jpg"
                }
                alt={product.name}
                className="productPage__main-img productPage__main-img--clickable"
                onClick={handleImageEnlarge}
              />
              <button
                onClick={handleNextImage}
                aria-label="Next Image"
                className="productPage__arrow productPage__arrow--next">
                <AiOutlineRight />
              </button>
            </div>
            <div className="productPage__thumbnails">
              {((config.useMockData && product.imgs) ||
                (!config.useMockData && product.photos)) &&
                ((config.useMockData && product.imgs) || product.photos || [])
                  .length > 0 && (
                  <Slider {...thumbnailSliderSettings}>
                    {(config.useMockData
                      ? product.imgs || []
                      : product.photos || []
                    ).map((photo, idx) => (
                      <div key={`thumb-${photo?.id ?? photo?.path ?? idx}`}>
                        <img
                          src={
                            photo?.path
                              ? `${config.apiUrl}/media/${photo.path}`
                              : "/placeholder.jpg"
                          }
                          alt={`Thumbnail ${idx + 1}`}
                          className={`productPage__thumbnail ${
                            idx === currentIndex
                              ? "productPage__thumbnail--active"
                              : ""
                          }`}
                          onClick={() => setCurrentIndex(idx)}
                        />
                      </div>
                    ))}
                  </Slider>
                )}
            </div>
          </div>

          {isImageEnlarged && (
            <div className="common-image-overlay" onClick={closeImageOverlay}>
              <div className="common-image-overlay__content">
                <button
                  className="common-close-button"
                  onClick={() => setIsImageEnlarged(false)}
                  aria-label="Close image">
                  ×
                </button>
                <img
                  className="common-image-overlay__image"
                  src={
                    product.photos && product.photos[currentIndex]
                      ? `${config.apiUrl}/media/${product.photos[currentIndex].path}`
                      : "/placeholder.jpg"
                  }
                  alt={product.name}
                />
              </div>
            </div>
          )}

          <div className="productPage__info">
            <div className="productPage__category">
              {product.categories && product.categories.length > 0
                ? product.categories
                    .map((category) => category.replace(/\./g, " › "))
                    .join(", ")
                : "Uncategorized"}
            </div>
            <h1 className="productPage__title">{product.name}</h1>

            {product.tags && product.tags.length > 0 && (
              <div className="productPage__tags">
                {product.tags.map((tag, index) => (
                  <span
                    key={`tag-${tag}-${index}`}
                    className="productPage__tag">
                    {tag}
                  </span>
                ))}
              </div>
            )}

            <div className="productPage__price-section">
              {product.old_price && !isNaN(product.old_price) && (
                <span className="productPage__old-price">
                  ${parseFloat(product.old_price).toFixed(2)}
                </span>
              )}
              <span className="productPage__current-price">
                ${parseFloat(product.price).toFixed(2)}
              </span>
            </div>

            <button className="productPage__cart-btn" onClick={handleAddToCart}>
              Add to Cart {quantityInCart > 0 && `(${quantityInCart})`}
            </button>

            {similarProducts.length > 0 && (
              <div className="productPage__quick-recommendations">
                <h3 className="productPage__quick-recommendations-title">
                  You May Also Like
                </h3>
                <div className="productPage__quick-recommendations-grid">
                  {similarProducts.slice(0, 3).map((recProduct) => (
                    <div
                      key={`quick-rec-${recProduct.id}`}
                      className="productPage__quick-rec-card"
                      onClick={() => navigate(`/product/${recProduct.id}`)}>
                      <img
                        src={
                          recProduct.photos && recProduct.photos[0]
                            ? `${config.apiUrl}/media/${recProduct.photos[0].path}`
                            : "/placeholder.jpg"
                        }
                        alt={recProduct.name}
                        className="productPage__quick-rec-img"
                      />
                      <div className="productPage__quick-rec-info">
                        <p className="productPage__quick-rec-name">
                          {recProduct.name}
                        </p>
                        <p className="productPage__quick-rec-price">
                          ${parseFloat(recProduct.price).toFixed(2)}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="productPage__details">
          <div className="productPage__tabs">
            <button
              className={`productPage__tab ${
                activeTab === "description" ? "productPage__tab--active" : ""
              }`}
              onClick={() => setActiveTab("description")}>
              Description
            </button>
            <button
              className={`productPage__tab ${
                activeTab === "specifications" ? "productPage__tab--active" : ""
              }`}
              onClick={() => setActiveTab("specifications")}>
              Specifications
            </button>
            <button
              className={`productPage__tab ${
                activeTab === "reviews" ? "productPage__tab--active" : ""
              }`}
              onClick={() => setActiveTab("reviews")}>
              Reviews ({product.opinions ? product.opinions.length : 0})
            </button>
          </div>
          {renderTabContent()}
        </div>
        {similarProducts.length > 0 && (
          <div className="productPage__similar-products">
            <h2 className="productPage__similar-products-title">
              You May Also Like
              {getCurrentCategory() && ` in `}
              <span>{getCurrentCategory()}</span>
            </h2>
            {similarProductsLoading ? (
              <div className="productPage__loading">Loading products...</div>
            ) : (
              <Slider {...sliderSettings}>
                {similarProducts.map((similarProduct) => (
                  <div
                    key={`similar-${similarProduct.id}`}
                    className="productPage__similar-product">
                    <div
                      className="productPage__similar-product-inner"
                      onClick={() => navigate(`/product/${similarProduct.id}`)}>
                      <img
                        src={
                          similarProduct.photos && similarProduct.photos[0]
                            ? `${config.apiUrl}/media/${similarProduct.photos[0].path}`
                            : "/placeholder.jpg"
                        }
                        alt={similarProduct.name}
                        className="productPage__similar-product-img"
                      />
                      <div className="productPage__similar-product-content">
                        <p className="productPage__similar-product-category">
                          {`CATEGORY: ${
                            similarProduct.categories?.[0]
                              ?.replace(".", " > ")
                              .toUpperCase() || "N/A"
                          }`}
                        </p>
                        <h3 className="productPage__similar-product-name">
                          {similarProduct.name}
                        </h3>
                        <div className="productPage__similar-product-prices">
                          {similarProduct.old_price &&
                            !isNaN(similarProduct.old_price) && (
                              <span className="productPage__similar-product-old-price">
                                $
                                {parseFloat(similarProduct.old_price).toFixed(
                                  2,
                                )}
                              </span>
                            )}
                          <span className="productPage__similar-product-current-price">
                            ${parseFloat(similarProduct.price).toFixed(2)}
                          </span>
                        </div>
                        <button
                          className="productPage__similar-product-btn"
                          onClick={(e) => {
                            e.stopPropagation();
                            addToCart(similarProduct.id);
                            toast.success("Added to Cart", {
                              position: "top-center",
                              autoClose: 3000,
                              theme: "colored",
                            });
                          }}>
                          ADD TO CART{" "}
                          {items[similarProduct.id] > 0 && (
                            <span>({items[similarProduct.id]})</span>
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </Slider>
            )}
          </div>
        )}
      </div>
    </section>
  );
};

export default ProductPage;
