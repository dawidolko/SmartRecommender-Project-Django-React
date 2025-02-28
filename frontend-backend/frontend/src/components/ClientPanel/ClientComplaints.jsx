// ClientComplaints.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { format } from "date-fns";
import "./ClientPanel.scss";

const ClientComplaints = () => {
  const [complaints, setComplaints] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access");
    axios
      .get("http://127.0.0.1:8000/api/complaints/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setComplaints(res.data))
      .catch((err) => console.error("Error fetching complaints:", err));
  }, []);

  const handleViewDetails = (complaintId) => {
    navigate(`/client/complaints/${complaintId}`);
  };

  return (
    <div className="container client-complaints">
      <h1>My Complaints</h1>
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th>#</th>
              <th>Order ID</th>
              <th>Cause</th>
              <th>Status</th>
              <th>Submission Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {complaints.map((complaint) => (
              <tr key={complaint.id}>
                <td>{complaint.id}</td>
                <td>{complaint.order}</td>
                <td>{complaint.cause}</td>
                <td>{complaint.status}</td>
                <td>{format(new Date(complaint.submission_date), "dd MMM yyyy, HH:mm")}</td>
                <td>
                  <button className="btn btn-primary" onClick={() => handleViewDetails(complaint.id)}>
                    View Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ClientComplaints;
