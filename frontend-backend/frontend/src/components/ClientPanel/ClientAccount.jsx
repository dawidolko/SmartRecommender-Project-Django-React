import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import "./ClientAccount.scss";

const ClientAccount = () => {
  const { user, setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const [initialData, setInitialData] = useState({
    first_name: "",
    last_name: "",
    email: "",
  });

  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (user) {
      const { first_name, last_name, email } = user;
      setInitialData({ first_name, last_name, email });
      setFormData((prev) => ({
        ...prev,
        first_name,
        last_name,
        email,
      }));
    }
  }, [user]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const validateForm = () => {
    const nameRegex = /^[A-Za-z]+$/;
    if (!formData.first_name.trim()) {
      return "First name cannot be empty";
    }
    if (!nameRegex.test(formData.first_name)) {
      return "First name can contain only letters";
    }
    if (formData.first_name.length > 50) {
      return "First name must not exceed 50 characters";
    }
    if (!formData.last_name.trim()) {
      return "Last name cannot be empty";
    }
    if (!nameRegex.test(formData.last_name)) {
      return "Last name can contain only letters";
    }
    if (formData.last_name.length > 50) {
      return "Last name must not exceed 50 characters";
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      return "Enter a valid email address";
    }
    if (formData.password.trim() !== "") {
      if (formData.password.length < 8) {
        return "Password must have at least 8 characters";
      }
      if (!/\d/.test(formData.password)) {
        return "Password must contain at least one digit";
      }
      if (formData.password !== formData.confirm_password) {
        return "Passwords do not match";
      }
    }
    return "";
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setErrorMessage("");
    
    const validationError = validateForm();
    if (validationError) {
      setErrorMessage(validationError);
      return;
    }
    
    const token = localStorage.getItem("access");

    let payload = {};
    if (formData.first_name !== initialData.first_name) {
      payload.first_name = formData.first_name;
    }
    if (formData.last_name !== initialData.last_name) {
      payload.last_name = formData.last_name;
    }
    if (formData.email !== initialData.email) {
      payload.email = formData.email;
    }
    if (formData.password.trim() !== "") {
      payload.password = formData.password;
    }

    if (Object.keys(payload).length === 0) {
      setErrorMessage("No changes to update");
      return;
    }

    axios
      .patch("http://127.0.0.1:8000/api/me/", payload, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setUser(res.data);
        localStorage.setItem("loggedUser", JSON.stringify(res.data));
        alert("Account updated!");
        navigate("/client");
      })
      .catch((err) => {
        console.error("Error updating account:", err);
        setErrorMessage("Error updating account");
      });
  };

  return (
    <div className="container client-account">
      <h1>Account Settings</h1>
      <form onSubmit={handleSubmit} className="account-form">
        <div className="form-group">
          <label htmlFor="first_name">First Name:</label>
          <input
            type="text"
            name="first_name"
            id="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="last_name">Last Name:</label>
          <input
            type="text"
            name="last_name"
            id="last_name"
            value={formData.last_name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email Address:</label>
          <input
            type="email"
            name="email"
            id="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">New Password:</label>
          <input
            type="password"
            name="password"
            id="password"
            value={formData.password}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label htmlFor="confirm_password">Confirm Password:</label>
          <input
            type="password"
            name="confirm_password"
            id="confirm_password"
            value={formData.confirm_password}
            onChange={handleChange}
          />
        </div>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        <button type="submit" className="btn-submit">
          Update
        </button>
      </form>
    </div>
  );
};

export default ClientAccount;
