import { color, motion } from "framer-motion";
import AnimationVariants from "../AnimationVariants/AnimationVariants";
import FormComponent from "./FormComponent";
import { AiOutlineClose } from "react-icons/ai";

const ModalComponent = ({
  onClose,
  handleSubmit,
  setIsMessageSent,
  setMessage,
  isMessageSent,
  message,
}) => {
  const handleClose = () => {
    setIsMessageSent(false);
    setMessage("");
    onClose();
  };

  return (
    <motion.div
      variants={AnimationVariants.overlayAnimation}
      initial="initial"
      animate="animate"
      exit="exit"
      key="modal"
      onClick={handleClose}
      className="modal__overlay">
      <motion.div
        variants={AnimationVariants.modalAnimation}
        initial="initial"
        animate="animate"
        exit="exit"
        onClick={(e) => e.stopPropagation()}
        className="modal">
        <h2 style={{ color: "white" }} className="modal__title">
          Request a Callback
        </h2>
        <p className="modal__text">
          Enter your details below, and we will call you back within 30 seconds.
        </p>
        <FormComponent
          handleSubmit={handleSubmit}
          setIsMessageSent={setIsMessageSent}
          setMessage={setMessage}
          isMessageSent={isMessageSent}
          message={message}
        />
        <button
          className="modal__close modal__close--absolute"
          onClick={handleClose}
          aria-label="Close">
          <AiOutlineClose />
        </button>
      </motion.div>
    </motion.div>
  );
};

export default ModalComponent;
