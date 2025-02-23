import React, { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import { CartContext } from "../ShopContext/ShopContext";
import { useFavorites } from "../FavoritesContent/FavoritesContext";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import {
  AiOutlineHeart,
  AiFillHeart,
  AiOutlineLeft,
  AiOutlineRight,
} from "react-icons/ai";
import { FaStar } from "react-icons/fa";
import "./ProductPage.scss";

const ProductPage = () => {
  const { id } = useParams();
  const { addToCart, items } = useContext(CartContext);
  const { addToFavorites, removeFromFavorites, isFavorite } = useFavorites();

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [favorite, setFavorite] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isImageEnlarged, setIsImageEnlarged] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/product/${id}/`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch product details.");
        }
        const data = await response.json();
        setProduct(data);
        setFavorite(isFavorite(data.id));
      } catch (error) {
        console.error(error);
        toast.error("Error loading product details.", {
          position: "top-center",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id, isFavorite]);

  if (loading) {
    return <h2>Loading...</h2>;
  }

  if (!product) {
    return <h2>Product not found.</h2>;
  }

  const handleToggleFavorite = () => {
    if (favorite) {
      removeFromFavorites(product.id);
      toast.success("Removed from Favorites", { position: "top-center" });
    } else {
      addToFavorites({
        id: product.id,
        img: `http://localhost:8000/media/${product.photos[0]?.path}`,
        name: product.name,
        price: product.price,
      });
      toast.success("Added to Favorites", { position: "top-center" });
    }
    setFavorite(!favorite);
  };

  const handleAddToCart = () => {
    addToCart(product.id);
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

  const handleImageEnlarge = () => {
    setIsImageEnlarged(true);
  };

  const closeImageOverlay = (e) => {
    if (e.target.className.includes("productPage__overlay")) {
      setIsImageEnlarged(false);
    }
  };

  const quantityInCart = items[product.id] || 0;

  return (
    <section className="productPage">
      <div className="productPage__container">
        <div className="productPage__buttons-top">
          <button
            className="productPage__fav-btn"
            onClick={handleToggleFavorite}
          >
            {favorite ? <AiFillHeart /> : <AiOutlineHeart />}
          </button>
        </div>

        <div className="productPage__images">
          <div className="productPage__slider">
            <button
              onClick={handlePrevImage}
              aria-label="Previous Image"
              className="productPage__arrow"
            >
              <AiOutlineLeft />
            </button>
            <img
              src={`http://localhost:8000/media/${product.photos[currentIndex]?.path}`}
              alt={product.name}
              className="productPage__main-img"
              onClick={handleImageEnlarge}
            />
            <button
              onClick={handleNextImage}
              aria-label="Next Image"
              className="productPage__arrow"
            >
              <AiOutlineRight />
            </button>
          </div>
          <div className="productPage__thumbnails">
            {product.photos.map((photo, idx) => (
              <img
                key={idx}
                src={`http://localhost:8000/media/${photo.path}`}
                alt={`Thumbnail ${idx + 1}`}
                className={`productPage__thumbnail ${idx === currentIndex ? "active" : ""
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
              onClick={() => setIsImageEnlarged(false)}
            >
              X
            </button>
            <img
              className="productPage__overlay-image"
              src={`http://localhost:8000/media/${product.photos[currentIndex]?.path}`}
              alt={product.name}
            />
          </div>
        )}

        <div className="productPage__info">
          <div className="productPage__info__main">
          <h2 className="productPage__title">{product.name}</h2>
          <p className="productPage__category">
            Category: {product.categories
              .map(category => category.replace(/\./g, " > "))
              .join(", ")
              .toUpperCase()}

          </p>
          <div className="productPage__tags">
            <p className="tags">
              <span className="tagsHeader">Tags: </span>
              {product.tags.length > 0 ? (
                product.tags.map((tag, index) => (
                  <span key={index} className={index === 2 ? "tag active" : "tag"}>{tag}</span>
                ))
              ) : (
                <p>No tags available for this product.</p>
              )}
            </p>
          </div>
          <div className="productPage__prices">
            {product.old_price && !isNaN(product.old_price) ? (
              <span className="productPage__old-price">
                ${parseFloat(product.old_price).toFixed(2)}
              </span>
            ) : null}
            <span className="productPage__current-price">
              ${parseFloat(product.price).toFixed(2)}
            </span>
            <button className="productPage__cart-btn" onClick={handleAddToCart}>
              Add to Cart {quantityInCart > 0 && `(${quantityInCart})`}
            </button>
          </div>
          </div>

          <div className="productPage__desc">
            <h4>Description:</h4>
            <div
              dangerouslySetInnerHTML={{
                __html: product.description,
              }}
            />
          </div>

          <div className="productPage__specs">
            <h4>Specifications:</h4>
            <table>
              <tbody>
                {product.specifications.map((spec, index) => (
                  <tr key={index}>
                    <td>{spec.parameter_name}</td>
                    <td>{spec.specification}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="productPage__reviews">
            <h4>Customer Reviews</h4>
            {product.opinions.length > 0 ? (
              product.opinions.map((review) => (
                <div key={review.id} className="productPage__review">
                  <div className="productPage__review-header">
                    <span>{review.user_email}</span>
                    <div className="productPage__review-stars">
                      {Array.from({ length: 5 }, (_, index) => (
                        <FaStar
                          key={index}
                          className={
                            index < review.rating
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
      </div>
      <ToastContainer />
    </section>
  );
};

export default ProductPage;
