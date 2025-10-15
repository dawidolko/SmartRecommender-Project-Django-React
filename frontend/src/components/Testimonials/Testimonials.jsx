import { useEffect, useState } from "react";
import axios from "axios";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./Testimonials.scss";
import TestimonialsItem from "./TestimonialsItem";
import config from "../../config/config";

const Testimonials = () => {
  const [productsState, setProductsState] = useState({
    currentAlgorithm: null,
    products: [],
    isLoading: true,
  });

  useEffect(() => {
    const fetchData = async () => {
      setProductsState((prev) => ({ ...prev, isLoading: true }));
      try {
        const token = localStorage.getItem("access");
        if (token) {
          const settingsResponse = await axios.get(
            `${config.apiUrl}/api/recommendation-settings/`,
            { headers: { Authorization: `Bearer ${token}` } }
          );
          const algorithm =
            settingsResponse.data.active_algorithm || "collaborative";
          setProductsState((prev) => ({
            ...prev,
            currentAlgorithm: algorithm,
          }));

          await fetchProducts(algorithm, token);
        } else {
          await fetchProducts(null, null);
        }
      } catch (error) {
        console.error("Error in initial fetch:", error);
      } finally {
        setProductsState((prev) => ({ ...prev, isLoading: false }));
      }
    };

    fetchData();

    const handleStorageChange = (e) => {
      if (e.key === "recommendationAlgorithm") {
        setProductsState((prev) => ({
          ...prev,
          currentAlgorithm: e.newValue || "collaborative",
        }));
      }
    };

    const handleCustomEvent = (e) => {
      if (e.detail && e.detail.algorithm) {
        setProductsState((prev) => ({
          ...prev,
          currentAlgorithm: e.detail.algorithm,
        }));
      }
    };

    window.addEventListener("storage", handleStorageChange);
    window.addEventListener("algorithmChanged", handleCustomEvent);

    return () => {
      window.removeEventListener("storage", handleStorageChange);
      window.removeEventListener("algorithmChanged", handleCustomEvent);
    };
  }, []);

  useEffect(() => {
    if (productsState.currentAlgorithm !== null) {
      const token = localStorage.getItem("access");
      fetchProducts(productsState.currentAlgorithm, token);
    }
  }, [productsState.currentAlgorithm]);

  const fetchProducts = async (algorithm, token) => {
    try {
      if (token && algorithm) {
        try {
          const previewResponse = await axios.get(
            `${config.apiUrl}/api/recommendation-preview/?algorithm=${algorithm}`,
            { headers: { Authorization: `Bearer ${token}` } }
          );

          if (previewResponse.data && previewResponse.data.length > 0) {
            setProductsState((prev) => ({
              ...prev,
              products: previewResponse.data,
            }));
            return;
          }
        } catch (error) {
          console.error("Error fetching recommendations:", error);
        }
      }

      const response = await axios.get(`${config.apiUrl}/api/random-products/`);
      setProductsState((prev) => ({ ...prev, products: response.data }));
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const sliderSettings = {
    infinite: true,
    speed: 2000,
    slidesToShow: 3,
    slidesToScroll: 1,
    arrows: false,
    autoplay: true,
    autoplaySpeed: 4000,
    responsive: [
      {
        breakpoint: 1124,
        settings: {
          slidesToShow: 2,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,
        },
      },
    ],
  };

  const getTitle = () => {
    if (localStorage.getItem("access") && productsState.currentAlgorithm) {
      return productsState.currentAlgorithm === "collaborative"
        ? "Personalized Recommendations (Collaborative Filtering)"
        : productsState.currentAlgorithm === "content_based"
        ? "Personalized Recommendations (Content-Based)"
        : productsState.currentAlgorithm === "fuzzy_logic"
        ? "Personalized Recommendations (Fuzzy Logic)"
        : "Personalized Recommendations";
    }
    return "Discover Our Products";
  };

  const getSubtitle = () => {
    if (localStorage.getItem("access") && productsState.currentAlgorithm) {
      return productsState.currentAlgorithm === "collaborative"
        ? "Based on what users like you are buying"
        : productsState.currentAlgorithm === "content_based"
        ? "Based on products similar to your preferences"
        : productsState.currentAlgorithm === "fuzzy_logic"
        ? "Based on fuzzy logic matching your preferences with uncertainty modeling"
        : "Based on your shopping patterns";
    }
    return "Check out selected proposals from our product database – scroll to see more and test our recommendation system in action!";
  };

  if (productsState.isLoading) {
    return <div className="testimonials">Loading...</div>;
  }

  return (
    <section className="testimonials">
      <div className="testimonials__wrapper">
        <h2 className="testimonials__title">{getTitle()}</h2>
        <p className="testimonials__subtitle">{getSubtitle()}</p>

        <Slider {...sliderSettings}>
          {productsState.products.map((product) => (
            <TestimonialsItem key={product.id} {...product} />
          ))}
        </Slider>
      </div>
    </section>
  );
};

export default Testimonials;
