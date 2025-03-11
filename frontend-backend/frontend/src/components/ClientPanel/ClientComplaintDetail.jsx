import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import { format } from "date-fns";
import "./ClientComplaintDetail.scss";

const ClientComplaintDetail = () => {
  const { id } = useParams();
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access");
    axios
      .get(`http://127.0.0.1:8000/api/complaints/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setComplaint(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching complaint details:", err);
        setError("Failed to fetch complaint details");
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div>Loading complaint details...</div>;
  if (error) return <div>{error}</div>;
  if (!complaint) return <div>No complaint found.</div>;

  return (
    <div className="container client-complaint-detail">
      <h2>Complaint #{complaint.id} Details</h2>
      <p>
        <strong>Order ID:</strong> {complaint.order}
      </p>
      <p>
        <strong>Cause:</strong> {complaint.cause}
      </p>
      <p>
        <strong>Status:</strong> {complaint.status}
      </p>
      <p>
        <strong>Submission Date:</strong>{" "}
        {format(new Date(complaint.submission_date), "dd MMM yyyy, HH:mm")}
      </p>
      <button className="btn btn-primary back_button" onClick={() => navigate(-1)}>
        Back to Complaints
      </button>
    </div>
  );
};

export default ClientComplaintDetail;
