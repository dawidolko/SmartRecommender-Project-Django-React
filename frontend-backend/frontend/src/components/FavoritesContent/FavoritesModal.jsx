import "./FavoritesContent.scss";
import { motion, AnimatePresence } from "framer-motion";
import AnimationVariants from "../AnimationVariants/AnimationVariants";

const FavoritesModal = ({ isOpen, closeModal }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          variants={AnimationVariants.overlayAnimation}
          initial="initial"
          animate="animate"
          exit="exit"
          key="modal"
          className="favorites__modal-overlay">
          <motion.div
            variants={AnimationVariants.modalAnimation}
            initial="initial"
            animate="animate"
            exit="exit"
            className="favorites__modal">
            <h2 className="favorites__modal-title">Moved to Cart</h2>
            <p className="favorites__modal-text">
              Your item has been successfully moved to the cart.
            </p>
            <button className="favorites__modal-btn" onClick={closeModal}>
              Close
            </button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default FavoritesModal;
