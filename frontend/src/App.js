import { Route, Routes, useLocation, Navigate } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import { ToastContainer } from "react-toastify";
import React, { useContext } from "react";
import { AuthContext } from "./context/AuthContext";
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
import SearchResults from "./components/Search/SearchResults";
import PublicRoute from "./components/PublicRoute/PublicRoute";

import AdminPanel from "./pages/AdminPanel";
import ClientPanel from "./pages/ClientPanel";
import ClientDashboard from "./components/ClientPanel/ClientDashboard";
import ClientOrders from "./components/ClientPanel/ClientOrders";
import ClientOrderDetail from "./components/ClientPanel/ClientOrderDetail";
import ClientComplaints from "./components/ClientPanel/ClientComplaints";
import ClientAccount from "./components/ClientPanel/ClientAccount";

import ScrollToTop from "./utils/ScrollToTop";

function PrivateRoute({ children, roles }) {
  const { user } = useContext(AuthContext);
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  if (!user.role || (roles && !roles.includes(user.role))) {
    console.warn("[PrivateRoute] Unauthorized access, redirecting...");
    setTimeout(() => {
      window.location.reload();
    }, 0);
    return <Navigate to="/" replace />;
  }

  return children;
}

function App() {
  const location = useLocation();

  return (
    <>
      <ScrollToTop />
      <FavoritesProvider>
        <ShopContext>
          {location.pathname.startsWith("/admin") ? null : <Navbar />}
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
              <Route path="/category/:category" element={<Shop />} />
              <Route path="/search/:query" element={<SearchResults />} />

              <Route
                path="/login"
                element={
                  <PublicRoute>
                    <LoginPanel />
                  </PublicRoute>
                }
              />
              <Route
                path="/signup"
                element={
                  <PublicRoute>
                    <RegisterPanel />
                  </PublicRoute>
                }
              />

              <Route
                path="/admin/*"
                element={
                  <PrivateRoute roles={["admin"]}>
                    <AdminPanel />
                  </PrivateRoute>
                }
              />
              <Route
                path="/client/*"
                element={
                  <PrivateRoute roles={["client"]}>
                    <ClientPanel />
                  </PrivateRoute>
                }>
                <Route index element={<ClientDashboard />} />
                <Route path="orders" element={<ClientOrders />} />
                <Route path="orders/:id" element={<ClientOrderDetail />} />
                <Route path="complaints" element={<ClientComplaints />} />
                <Route path="account" element={<ClientAccount />} />
              </Route>
              <Route path="*" element={<NotFound />} />
            </Routes>
          </AnimatePresence>
          {location.pathname.startsWith("/admin") ? null : <Footer />}
        </ShopContext>
      </FavoritesProvider>
    </>
  );
}

export default App;
