import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { CartContext } from "../ShopContext/ShopContext";
import CartModal from "./CartModal";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import axios from "axios";

const TotalAmount = () => {
  const { totalAmount, totalCartItems, resetCart, items } =
    useContext(CartContext);
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const formattedTotalAmount =
    typeof totalAmount() === "number" ? totalAmount().toFixed(2) : "0.00";

  const handleCheckout = async () => {
    const loggedUser = JSON.parse(localStorage.getItem("loggedUser"));

    if (!loggedUser) {
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

    try {
      await axios.post("http://localhost:8000/api/orders/", {
        userId: loggedUser.id,
        items,
        total: totalAmount(),
      });
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
    <div className="cart__info">
      <ToastContainer />
      <h3 className="cart__info-title">Cart Total</h3>
      <p className="cart__total-amount">Total Price: ${formattedTotalAmount}</p>
      <p className="cart__total-amount">Total Items: {totalCartItems()}</p>
      <div className="cart__buttons">
        <button className="cart__btn" onClick={() => navigate("/shop")}>
          Continue Shopping
        </button>
        <button className="cart__btn" onClick={handleCheckout}>
          Checkout
        </button>
      </div>
      <CartModal isOpen={isModalOpen} closeModal={closeModal} />
    </div>
  );
};

export default TotalAmount;
