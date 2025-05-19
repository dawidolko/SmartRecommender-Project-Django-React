import AboutContent from "../AboutContent/AboutContent";
import about from "../../assets/about.webp";

const AboutUs = () => {
  return (
    <>
      <AboutContent
        img={about}
        alt="An electronics shop showcasing laptops, smartphones, and accessories."
        title="Discover the Future of"
        span="Recommendations with SmartRecommender!"
        text="At SmartRecommender, we utilize advanced machine learning algorithms to provide intelligent recommendations for computers, electronics, and accessories. Our mission is to deliver exceptional value by combining precise product recommendations with professional technical support. Whether you're looking for a powerful laptop, modern smartphone, or specialized peripherals, our system will help you find the perfect match."
      />
    </>
  );
};

export default AboutUs;
