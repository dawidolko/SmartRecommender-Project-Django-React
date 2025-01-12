import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import "./PanelLogin.scss";

const LoginPanel = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email) {
      toast.error("Email is required.");
      console.log("[LoginPanel] Email is empty; cannot login.");
      return;
    }
    if (!password) {
      toast.error("Password is required.");
      console.log("[LoginPanel] Password is empty; cannot login.");
      return;
    }

    console.log("[LoginPanel] Sending login data:", { email, password });

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/login/", {
        email,
        password,
      });

      console.log("[LoginPanel] Response from /api/login:", response);

      const { user } = response.data;
      localStorage.setItem("loggedUser", JSON.stringify(user));

      toast.success("Logged in successfully!");

      setTimeout(() => {
        if (user.role === "admin") {
          window.location.href = "/admin";
        } else {
          window.location.href = "/client";
        }
      }, 500);
    } catch (error) {
      console.log("[LoginPanel] Error while logging in:", error);

      if (!error.response) {
        toast.error("Cannot connect to the server. Check network console.");
        return;
      }

      toast.error(error.response.data?.error || "Invalid email or password.");
    }
  };

  return (
    <div className="loginPanel">
      <div className="loginPanel__content">
        <h2 className="loginPanel__title">Welcome back</h2>
        <p className="loginPanel__subtitle">
          Please enter your details to log in.
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
