import React, { useEffect, useState } from "react";
import axios from "axios";
import "./ClientPanel.scss";

const ClientComplaints = () => {
  const [complaints, setComplaints] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("access");
    axios
      .get("http://127.0.0.1:8000/api/complaints/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setComplaints(res.data))
      .catch((err) => console.error("Error fetching complaints:", err));
  }, []);

  return (
    <div className="container">
      <h1>My Complaints</h1>
      <ul>
        {complaints.map((complaint) => (
          <li key={complaint.id}>
            Complaint #{complaint.id} - Status: {complaint.status}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ClientComplaints;
