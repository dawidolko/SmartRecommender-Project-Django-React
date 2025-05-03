import React, { useEffect, useState, useCallback } from "react";
import { motion } from "framer-motion";
import {
  Trash2,
  Edit,
  Search,
  ChevronLeft,
  ChevronRight,
  ChevronUp,
  ChevronDown,
} from "lucide-react";
import axios from "axios";
import config from "../../config/config";
import StatCard from "./StatCard";
import ConfirmationModal from "./ConfirmationModal";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./AdminPanel.scss";

const AdminUsers = () => {
  const [customers, setCustomers] = useState([]);
  const [stats, setStats] = useState({
    totalOpinions: 0,
    averageRating: 0,
    topCategoryName: "",
    topTagName: "",
  });

  const [newEmail, setNewEmail] = useState("");
  const [newUsername, setNewUsername] = useState("");
  const [newFirstName, setNewFirstName] = useState("");
  const [newLastName, setNewLastName] = useState("");
  const [newRole, setNewRole] = useState("client");

  const [editId, setEditId] = useState(null);
  const [editEmail, setEditEmail] = useState("");
  const [editUsername, setEditUsername] = useState("");
  const [editFirstName, setEditFirstName] = useState("");
  const [editLastName, setEditLastName] = useState("");
  const [editRole, setEditRole] = useState("");

  const [searchTerm, setSearchTerm] = useState("");
  const [filteredCustomers, setFilteredCustomers] = useState([]);
  const [sortField, setSortField] = useState("id");
  const [sortDirection, setSortDirection] = useState("asc");

  const [currentPage, setCurrentPage] = useState(1);
  const [customersPerPage] = useState(10);

  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState(null);
  const [isAddConfirmModalOpen, setIsAddConfirmModalOpen] = useState(false);
  const [isEditConfirmModalOpen, setIsEditConfirmModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCustomers();
    fetchStatsFromBackend();
  }, []);

  const handleFilteringAndSorting = useCallback(() => {
    if (!customers.length) return;

    let data = [...customers];

    if (searchTerm.trim() !== "") {
      const term = searchTerm.toLowerCase().trim();
      data = data.filter((c) => {
        return (
          (c.email && c.email.toLowerCase().includes(term)) ||
          (c.username && c.username.toLowerCase().includes(term)) ||
          (c.first_name && c.first_name.toLowerCase().includes(term)) ||
          (c.last_name && c.last_name.toLowerCase().includes(term)) ||
          (c.role && c.role.toLowerCase().includes(term)) ||
          (c.id && c.id.toString().includes(term))
        );
      });
    }

    data.sort((a, b) => {
      let fieldA = a[sortField];
      let fieldB = b[sortField];

      if (fieldA === null || fieldA === undefined) fieldA = "";
      if (fieldB === null || fieldB === undefined) fieldB = "";

      if (typeof fieldA !== "string") fieldA = String(fieldA);
      if (typeof fieldB !== "string") fieldB = String(fieldB);

      fieldA = fieldA.toLowerCase();
      fieldB = fieldB.toLowerCase();

      if (fieldA < fieldB) return sortDirection === "asc" ? -1 : 1;
      if (fieldA > fieldB) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });

    setFilteredCustomers(data);
    if (
      data.length > 0 &&
      currentPage > Math.ceil(data.length / customersPerPage)
    ) {
      setCurrentPage(1);
    } else if (currentPage === 0 && data.length > 0) {
      setCurrentPage(1);
    }
  }, [
    customers,
    searchTerm,
    sortField,
    sortDirection,
    currentPage,
    customersPerPage,
  ]);

  useEffect(() => {
    handleFilteringAndSorting();
  }, [handleFilteringAndSorting]);

  const fetchCustomers = async () => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(`${config.apiUrl}/api/users/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setCustomers(res.data);
      setFilteredCustomers(res.data);
      setLoading(false);
    } catch (err) {
      console.error("Error fetching customers:", err);
      toast.error("Failed to fetch customers. Please try again.");
      setLoading(false);
    }
  };

  const fetchStatsFromBackend = async () => {
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        `${config.apiUrl}/api/admin-dashboard-stats/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setStats({
        totalOpinions: res.data.totalOpinions || 0,
        averageRating: res.data.averageRating || 0,
        topCategoryName: res.data.topCategoryName || "",
        topTagName: res.data.topTagName || "",
      });
    } catch (err) {
      console.error("Error fetching new stats (opinions, rating, etc.):", err);
      toast.error("Failed to fetch statistics. Please try again.");
    }
  };

  const handleAddUserClick = (e) => {
    e.preventDefault();

    if (!newEmail || !newUsername) {
      toast.error("Email and Username are required to create a user.");
      return;
    }

    setIsAddConfirmModalOpen(true);
  };

  const handleAddUser = async () => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      await axios.post(
        `${config.apiUrl}/api/users/`,
        {
          username: newUsername,
          email: newEmail,
          first_name: newFirstName,
          last_name: newLastName,
          role: newRole,
          password: "DefaultPass123",
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchCustomers();
      setNewEmail("");
      setNewUsername("");
      setNewFirstName("");
      setNewLastName("");
      setNewRole("client");
      toast.success("User added successfully!");
    } catch (err) {
      console.error("Error creating new user:", err);
      toast.error("Error occurred while creating user. Please try again.");
    } finally {
      setIsAddConfirmModalOpen(false);
      setLoading(false);
    }
  };

  const startEdit = (cust) => {
    setEditId(cust.id);
    setEditEmail(cust.email || "");
    setEditUsername(cust.username || "");
    setEditFirstName(cust.first_name || "");
    setEditLastName(cust.last_name || "");
    setEditRole(cust.role || "client");
  };

  const cancelEdit = () => {
    setEditId(null);
    setEditEmail("");
    setEditUsername("");
    setEditFirstName("");
    setEditLastName("");
    setEditRole("");
  };

  const handleEditClick = (e) => {
    e.preventDefault();

    if (!editEmail || !editUsername) {
      toast.error("Email and Username cannot be empty.");
      return;
    }

    setIsEditConfirmModalOpen(true);
  };

  const handleEditSubmit = async () => {
    setLoading(true);
    const token = localStorage.getItem("access");
    try {
      await axios.put(
        `${config.apiUrl}/api/users/${editId}/`,
        {
          email: editEmail,
          username: editUsername,
          first_name: editFirstName,
          last_name: editLastName,
          role: editRole,
          password: "DefaultPass123",
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchCustomers();
      cancelEdit();
      toast.success("User updated successfully!");
    } catch (err) {
      console.error("Error updating user:", err);
      toast.error("Error occurred while updating user. Please try again.");
    } finally {
      setIsEditConfirmModalOpen(false);
      setLoading(false);
    }
  };

  const handleDeleteClick = (userId) => {
    setPendingDeleteId(userId);
    setIsDeleteModalOpen(true);
  };

  const handleDelete = async () => {
    if (!pendingDeleteId) return;
    setLoading(true);

    const token = localStorage.getItem("access");
    try {
      await axios.delete(`${config.apiUrl}/api/users/${pendingDeleteId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchCustomers();
      toast.success("User deleted successfully!");
    } catch (error) {
      console.error("Error deleting user:", error);
      toast.error("Failed to delete user. Please try again.");
    } finally {
      setIsDeleteModalOpen(false);
      setPendingDeleteId(null);
      setLoading(false);
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

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const paginate = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const nextPage = () => {
    const maxPage = Math.ceil(filteredCustomers.length / customersPerPage);
    if (currentPage < maxPage) {
      setCurrentPage((prevPage) => prevPage + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage((prevPage) => prevPage - 1);
    }
  };

  const indexOfLast = currentPage * customersPerPage;
  const indexOfFirst = indexOfLast - customersPerPage;
  const currentSlice = filteredCustomers.slice(indexOfFirst, indexOfLast);
  const totalPages = Math.ceil(filteredCustomers.length / customersPerPage);

  const renderPaginationButtons = () => {
    const pageNumbers = [];
    const maxVisibleButtons = 5;

    if (totalPages <= maxVisibleButtons) {
      for (let i = 1; i <= totalPages; i++) {
        pageNumbers.push(i);
      }
    } else {
      let startPage = Math.max(
        1,
        currentPage - Math.floor(maxVisibleButtons / 2)
      );
      let endPage = startPage + maxVisibleButtons - 1;

      if (endPage > totalPages) {
        endPage = totalPages;
        startPage = Math.max(1, endPage - maxVisibleButtons + 1);
      }

      for (let i = startPage; i <= endPage; i++) {
        pageNumbers.push(i);
      }
    }

    return pageNumbers.map((number) => (
      <button
        key={number}
        onClick={() => paginate(number)}
        className={`pagination-number ${
          currentPage === number ? "active" : ""
        }`}>
        {number}
      </button>
    ));
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
            name="All Opinions"
            icon={Edit}
            value={stats.totalOpinions.toLocaleString()}
            color="#6366F1"
          />
          <StatCard
            name="Average Rating"
            icon={Edit}
            value={stats.averageRating}
            color="#10B981"
          />
          <StatCard
            name="Top Category"
            icon={Edit}
            value={stats.topCategoryName || "—"}
            color="#F59E0B"
          />
          <StatCard
            name="Top Tag"
            icon={Edit}
            value={stats.topTagName || "—"}
            color="#EF4444"
          />
        </motion.div>

        <motion.div
          className="product-form"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}>
          <h4 className="product-form__title">Add new user</h4>
          <form onSubmit={handleAddUserClick}>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={newEmail}
                onChange={(e) => setNewEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                required
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>First Name</label>
                <input
                  type="text"
                  value={newFirstName}
                  onChange={(e) => setNewFirstName(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label>Last Name</label>
                <input
                  type="text"
                  value={newLastName}
                  onChange={(e) => setNewLastName(e.target.value)}
                />
              </div>
            </div>
            <div className="form-group">
              <label>Role</label>
              <select
                value={newRole}
                onChange={(e) => setNewRole(e.target.value)}>
                <option value="client">Client</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <button type="submit" className="btn-primary">
              Add User
            </button>
          </form>
        </motion.div>

        <motion.div
          className="product-table-container"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}>
          <div className="product-table-header">
            <h2>All Customers</h2>
            <div className="search-container">
              <input
                type="text"
                placeholder="Search customers..."
                onChange={handleSearchChange}
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
                      <span>ID</span>
                      {renderSortIcon("id")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("email")}
                    className="sortable-header"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>Email</span>
                      {renderSortIcon("email")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("username")}
                    className="sortable-header"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>Username</span>
                      {renderSortIcon("username")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("first_name")}
                    className="sortable-header"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>First Name</span>
                      {renderSortIcon("first_name")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("last_name")}
                    className="sortable-header"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>Last Name</span>
                      {renderSortIcon("last_name")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("role")}
                    className="sortable-header"
                    style={{ textAlign: "center" }}>
                    <div className="header-content">
                      <span>Role</span>
                      {renderSortIcon("role")}
                    </div>
                  </th>
                  <th style={{ textAlign: "center" }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {currentSlice.length > 0 ? (
                  currentSlice.map((cust) =>
                    editId === cust.id ? (
                      <motion.tr
                        key={cust.id}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.3 }}
                        className="edit-row">
                        <td style={{ textAlign: "center" }}>{cust.id}</td>
                        <td style={{ textAlign: "center" }}>
                          <input
                            type="email"
                            value={editEmail}
                            onChange={(e) => setEditEmail(e.target.value)}
                          />
                        </td>
                        <td style={{ textAlign: "center" }}>
                          <input
                            type="text"
                            value={editUsername}
                            onChange={(e) => setEditUsername(e.target.value)}
                          />
                        </td>
                        <td style={{ textAlign: "center" }}>
                          <input
                            type="text"
                            value={editFirstName}
                            onChange={(e) => setEditFirstName(e.target.value)}
                          />
                        </td>
                        <td style={{ textAlign: "center" }}>
                          <input
                            type="text"
                            value={editLastName}
                            onChange={(e) => setEditLastName(e.target.value)}
                          />
                        </td>
                        <td style={{ textAlign: "center" }}>
                          <select
                            value={editRole}
                            onChange={(e) => setEditRole(e.target.value)}
                            style={{ textAlign: "center" }}>
                            <option value="client">Client</option>
                            <option value="admin">Admin</option>
                          </select>
                        </td>
                        <td
                          className="action-cell"
                          style={{ textAlign: "center" }}>
                          <button
                            onClick={handleEditClick}
                            className="btn-save">
                            Save
                          </button>
                          <button onClick={cancelEdit} className="btn-cancel">
                            Cancel
                          </button>
                        </td>
                      </motion.tr>
                    ) : (
                      <motion.tr
                        key={cust.id}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.3 }}>
                        <td style={{ textAlign: "center" }}>{cust.id}</td>
                        <td style={{ textAlign: "center" }}>{cust.email}</td>
                        <td style={{ textAlign: "center" }}>{cust.username}</td>
                        <td style={{ textAlign: "center" }}>
                          {cust.first_name}
                        </td>
                        <td style={{ textAlign: "center" }}>
                          {cust.last_name}
                        </td>
                        <td style={{ textAlign: "center" }}>{cust.role}</td>
                        <td
                          className="action-cell"
                          style={{ textAlign: "center" }}>
                          <button
                            onClick={() => startEdit(cust)}
                            className="btn-edit">
                            <Edit size={18} />
                          </button>
                          <button
                            onClick={() => handleDeleteClick(cust.id)}
                            className="btn-delete">
                            <Trash2 size={18} />
                          </button>
                        </td>
                      </motion.tr>
                    )
                  )
                ) : (
                  <tr>
                    <td colSpan="7" className="no-results">
                      No users found matching your search criteria
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {filteredCustomers.length > 0 && (
            <div className="pagination-container">
              <div className="pagination-info">
                <p className="pagination-text">
                  Displaying {indexOfFirst + 1} to{" "}
                  {Math.min(indexOfLast, filteredCustomers.length)} of{" "}
                  {filteredCustomers.length} users
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

                {renderPaginationButtons()}

                <button
                  onClick={nextPage}
                  disabled={currentPage >= totalPages}
                  className={`pagination-button ${
                    currentPage >= totalPages ? "disabled" : ""
                  }`}>
                  <ChevronRight size={16} />
                  <span>&gt;</span>
                </button>
              </div>
            </div>
          )}
        </motion.div>
      </main>

      <ConfirmationModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        onConfirm={handleDelete}
        title="Confirm Deletion"
        message="Are you sure you want to delete this user? This action cannot be undone."
      />

      <ConfirmationModal
        isOpen={isEditConfirmModalOpen}
        onClose={() => setIsEditConfirmModalOpen(false)}
        onConfirm={handleEditSubmit}
        title="Confirm Update"
        message="Do you want to save changes to this user?"
      />

      <ConfirmationModal
        isOpen={isAddConfirmModalOpen}
        onClose={() => setIsAddConfirmModalOpen(false)}
        onConfirm={handleAddUser}
        title="Confirm Addition"
        message="Do you want to add this new user?"
      />
    </div>
  );
};

export default AdminUsers;
