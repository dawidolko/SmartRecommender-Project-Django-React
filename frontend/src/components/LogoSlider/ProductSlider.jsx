import { useEffect, useState } from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import config from "../../config/config";

import "./ProductSlider.scss";
import axios from "axios";
import ProductSliderItem from "./ProductSliderItem";

const ProductSlider = () => {
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

  const settings = {
    dots: false,
    infinite: true,
    speed: 3000,
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: true,
    arrows: false,
    initialSlide: 0,
    autoplaySpeed: 4000,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
        },
      },
    ],
  };

  if (productsState.isLoading) {
    return <div className="slider">Loading...</div>;
  }

  return (
    <div className="slider">
      <div className="slider__wrapper">
        <Slider {...settings}>
          {productsState.products.map((product) => (
            <div key={product.id} className="slider__box">
              <ProductSliderItem {...product} />
            </div>
          ))}
        </Slider>
      </div>
    </div>
  );
};

export default ProductSlider;
