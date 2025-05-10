/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import "./RegisterPanel.scss";
import config from "../../config/config";

const RegisterPanel = () => {
  const navigate = useNavigate();
  const [nickname, setNickname] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [submitForm, setSubmitForm] = useState(false);

  const validateForm = () => {
    if (!nickname.trim()) {
      return "Nickname is required.";
    }
    if (!firstName.trim()) {
      return "First name is required.";
    }
    if (firstName.length > 50) {
      return "First name must not exceed 50 characters.";
    }
    if (!/^[A-Za-z]+$/.test(firstName)) {
      return "First name can contain only letters.";
    }
    if (!lastName.trim()) {
      return "Last name is required.";
    }
    if (lastName.length > 50) {
      return "Last name must not exceed 50 characters.";
    }
    if (!/^[A-Za-z]+$/.test(lastName)) {
      return "Last name can contain only letters.";
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return "Enter a valid email address.";
    }
    if (password1.length < 8) {
      return "Password must have at least 8 characters.";
    }
    if (!/\d/.test(password1)) {
      return "Password must contain at least one digit.";
    }
    if (password1 !== password2) {
      return "Passwords do not match.";
    }
    return "";
  };

  const handleRegister = async () => {
    const error = validateForm();
    if (error) {
      toast.error(error);
      return;
    }
    try {
      const response = await axios.post(`${config.apiUrl}/api/register/`, {
        nickname,
        email,
        first_name: firstName,
        last_name: lastName,
        password: password1,
      });
      toast.success(response.data.message || "Registered successfully!");
      setNickname("");
      setEmail("");
      setFirstName("");
      setLastName("");
      setPassword1("");
      setPassword2("");
      setTimeout(() => {
        navigate("/login");
      }, 1000);
    } catch (error) {
      if (!error.response) {
        toast.error("Cannot connect to the server. Check network console.");
        return;
      }
      toast.error(error.response.data?.error || "An error occurred.");
    }
  };

  useEffect(() => {
    if (submitForm) {
      handleRegister();
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
    <div className="registerPanel">
      <div className="registerPanel__container">
        <div className="registerPanel__image"></div>
        <form className="registerPanel__form" onSubmit={handleSubmit}>
          <h2>Create an account</h2>
          <p>Enter your details below.</p>

          <div className="floating-label">
            <input
              type="text"
              id="nickname"
              name="nickname"
              placeholder="Nickname"
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
              required
            />
          </div>
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
              type="text"
              id="firstName"
              name="firstName"
              placeholder="First Name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>
          <div className="floating-label">
            <input
              type="text"
              id="lastName"
              name="lastName"
              placeholder="Last Name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>
          <div className="floating-label">
            <input
              type="password"
              id="password1"
              name="password1"
              placeholder="Password"
              value={password1}
              onChange={(e) => setPassword1(e.target.value)}
              required
            />
          </div>
          <div className="floating-label">
            <input
              type="password"
              id="password2"
              name="password2"
              placeholder="Confirm Password"
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
              required
            />
          </div>

          <div className="registerPanel__buttons">
            <button type="button" onClick={() => setSubmitForm(true)}>
              Create Account
            </button>
          </div>

          <div className="registerPanel__footer">
            <p>
              Already have an account?{" "}
              <a href="/login" className="registerPanel__link">
                Login
              </a>
              .
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterPanel;
