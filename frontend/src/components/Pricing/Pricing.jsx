import "./Pricing.scss";
import pricingData from "./PricingData";
import PricingItem from "./PricingItem";
import AnimationVariants from "../AnimationVariants/AnimationVariants";
import { motion, useInView } from "framer-motion";
import { useRef } from "react";

const Pricing = () => {
  const ref = useRef();
  const isInView = useInView(ref, { once: true });

  return (
    <motion.section
      variants={AnimationVariants.slideIn}
      initial="initial"
      animate={isInView ? "animate" : "initial"}
      ref={ref}
      className="pricing">
      <h2 className="pricing__title">Affordable Plans for Your Tech Needs</h2>
      <p className="pricing__subtitle">
        Choose the best plan that suits your requirements. Our plans are
        tailored for flexibility and value.
      </p>
      <div className="pricing__container">
        {pricingData.map((data) => (
          <PricingItem key={data.id} {...data} />
        ))}
      </div>
    </motion.section>
  );
};

export default Pricing;
