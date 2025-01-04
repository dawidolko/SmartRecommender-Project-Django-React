import { Route, Routes, useLocation, Navigate } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Navbar from "./components/Navbar/Navbar";
import Home from "./pages/Home";
import About from "./pages/About";
import Faq from "./pages/Faq";
import Blog from "./pages/Blog";
import BlogId from "./components/BlogContent/Article/Article";
import Contact from "./pages/Contact";
import Footer from "./components/Footer/Footer";
import NotFound from "./components/NotFound/NotFound";
import Shop from "./pages/Shop";
import Cart from "./pages/Cart";
import Favorites from "./pages/Favorites";
import { FavoritesProvider } from "./components/FavoritesContent/FavoritesContext";
import ShopContext from "./components/ShopContext/ShopContext";
import ProductSection from "./pages/ProductSection";
import LoginPanel from "./components/panelLogin/LoginPanel";
import RegisterPanel from "./components/panelLogin/RegisterPanel";
import AdminPanel from "./pages/AdminPanel";
import ClientPanel from "./pages/ClientPanel";

function App() {
  const location = useLocation();

  return (
    <>
      <FavoritesProvider>
        <ShopContext>
          <Navbar />
          <ToastContainer
            position="top-center"
            autoClose={3000}
            hideProgressBar={true}
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
            theme="colored"
          />
          <AnimatePresence mode="sync" initial={false}>
            <Routes location={location} key={location.pathname}>
              <Route path="/" element={<Navigate to="/home" />} />
              <Route path="/home" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/shop" element={<Shop />} />
              <Route path="/faq" element={<Faq />} />
              <Route path="/blog" element={<Blog />} />
              <Route path="/blog/:id" element={<BlogId />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/cart" element={<Cart />} />
              <Route path="/favorites" element={<Favorites />} />
              <Route path="/product/:id" element={<ProductSection />} />
              <Route path="/login" element={<LoginPanel />} />
              <Route path="/signup" element={<RegisterPanel />} />
              <Route path="/admin" element={<AdminPanel />} />
              <Route path="/client" element={<ClientPanel />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </AnimatePresence>
          <Footer />
        </ShopContext>
      </FavoritesProvider>
    </>
  );
}

export default App;
