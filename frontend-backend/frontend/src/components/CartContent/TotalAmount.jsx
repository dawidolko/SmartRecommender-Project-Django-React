import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { CartContext } from "../ShopContext/ShopContext";
import CartModal from "./CartModal";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const TotalAmount = () => {
  const { totalAmount, totalCartItems, resetCart, items } =
    useContext(CartContext);
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const formattedTotalAmount =
    typeof totalAmount() === "number" ? totalAmount().toFixed(2) : "0.00";

  const handleCheckout = () => {
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

    const clientOrders = JSON.parse(localStorage.getItem("clientOrders")) || [];
    const newOrder = {
      id: Date.now(),
      userId: loggedUser.id,
      items: items,
      total: totalAmount(),
    };

    clientOrders.push(newOrder);
    localStorage.setItem("clientOrders", JSON.stringify(clientOrders));

    openModal();
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
