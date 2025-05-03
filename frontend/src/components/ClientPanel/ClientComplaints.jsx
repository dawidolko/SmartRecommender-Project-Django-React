import React, { useEffect, useState } from "react";
import axios from "axios";
import { format } from "date-fns";
import {
  ChevronUp,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Search,
} from "lucide-react";
import "./ClientPanel.scss";
import Modal from "./Modal";
import config from "../../config/config";

const ClientComplaints = () => {
  const [complaints, setComplaints] = useState([]);
  const [sortKey, setSortKey] = useState("date");
  const [sortOrder, setSortOrder] = useState("asc");
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredComplaints, setFilteredComplaints] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [complaintsPerPage] = useState(10);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedComplaint, setSelectedComplaint] = useState(null);
  const [complaintLoading, setComplaintLoading] = useState(false);
  const [complaintError, setComplaintError] = useState(null);

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
    setLoading(true);
    axios
      .get(`${config.apiUrl}/api/complaints/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setComplaints(res.data);
        setFilteredComplaints(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching complaints:", err);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    handleFilteringAndSorting();
  }, [searchTerm, sortKey, sortOrder, complaints]);

  const handleFilteringAndSorting = () => {
    if (!complaints.length) return;

    let data = [...complaints];

    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      data = data.filter((complaint) => {
        const idMatch = complaint.id.toString().includes(term);
        const orderMatch = complaint.order.toString().includes(term);
        const causeMatch = complaint.cause?.toLowerCase().includes(term);
        const statusMatch = complaint.status?.toLowerCase().includes(term);

        const complaintDate = format(
          new Date(complaint.submission_date),
          "dd MMM yyyy, HH:mm"
        ).toLowerCase();
        const dateMatch = complaintDate.includes(term);

        return idMatch || orderMatch || causeMatch || statusMatch || dateMatch;
      });
    }

    data.sort((a, b) => {
      let comp = 0;
      if (sortKey === "date") {
        comp = new Date(a.submission_date) - new Date(b.submission_date);
      } else if (sortKey === "status") {
        comp = a.status.localeCompare(b.status);
      } else if (sortKey === "id") {
        comp = a.id - b.id;
      } else if (sortKey === "order") {
        comp = a.order - b.order;
      } else if (sortKey === "cause") {
        comp = a.cause.localeCompare(b.cause);
      }
      return sortOrder === "asc" ? comp : -comp;
    });

    setFilteredComplaints(data);
    setCurrentPage(1);
  };

  const handleViewDetails = (complaintId) => {
    const token = localStorage.getItem("access");
    setComplaintLoading(true);
    setComplaintError(null);

    axios
      .get(`${config.apiUrl}/api/complaints/${complaintId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setSelectedComplaint(res.data);
        setComplaintLoading(false);
        setIsModalOpen(true);
      })
      .catch((err) => {
        console.error("Error fetching complaint details:", err);
        setComplaintError("Failed to fetch complaint details");
        setComplaintLoading(false);
      });
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedComplaint(null);
  };

  const handleSort = (column) => {
    if (sortKey === column) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortKey(column);
      setSortOrder("asc");
    }
  };

  const handleSearch = (value) => {
    setSearchTerm(value);
  };

  const renderSortIcon = (column) => {
    if (sortKey !== column) return null;
    return sortOrder === "asc" ? (
      <ChevronUp size={14} />
    ) : (
      <ChevronDown size={14} />
    );
  };

  const indexOfLast = currentPage * complaintsPerPage;
  const indexOfFirst = indexOfLast - complaintsPerPage;
  const currentComplaints = filteredComplaints.slice(indexOfFirst, indexOfLast);

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
    return (
      <div className="admin-content">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  const tableCellStyle = {
    textAlign: "center",
    verticalAlign: "middle",
  };

  const renderComplaintDetails = () => {
    if (complaintLoading) return <div className="loading-spinner"></div>;
    if (complaintError) return <div>{complaintError}</div>;
    if (!selectedComplaint) return <div>No complaint found.</div>;

    return (
      <div className="complaint-detail-modal">
        <p>
          <strong>Order ID:</strong> {selectedComplaint.order}
        </p>
        <p>
          <strong>Cause:</strong> {selectedComplaint.cause}
        </p>
        <p>
          <strong>Status:</strong>{" "}
          <span className={getStatusClass(selectedComplaint.status)}>
            {selectedComplaint.status}
          </span>
        </p>
        <p>
          <strong>Submission Date:</strong>{" "}
          {format(
            new Date(selectedComplaint.submission_date),
            "dd MMM yyyy, HH:mm"
          )}
        </p>
      </div>
    );
  };

  return (
    <div className="client-main">
      <div className="product-table-container2">
        <div className="product-table-header2">
          <h2>My Complaints</h2>
          <div className="search-container2">
            <input
              type="text"
              placeholder="Search complaints... (ID, Order, Status, Cause, Date)"
              onChange={(e) => handleSearch(e.target.value)}
              value={searchTerm}
            />
            <Search className="search-icon" size={18} />
          </div>
        </div>

        <div className="table-wrapper">
          <table className="product-table2">
            <thead>
              <tr>
                <th
                  style={tableCellStyle}
                  onClick={() => handleSort("id")}
                  className="sortable-header">
                  <div className="header-content">
                    <span>#</span>
                    {renderSortIcon("id")}
                  </div>
                </th>
                <th
                  style={tableCellStyle}
                  onClick={() => handleSort("order")}
                  className="sortable-header">
                  <div className="header-content">
                    <span>Order ID</span>
                    {renderSortIcon("order")}
                  </div>
                </th>
                <th
                  style={tableCellStyle}
                  onClick={() => handleSort("cause")}
                  className="sortable-header">
                  <div className="header-content">
                    <span>Cause</span>
                    {renderSortIcon("cause")}
                  </div>
                </th>
                <th
                  style={tableCellStyle}
                  onClick={() => handleSort("status")}
                  className="sortable-header">
                  <div className="header-content">
                    <span>Status</span>
                    {renderSortIcon("status")}
                  </div>
                </th>
                <th
                  style={tableCellStyle}
                  onClick={() => handleSort("date")}
                  className="sortable-header">
                  <div className="header-content">
                    <span>Submission Date</span>
                    {renderSortIcon("date")}
                  </div>
                </th>
                <th style={tableCellStyle}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {currentComplaints.length > 0 ? (
                currentComplaints.map((complaint) => (
                  <tr key={complaint.id}>
                    <td style={tableCellStyle}>{complaint.id}</td>
                    <td style={tableCellStyle}>{complaint.order}</td>
                    <td style={tableCellStyle}>{complaint.cause}</td>
                    <td style={tableCellStyle}>
                      <span
                        className={`status-badge ${getStatusClass(
                          complaint.status
                        )}`}>
                        {complaint.status}
                      </span>
                    </td>
                    <td style={tableCellStyle}>
                      {format(
                        new Date(complaint.submission_date),
                        "dd MMM yyyy, HH:mm"
                      )}
                    </td>
                    <td style={tableCellStyle}>
                      <button
                        className="btn-primary"
                        onClick={() => handleViewDetails(complaint.id)}>
                        View Details
                      </button>
                    </td>
                  </tr>
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
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={
          selectedComplaint
            ? `Complaint #${selectedComplaint.id} Details`
            : "Complaint Details"
        }>
        {renderComplaintDetails()}
      </Modal>
    </div>
  );
};

export default ClientComplaints;
