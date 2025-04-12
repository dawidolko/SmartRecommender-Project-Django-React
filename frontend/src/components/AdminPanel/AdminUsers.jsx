import React, { useEffect, useState } from "react";
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

import StatCard from "./StatCard";
import UserGrowthChart from "./UserGrowthChart";
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

  useEffect(() => {
    fetchCustomers();
    fetchStatsFromBackend();
  }, []);

  useEffect(() => {
    handleFilteringAndSorting();
  }, [
    customers,
    searchTerm,
    sortField,
    sortDirection,
    // eslint-disable-next-line no-use-before-define
    handleFilteringAndSorting,
  ]);

  const fetchCustomers = async () => {
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/users/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setCustomers(res.data);
    } catch (err) {
      console.error("Error fetching customers:", err);
    }
  };

  const fetchStatsFromBackend = async () => {
    const token = localStorage.getItem("access");
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/api/admin-dashboard-stats/",
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
    }
  };

  const handleAddUser = async (e) => {
    e.preventDefault();
    if (!newEmail || !newUsername) {
      alert("Email i Username są wymagane do utworzenia użytkownika.");
      return;
    }
    const token = localStorage.getItem("access");
    try {
      await axios.post(
        "http://127.0.0.1:8000/api/users/",
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
    } catch (err) {
      console.error("Error creating new user:", err);
      alert("Error occurred while creating user.");
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

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    if (!editEmail || !editUsername) {
      alert("Email i Username nie mogą być puste.");
      return;
    }
    const token = localStorage.getItem("access");
    try {
      await axios.put(
        `http://127.0.0.1:8000/api/users/${editId}/`,
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
    } catch (err) {
      console.error("Error updating user:", err);
      alert("Error occurred while updating user.");
    }
  };

  const handleDelete = async (userId) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;
    const token = localStorage.getItem("access");
    try {
      await axios.delete(`http://127.0.0.1:8000/api/users/${userId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchCustomers();
    } catch (error) {
      console.error("Error deleting user:", error);
    }
  };

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const handleFilteringAndSorting = () => {
    let data = [...customers];

    data = data.filter((c) => {
      const term = searchTerm.toLowerCase();
      const emailMatch = c.email?.toLowerCase().includes(term);
      const userMatch = c.username?.toLowerCase().includes(term);
      const fnameMatch = c.first_name?.toLowerCase().includes(term);
      const lnameMatch = c.last_name?.toLowerCase().includes(term);
      return emailMatch || userMatch || fnameMatch || lnameMatch;
    });

    data.sort((a, b) => {
      let fieldA = a[sortField] || "";
      let fieldB = b[sortField] || "";
      if (typeof fieldA === "string") fieldA = fieldA.toLowerCase();
      if (typeof fieldB === "string") fieldB = fieldB.toLowerCase();

      if (fieldA < fieldB) return sortDirection === "asc" ? -1 : 1;
      if (fieldA > fieldB) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });

    setFilteredCustomers(data);
    setCurrentPage(1);
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

  const indexOfLast = currentPage * customersPerPage;
  const indexOfFirst = indexOfLast - customersPerPage;
  const currentSlice = filteredCustomers.slice(indexOfFirst, indexOfLast);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const nextPage = () => {
    if (currentPage < Math.ceil(filteredCustomers.length / customersPerPage)) {
      setCurrentPage(currentPage + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

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
          <form onSubmit={handleAddUser}>
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
                onChange={(e) => setSearchTerm(e.target.value)}
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
                    className="sortable-header">
                    <div className="header-content">
                      <span>ID</span>
                      {renderSortIcon("id")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("email")}
                    className="sortable-header">
                    <div className="header-content">
                      <span>Email</span>
                      {renderSortIcon("email")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("username")}
                    className="sortable-header">
                    <div className="header-content">
                      <span>Username</span>
                      {renderSortIcon("username")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("first_name")}
                    className="sortable-header">
                    <div className="header-content">
                      <span>First Name</span>
                      {renderSortIcon("first_name")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("last_name")}
                    className="sortable-header">
                    <div className="header-content">
                      <span>Last Name</span>
                      {renderSortIcon("last_name")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("role")}
                    className="sortable-header">
                    <div className="header-content">
                      <span>Role</span>
                      {renderSortIcon("role")}
                    </div>
                  </th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {currentSlice.map((cust) =>
                  editId === cust.id ? (
                    <motion.tr
                      key={cust.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.3 }}
                      className="edit-row">
                      <td>{cust.id}</td>
                      <td>
                        <input
                          type="email"
                          value={editEmail}
                          onChange={(e) => setEditEmail(e.target.value)}
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          value={editUsername}
                          onChange={(e) => setEditUsername(e.target.value)}
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          value={editFirstName}
                          onChange={(e) => setEditFirstName(e.target.value)}
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          value={editLastName}
                          onChange={(e) => setEditLastName(e.target.value)}
                        />
                      </td>
                      <td>
                        <select
                          value={editRole}
                          onChange={(e) => setEditRole(e.target.value)}>
                          <option value="client">Client</option>
                          <option value="admin">Admin</option>
                        </select>
                      </td>
                      <td className="action-cell">
                        <button onClick={handleEditSubmit} className="btn-save">
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
                      <td>{cust.id}</td>
                      <td>{cust.email}</td>
                      <td>{cust.username}</td>
                      <td>{cust.first_name}</td>
                      <td>{cust.last_name}</td>
                      <td>{cust.role}</td>
                      <td className="action-cell">
                        <button
                          onClick={() => startEdit(cust)}
                          className="btn-edit">
                          <Edit size={18} />
                        </button>
                        <button
                          onClick={() => handleDelete(cust.id)}
                          className="btn-delete">
                          <Trash2 size={18} />
                        </button>
                      </td>
                    </motion.tr>
                  )
                )}
              </tbody>
            </table>
          </div>

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
              {Array.from({
                length: Math.ceil(filteredCustomers.length / customersPerPage),
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
                    Math.ceil(filteredCustomers.length / customersPerPage),
                    currentPage + 2
                  )
                )}
              <button
                onClick={nextPage}
                disabled={
                  currentPage >=
                  Math.ceil(filteredCustomers.length / customersPerPage)
                }
                className={`pagination-button ${
                  currentPage >=
                  Math.ceil(filteredCustomers.length / customersPerPage)
                    ? "disabled"
                    : ""
                }`}>
                <ChevronRight size={16} />
                <span>&gt;</span>
              </button>
            </div>
          </div>
        </motion.div>

        <div className="chart-container-products">
          <div className="chart-item">
            <UserGrowthChart />
          </div>
          <div className="chart-item"></div>
        </div>
      </main>
    </div>
  );
};

export default AdminUsers;
