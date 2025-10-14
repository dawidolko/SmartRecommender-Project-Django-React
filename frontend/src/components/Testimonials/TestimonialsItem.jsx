import "./Testimonials.scss";
import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { CartContext } from "../ShopContext/ShopContext";
import { toast } from "react-toastify";
import config from "../../config/config";

const TestimonialsItem = ({
  id,
  photos,
  name,
  price,
  old_price,
  categories,
}) => {
  const navigate = useNavigate();
  const { items, addToCart } = useContext(CartContext);
  const itemsInfo = items ? items[id] : 0;

  const handleBoxClick = () => {
    if (id) {
      navigate(`/product/${id}`);
    }
  };

  const handleAddToCart = (e) => {
    e.stopPropagation();
    addToCart(id);
    toast.success("Added to Cart", {
      position: "top-center",
      autoClose: 3000,
      theme: "colored",
    });
  };

  const formattedPrice =
    typeof price === "string" && !isNaN(parseFloat(price))
      ? parseFloat(price).toFixed(2)
      : "N/A";

  const formattedOldPrice =
    old_price && typeof old_price === "string" && !isNaN(parseFloat(old_price))
      ? parseFloat(old_price).toFixed(2)
      : null;

  return (
    <div className="testimonials__box" onClick={handleBoxClick}>
      <div className="testimonials__image-container">
        <img
          src={
            photos?.[0]?.path
              ? `${config.apiUrl}/media/${photos[0].path}`
              : "/placeholder.jpg"
          }
          alt={name}
          className="testimonials__img"
        />
      </div>

      <div className="testimonials__content">
        <p className="testimonials__category">
          {`CATEGORY: ${
            categories?.[0]?.replace(".", " > ").toUpperCase() || "N/A"
          }`}
        </p>

        <p className="testimonials__name">{name}</p>

        <div className="testimonials__prices">
          {formattedOldPrice && (
            <span className="testimonials__old-price">
              ${formattedOldPrice}
            </span>
          )}
          <span className="testimonials__current-price">${formattedPrice}</span>
        </div>

        <button className="testimonials__btn" onClick={handleAddToCart}>
          ADD TO CART {itemsInfo > 0 && <span>({itemsInfo})</span>}
        </button>
      </div>
    </div>
  );
};

export default TestimonialsItem;
