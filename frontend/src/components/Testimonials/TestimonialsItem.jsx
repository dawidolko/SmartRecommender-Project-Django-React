import "./Testimonials.scss";
import { useNavigate } from "react-router-dom";
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

  const handleBoxClick = () => {
    if (id) {
      navigate(`/product/${id}`);
    }
  };

  const formattedPrice =
    typeof price === "string" && !isNaN(parseFloat(price))
      ? `$${parseFloat(price).toFixed(2)}`
      : "Price not available";

  const formattedOldPrice =
    typeof old_price === "string" && !isNaN(parseFloat(old_price))
      ? `$${parseFloat(old_price).toFixed(2)}`
      : null;

  return (
    <div className="testimonials__box" onClick={handleBoxClick}>
      <img
        src={
          photos?.[0]?.path
            ? `${config.apiUrl}/media/${photos[0].path}`
            : "/placeholder.jpg"
        }
        alt={name}
        className="testimonials__img"
      />
      <p className="testimonials__category">
        CATEGORY: {categories?.[0]?.toUpperCase() || "N/A"}
      </p>
      <p className="testimonials__name">{name}</p>
      <p className="testimonials__price">
        {formattedOldPrice && (
          <span className="testimonials__old-price">{formattedOldPrice}</span>
        )}
        <span className="testimonials__current-price">{formattedPrice}</span>
      </p>
    </div>
  );
};

export default TestimonialsItem;
