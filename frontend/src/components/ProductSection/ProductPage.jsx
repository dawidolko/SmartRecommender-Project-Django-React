import React, { useState, useEffect, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { CartContext } from "../ShopContext/ShopContext";
import { useFavorites } from "../FavoritesContent/FavoritesContext";
import { AuthContext } from "../../context/AuthContext";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
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
import axios from "axios";

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

  const sendInteraction = async (type) => {
    try {
      const token = localStorage.getItem("access");
      await axios.post(
        `${config.apiUrl}/api/interaction/`,
        { product_id: id, interaction_type: type },
        { headers: { Authorization: `Bearer ${token}` } }
      );
    } catch (error) {
      console.error("Error sending interaction:", error);
    }
  };

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await axios.get(`${config.apiUrl}/api/product/${id}/`);
        setProduct(response.data);
        setFavorite(isFavorite(response.data.id));
        sendInteraction("view");
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
  }, [id, isFavorite, logout, navigate]);

  useEffect(() => {
    const fetchSimilarProducts = async () => {
      if (!product || !product.categories || product.categories.length === 0)
        return;

      setSimilarProductsLoading(true);
      try {
        const category = product.categories[0];
        const token = localStorage.getItem("access");
        const headers = {};
        if (token) headers.Authorization = `Bearer ${token}`;

        const response = await axios.get(`${config.apiUrl}/api/products/`, {
          params: { category: category },
          headers: headers,
        });

        const filteredProducts = response.data.filter(
          (p) => p.id !== product.id
        );
        const sortedProducts = filteredProducts.sort(() => 0.5 - Math.random());
        setSimilarProducts(sortedProducts.slice(0, 10));
      } catch (error) {
        console.error("Error fetching similar products:", error);
        setSimilarProducts([]);
      } finally {
        setSimilarProductsLoading(false);
      }
    };

    if (product && product.categories) fetchSimilarProducts();
  }, [product]);

  if (loading) return <div className="loading-spinner"></div>;
  if (!product) return <h2>Product not found.</h2>;

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
    setCurrentIndex((prev) =>
      prev === 0 ? product.photos.length - 1 : prev - 1
    );
  };

  const handleNextImage = () => {
    setCurrentIndex((prev) =>
      prev === product.photos.length - 1 ? 0 : prev + 1
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

  const getSimpleCategory = (category) => category.split(".")[0];
  const getCurrentCategory = () =>
    product?.categories?.[0] ? getSimpleCategory(product.categories[0]) : "";

  return (
    <section className="productPage">
      <div className="productPage__container">
        <div className="productPage__buttons-top">
          <button
            className="productPage__fav-btn"
            onClick={handleToggleFavorite}>
            {favorite ? <AiFillHeart /> : <AiOutlineHeart />}
          </button>
        </div>
        <div className="productPage__main__section">
          <div className="productPage__main__subsection">
            <div className="productPage__images">
              <div className="productPage__slider">
                <button
                  onClick={handlePrevImage}
                  aria-label="Previous Image"
                  className="productPage__arrow">
                  <AiOutlineLeft />
                </button>
                <img
                  src={`${config.apiUrl}/media/${product.photos[currentIndex]?.path}`}
                  alt={product.name}
                  className="productPage__main-img"
                  onClick={handleImageEnlarge}
                />
                <button
                  onClick={handleNextImage}
                  aria-label="Next Image"
                  className="productPage__arrow">
                  <AiOutlineRight />
                </button>
              </div>
              <div className="productPage__thumbnails">
                {product.photos.map((photo, idx) => (
                  <img
                    key={photo.id || photo.path || idx}
                    src={`${config.apiUrl}/media/${photo.path}`}
                    alt={`Thumbnail ${idx + 1}`}
                    className={`productPage__thumbnail ${
                      idx === currentIndex ? "active" : ""
                    }`}
                    onClick={() => setCurrentIndex(idx)}
                  />
                ))}
              </div>
            </div>
            {isImageEnlarged && (
              <div className="productPage__overlay" onClick={closeImageOverlay}>
                <button
                  className="productPage__overlay-close"
                  onClick={() => setIsImageEnlarged(false)}>
                  X
                </button>
                <img
                  className="productPage__overlay-image"
                  src={`${config.apiUrl}/media/${product.photos[currentIndex]?.path}`}
                  alt={product.name}
                />
              </div>
            )}
            <div className="productPage__info__main">
              <p className="productPage__category">
                Category:{" "}
                {product.categories
                  .map((category) => category.replace(/\./g, " > "))
                  .join(", ")
                  .toUpperCase()}
              </p>
              <h2 className="productPage__title">{product.name}</h2>
              <div className="productPage__tags">
                <p className="tags">
                  <span className="tagsHeader">Tags: </span>
                  {product.tags.length > 0 ? (
                    product.tags.map((tag, index) => (
                      <span key={tag || `tag-${index}`} className="tag">
                        {tag}
                      </span>
                    ))
                  ) : (
                    <p>No tags available for this product.</p>
                  )}
                </p>
              </div>
              <div className="productPage__prices">
                {product.old_price && !isNaN(product.old_price) && (
                  <span className="productPage__old-price">
                    ${parseFloat(product.old_price).toFixed(2)}
                  </span>
                )}
                <span className="productPage__current-price">
                  ${parseFloat(product.price).toFixed(2)}
                </span>
              </div>
              <div className="productPage__btn_price">
                <button
                  className="productPage__cart-btn"
                  onClick={handleAddToCart}>
                  Add to Cart {quantityInCart > 0 && `(${quantityInCart})`}
                </button>
              </div>
            </div>
          </div>
          <div className="productPage__description">
            <div className="productPage__desc">
              <h1>Description:</h1>
              <div dangerouslySetInnerHTML={{ __html: product.description }} />
            </div>
          </div>
          <div className="productPage__specs">
            <h1>Specifications:</h1>
            <table>
              <tbody>
                {product.specifications.map((spec, index) => (
                  <tr key={spec.parameter_name || index}>
                    <td>{spec.parameter_name}</td>
                    <td>{spec.specification}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="productPage__reviews">
            <h1>Customer Reviews</h1>
            {product.opinions.length > 0 ? (
              product.opinions.map((review) => (
                <div key={review.id} className="productPage__review">
                  <div className="productPage__review-header">
                    <span>{review.user_email}</span>
                    <div className="productPage__review-stars">
                      {Array.from({ length: 5 }, (_, starIndex) => (
                        <FaStar
                          key={`${review.id}-star-${starIndex}`}
                          className={
                            starIndex < review.rating
                              ? "productPage__review-stars__star--active"
                              : "productPage__review-stars__star"
                          }
                        />
                      ))}
                    </div>
                  </div>
                  <p>{review.content}</p>
                </div>
              ))
            ) : (
              <p>No reviews yet for this product.</p>
            )}
          </div>
        </div>
        <div className="productPage__similar-products">
          <h2 className="productPage__similar-products-title">
            Similar Products{" "}
            {getCurrentCategory() && `in ${getCurrentCategory().toUpperCase()}`}
          </h2>
          {similarProductsLoading ? (
            <div style={{ textAlign: "center" }}>Loading products...</div>
          ) : similarProducts.length > 0 ? (
            <Slider {...sliderSettings}>
              {similarProducts.map((similarProduct) => (
                <div
                  key={similarProduct.id}
                  className="productPage__similar-product"
                  onClick={() => navigate(`/product/${similarProduct.id}`)}>
                  <div className="productPage__similar-product-inner">
                    <img
                      src={`${config.apiUrl}/media/${similarProduct.photos[0]?.path}`}
                      alt={similarProduct.name}
                      className="productPage__similar-product-img"
                    />
                    <h3 className="productPage__similar-product-name">
                      {similarProduct.name}
                    </h3>
                    <div className="productPage__similar-product-prices">
                      {similarProduct.old_price &&
                        !isNaN(similarProduct.old_price) && (
                          <span className="productPage__similar-product-old-price">
                            ${parseFloat(similarProduct.old_price).toFixed(2)}
                          </span>
                        )}
                      <span className="productPage__similar-product-current-price">
                        ${parseFloat(similarProduct.price).toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </Slider>
          ) : (
            <p>No similar products found in this category.</p>
          )}
        </div>
      </div>
      <ToastContainer />
    </section>
  );
};

export default ProductPage;
