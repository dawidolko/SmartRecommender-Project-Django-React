import { useState, useEffect, useRef } from "react";
import ShopProduct from "../ShopContent/ShopProduct";
import { useNavigate } from "react-router-dom";
import { motion, useInView } from "framer-motion";
import AnimationVariants from "../AnimationVariants/AnimationVariants";
import axios from "axios";
import config from "../../config/config";

const NewProducts = () => {
  const [randomProducts, setRandomProducts] = useState([]);
  const ref = useRef();
  const isInView = useInView(ref, { once: true });
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRandomProducts = async () => {
      try {
        const response = await axios.get(
          `${config.apiUrl}/api/random-products/`
        );
        const formattedProducts = response.data.map((product) => ({
          id: product.id,
          name: product.name,
          price: parseFloat(product.price),
          old_price: product.old_price ? parseFloat(product.old_price) : null,
          imgs: product.photos.map(
            (photo) => `${config.apiUrl}/media/${photo.path}`
          ),
          category: product.categories[0] || "N/A",
        }));
        setRandomProducts(formattedProducts.slice(0, 9));
      } catch (error) {
        console.error("Error fetching random products:", error);
      }
    };

    fetchRandomProducts();
  }, []);

  return (
    <motion.section
      variants={AnimationVariants.slideIn}
      initial="initial"
      animate={isInView ? "animate" : "initial"}
      ref={ref}
      className="shop container">
      <h2 className="shop__title">Our Latest Products</h2>
      <div className="shop__products">
        {randomProducts.length > 0 ? (
          randomProducts.map((product) => (
            <ShopProduct key={product.id} {...product} />
          ))
        ) : (
          <div className="loading-spinner"></div>
        )}
      </div>
      <button onClick={() => navigate("/shop")} className="shop__navigate">
        Explore All Products
      </button>
    </motion.section>
  );
};

export default NewProducts;
