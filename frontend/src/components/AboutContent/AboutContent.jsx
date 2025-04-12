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
    <section className="about container">
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
                <GiCheckMark className="about__mark" />A wide selection of the
                latest electronics and accessories
              </p>
              <p className="about__marks">
                <GiCheckMark className="about__mark" />
                Professional technical support and advice
              </p>
              <p className="about__marks">
                <GiCheckMark className="about__mark" />
                Quality assurance and fast delivery
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
