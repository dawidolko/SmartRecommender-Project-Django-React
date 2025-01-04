import "./Hero.scss";

const Hero = ({ cName, title }) => {
  return (
    <section className="hero">
      <div className={cName}>
        <h2 className="hero__title">{title}</h2>
      </div>
    </section>
  );
};

export default Hero;
