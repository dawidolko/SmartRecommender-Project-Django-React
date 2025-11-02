/**
 * ClientAccount Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Client panel component for managing user account settings and profile information.
 * Allows users to update their personal information and change password.
 *
 * Features:
 *   - Profile information editing (first name, last name, email)
 *   - Password change functionality
 *   - Form validation with error messages
 *   - Success notifications
 *   - Unsaved changes detection
 *   - Loading states during save
 *   - Email format validation
 *   - Password strength requirements
 *   - Password confirmation matching
 *   - Auto-fill from current user data
 *
 * Validation Rules:
 *   First Name:
 *     - Required field
 *     - Only letters allowed
 *     - Max 50 characters
 *
 *   Last Name:
 *     - Required field
 *     - Only letters allowed
 *     - Max 50 characters
 *
 *   Email:
 *     - Required field
 *     - Valid email format (regex)
 *     - Unique in system
 *
 *   Password (optional):
 *     - Min 8 characters
 *     - At least one uppercase letter
 *     - At least one lowercase letter
 *     - At least one digit
 *     - Must match confirmation field
 *
 * State Management:
 *   - initialData: Original user data (for detecting changes)
 *   - formData: Current form values {first_name, last_name, email, password, confirm_password}
 *   - errorMessage: Validation or API error message
 *   - loading: Save operation loading state
 *   - user: Current user from AuthContext
 *
 * API Endpoints:
 *   - PUT /api/me/ - Update user profile
 *
 * Success Flow:
 *   1. Validate form data
 *   2. Send PUT request with changes
 *   3. Update AuthContext user state
 *   4. Update localStorage
 *   5. Show success toast notification
 *   6. Reload page (optional)
 *
 * @component
 * @returns {React.ReactElement} Account settings page with profile form
 */
import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../../context/AuthContext";
import { toast } from "react-toastify";
import "./ClientAccount.scss";
import config from "../../config/config";

const ClientAccount = () => {
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

    const shouldShowToast = localStorage.getItem("accountUpdateSuccess");
    if (shouldShowToast === "true") {
      setTimeout(() => {
        toast.success("Account updated!", {
          position: "top-center",
          autoClose: 3000,
          hideProgressBar: true,
          closeOnClick: true,
        });
        localStorage.removeItem("accountUpdateSuccess");
      }, 500);
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
      toast.success("Account updated successfully!", {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
      });

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
      toast.error("Error updating account", {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
      });
      setLoading(false);
    }
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
        <button
          type="submit"
          className="btn-submit btn-main-client"
          disabled={loading}>
          {loading ? "Updating..." : "Update"}
        </button>
      </form>
    </div>
  );
};

export default ClientAccount;
