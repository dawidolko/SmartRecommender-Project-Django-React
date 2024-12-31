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
              {/* Poniższy <p> jest pusty – wypełnia go obrazek w tle */}
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
