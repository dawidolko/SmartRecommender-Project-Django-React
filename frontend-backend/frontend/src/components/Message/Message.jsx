import "./Message.scss";
import { Link } from "react-router-dom";
import { AiOutlineMail } from "react-icons/ai";

const Message = () => {
  return (
    <section className="message">
      <h2 className="message__title">Get in Touch</h2>
      <p className="message__text">
        Have questions or need assistance? Contact us today and let us know how
        we can help. Our team is ready to assist you!
      </p>
      <Link className="message__link" to="/contact">
        <AiOutlineMail className="message__icon" />
        SEND US A MESSAGE
      </Link>
    </section>
  );
};

export default Message;
