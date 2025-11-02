/**
 * AboutContent Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Reusable about section component displaying company information with
 * image, title, description, and feature highlights.
 *
 * Features:
 *   - Flexible image and text layout
 *   - Customizable title with optional span highlight
 *   - Feature list with checkmark icons
 *   - Optional feature icons display
 *   - Responsive two-column layout
 *   - PropTypes validation
 *
 * Use Cases:
 *   - About page main content
 *   - Company mission statement
 *   - Product features showcase
 *   - Service highlights
 *
 * Feature Highlights (when showIcons=true):
 *   1. Advanced recommendation algorithms
 *   2. Multidimensional product analysis
 *   3. Personalized suggestions based on history
 *   4. Machine learning improvements
 *
 * Props:
 *   @param {string} img - Image URL/path
 *   @param {string} alt - Image alt text for accessibility
 *   @param {string} title - Main section title
 *   @param {string} [span=""] - Optional highlighted text in title
 *   @param {string} text - Main description paragraph
 *   @param {boolean} [showIcons=true] - Toggle feature list display
 *
 * Layout:
 *   - Left: Featured image
 *   - Right: Title, description, feature list
 *
 * Icons:
 *   - GiCheckMark - Feature bullet points
 *
 * @component
 * @returns {React.ReactElement} About section with image and content
 */
import "./AboutContent.scss";
import { GiCheckMark } from "react-icons/gi";
import PropTypes from "prop-types";

const AboutContent = ({
  img,
  alt,
  title,
  span = "",
  text,
  showIcons = true,
}) => {
  return (
    <section className="about">
      <div className="about__container container">
        <div className="about__img-container">
          <img className="about__img" src={img} alt={alt} />
        </div>
        <div className="about__content">
          <h2 className="about__title">
            {title}
            <span className="about__span"> {span} </span>
          </h2>
          <p className="about__text">{text}</p>
          {showIcons && (
            <>
              <p className="about__marks">
                <GiCheckMark className="about__mark" />
                Advanced recommendation algorithms considering individual
                preferences
              </p>
              <p className="about__marks">
                <GiCheckMark className="about__mark" />
                Multidimensional analysis of product technical parameters
              </p>
              <p className="about__marks">
                <GiCheckMark className="about__mark" />
                Personalized suggestions based on browsing history and
                interactions
              </p>
              <p className="about__marks">
                <GiCheckMark className="about__mark" />
                Continuous system improvement through machine learning
              </p>
            </>
          )}
        </div>
      </div>
    </section>
  );
};

AboutContent.propTypes = {
  img: PropTypes.string.isRequired,
  alt: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  span: PropTypes.string,
  text: PropTypes.string.isRequired,
  showIcons: PropTypes.bool,
};

export default AboutContent;
