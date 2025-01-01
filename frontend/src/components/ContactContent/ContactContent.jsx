import "./ContactContent.scss";
import boxData from "./BoxData";
import ContactBox from "./ContactBox";
import ContactForm from "./ContactForm";

const ContactContent = () => {
  return (
    <section className="contact">
      <div className="contact__container">
        <div className="contact__boxes">
          {boxData.map((box) => (
            <ContactBox {...box} key={box.id} />
          ))}
        </div>

        <div className="contact__wrapper">
          <h2 className="contact__form-title">Get in Touch</h2>
          <p className="contact__form-description">
            If you have any questions or need assistance, feel free to reach out
            to us using the form below.
          </p>

          <ContactForm />
        </div>
      </div>
    </section>
  );
};

export default ContactContent;
