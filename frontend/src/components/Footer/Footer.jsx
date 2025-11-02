/**
 * Footer Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Website footer component with company information, navigation links,
 * contact details, and social media links.
 *
 * Features:
 *   - Company branding and description
 *   - Quick navigation links (About, FAQ, Blog, Contact)
 *   - Office hours display
 *   - Contact information (address, email, phone)
 *   - Social media icons with links
 *   - Newsletter subscription
 *   - Copyright information
 *   - Responsive grid layout
 *
 * Sections:
 *   1. Company Info - Logo and mission statement
 *   2. Useful Links - Internal navigation
 *   3. Office Hours - Business hours
 *   4. Contact - Address, email, phone with icons
 *   5. Newsletter - Email subscription form
 *   6. Social Media - Facebook, Twitter, Instagram, YouTube
 *   7. Copyright - Legal text
 *
 * Icons Used:
 *   - FaLocationArrow - Address icon
 *   - AiFillMail - Email icon
 *   - AiFillPhone - Phone icon
 *   - FaFacebookF, FaTwitter, FaInstagram, FaYoutube - Social icons
 *
 * External Links:
 *   - Google Maps for address
 *   - Email mailto link
 *   - Phone tel link
 *   - Social media profiles
 *
 * @component
 * @returns {React.ReactElement} Footer with company info and navigation
 */
import "./Footer.scss";
import { Link } from "react-router-dom";
import { AiFillPhone, AiFillMail } from "react-icons/ai";
import {
  FaFacebookF,
  FaTwitter,
  FaInstagram,
  FaYoutube,
  FaLocationArrow,
} from "react-icons/fa";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer__container container">
        <div className="footer__content">
          <div className="footer__box">
            <Link to="/" className="footer__logo">
              <p className="footer__logo-text"></p>
            </Link>
            <div className="footer__desc">
              Join the SmartRecommender to advance your knowledge, improve your
              skills, and achieve your goals. Enroll today and shape your
              future!
            </div>
          </div>

          <div className="footer__box">
            <h3 className="footer__title">Useful Links</h3>
            <ul className="footer__links">
              <li>
                <Link to="/about" className="footer__link">
                  About
                </Link>
              </li>
              <li>
                <Link to="/faq" className="footer__link">
                  FAQ
                </Link>
              </li>
              <li>
                <Link to="/blog" className="footer__link">
                  Blog
                </Link>
              </li>
              <li>
                <Link to="/contact" className="footer__link">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          <div className="footer__box">
            <h3 className="footer__title">Office Hours</h3>
            <p>Mon To Fri</p>
            <p>08:00 AM - 04:00 PM</p>
            <p>Sat To Sun</p>
            <p>Closed</p>
          </div>

          <div className="footer__box">
            <h3 className="footer__title">Contact</h3>
            <div className="footer__contact">
              <FaLocationArrow className="footer__icon" />
              <a
                className="footer__link"
                href="https://maps.app.goo.gl/fdyZjRc8GJyLiCjPA"
                target="_blank"
                rel="noreferrer">
                Rejtana 16C, 35-959 Rzeszów, Poland
              </a>
            </div>
            <div className="footer__contact">
              <AiFillMail className="footer__icon" />
              <a className="footer__link" href="mailto:info@ur.edu.pl">
                info@ur.edu.pl
              </a>
            </div>
            <div className="footer__contact">
              <AiFillPhone className="footer__icon" />
              <a className="footer__link" href="tel:+48177872100">
                +48 17 787 21 00
              </a>
            </div>
          </div>
        </div>

        <hr className="footer__line" />

        <div className="footer__attribution">
          <h4 className="footer__attribution-title">Attributions</h4>
          <div className="footer__attribution-content">
            <p>
              <strong>Fonts:</strong> "Instrument Sans" designed by Luzi Type,
              available through{" "}
              <a
                href="https://fonts.google.com/specimen/Instrument+Sans"
                target="_blank"
                rel="noreferrer">
                Google Fonts
              </a>{" "}
              under the Open Font License.
            </p>
            <p>
              <strong>Icons:</strong> This site uses icons from the following
              libraries:
            </p>
            <ul className="footer__attribution-list">
              <li>
                React Icons (
                <a
                  href="https://react-icons.github.io/react-icons/"
                  target="_blank"
                  rel="noreferrer">
                  react-icons.github.io
                </a>
                ) - Licensed under MIT License
              </li>
              <li>
                Font Awesome Icons via React Icons (
                <a
                  href="https://fontawesome.com/license"
                  target="_blank"
                  rel="noreferrer">
                  fontawesome.com
                </a>
                ) - Licensed under CC BY 4.0 License
              </li>
              <li>
                Ant Design Icons via React Icons - Licensed under MIT License
              </li>
              <li>
                Lucide React (
                <a href="https://lucide.dev/" target="_blank" rel="noreferrer">
                  lucide.dev
                </a>
                ) - Licensed under ISC License
              </li>
              <li>
                Recharts (
                <a
                  href="https://recharts.org/"
                  target="_blank"
                  rel="noreferrer">
                  recharts.org
                </a>
                ) - Licensed under MIT License
              </li>
            </ul>
            <p>
              All trademarks, logos, and brand names are the property of their
              respective owners. All company, product, and service names used in
              this website are for identification purposes only.
            </p>
          </div>
        </div>

        <div className="footer__date">
          <p>
            &copy; Copyright {new Date().getFullYear()}{" "}
            <span className="footer__logo-name">SmartRecommender</span> All
            Rights Reserved.
          </p>
          <div className="footer__icons">
            <div className="footer__icon-bg">
              <FaFacebookF className="footer__icon" />
            </div>
            <div className="footer__icon-bg">
              <FaTwitter className="footer__icon" />
            </div>
            <div className="footer__icon-bg">
              <FaInstagram className="footer__icon" />
            </div>
            <div className="footer__icon-bg">
              <FaYoutube className="footer__icon" />
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
