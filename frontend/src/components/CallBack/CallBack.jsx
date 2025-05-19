import "./CallBack.scss";
import Modal from "../Modal/Modal";
import { FaPhoneVolume } from "react-icons/fa";
import { useState } from "react";

const CallBack = () => {
  const [openModal, setOpenModal] = useState(false);

  return (
    <section className="callBack">
      <h2 className="callBack__title">
        Advanced Research-Based Recommendation Methods
      </h2>
      <FaPhoneVolume className="callBack__icon" />

      <p className="callBack__text">Consult with us for FREE</p>
      <p className="callBack__ptext">
        Our system integrates sophisticated techniques such as collaborative filtering, content-based filtering, probabilistic models, fuzzy logic decision systems, and sentiment analysis. We leverage these methods to create a highly personalized shopping experience, drawing on both user data and product attributes. The system analyzes purchase patterns, technical preferences, and contextual information to ensure optimal recommendations. If you want to learn more about how these algorithms form the foundation of our engineering project, our experts are here to help.
      </p>

      <button className="callBack__btn" onClick={() => setOpenModal(true)}>
        Send Request
      </button>
      <Modal open={openModal} onClose={() => setOpenModal(false)} />
    </section>
  );
};

export default CallBack;
