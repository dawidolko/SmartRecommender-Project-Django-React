// src/components/panelLogin/LoginPanel.jsx

import React, { useState } from "react";
import "./PanelLogin.scss";
import accountData from "./AccountData";

/**
 * Panel logowania.
 * Sprawdza zarówno "wbudowanych" userów (accountData),
 * jak i tych zarejestrowanych w localStorage (key: "registeredUsers").
 */
const LoginPanel = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    // 1. Pobieramy zarejestrowanych userów z localStorage
    const storedUsers = localStorage.getItem("registeredUsers");
    let customUsersArray = [];

    if (storedUsers) {
      try {
        customUsersArray = JSON.parse(storedUsers);
        if (!Array.isArray(customUsersArray)) {
          customUsersArray = [];
        }
      } catch (err) {
        customUsersArray = [];
      }
    }

    // 2. Łączymy accountData + customUsersArray w jedną tablicę
    const allUsers = [...accountData, ...customUsersArray];

    // 3. Szukamy usera po emailu i haśle
    const foundUser = allUsers.find(
      (item) => item.email === email && item.password === password
    );

    if (foundUser) {
      // Ustawiamy w localStorage info o zalogowanym userze
      const userData = {
        id: foundUser.id,
        email: foundUser.email,
        role: foundUser.role,
      };
      localStorage.setItem("loggedUser", JSON.stringify(userData));

      // Przekierowanie w zależności od roli
      if (foundUser.role === "Admin") {
        window.location.href = "/admin";
      } else {
        window.location.href = "/client";
      }
    } else {
      setErrorMsg("Invalid email or password.");
    }
  };

  return (
    <div className="loginPanel">
      <div className="loginPanel__content">
        <h2 className="loginPanel__title">Welcome back</h2>
        <p className="loginPanel__subtitle">
          Welcome back, please enter your details.
        </p>

        <button className="loginPanel__googleBtn">
          <img
            className="loginPanel__googleIcon"
            src="https://static.cdnlogo.com/logos/g/35/google-icon.svg"
            alt="Google"
          />
          Log in with Google
        </button>

        <div className="loginPanel__divider">
          <span>or</span>
        </div>

        {errorMsg && (
          <div style={{ color: "red", marginBottom: "1em" }}>{errorMsg}</div>
        )}

        <form className="loginPanel__form" onSubmit={handleSubmit}>
          <div className="loginPanel__inputGroup">
            <input
              type="email"
              className="loginPanel__input"
              placeholder="Email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="loginPanel__inputGroup">
            <input
              type="password"
              className="loginPanel__input"
              placeholder="Password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button type="submit" className="loginPanel__submitBtn">
            Log in
          </button>
        </form>

        <div className="loginPanel__footer">
          <p>
            If you have not created an account yet, please{" "}
            <a href="/signup" className="loginPanel__link">
              Sign up for free
            </a>
            .
          </p>
        </div>
      </div>

      <div className="loginPanel__imageWrapper">
        <div className="loginPanel__overlay" />
      </div>
    </div>
  );
};

export default LoginPanel;
