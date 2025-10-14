import React from "react";
import { motion } from "framer-motion";
import "./AdminPanel.scss";

const ConfirmationModal = ({ isOpen, onClose, onConfirm, title, message }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <motion.div
        className="modal-content"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -50 }}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button
            className="common-modal-close modal-close"
            onClick={onClose}
            aria-label="Close modal">
            ×
          </button>
        </div>
        <div className="modal-body">
          <p>{message}</p>
        </div>
        <div className="modal-footer">
          <button className="btn-cancel" onClick={onClose}>
            Cancel
          </button>
          <button className="btn-confirm" onClick={onConfirm}>
            Confirm
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default ConfirmationModal;
