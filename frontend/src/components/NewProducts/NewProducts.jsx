import { useState, useEffect, useRef } from "react";
import ShopProduct from "../ShopContent/ShopProduct";
import { useNavigate } from "react-router-dom";
import { motion, useInView } from "framer-motion";
import AnimationVariants from "../AnimationVariants/AnimationVariants";
import axios from "axios";
import config from "../../config/config";

const NewProducts = () => {
  const [randomProducts, setRandomProducts] = useState([]);
  const [currentAlgorithm, setCurrentAlgorithm] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const ref = useRef();
  const isInView = useInView(ref, { once: true });
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const token = localStorage.getItem("access");
        if (token) {
          const settingsResponse = await axios.get(
            `${config.apiUrl}/api/recommendation-settings/`,
            { headers: { Authorization: `Bearer ${token}` } }
          );
          const algorithm =
            settingsResponse.data.active_algorithm || "collaborative";
          setCurrentAlgorithm(algorithm);

          await fetchProducts(algorithm, token);
        } else {
          await fetchProducts(null, null);
        }
      } catch (error) {
        console.error("Error in initial fetch:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const fetchProducts = async (algorithm, token) => {
    try {
      if (token && algorithm) {
        try {
          const previewResponse = await axios.get(
            `${config.apiUrl}/api/recommendation-preview/?algorithm=${algorithm}`,
            { headers: { Authorization: `Bearer ${token}` } }
          );

          if (previewResponse.data && previewResponse.data.length > 0) {
            const formattedProducts = previewResponse.data.map((product) => ({
              id: product.id,
              name: product.name,
              price: parseFloat(product.price),
              old_price: product.old_price
                ? parseFloat(product.old_price)
                : null,
              imgs: product.photos.map(
                (photo) => `${config.apiUrl}/media/${photo.path}`
              ),
              category: product.categories?.[0] || "N/A",
            }));
            setRandomProducts(formattedProducts.slice(0, 9));
            return;
          }
        } catch (error) {
          console.error("Error fetching recommendations:", error);
        }
      }

      const response = await axios.get(`${config.apiUrl}/api/random-products/`);
      const formattedProducts = response.data.map((product) => ({
        id: product.id,
        name: product.name,
        price: parseFloat(product.price),
        old_price: product.old_price ? parseFloat(product.old_price) : null,
        imgs: product.photos.map(
          (photo) => `${config.apiUrl}/media/${photo.path}`
        ),
        category: product.categories?.[0] || "N/A",
      }));
      setRandomProducts(formattedProducts.slice(0, 9));
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const getTitle = () => {
    if (currentAlgorithm) {
      return currentAlgorithm === "collaborative"
        ? "Recommended for You (Collaborative Filtering)"
        : currentAlgorithm === "content_based"
        ? "Recommended for You (Content-Based)"
        : currentAlgorithm === "fuzzy_logic"
        ? "Recommended for You (Fuzzy Logic)"
        : "Recommended for You";
    }
    return "Our Latest Products";
  };

  if (isLoading) {
    return (
      <motion.section
        variants={AnimationVariants.slideIn}
        initial="initial"
        animate={isInView ? "animate" : "initial"}
        ref={ref}
        className="shop container">
        <div className="loading-spinner"></div>
      </motion.section>
    );
  }

  return (
    <motion.section
      variants={AnimationVariants.slideIn}
      initial="initial"
      animate={isInView ? "animate" : "initial"}
      ref={ref}
      className="shop container">
      <h2 className="shop__title">{getTitle()}</h2>
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
