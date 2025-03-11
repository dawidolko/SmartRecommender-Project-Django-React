import React, { useEffect, useState } from "react";
import axios from "axios";
import { format } from "date-fns";
import { useNavigate } from "react-router-dom";

const ClientOrders = () => {
  const [orders, setOrders] = useState([]);
  const [sortKey, setSortKey] = useState("date");
  const [sortOrder, setSortOrder] = useState("asc");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access");
    axios
      .get("http://127.0.0.1:8000/api/orders/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setOrders(res.data))
      .catch((err) => console.error("Error fetching orders:", err));
  }, []);

  const handleViewDetails = (orderId) => {
    navigate(`/client/orders/${orderId}`);
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

  const sortedOrders = [...orders].sort((a, b) => {
    let comp = 0;
    if (sortKey === "date") {
      comp = new Date(a.date_order) - new Date(b.date_order);
    } else if (sortKey === "status") {
      comp = a.status.localeCompare(b.status);
    }
    return sortOrder === "asc" ? comp : -comp;
  });

  return (
    <div className="container client-orders">
      <h2>Your Orders</h2>
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th>#</th>
              <th style={{ cursor: "pointer" }} onClick={() => handleSort("date")}>
                Date{renderSortIndicator("date")}
              </th>
              <th style={{ cursor: "pointer" }} onClick={() => handleSort("status")}>
                Status{renderSortIndicator("status")}
              </th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {sortedOrders.map((order) => (
              <tr key={order.id}>
                <td>{order.id}</td>
                <td>{format(new Date(order.date_order), "dd MMM yyyy, HH:mm")}</td>
                <td>{order.status}</td>
                <td>
                  <button className="btn btn-primary" onClick={() => handleViewDetails(order.id)}>
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

export default ClientOrders;
