import React, { useState, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";
import "./PanelLogin.scss";

const LoginPanel = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email) {
      toast.error("Email is required.");
      return;
    }
    if (!password) {
      toast.error("Password is required.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/token/", {
        email,
        password,
      });

      const { access, refresh } = response.data;
      login(access);

      toast.success("Logged in successfully!");

      setTimeout(() => {
        const decoded = JSON.parse(atob(access.split(".")[1]));
        if (decoded.role === "admin") {
          navigate("/admin");
        } else {
          navigate("/client");
        }
      }, 500);
    } catch (error) {
      console.error("[LoginPanel] Error while logging in:", error);

      if (!error.response) {
        toast.error("Cannot connect to the server. Check your connection.");
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
