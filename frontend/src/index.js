import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { AuthProvider } from "./context/AuthContext";
import { CartProvider } from "./context/CartContext";
import { BrowserRouter } from "react-router-dom";

const root = ReactDOM.createRoot(document.getElementById("root"));

if (window.location.hostname === "localhost") {
  const originalFetch = window.fetch;
  window.fetch = (...args) => {
    if (args[0]?.includes("sentry.ekance.com")) {
      console.warn("[BLOCKED] Sentry request prevented:", args[0]);
      return Promise.resolve({ ok: true, status: 200 });
    }
    return originalFetch(...args);
  };

  const originalConsoleError = console.error;
  console.error = (...args) => {
    try {
      const msg = args && args[0];
      if (
        typeof msg === "string" &&
        (msg.includes('Each child in a list should have a unique "key" prop') ||
          msg.includes(
            'Warning: Each child in a list should have a unique "key" prop'
          ))
      ) {
        return;
      }
    } catch (_) {}
    return originalConsoleError(...args);
  };
}

root.render(
  <React.StrictMode>
    <AuthProvider>
      <BrowserRouter
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <CartProvider>
          <App />
        </CartProvider>
      </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>
);
