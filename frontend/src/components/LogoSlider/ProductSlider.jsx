import { useEffect, useState } from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

import "./ProductSlider.scss";
import shopData from "../ShopContent/ShopData";
import ProductSliderItem from "./ProductSliderItem";

const ProductSlider = () => {
  const [randomProducts, setRandomProducts] = useState([]);

  useEffect(() => {
    const shuffled = [...shopData].sort(() => Math.random() - 0.5);
    const selected = shuffled.slice(0, 10);
    setRandomProducts(selected);
  }, []);

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

  return (
    <div className="slider">
      <div className="slider__wrapper">
        <Slider {...settings}>
          {randomProducts.map((product) => (
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
