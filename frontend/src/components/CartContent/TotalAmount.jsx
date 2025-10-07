import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { CartContext } from "../ShopContext/ShopContext";
import CartModal from "./CartModal";
import { toast } from "react-toastify";
import axios from "axios";
import config from "../../config/config";

const TotalAmount = () => {
  const { totalAmount, totalCartItems, resetCart, items } =
    useContext(CartContext);
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const formattedTotalAmount =
    typeof totalAmount() === "number" ? totalAmount().toFixed(2) : "0.00";

  const handleCheckout = async () => {
    const loggedUser = JSON.parse(localStorage.getItem("loggedUser"));
    const token = localStorage.getItem("access");

    if (!loggedUser || !token) {
      toast.error("You must be logged in to complete the purchase.", {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
      return;
    }

    const validItems = Object.entries(items).filter(
      ([itemId, quantity]) => quantity > 0
    );
    if (validItems.length === 0) {
      toast.error("Your cart is empty or contains items with zero quantity.", {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
      return;
    }

    setIsLoading(true);

    try {
      await axios.post(
        `${config.apiUrl}/api/orders/`,
        {
          items: Object.fromEntries(validItems),
          total: totalAmount(),
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      openModal();
    } catch (error) {
      console.error("Error during checkout:", error);
      toast.error("Checkout failed. Please try again.", {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    resetCart();
    navigate("/client");
  };

  return (
    <>
      <div className="cart__info">
        <h3 className="cart__info-title">Cart Total</h3>
        <p className="cart__total-amount">
          Total Price: ${formattedTotalAmount}
        </p>
        <p className="cart__total-amount">Total Items: {totalCartItems()}</p>
        <div className="cart__buttons">
          <button
            className="cart__btn"
            onClick={() => navigate("/shop")}
            disabled={isLoading}>
            Continue Shopping
          </button>
          <button
            className="cart__btn"
            onClick={handleCheckout}
            disabled={isLoading}>
            {isLoading ? "Processing..." : "Checkout"}
          </button>
        </div>
        <CartModal isOpen={isModalOpen} closeModal={closeModal} />
      </div>

      {isLoading && (
        <div className="cart__loading-overlay">
          <div className="cart__loading-spinner">
            <div className="cart__spinner"></div>
            <p>Processing your order...</p>
          </div>
        </div>
      )}
    </>
  );
};

export default TotalAmount;
