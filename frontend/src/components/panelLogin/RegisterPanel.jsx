// src/components/panelLogin/RegisterPanel.jsx

import React, { useState } from "react";
import "./PanelLogin.scss";

/**
 * Panel rejestracji.
 * Po rejestracji dane użytkownika zapisywane są w localStorage w kluczu "registeredUsers".
 * Domyślnie rejestrowany użytkownik ma rolę "Client".
 */
const RegisterPanel = () => {
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    // Walidacja czy hasła się zgadzają
    if (password1 !== password2) {
      setErrorMsg("Passwords do not match.");
      return;
    }

    // Pobieramy już zarejestrowanych użytkowników z localStorage
    const storedUsers = localStorage.getItem("registeredUsers");
    let usersArray = [];

    if (storedUsers) {
      try {
        usersArray = JSON.parse(storedUsers);
        if (!Array.isArray(usersArray)) {
          usersArray = [];
        }
      } catch (err) {
        usersArray = [];
      }
    }

    // Sprawdzamy, czy nie ma już konta o tym emailu
    const userExists = usersArray.some((user) => user.email === email);
    if (userExists) {
      setErrorMsg("An account with this email already exists.");
      return;
    }

    // Tworzymy nowego usera
    const newUser = {
      id: Date.now(), // losowe ID
      email: email,
      password: password1,
      role: "Client",
    };

    // Dodajemy do tablicy
    usersArray.push(newUser);

    // Zapisujemy w localStorage
    localStorage.setItem("registeredUsers", JSON.stringify(usersArray));

    // Czyścimy pola i komunikaty
    setEmail("");
    setPassword1("");
    setPassword2("");
    setErrorMsg("");
    setSuccessMsg("Account created successfully! You can now log in.");

    // Ewentualnie redirect po chwili:
    // setTimeout(() => {
    //   window.location.href = "/login";
    // }, 1500);
  };

  return (
    <div className="registerPanel">
      <div className="registerPanel__content">
        <h2 className="registerPanel__title">Welcome back</h2>
        <p className="registerPanel__subtitle">
          Welcome back, please enter your details.
        </p>

        <button className="registerPanel__googleBtn">
          <img
            className="registerPanel__googleIcon"
            src="https://static.cdnlogo.com/logos/g/35/google-icon.svg"
            alt="Google"
          />
          Sign Up with Google
        </button>

        <div className="registerPanel__divider">
          <span>or</span>
        </div>

        {/* Komunikaty o błędzie lub sukcesie */}
        {errorMsg && (
          <div style={{ color: "red", marginBottom: "1em" }}>{errorMsg}</div>
        )}
        {successMsg && (
          <div style={{ color: "green", marginBottom: "1em" }}>
            {successMsg}
          </div>
        )}

        <form className="registerPanel__form" onSubmit={handleSubmit}>
          <div className="registerPanel__inputGroup">
            <input
              type="email"
              className="registerPanel__input"
              placeholder="Email"
              required
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setErrorMsg("");
                setSuccessMsg("");
              }}
            />
          </div>
          <div className="registerPanel__inputGroup">
            <input
              type="password"
              className="registerPanel__input"
              placeholder="Password"
              required
              value={password1}
              onChange={(e) => {
                setPassword1(e.target.value);
                setErrorMsg("");
                setSuccessMsg("");
              }}
            />
          </div>
          <div className="registerPanel__inputGroup">
            <input
              type="password"
              className="registerPanel__input"
              placeholder="Confirm Password"
              required
              value={password2}
              onChange={(e) => {
                setPassword2(e.target.value);
                setErrorMsg("");
                setSuccessMsg("");
              }}
            />
          </div>

          <button type="submit" className="registerPanel__submitBtn">
            Create Account
          </button>
        </form>

        <div className="registerPanel__footer">
          <p>
            Already have an account?{" "}
            <a href="/login" className="registerPanel__link">
              Login
            </a>
            .
          </p>
        </div>
      </div>

      <div className="registerPanel__imageWrapper">
        <div className="registerPanel__overlay" />
      </div>
    </div>
  );
};

export default RegisterPanel;
