import { useState, useEffect } from "react";
import shopData from "../ShopContent/ShopData";
import ShopProduct from "../ShopContent/ShopProduct";
import { useNavigate } from "react-router-dom";
import { useRef } from "react";
import { motion, useInView } from "framer-motion";
import AnimationVariants from "../AnimationVariants/AnimationVariants";

const NewProducts = () => {
  const [randomProducts, setRandomProducts] = useState([]);
  const ref = useRef();
  const isInView = useInView(ref, { once: true });
  const navigate = useNavigate();

  useEffect(() => {
    // Shuffle the products array and select the first 9 products
    const shuffledProducts = [...shopData].sort(() => Math.random() - 0.5);
    const selectedProducts = shuffledProducts.slice(0, 9);
    setRandomProducts(selectedProducts);
  }, []); // Empty dependency array ensures this runs once on component mount

  return (
    <motion.section
      variants={AnimationVariants.slideIn}
      initial="initial"
      animate={isInView ? "animate" : "initial"}
      ref={ref}
      className="shop container">
      <h2 className="shop__title">Our Latest Products</h2>
      <div className="shop__products">
        {randomProducts.map((product) => (
          <ShopProduct key={product.id} {...product} />
        ))}
      </div>
      <button onClick={() => navigate("/shop")} className="shop__navigate">
        Explore All Products
      </button>
    </motion.section>
  );
};

export default NewProducts;
