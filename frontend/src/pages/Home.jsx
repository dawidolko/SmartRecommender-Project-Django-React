import AnimatedPage from "../components/AnimatedPage/AnimatedPage";
import MainBackground from "../components/MainBackground/MainBackground";
import Technology from "../components/Technology/Technology";
import FixedBg from "../components/FixedBg/FixedBg";
import Pricing from "../components/Pricing/Pricing";
import Counter from "../components/Counter/Counter";
import Team from "../components/Team/Team";
import Testimonials from "../components/Testimonials/Testimonials";
import CallBack from "../components/CallBack/CallBack";
import ProductSlider from "../components/LogoSlider/ProductSlider";
import NewProducts from "../components/NewProducts/NewProducts";

const Home = () => {
  return (
    <AnimatedPage>
      <MainBackground />
      <Technology />
      <FixedBg
        cName="fixed"
        text="WHATEVER YOUR TECH NEEDS ARE…"
        title="… Our Recommendation System Will Find the Optimal Solution!"
      />
      <NewProducts />
      <Counter />
      <Team />
      <FixedBg
        cName="fixed__secondary"
        text="Welcome to SmartRecommender…"
        title="… Your Guide to the World of Technology!"
      />
      <Pricing />
      <Testimonials />
      <ProductSlider />
      <CallBack />
    </AnimatedPage>
  );
};

export default Home;
