import React, { useEffect, useState } from "react";
import axios from "axios";
import "./ClientAccount.scss";

const ClientAccount = () => {
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
    const token = localStorage.getItem("access");
    axios
      .get("http://127.0.0.1:8000/api/user/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        const data = res.data;
        const first_name = data.first_name || "";
        const last_name = data.last_name || "";
        const email = data.email || "";
        setInitialData({ first_name, last_name, email });
        setFormData((prev) => ({
          ...prev,
          first_name,
          last_name,
          email,
        }));
      })
      .catch((err) => {
        console.error("Error fetching user data:", err);
      });
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setErrorMessage("");

    if (formData.password !== formData.confirm_password) {
      setErrorMessage("Passwords do not match");
      return;
    }

    const token = localStorage.getItem("access");

    // Payload only with changed fields
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
      .put("http://127.0.0.1:8000/api/me/", payload, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then(() => alert("Account updated!"))
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
