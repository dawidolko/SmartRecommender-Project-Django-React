/**
 * Hero Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Simple hero/banner component for page headers.
 * Displays a title with customizable styling via className prop.
 *
 * Features:
 *   - Flexible styling via className prop
 *   - Dynamic title text
 *   - Centered text layout
 *   - Responsive design
 *
 * Usage:
 *   <Hero cName="hero-shop" title="Our Products" />
 *   <Hero cName="hero-about" title="About Us" />
 *
 * @component
 * @param {Object} props
 * @param {string} props.cName - CSS class name for custom styling
 * @param {string} props.title - Hero title text to display
 * @returns {React.ReactElement} Hero section with title
 */
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
