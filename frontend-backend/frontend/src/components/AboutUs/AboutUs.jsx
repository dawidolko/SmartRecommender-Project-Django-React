import AboutContent from "../AboutContent/AboutContent";
import about from "../../assets/about.webp";

const AboutUs = () => {
  return (
    <>
      <AboutContent
        img={about}
        alt="An electronics shop showcasing laptops, smartphones, and accessories."
        title="Discover the Future of"
        span="Technology with SmartRecommender"
        text="At SmartRecommender, we are committed to providing the latest in computers, electronics, and accessories. Our mission is to deliver exceptional value, combining innovative products with professional support. Whether you're looking for the newest laptop, cutting-edge smartphone, or high-quality peripherals, we have everything you need. Explore our wide selection, experience seamless shopping, and join our community of tech enthusiasts."
      />
    </>
  );
};

export default AboutUs;
