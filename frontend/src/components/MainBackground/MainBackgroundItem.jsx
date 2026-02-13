import { Link } from "react-router-dom";
import { motion, useInView } from "framer-motion";
import { useRef, useState } from "react";
import AnimationVariants from "../AnimationVariants/AnimationVariants";

import logoWheel from "../../assets/logo-wheel.webp";

const MainBackgroundItem = ({ item, currentSlide }) => {
  const ref = useRef();
  const isInView = useInView(ref, { once: true });
  const [imgError, setImgError] = useState(false);
  const [logoError, setLogoError] = useState(false);

  return (
    <div
      className="mainBackground__slider"
      style={{ transform: `translateX(-${currentSlide * 100}vw)` }}>
      <div className="mainBackground__img">
        <img
          className="mainBackground__image"
          src={imgError ? "/placeholder.jpg" : item.img}
          alt={item.alt}
          onError={() => setImgError(true)}
        />
      </div>

      <div className="mainBackground__content">
        <motion.img
          src={logoError ? "/placeholder.jpg" : logoWheel}
          alt="Logo Wheel"
          className="mainBackground__logo"
          initial={{ opacity: 0, scale: 0.5, rotate: -180 }}
          animate={{ opacity: 1, scale: 1, rotate: 0 }}
          transition={{ duration: 1.5, ease: "easeInOut" }}
          whileHover={{ scale: 1.1, rotate: 10 }}
          onError={() => setLogoError(true)}
        />

        <motion.h1
          variants={AnimationVariants.fadeIn}
          initial="initial"
          animate={isInView ? "animate" : "initial"}
          ref={ref}
          className="mainBackground__title">
          {item.title}
        </motion.h1>

        <motion.p
          variants={AnimationVariants.fadeIn2}
          initial="initial"
          animate={isInView ? "animate" : "initial"}
          ref={ref}
          className="mainBackground__text">
          {item.text}
        </motion.p>

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
