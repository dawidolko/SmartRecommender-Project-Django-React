const ContactBox = ({ link, target = "_self", icon, boxTitle, details }) => {
  return (
    <div className="contact__box">
      <a
        href={link}
        target={target}
        rel={target === "_blank" ? "noopener noreferrer" : undefined}
        className="contact__link">
        <span className="contact__icon">{icon}</span>
        <h3 className="contact__box-title">{boxTitle}</h3>
        <p className="contact__box-details">{details}</p>
      </a>
    </div>
  );
};

export default ContactBox;
