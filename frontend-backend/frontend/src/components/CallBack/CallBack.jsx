import "./CallBack.scss";
import Modal from "../Modal/Modal";
import { FaPhoneVolume } from "react-icons/fa";
import { useState } from "react";

const CallBack = () => {
  const [openModal, setOpenModal] = useState(false);

  return (
    <section className="callBack">
      <h2 className="callBack__title">
        Research-Driven Recommendation Methods
      </h2>
      <FaPhoneVolume className="callBack__icon" />

      <p className="callBack__text">Request a FREE consultation call</p>
      <p>
        Our team integrates advanced techniques such as Collaborative Filtering,
        Content-Based Filtering, Probabilistic Models, Fuzzy Decision Systems,
        and Sentiment-Based Analysis. We use these methods to develop a
        highly-personalized shopping experience, drawing on both user data and
        product attributes to ensure optimal recommendations. If you wish to
        learn more about how these algorithms form the backbone of our
        engineering project, our experts are here to help.
      </p>

      <button className="callBack__btn" onClick={() => setOpenModal(true)}>
        Send Request
      </button>
      <Modal open={openModal} onClose={() => setOpenModal(false)} />
    </section>
  );
};

export default CallBack;
