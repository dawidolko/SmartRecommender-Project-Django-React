import React, { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import shopData from "../ShopContent/ShopData";
import { CartContext } from "../ShopContext/ShopContext";
import { useFavorites } from "../FavoritesContent/FavoritesContext";
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

  // Index obrazka w sliderze
  const [currentIndex, setCurrentIndex] = useState(0);

  // Powiększanie: czy overlay jest otwarty i które zdjęcie pokazujemy
  const [enlargedImage, setEnlargedImage] = useState(null);

  useEffect(() => {
    if (product) {
      const isFav = isFavorite(product.id);
      setFavorite(isFav);
      const difference = Math.floor(Math.random() * 51);
      if (difference > 0) {
        setOldPrice(parseFloat(product.price) + difference);
      }
    }
  }, [product, isFavorite]);

  if (!product) {
    return <h2 style={{ textAlign: "center" }}>Product not found.</h2>;
  }

  const handleToggleFavorite = () => {
    if (favorite) {
      removeFromFavorites(product.id);
    } else {
      addToFavorites({
        id: product.id,
        img: product.imgs[0],
        name: product.name,
        price: product.price,
      });
    }
    setFavorite(!favorite);
  };

  const handleAddToCart = () => {
    addToCart(product.id);
  };

  const quantityInCart = items[product.id] || 0;

  // Slider: poprzednie i następne zdjęcie
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

  // Kliknięcie w zdjęcie => powiększenie
  const handleEnlargeImage = (imgUrl) => {
    setEnlargedImage(imgUrl);
  };

  // Zamknięcie overlay
  const handleCloseOverlay = () => {
    setEnlargedImage(null);
  };

  // Kliknięcie tła overlay
  const handleOverlayBackgroundClick = (e) => {
    if (e.target === e.currentTarget) {
      handleCloseOverlay();
    }
  };

  return (
    <section className="productPage">
      <div className="productPage__container">
        <div className="productPage__images">
          {/* Slider */}
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
              onClick={() => handleEnlargeImage(product.imgs[currentIndex])}
            />

            <button
              className="productPage__arrow"
              onClick={handleNextImage}
              aria-label="Next Image">
              <AiOutlineRight />
            </button>
          </div>

          {/* Miniaturki (opcjonalne) */}
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
        </div>
      </div>

      {enlargedImage && (
        <div
          className="productPage__overlay"
          onClick={handleOverlayBackgroundClick}>
          <button
            className="productPage__overlay-close"
            onClick={handleCloseOverlay}
            aria-label="Close Overlay">
            X
          </button>
          <img
            className="productPage__overlay-image"
            src={enlargedImage}
            alt="Enlarged"
          />
        </div>
      )}
    </section>
  );
};

export default ProductPage;
