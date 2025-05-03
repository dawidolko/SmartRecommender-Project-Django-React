import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../../context/AuthContext";
import { motion } from "framer-motion";
import { toast } from "react-toastify";
import config from "../../config/config";
import "./AdminPanel.scss";

const AdminAccount = () => {
  const { user, setUser } = useContext(AuthContext);

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
  const [loading, setLoading] = useState(false);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setLoading(true);

    const validationError = validateForm();
    if (validationError) {
      setErrorMessage(validationError);
      setLoading(false);
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
      setLoading(false);
      return;
    }

    try {
      const response = await axios.patch(`${config.apiUrl}/api/me/`, payload, {
        headers: { Authorization: `Bearer ${token}` },
      });

      const updatedUser = { ...user, ...response.data };
      setUser(updatedUser);
      localStorage.setItem("loggedUser", JSON.stringify(updatedUser));

      toast.success("Account updated successfully!");
      setLoading(false);
      setFormData((prev) => ({
        ...prev,
        password: "",
        confirm_password: "",
      }));
      setInitialData({
        first_name: response.data.first_name,
        last_name: response.data.last_name,
        email: response.data.email,
      });
    } catch (err) {
      console.error("Error updating account:", err);
      toast.error("Error updating account. Please try again.");
      setLoading(false);
    }
  };

  return (
    <div className="admin-content">
      <motion.div
        className="admin-account-container"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}>
        <div className="admin-account-card">
          <h2 className="admin-account-title">Account Settings</h2>
          <form onSubmit={handleSubmit} className="admin-account-form">
            <div className="form-group">
              <label htmlFor="first_name">First Name</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                required
                className="admin-account-input"
              />
            </div>
            <div className="form-group">
              <label htmlFor="last_name">Last Name</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                required
                className="admin-account-input"
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="admin-account-input"
              />
            </div>
            <div className="form-group">
              <label htmlFor="password">New Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="admin-account-input"
              />
              <small className="admin-account-hint">
                Leave blank to keep current password
              </small>
            </div>
            <div className="form-group">
              <label htmlFor="confirm_password">Confirm New Password</label>
              <input
                type="password"
                id="confirm_password"
                name="confirm_password"
                value={formData.confirm_password}
                onChange={handleChange}
                className="admin-account-input"
              />
            </div>
            {errorMessage && (
              <div className="admin-account-error">{errorMessage}</div>
            )}
            <button
              type="submit"
              className="admin-account-btn-submit"
              disabled={loading}>
              {loading ? "Updating..." : "Update Account"}
            </button>
          </form>
        </div>
      </motion.div>
    </div>
  );
};

export default AdminAccount;
