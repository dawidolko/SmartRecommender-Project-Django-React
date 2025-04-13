import React, { useEffect, useState } from "react";
import axios from "axios";
import { format } from "date-fns";
import { useNavigate } from "react-router-dom";
import config from "../../config/config";

const ClientOrders = () => {
  const [orders, setOrders] = useState([]);
  const [sortKey, setSortKey] = useState("date");
  const [sortOrder, setSortOrder] = useState("asc");
  const navigate = useNavigate();

  const getStatusClass = (status) => {
    switch (status) {
      case "Pending":
        return "status-pending";
      case "Processing":
        return "status-processing";
      case "Shipped":
        return "status-shipped";
      case "Delivered":
        return "status-delivered";
      case "Cancelled":
        return "status-cancelled";
      default:
        return "";
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("access");
    axios
      .get(`${config.apiUrl}/api/orders/`, {
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
              <th class="text-align-client">#</th>
              <th
                className="hide-complaints2 text-align-client"
                style={{ cursor: "pointer" }}
                onClick={() => handleSort("date")}>
                Date {renderSortIndicator("date")}
              </th>
              <th
                style={{ cursor: "pointer", textAlign: "center" }}
                onClick={() => handleSort("status")}>
                Status {renderSortIndicator("status")}
              </th>
              <th class="text-align-client">Actions</th>
            </tr>
          </thead>
          <tbody>
            {sortedOrders.map((order) => (
              <tr key={order.id}>
                <td class="text-align-client">{order.id}</td>
                <td className="hide-complaints2 text-align-client">
                  {format(new Date(order.date_order), "dd MMM yyyy, HH:mm")}
                </td>
                <td
                  style={{ textAlign: "center" }}
                  className={getStatusClass(order.status)}>
                  {order.status}
                </td>
                <td className="table-center">
                  <button
                    className="btn btn-primary btn-main-client"
                    onClick={() => handleViewDetails(order.id)}>
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
