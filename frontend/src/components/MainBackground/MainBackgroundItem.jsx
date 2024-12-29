import { Link } from "react-router-dom";
import { motion, useInView } from "framer-motion";
import { useRef } from "react";
import AnimationVariants from "../AnimationVariants/AnimationVariants";

// 1. Import logo:
import logoWheel from "../../assets/logo-wheel.webp";

const MainBackgroundItem = ({ item, currentSlide }) => {
  const ref = useRef();
  const isInView = useInView(ref, { once: true });

  return (
    <div
      className="mainBackground__slider"
      style={{ transform: `translateX(-${currentSlide * 100}vw)` }}>
      <div className="mainBackground__img">
        <img className="mainBackground__image" src={item.img} alt={item.alt} />
      </div>

      <div className="mainBackground__content">
        {/* 2. Logo nad tytułem (np. "NEVER STOP LEARNING") */}
        <motion.img
          src={logoWheel}
          alt="Logo Wheel"
          className="mainBackground__logo"
          // PRZYKŁADOWA animacja we Framer Motion
          initial={{ opacity: 0, scale: 0.5, rotate: -180 }}
          animate={{ opacity: 1, scale: 1, rotate: 0 }}
          transition={{ duration: 1.5, ease: "easeInOut" }}
          whileHover={{ scale: 1.1, rotate: 10 }}
        />

        {/* Tytuł */}
        <motion.h1
          variants={AnimationVariants.fadeIn}
          initial="initial"
          animate={isInView ? "animate" : "initial"}
          ref={ref}
          className="mainBackground__title">
          {item.title}
        </motion.h1>

        {/* Tekst */}
        <motion.p
          variants={AnimationVariants.fadeIn2}
          initial="initial"
          animate={isInView ? "animate" : "initial"}
          ref={ref}
          className="mainBackground__text">
          {item.text}
        </motion.p>

        {/* Przycisk/Link */}
        <motion.div
          variants={AnimationVariants.fadeIn2}
          initial="initial"
          animate={isInView ? "animate" : "initial"}
          ref={ref}>
          <Link className="mainBackground__link" to="/contact">
            Contact Us
          </Link>
        </motion.div>
      </div>
    </div>
  );
};

export default MainBackgroundItem;
