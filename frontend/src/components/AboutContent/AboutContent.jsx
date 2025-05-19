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
                <GiCheckMark className="about__mark" />Advanced recommendation algorithms considering individual preferences
              </p>
              <p className="about__marks">
                <GiCheckMark className="about__mark" />
                Multidimensional analysis of product technical parameters
              </p>
              <p className="about__marks">
                <GiCheckMark className="about__mark" />
                Personalized suggestions based on browsing history and interactions
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
