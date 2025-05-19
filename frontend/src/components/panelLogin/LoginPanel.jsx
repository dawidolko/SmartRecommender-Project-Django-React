/* eslint-disable react-hooks/exhaustive-deps */
import { useState, useContext, useEffect } from "react";
import { AuthContext } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";
import "./PanelLogin.scss";
import config from "../../config/config";

const LoginPanel = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const [submitForm, setSubmitForm] = useState(false);

  const handleLogin = async () => {
    if (!email || !password) {
      toast.error("Please enter email and password.");
      return;
    }

    try {
      const response = await axios.post(`${config.apiUrl}/api/token/`, {
        email,
        password,
      });

      const { access } = response.data;
      login(access);
      localStorage.setItem("access", access);

      const decoded = JSON.parse(atob(access.split(".")[1]));
      localStorage.setItem("loggedUser", JSON.stringify(decoded));

      toast.success("Logged in successfully!");

      setTimeout(() => {
        navigate(decoded.role === "admin" ? "/admin" : "/client");
      }, 500);
    } catch (error) {
      toast.error(error.response?.data?.error || "Invalid email or password.");
    }
  };

  useEffect(() => {
    if (submitForm) {
      handleLogin();
      setSubmitForm(false);
    }
  }, [submitForm]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitForm(true);
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        setSubmitForm(true);
      }
    };

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  return (
    <div className="loginPanel">
      <div className="loginPanel__container">
        <div className="loginPanel__image"></div>

        <form className="loginPanel__form" onSubmit={handleSubmit}>
          <h2>Welcome back</h2>
          <p>Please enter your details to log in.</p>

          <div className="floating-label">
            <input
              type="email"
              id="email"
              name="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="floating-label">
            <input
              type="password"
              id="password"
              name="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="loginPanel__buttons">
            <button type="button" onClick={() => setSubmitForm(true)}>
              Log in
            </button>
            <span className="loginPanel__or">OR</span>
            <button
              type="button"
              className="loginPanel__signupBtn"
              onClick={() => navigate("/signup")}>
              Sign Up
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPanel;
