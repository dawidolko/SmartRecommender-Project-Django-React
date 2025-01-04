import { useEffect, useState } from "react";
import axios from "axios";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./Testimonials.scss";
import TestimonialsItem from "./TestimonialsItem";

const Testimonials = () => {
  const [randomProducts, setRandomProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/random-products/"
        );
        setRandomProducts(response.data);
      } catch (error) {
        console.error("Error fetching random products:", error);
      }
    };

    fetchProducts();
  }, []);

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

  return (
    <section className="testimonials">
      <div className="testimonials__wrapper">
        <h2 className="testimonials__title">Explore Our Latest Products</h2>
        <p className="testimonials__subtitle">
          Check out a few random picks from our store – swipe to see more!
        </p>

        <Slider {...sliderSettings}>
          {randomProducts.map((product) => (
            <TestimonialsItem key={product.id} {...product} />
          ))}
        </Slider>
      </div>
    </section>
  );
};

export default Testimonials;
