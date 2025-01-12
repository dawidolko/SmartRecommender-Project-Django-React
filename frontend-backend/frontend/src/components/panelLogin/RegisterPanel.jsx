import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import "./PanelLogin.scss";

const RegisterPanel = () => {
  const [nickname, setNickname] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password1 !== password2) {
      toast.error("Passwords do not match.");
      console.log("[RegisterPanel] Passwords do not match.");
      return;
    }

    if (!nickname) {
      toast.error("Nickname is required.");
      console.log("[RegisterPanel] Nickname is empty; cannot register.");
      return;
    }
    console.log("[RegisterPanel] Sending register data:", {
      nickname,
      email,
      first_name: firstName,
      last_name: lastName,
      password: password1,
    });

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/register/", {
        nickname,
        email,
        first_name: firstName,
        last_name: lastName,
        password: password1,
      });

      console.log("[RegisterPanel] Response from /api/register:", response);

      toast.success(response.data.message || "Registered successfully!");

      setNickname("");
      setEmail("");
      setFirstName("");
      setLastName("");
      setPassword1("");
      setPassword2("");

      setTimeout(() => {
        window.location.href = "/login";
      }, 1000);
    } catch (error) {
      console.log("[RegisterPanel] Error while registering:", error);

      if (!error.response) {
        toast.error("Cannot connect to the server. Check network console.");
        return;
      }

      toast.error(error.response.data?.error || "An error occurred.");
    }
  };

  return (
    <div className="registerPanel">
      <div className="registerPanel__content">
        <h2 className="registerPanel__title">Create an account</h2>
        <p className="registerPanel__subtitle">Enter your details below.</p>

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

        <form className="registerPanel__form" onSubmit={handleSubmit}>
          <div className="registerPanel__inputGroup">
            <input
              type="text"
              className="registerPanel__input"
              placeholder="Nickname"
              required
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
            />
          </div>
          <div className="registerPanel__inputGroup">
            <input
              type="email"
              className="registerPanel__input"
              placeholder="Email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="registerPanel__inputGroup">
            <input
              type="text"
              className="registerPanel__input"
              placeholder="First Name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
            />
          </div>
          <div className="registerPanel__inputGroup">
            <input
              type="text"
              className="registerPanel__input"
              placeholder="Last Name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
            />
          </div>
          <div className="registerPanel__inputGroup">
            <input
              type="password"
              className="registerPanel__input"
              placeholder="Password"
              required
              value={password1}
              onChange={(e) => setPassword1(e.target.value)}
            />
          </div>
          <div className="registerPanel__inputGroup">
            <input
              type="password"
              className="registerPanel__input"
              placeholder="Confirm Password"
              required
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
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
