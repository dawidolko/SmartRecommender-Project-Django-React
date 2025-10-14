import React, { useEffect } from "react";
import "./Modal.scss";

const Modal = ({ isOpen, onClose, title, children }) => {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }

    return () => {
      document.body.style.overflow = "auto";
    };
  }, [isOpen]);

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="modal-content2">
        <div className="modal-header2">
          <h2>{title}</h2>
          <button
            className="common-modal-close close-button"
            onClick={onClose}
            aria-label="Close modal">
            ×
          </button>
        </div>
        <div className="modal-body2">{children}</div>
      </div>
    </div>
  );
};

export default Modal;
