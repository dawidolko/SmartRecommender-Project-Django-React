import "./CallBack.scss";
import Modal from "../Modal/Modal";
import { FaPhoneVolume } from "react-icons/fa";
import { useState } from "react";

const CallBack = () => {
  const [openModal, setOpenModal] = useState(false);

  return (
    <section className="callBack">
      <h2 className="callBack__title">Expert Advice for All Your Tech Needs</h2>
      <FaPhoneVolume className="callBack__icon" />
      <p className="callBack__text">Request a FREE call back</p>
      <p>
        Our team of experts is here to assist you with any questions about our
        products or services.
      </p>
      <button className="callBack__btn" onClick={() => setOpenModal(true)}>
        Send Request
      </button>
      <Modal open={openModal} onClose={() => setOpenModal(false)} />
    </section>
  );
};

export default CallBack;
