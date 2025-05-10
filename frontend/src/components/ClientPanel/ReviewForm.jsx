/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { Star, AlertCircle } from "lucide-react";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import config from "../../config/config";
import "./ReviewForm.scss";

const parseJwt = (token) => {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    return JSON.parse(atob(base64));
  } catch {
    return {};
  }
};

const ReviewForm = ({ product = null, onReviewSubmitted, onClose }) => {
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);
  const [review, setReview] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const token = localStorage.getItem("access");
  const currentUserEmail = token ? parseJwt(token)?.email : null;

  useEffect(() => {
    setRating(0);
    setHoverRating(0);
    setReview("");
    setError("");
    setLoading(false);
    setSubmitted(false);

    if (!product?.id || !currentUserEmail) return;

    axios
      .get(`${config.apiUrl}/api/products/${product.id}/reviews/`, {
        headers: { Authorization: token ? `Bearer ${token}` : undefined },
      })
      .then((res) => {
        const already = res.data.some((r) => r.user_email === currentUserEmail);
        if (already) setSubmitted(true);
      })
      .catch(() => {});
  }, [product?.id]);

  const validateForm = useCallback(() => {
    if (!rating) return "Please select a rating before submitting";
    if (!review.trim()) return "Please write a review before submitting";
    if (review.trim().length < 3)
      return "Review is too short. Please write at least 3 characters";
    return "";
  }, [rating, review]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (submitted) return;

    const validationMsg = validateForm();
    if (validationMsg) {
      setError(validationMsg);
      return;
    }
    if (!product?.id) {
      setError("Invalid product information. Please try again later.");
      return;
    }

    setLoading(true);
    setError("");

    const url = `${config.apiUrl}/api/products/${product.id}/reviews/`;

    try {
      const resp = await axios.post(
        url,
        { rating, content: review },
        { headers: { Authorization: token ? `Bearer ${token}` : undefined } }
      );
      onReviewSubmitted?.(resp.data);
      setSubmitted(true);
      setLoading(false);
      toast.success("Review added – thank you!");
      setTimeout(() => onClose?.(), 2500);
    } catch (err) {
      const apiData = err.response?.data;
      let msg = "Failed to submit your review. Please try again later.";

      if (apiData?.detail) {
        if (
          apiData.detail === "A review has already been added for this product."
        ) {
          toast.error(apiData.detail);
          setLoading(false);
          setTimeout(() => onClose?.(), 1000);
          return;
        }
        msg = apiData.detail;
      } else if (apiData) {
        msg = Object.values(apiData).flat().join(" ");
      }

      setError(msg);
      setLoading(false);
      toast.error(msg);
    }
  };

  return (
    <div className="review-form-container">
      <h3>Write a Review for {product?.name ?? "Product"}</h3>
      {error && (
        <div className="review-form-error">
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}
      <form onSubmit={handleSubmit}>
        <div className="rating-container">
          <p>Your Rating:</p>
          <div className="stars-container">
            {[1, 2, 3, 4, 5].map((star) => (
              <Star
                key={star}
                size={28}
                onClick={() => !loading && !submitted && setRating(star)}
                onMouseEnter={() =>
                  !loading && !submitted && setHoverRating(star)
                }
                onMouseLeave={() => !loading && !submitted && setHoverRating(0)}
                fill={star <= (hoverRating || rating) ? "#FFD700" : "none"}
                stroke={star <= (hoverRating || rating) ? "#FFD700" : "#ccc"}
                className="star-icon"
                style={{
                  cursor: loading || submitted ? "not-allowed" : "pointer",
                }}
              />
            ))}
          </div>
        </div>
        <div className="review-text-container">
          <label htmlFor="review-text">Your Review:</label>
          <textarea
            id="review-text"
            placeholder="What did you think about this product? (minimum 3 characters)"
            value={review}
            onChange={(e) => {
              setReview(e.target.value);
              if (error) setError("");
            }}
            rows={4}
            disabled={loading || submitted}
          />
        </div>
        <div className="review-form-actions">
          <button
            type="button"
            className="btn-secondary"
            onClick={onClose}
            disabled={loading}>
            Cancel
          </button>
          <button
            type="submit"
            className="btn-primary"
            disabled={loading || submitted}>
            {loading
              ? "Submitting..."
              : submitted
              ? "Submitted"
              : "Submit Review"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ReviewForm;
