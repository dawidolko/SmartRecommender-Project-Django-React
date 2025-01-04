import FavoritesContent from "../components/FavoritesContent/FavoritesContent";
import Hero from "../components/Hero/Hero";

const Favorites = () => {
  return (
    <>
      <Hero title="Your Favorites items" cName="hero__img" />
      <FavoritesContent />
    </>
  );
};

export default Favorites;
