/**
 * NewProducts Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Homepage component displaying personalized product recommendations or
 * random products for non-authenticated users.
 *
 * Features:
 *   - Personalized recommendations for logged-in users
 *   - Random products for guests
 *   - Multiple recommendation algorithms:
 *     * Collaborative Filtering - Based on similar users
 *     * Content-Based Filtering - Based on product attributes
 *     * Fuzzy Logic - Based on fuzzy user profile
 *   - Algorithm name display in section title
 *   - Animated entrance with Framer Motion
 *   - Intersection Observer (appears when scrolled into view)
 *   - Loading skeleton/state
 *   - Navigation to shop page
 *
 * Algorithm Selection:
 *   1. Checks user's active algorithm preference from settings
 *   2. Falls back to collaborative filtering if not set
 *   3. For guests: displays random products
 *
 * API Endpoints:
 *   - GET /api/recommendation-settings/ - Get user's algorithm preference
 *   - GET /api/recommendation-preview/?algorithm={alg} - Get personalized recommendations
 *   - GET /api/random-products/ - Get random products for guests
 *
 * State Management:
 *   - randomProducts: Array of products to display (recommendations or random)
 *   - currentAlgorithm: Active recommendation algorithm name
 *   - isLoading: Loading state for async fetch
 *   - isInView: Boolean from Intersection Observer (for animation trigger)
 *
 * Display Logic:
 *   - Authenticated user with valid recommendations → Show recommended products
 *   - Authenticated user without recommendations → Show random products
 *   - Guest user → Show random products
 *
 * Animation:
 *   - Uses Framer Motion's useInView hook
 *   - Triggers animation when component scrolls into viewport
 *   - once: true - Animation plays only once
 *
 * @component
 * @returns {React.ReactElement} Product recommendation section for homepage
 */
import { useState, useEffect, useRef } from "react";
import ShopProduct from "../ShopContent/ShopProduct";
import { useNavigate } from "react-router-dom";
import { motion, useInView } from "framer-motion";
import AnimationVariants from "../AnimationVariants/AnimationVariants";
import axios from "axios";
import config from "../../config/config";
import { mockAPI, PLACEHOLDER_IMAGE } from "../../utils/mockData";

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
        if (config.useMockData) {
          // Use mock data for GitHub Pages
          await fetchProducts(null, null);
        } else {
          const token = localStorage.getItem("access");
          if (token) {
            const settingsResponse = await axios.get(
              `${config.apiUrl}/api/recommendation-settings/`,
              { headers: { Authorization: `Bearer ${token}` } },
            );
            const algorithm =
              settingsResponse.data.active_algorithm || "collaborative";
            setCurrentAlgorithm(algorithm);

            await fetchProducts(algorithm, token);
          } else {
            await fetchProducts(null, null);
          }
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
      if (config.useMockData) {
        // Use mock data for GitHub Pages
        const data = await mockAPI.getRandomProducts(9);
        const formattedProducts = data.map((product) => ({
          id: product.id,
          name: product.name,
          price: parseFloat(product.price),
          old_price: product.old_price ? parseFloat(product.old_price) : null,
          imgs: product.imgs || [PLACEHOLDER_IMAGE],
          category: product.category || "N/A",
        }));
        setRandomProducts(formattedProducts);
        return;
      }

      if (token && algorithm) {
        try {
          const previewResponse = await axios.get(
            `${config.apiUrl}/api/recommendation-preview/?algorithm=${algorithm}`,
            { headers: { Authorization: `Bearer ${token}` } },
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
                (photo) => `${config.apiUrl}/media/${photo.path}`,
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
          (photo) => `${config.apiUrl}/media/${photo.path}`,
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
