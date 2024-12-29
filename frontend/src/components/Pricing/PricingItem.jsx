import { Link } from "react-router-dom";
import { AiOutlineCheck } from "react-icons/ai";

const PricingItem = ({ title, price, features, bestOffer }) => {
  return (
    <div
      className="pricing__box"
      style={{ backgroundColor: bestOffer ? "#111" : "" }}>
      {bestOffer && <span className="pricing__best-offer">Best Offer</span>}
      <h3 className="pricing__box-title">{title}</h3>
      <p className="pricing__price">
        ${price} <span className="pricing__month">/monthly</span>
      </p>
      <hr className="pricing__line" />
      <ul className="pricing__list">
        {features.map((feature, index) => (
          <li className="pricing__item" key={index}>
            <span>
              <AiOutlineCheck className="pricing__icon" />
            </span>
            {feature}
          </li>
        ))}
      </ul>
      <Link className="pricing__link" to="/contact">
        GET PLAN
      </Link>
    </div>
  );
};

export default PricingItem;
