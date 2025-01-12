import React, { useEffect, useState } from "react";
import axios from "axios";

const AdminCustomers = () => {
  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/users/?role=client")
      .then((res) => {
        setCustomers(res.data);
      })
      .catch((err) => {
        console.error("Error fetching customers:", err);
      });
  }, []);

  const handleDelete = async (userId) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;
    try {
      await axios.delete(`http://127.0.0.1:8000/api/users/${userId}/`);
      setCustomers((prev) => prev.filter((c) => c.id !== userId));
    } catch (error) {
      console.error("Error deleting user:", error);
    }
  };

  return (
    <div className="container">
      <h1>Customers</h1>
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th>#</th>
              <th>Email</th>
              <th>Nickname</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {customers.map((cust) => (
              <tr key={cust.id}>
                <td>{cust.id}</td>
                <td>{cust.email}</td>
                <td>{cust.nickname}</td>
                <td>
                  <button
                    className="table-button table-button--delete btn btn-danger"
                    onClick={() => handleDelete(cust.id)}>
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

export default AdminCustomers;
