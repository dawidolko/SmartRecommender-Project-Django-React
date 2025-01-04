import React, { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import shopData from "../ShopContent/ShopData";
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
import "./ProductPage.scss";

const ProductPage = () => {
  const { id } = useParams();
  const productId = parseInt(id, 10);

  const { addToCart, items } = useContext(CartContext);
  const { addToFavorites, removeFromFavorites, isFavorite } = useFavorites();

  const product = shopData.find((p) => p.id === productId);

  const [oldPrice, setOldPrice] = useState(null);
  const [favorite, setFavorite] = useState(false);
  const [reviews, setReviews] = useState([]);
  const [newReview, setNewReview] = useState({ rating: 0, text: "" });
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [isImageEnlarged, setIsImageEnlarged] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (product) {
      const isFav = isFavorite(product.id);
      setFavorite(isFav);
      const difference = Math.floor(Math.random() * 51);
      if (difference > 0) {
        setOldPrice(parseFloat(product.price) + difference);
      }
    }

    const savedReviews =
      JSON.parse(localStorage.getItem("productReviews")) || [];
    const productReviews = savedReviews.filter(
      (review) => review.productId === productId
    );
    setReviews(productReviews);
  }, [product, isFavorite, productId]);

  if (!product) {
    return <h2 style={{ textAlign: "center" }}>Product not found.</h2>;
  }

  const handleToggleFavorite = () => {
    if (favorite) {
      removeFromFavorites(product.id);
      toast.success("Removed from Favorites", {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
    } else {
      addToFavorites({
        id: product.id,
        img: product.imgs[0],
        name: product.name,
        price: product.price,
      });
      toast.success("Added to Favorites", {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
    }
    setFavorite(!favorite);
  };

  const handleAddToCart = () => {
    addToCart(product.id);
    toast.success("Added to Cart", {
      position: "top-center",
      autoClose: 3000,
      hideProgressBar: true,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "colored",
    });
  };

  const quantityInCart = items[product.id] || 0;

  const handlePrevImage = () => {
    setCurrentIndex((prev) =>
      prev === 0 ? product.imgs.length - 1 : prev - 1
    );
  };

  const handleNextImage = () => {
    setCurrentIndex((prev) =>
      prev === product.imgs.length - 1 ? 0 : prev + 1
    );
  };

  const handleImageEnlarge = () => {
    setIsImageEnlarged(true);
  };

  const closeImageOverlay = () => {
    setIsImageEnlarged(false);
  };

  const handleAddReview = () => {
    if (
      newReview.rating < 1 ||
      newReview.rating > 5 ||
      !newReview.text.trim()
    ) {
      toast.error("Please provide a valid rating (1-5) and a review text.", {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
      return;
    }

    const updatedReviews = [
      ...reviews,
      { productId, ...newReview, id: Date.now() },
    ];
    localStorage.setItem("productReviews", JSON.stringify(updatedReviews));
    setReviews(updatedReviews);

    setNewReview({ rating: 0, text: "" });
    setShowReviewForm(false);
    toast.success("Your review has been submitted!", {
      position: "top-center",
      autoClose: 3000,
      hideProgressBar: true,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "colored",
    });
  };

  return (
    <section className="productPage">
      <div className="productPage__container">
        <div className="productPage__images">
          <div className="productPage__slider">
            <button
              className="productPage__arrow"
              onClick={handlePrevImage}
              aria-label="Previous Image">
              <AiOutlineLeft />
            </button>

            <img
              className="productPage__main-img"
              src={product.imgs[currentIndex]}
              alt={product.name}
              onClick={handleImageEnlarge}
            />

            <button
              className="productPage__arrow"
              onClick={handleNextImage}
              aria-label="Next Image">
              <AiOutlineRight />
            </button>
          </div>

          <div className="productPage__thumbnails">
            {product.imgs.map((imgUrl, idx) => (
              <img
                key={idx}
                src={imgUrl}
                alt={product.name}
                className={`productPage__thumbnail ${
                  idx === currentIndex ? "active" : ""
                }`}
                onClick={() => setCurrentIndex(idx)}
              />
            ))}
          </div>
        </div>

        {isImageEnlarged && (
          <div className="productPage__overlay">
            <button
              className="productPage__overlay-close"
              onClick={closeImageOverlay}
              aria-label="Close">
              &times;
            </button>
            <img
              className="productPage__overlay-image"
              src={product.imgs[currentIndex]}
              alt={product.name}
            />
          </div>
        )}

        <div className="productPage__info">
          <h2 className="productPage__title">{product.name}</h2>
          <p className="productPage__category">
            Category: {product.category.toUpperCase()}
          </p>

          <div className="productPage__prices">
            {oldPrice && (
              <span className="productPage__old-price">
                ${oldPrice.toFixed(2)}
              </span>
            )}
            <span className="productPage__current-price">${product.price}</span>
          </div>

          {product.description && (
            <div className="productPage__desc">
              <h4>Description:</h4>
              <div dangerouslySetInnerHTML={{ __html: product.description }} />
            </div>
          )}

          <div className="productPage__buttons">
            <button className="productPage__cart-btn" onClick={handleAddToCart}>
              Add to Cart {quantityInCart > 0 && `(${quantityInCart})`}
            </button>

            <button
              className="productPage__fav-btn"
              onClick={handleToggleFavorite}
              aria-label="Toggle Favorites">
              {favorite ? (
                <AiFillHeart style={{ color: "red", fontSize: "1.8rem" }} />
              ) : (
                <AiOutlineHeart style={{ fontSize: "1.8rem" }} />
              )}
            </button>
          </div>

          <div>
            <h3>Customer Reviews</h3>
            {reviews.length > 0 ? (
              reviews.map((review) => (
                <div
                  key={review.id}
                  style={{
                    border: "1px solid #ddd",
                    margin: "1rem 0",
                    padding: "1rem",
                  }}>
                  <p>
                    <strong>Rating:</strong> {review.rating} / 5
                  </p>
                  <p>{review.text}</p>
                </div>
              ))
            ) : (
              <p>No reviews yet for this product.</p>
            )}

            {showReviewForm ? (
              <div style={{ marginTop: "1rem" }}>
                <h4>Add a Review</h4>
                <label>
                  Rating (1-5):
                  <input
                    type="number"
                    min="1"
                    max="5"
                    value={newReview.rating}
                    onChange={(e) =>
                      setNewReview((prev) => ({
                        ...prev,
                        rating: parseInt(e.target.value, 10),
                      }))
                    }
                  />
                </label>
                <br />
                <label>
                  Review:
                  <textarea
                    rows="4"
                    value={newReview.text}
                    onChange={(e) =>
                      setNewReview((prev) => ({
                        ...prev,
                        text: e.target.value,
                      }))
                    }
                  />
                </label>
                <br />
                <button onClick={handleAddReview}>Submit</button>
                <button
                  onClick={() => setShowReviewForm(false)}
                  style={{ marginLeft: "1rem" }}>
                  Cancel
                </button>
              </div>
            ) : (
              <button
                onClick={() => setShowReviewForm(true)}
                style={{ marginTop: "1rem" }}>
                Add a Review
              </button>
            )}
          </div>
        </div>
      </div>
      <ToastContainer />
    </section>
  );
};

export default ProductPage;
