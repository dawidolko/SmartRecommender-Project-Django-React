import React, { useEffect, useState } from "react";
import axios from "axios";
import config from "../../config/config";

const AdminComplaints = () => {
  const [complaints, setComplaints] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("access");
    axios
      .get(`${config.apiUrl}/api/complaints/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setComplaints(res.data))
      .catch((err) => console.error("Error fetching complaints:", err));
  }, []);

  const handleStatusChange = async (complaintId, newStatus) => {
    const token = localStorage.getItem("access");
    try {
      await axios.put(
        `${config.apiUrl}/api/complaints/${complaintId}/`,
        { status: newStatus },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setComplaints((prev) =>
        prev.map((c) =>
          c.id === complaintId ? { ...c, status: newStatus } : c
        )
      );
    } catch (error) {
      console.error("Error updating complaint:", error);
    }
  };

  const handleDelete = async (complaintId) => {
    if (!window.confirm("Are you sure you want to delete this complaint?"))
      return;
    const token = localStorage.getItem("access");
    try {
      await axios.delete(`${config.apiUrl}/api/complaints/${complaintId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setComplaints((prev) => prev.filter((c) => c.id !== complaintId));
    } catch (error) {
      console.error("Error deleting complaint:", error);
    }
  };

  return (
    <div className="container">
      <h1>Complaints</h1>
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th>#</th>
              <th>Order ID</th>
              <th>Cause</th>
              <th>Status</th>
              <th>Submission Date</th>
              <th>Change Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {complaints.map((c) => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.order}</td>
                <td>{c.cause}</td>
                <td>{c.status}</td>
                <td>{c.submission_date}</td>
                <td>
                  <select
                    value={c.status}
                    onChange={(e) => handleStatusChange(c.id, e.target.value)}>
                    <option value="pending">pending</option>
                    <option value="accepted">accepted</option>
                    <option value="rejected">rejected</option>
                  </select>
                </td>
                <td>
                  <button
                    className="table-button table-button--delete btn btn-danger"
                    onClick={() => handleDelete(c.id)}>
                    Delete
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

export default AdminComplaints;
