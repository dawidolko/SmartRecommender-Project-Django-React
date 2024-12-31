import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { CartContext } from "../ShopContext/ShopContext";
import CartModal from "./CartModal";

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
      // Wyświetlenie komunikatu o braku logowania
      showNotification("You must be logged in to complete the purchase.");
      return;
    }

    // Zapisujemy produkty w panelu klienta (localStorage)
    const clientOrders = JSON.parse(localStorage.getItem("clientOrders")) || [];
    const newOrder = {
      id: Date.now(),
      userId: loggedUser.id,
      items: items,
      total: totalAmount(),
    };

    clientOrders.push(newOrder);
    localStorage.setItem("clientOrders", JSON.stringify(clientOrders));

    // Reset koszyka i wyświetlenie potwierdzenia zakupu
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

  const showNotification = (message) => {
    const notification = document.createElement("div");
    notification.innerText = message;
    notification.className = "cart__notification";
    document.body.appendChild(notification);
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 3000);
  };

  return (
    <div className="cart__info">
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
