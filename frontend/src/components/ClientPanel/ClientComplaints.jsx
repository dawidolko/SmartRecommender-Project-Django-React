import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { format } from "date-fns";
import "./ClientPanel.scss";
import config from "../../config/config";

const ClientComplaints = () => {
  const [complaints, setComplaints] = useState([]);
  const [sortKey, setSortKey] = useState("date");
  const [sortOrder, setSortOrder] = useState("asc");
  const navigate = useNavigate();

  const getStatusClass = (status) => {
    switch (status) {
      case "Pending":
        return "status-pending";
      case "Resolved":
        return "status-resolved";
      case "Rejected":
        return "status-rejected";
      default:
        return "";
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("access");
    axios
      .get(`${config.apiUrl}/api/complaints/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setComplaints(res.data))
      .catch((err) => console.error("Error fetching complaints:", err));
  }, []);

  const handleViewDetails = (complaintId) => {
    navigate(`/client/complaints/${complaintId}`);
  };

  const handleSort = (column) => {
    if (sortKey === column) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortKey(column);
      setSortOrder("asc");
    }
  };

  const renderSortIndicator = (column) => {
    if (sortKey === column) {
      return sortOrder === "asc" ? " ▲" : " ▼";
    }
    return "";
  };

  const sortedComplaints = [...complaints].sort((a, b) => {
    let comp = 0;
    if (sortKey === "date") {
      comp = new Date(a.submission_date) - new Date(b.submission_date);
    } else if (sortKey === "status") {
      comp = a.status.localeCompare(b.status);
    }
    return sortOrder === "asc" ? comp : -comp;
  });

  return (
    <div className="container client-complaints">
      <h1>My Complaints</h1>
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th className="hide-complaints text-align-client">#</th>
              <th className="hide-complaints text-align-client">Order ID</th>
              <th className="hide-complaints2 text-align-client">Cause</th>
              <th
                style={{ cursor: "pointer", textAlign: "center" }}
                onClick={() => handleSort("status")}>
                Status {renderSortIndicator("status")}
              </th>
              <th
                className="hide-complaints2 text-align-client"
                style={{ cursor: "pointer" }}
                onClick={() => handleSort("date")}>
                Submission Date {renderSortIndicator("date")}
              </th>
              <th class="text-align-client">Actions</th>
            </tr>
          </thead>
          <tbody>
            {sortedComplaints.map((complaint) => (
              <tr key={complaint.id}>
                <td className="hide-complaints text-align-client">
                  {complaint.id}
                </td>
                <td className="hide-complaints text-align-client">
                  {complaint.order}
                </td>
                <td className="hide-complaints2 text-align-client">
                  {complaint.cause}
                </td>
                <td
                  style={{ textAlign: "center" }}
                  className={getStatusClass(complaint.status)}>
                  {complaint.status}
                </td>
                <td className="hide-complaints2 text-align-client">
                  {format(
                    new Date(complaint.submission_date),
                    "dd MMM yyyy, HH:mm"
                  )}
                </td>
                <td className="table-center">
                  <button
                    className="btn btn-primary btn-main-client"
                    onClick={() => handleViewDetails(complaint.id)}>
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
