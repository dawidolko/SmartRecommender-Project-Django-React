/**
 * ContactContent Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Contact page component with contact information boxes and inquiry form.
 * Provides multiple ways for users to reach the company.
 *
 * Features:
 *   - Contact information boxes (phone, email, address, hours)
 *   - Contact form for inquiries
 *   - Responsive layout
 *   - Icon-based contact cards
 *   - Form validation
 *
 * Contact Methods:
 *   1. Phone - Direct call link
 *   2. Email - Mailto link
 *   3. Address - Google Maps integration
 *   4. Business Hours - Office availability
 *
 * Components:
 *   - ContactBox: Individual contact info card with icon
 *   - ContactForm: Form component for user inquiries
 *
 * Form Fields:
 *   - Name (required)
 *   - Email (required, validated)
 *   - Subject (required)
 *   - Message (required, textarea)
 *
 * Data Source:
 *   - BoxData.js - Array of contact information objects
 *   - Each box: {id, icon, title, content, link}
 *
 * @component
 * @returns {React.ReactElement} Contact page with info boxes and form
 */
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
