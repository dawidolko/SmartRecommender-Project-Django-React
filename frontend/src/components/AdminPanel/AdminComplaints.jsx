import React, { useEffect, useState } from "react";
import axios from "axios";
import config from "../../config/config";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const AdminComplaints = () => {
  const [complaints, setComplaints] = useState([]);
  const [statusChanges, setStatusChanges] = useState({});

  useEffect(() => {
    const token = localStorage.getItem("access");
    axios
      .get(`${config.apiUrl}/api/complaints/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setComplaints(res.data))
      .catch((err) => console.error("Error fetching complaints:", err));
  }, []);

  const handleStatusChange = (complaintId, newStatus) => {
    setStatusChanges((prev) => ({
      ...prev,
      [complaintId]: newStatus,
    }));
  };

  const handleUpdateStatus = async (complaintId) => {
    const newStatus = statusChanges[complaintId];
    const token = localStorage.getItem("access");

    if (!newStatus) {
      return;
    }

    const complaint = complaints.find((c) => c.id === complaintId);
    if (!complaint) {
      toast.error("Complaint not found.", {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
      return;
    }

    const updatedComplaintData = {
      cause: complaint.cause,
      order: complaint.order,
      status: newStatus,
    };

    try {
      const response = await axios.put(
        `${config.apiUrl}/api/complaints/${complaintId}/`,
        updatedComplaintData,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.status === 200) {
        setComplaints((prev) =>
          prev.map((c) =>
            c.id === complaintId ? { ...c, status: newStatus } : c
          )
        );

        setStatusChanges((prev) => {
          const { [complaintId]: _, ...rest } = prev;
          return rest;
        });

        toast.success("Status updated successfully!", {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
        });
      } else {
        toast.error("Failed to update status. Please try again.", {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
        });
      }
    } catch (error) {
      console.error(
        "Error updating complaint:",
        error.response ? error.response.data : error.message
      );

      toast.error("Failed to update status. Please try again.", {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
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

  const getStatusClass = (status) => {
    switch (status) {
      case "Resolved":
        return "resolved";
      case "Rejected":
        return "rejected";
      case "Pending":
      default:
        return "pending";
    }
  };

  return (
    <div className="container">
      <h1>Complaints</h1>
      <div className="table-responsive">
        <table className="table table-bordered table-hover table-collapse">
          <thead>
            <tr>
              <th className="hide-responsive2">#</th>
              <th>Order ID</th>
              <th className="hide-responsive">Cause</th>
              <th className="hide-responsive">Submission Date</th>
              <th>Change Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {complaints.map((c) => (
              <tr key={c.id} className={getStatusClass(c.status)}>
                <td className="hide-responsive2">{c.id}</td>
                <td>{c.order}</td>
                <td className="hide-responsive">{c.cause}</td>
                <td className="hide-responsive">{c.submission_date}</td>
                <td>
                  <select
                    value={statusChanges[c.id] || c.status}
                    onChange={(e) => handleStatusChange(c.id, e.target.value)}
                    className={getStatusClass(statusChanges[c.id] || c.status)}>
                    <option value="Pending">Pending</option>
                    <option value="Resolved">Resolved</option>
                    <option value="Rejected">Rejected</option>
                  </select>
                </td>
                <td className="table-button-container">
                  <button
                    className="table-button table-button--update btn btn-primary btn-primary-update"
                    onClick={() => handleUpdateStatus(c.id)}
                    disabled={
                      !statusChanges[c.id] || statusChanges[c.id] === c.status
                    }>
                    Update
                  </button>
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
      {/* Toast container */}
      <ToastContainer />
    </div>
  );
};

export default AdminComplaints;
