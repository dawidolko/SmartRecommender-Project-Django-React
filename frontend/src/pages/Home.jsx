import AnimatedPage from "../components/AnimatedPage/AnimatedPage";
import MainBackground from "../components/MainBackground/MainBackground";
import Technology from "../components/Technology/Technology";
import FixedBg from "../components/FixedBg/FixedBg";
import Pricing from "../components/Pricing/Pricing";
import Counter from "../components/Counter/Counter";
import Team from "../components/Team/Team";
import Testimonials from "../components/Testimonials/Testimonials";
import CallBack from "../components/CallBack/CallBack";
import LogoSlider from "../components/LogoSlider/LogoSlider";
import NewProducts from "../components/NewProducts/NewProducts";

const Home = () => {
  return (
    <AnimatedPage>
      <MainBackground />
      <Technology />
      <FixedBg
        cName="fixed"
        text="WHATEVER YOUR TECH NEEDS ARE…"
        title="… We’ve got the Perfect Solution for You!"
      />
      <NewProducts />
      <Counter />
      <Team />
      <FixedBg
        cName="fixed__secondary"
        text="Welcome to SmartRecommender…"
        title="… Your Partner in Smart Technology Choices!"
      />
      <Pricing />
      <Testimonials />
      <LogoSlider />
      <CallBack />
    </AnimatedPage>
  );
};

export default Home;
