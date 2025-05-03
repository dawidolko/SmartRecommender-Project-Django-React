import React, { useEffect, useState, useCallback } from "react";
import { motion } from "framer-motion";
import {
  Search,
  ChevronLeft,
  ChevronRight,
  ChevronUp,
  ChevronDown,
  AlertCircle,
  Trash2,
} from "lucide-react";
import axios from "axios";
import config from "../../config/config";
import StatCard from "./StatCard";
import "./AdminPanel.scss";
import { toast } from "react-toastify";

const AdminComplaints = () => {
  const [complaints, setComplaints] = useState([]);
  const [filteredComplaints, setFilteredComplaints] = useState([]);
  const [statusChanges, setStatusChanges] = useState({});
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortField, setSortField] = useState("id");
  const [sortDirection, setSortDirection] = useState("desc");
  const [currentPage, setCurrentPage] = useState(1);
  const [complaintsPerPage] = useState(10);
  const [stats, setStats] = useState({
    totalComplaints: 0,
    pendingComplaints: 0,
    resolvedComplaints: 0,
    rejectedComplaints: 0,
  });

  useEffect(() => {
    fetchComplaints();
  }, []);

  const fetchComplaints = async () => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(`${config.apiUrl}/api/complaints/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setComplaints(res.data);
      setFilteredComplaints(res.data);

      const data = res.data;
      const pending = data.filter((c) => c.status === "Pending").length;
      const resolved = data.filter((c) => c.status === "Resolved").length;
      const rejected = data.filter((c) => c.status === "Rejected").length;

      setStats({
        totalComplaints: data.length,
        pendingComplaints: pending,
        resolvedComplaints: resolved,
        rejectedComplaints: rejected,
      });

      setLoading(false);
    } catch (err) {
      console.error("Error fetching complaints:", err);
      setLoading(false);
    }
  };

  const handleFilteringAndSorting = useCallback(() => {
    if (!complaints.length) return;

    let data = [...complaints];

    data = data.filter((complaint) => {
      if (!searchTerm) return true;

      const term = searchTerm.toLowerCase();
      const idMatch = complaint.id.toString().includes(term);
      const orderMatch = complaint.order.toString().includes(term);
      const causeMatch = complaint.cause?.toLowerCase().includes(term);
      const statusMatch = complaint.status?.toLowerCase().includes(term);

      return idMatch || orderMatch || causeMatch || statusMatch;
    });

    data.sort((a, b) => {
      let fieldA = a[sortField] || "";
      let fieldB = b[sortField] || "";

      if (sortField === "submission_date") {
        fieldA = new Date(fieldA);
        fieldB = new Date(fieldB);
      } else if (typeof fieldA === "string") {
        fieldA = fieldA.toLowerCase();
        fieldB = fieldB.toLowerCase();
      }

      if (fieldA < fieldB) return sortDirection === "asc" ? -1 : 1;
      if (fieldA > fieldB) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });

    setFilteredComplaints(data);
  }, [complaints, searchTerm, sortField, sortDirection]);

  useEffect(() => {
    handleFilteringAndSorting();
  }, [handleFilteringAndSorting]);

  const handleSearch = (value) => {
    setSearchTerm(value);
    setCurrentPage(1);
  };

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
      toast.error("Complaint not found.");
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

        toast.success("Status updated successfully!");
      } else {
        toast.error("Failed to update status. Please try again.");
      }
    } catch (error) {
      console.error(
        "Error updating complaint:",
        error.response ? error.response.data : error.message
      );

      toast.error("Failed to update status. Please try again.");
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
      toast.success("Complaint deleted successfully!");
    } catch (error) {
      console.error("Error deleting complaint:", error);
      toast.error("Failed to delete complaint. Please try again.");
    }
  };

  const getStatusClass = (status) => {
    switch (status) {
      case "Resolved":
        return "admin-status-resolved";
      case "Rejected":
        return "admin-status-rejected";
      case "Pending":
      default:
        return "admin-status-pending";
    }
  };

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const renderSortIcon = (field) => {
    if (sortField !== field) return null;
    return sortDirection === "asc" ? (
      <ChevronUp size={14} />
    ) : (
      <ChevronDown size={14} />
    );
  };

  const formatDate = (dateString) => {
    if (!dateString) return "";
    const date = new Date(dateString);
    return date
      .toLocaleString("en-GB", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      })
      .replace(",", "");
  };

  const indexOfLast = currentPage * complaintsPerPage;
  const indexOfFirst = indexOfLast - complaintsPerPage;
  const currentSlice = filteredComplaints.slice(indexOfFirst, indexOfLast);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const nextPage = () => {
    if (
      currentPage < Math.ceil(filteredComplaints.length / complaintsPerPage)
    ) {
      setCurrentPage(currentPage + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  if (loading) {
    return <div className="loading-spinner"></div>;
  }

  return (
    <div className="admin-content">
      <main className="admin-products">
        <motion.div
          className="stat_Cards"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}>
          <StatCard
            name="Total Complaints"
            icon={AlertCircle}
            value={stats.totalComplaints.toLocaleString()}
            color="#6366F1"
          />
          <StatCard
            name="Pending Complaints"
            icon={AlertCircle}
            value={stats.pendingComplaints.toLocaleString()}
            color="#F59E0B"
          />
          <StatCard
            name="Resolved Complaints"
            icon={AlertCircle}
            value={stats.resolvedComplaints.toLocaleString()}
            color="#10B981"
          />
          <StatCard
            name="Rejected Complaints"
            icon={AlertCircle}
            value={stats.rejectedComplaints.toLocaleString()}
            color="#EF4444"
          />
        </motion.div>

        <motion.div
          className="product-table-container"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}>
          <div className="product-table-header">
            <h2>All Complaints</h2>
            <div className="search-container">
              <input
                type="text"
                placeholder="Search complaints..."
                onChange={(e) => handleSearch(e.target.value)}
                value={searchTerm}
              />
              <Search className="search-icon" size={18} />
            </div>
          </div>

          <div className="table-wrapper">
            <table className="product-table">
              <thead>
                <tr>
                  <th
                    onClick={() => handleSort("id")}
                    className="sortable-header"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>#</span>
                      {renderSortIcon("id")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("order")}
                    className="sortable-header"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>Order ID</span>
                      {renderSortIcon("order")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("cause")}
                    className="sortable-header hide-responsive"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>Cause</span>
                      {renderSortIcon("cause")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("submission_date")}
                    className="sortable-header hide-responsive"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>Submission Date</span>
                      {renderSortIcon("submission_date")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("status")}
                    className="sortable-header"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>Status</span>
                      {renderSortIcon("status")}
                    </div>
                  </th>
                  <th style={{ textAlign: "center" }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {currentSlice.length > 0 ? (
                  currentSlice.map((complaint) => (
                    <motion.tr
                      key={complaint.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.3 }}
                      className={getStatusClass(complaint.status)}>
                      <td style={{ textAlign: "center" }}>{complaint.id}</td>
                      <td style={{ textAlign: "center" }}>{complaint.order}</td>
                      <td
                        className="hide-responsive"
                        style={{ textAlign: "center" }}>
                        {complaint.cause}
                      </td>
                      <td
                        className="hide-responsive"
                        style={{ textAlign: "center" }}>
                        {formatDate(complaint.submission_date)}
                      </td>
                      <td style={{ textAlign: "center" }}>
                        <select
                          value={
                            statusChanges[complaint.id] || complaint.status
                          }
                          onChange={(e) =>
                            handleStatusChange(complaint.id, e.target.value)
                          }
                          className={`admin-status-select ${getStatusClass(
                            statusChanges[complaint.id] || complaint.status
                          )}`}>
                          <option value="Pending">Pending</option>
                          <option value="Resolved">Resolved</option>
                          <option value="Rejected">Rejected</option>
                        </select>
                      </td>
                      <td
                        className="action-cell"
                        style={{ textAlign: "center" }}>
                        <button
                          onClick={() => handleUpdateStatus(complaint.id)}
                          className="btn-save"
                          disabled={
                            !statusChanges[complaint.id] ||
                            statusChanges[complaint.id] === complaint.status
                          }>
                          Update
                        </button>
                        <button
                          onClick={() => handleDelete(complaint.id)}
                          className="btn-delete">
                          <Trash2 size={18} />
                        </button>
                      </td>
                    </motion.tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="6" className="no-results">
                      No complaints found matching your search criteria
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {filteredComplaints.length > 0 && (
            <div className="pagination-container">
              <div className="pagination-info">
                <p className="pagination-text">
                  Displaying {indexOfFirst + 1} to{" "}
                  {Math.min(indexOfLast, filteredComplaints.length)} of{" "}
                  {filteredComplaints.length} complaints
                </p>
              </div>
              <div className="pagination-controls">
                <button
                  onClick={prevPage}
                  disabled={currentPage === 1}
                  className={`pagination-button ${
                    currentPage === 1 ? "disabled" : ""
                  }`}>
                  <ChevronLeft size={16} />
                  <span>&lt;</span>
                </button>
                {Array.from({
                  length: Math.ceil(
                    filteredComplaints.length / complaintsPerPage
                  ),
                })
                  .map((_, index) => (
                    <button
                      key={index}
                      onClick={() => paginate(index + 1)}
                      className={`pagination-number ${
                        currentPage === index + 1 ? "active" : ""
                      }`}>
                      {index + 1}
                    </button>
                  ))
                  .slice(
                    Math.max(0, currentPage - 3),
                    Math.min(
                      Math.ceil(filteredComplaints.length / complaintsPerPage),
                      currentPage + 2
                    )
                  )}
                <button
                  onClick={nextPage}
                  disabled={
                    currentPage >=
                    Math.ceil(filteredComplaints.length / complaintsPerPage)
                  }
                  className={`pagination-button ${
                    currentPage >=
                    Math.ceil(filteredComplaints.length / complaintsPerPage)
                      ? "disabled"
                      : ""
                  }`}>
                  <ChevronRight size={16} />
                  <span>&gt;</span>
                </button>
              </div>
            </div>
          )}
        </motion.div>
      </main>
    </div>
  );
};

export default AdminComplaints;
