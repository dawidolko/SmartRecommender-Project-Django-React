import "./Testimonials.scss";
import { useNavigate } from "react-router-dom";

const TestimonialsItem = (props) => {
  const { id, imgs, name, price, category, isNew } = props;
  const navigate = useNavigate();

  // Kliknięcie w całą kartę (box) przenosi do strony szczegółów
  const handleBoxClick = () => {
    if (id) {
      navigate(`/product/${id}`);
    }
  };

  return (
    <div className="testimonials__box" onClick={handleBoxClick}>
      {isNew && <span className="testimonials__label">NEW</span>}

      <img src={imgs?.[0]} alt={name} className="testimonials__img" />

      <p className="testimonials__category">
        CATEGORY: {category?.toUpperCase()}
      </p>
      <p className="testimonials__name">{name}</p>
      <p className="testimonials__price">${price}</p>
    </div>
  );
};

export default TestimonialsItem;
