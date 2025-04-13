import React, { useEffect, useState } from "react";
import axios from "axios";
import config from "../../config/config";

const AdminOrders = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("access");
    axios
      .get(`${config.apiUrl}/api/orders/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        console.log("Orders data:", res.data);
        setOrders(res.data);
      })
      .catch((err) => {
        console.error("Error fetching orders:", err);
      });
  }, []);

  const getStatusClass = (status) => {
    switch (status) {
      case "Processing":
        return "processing";
      case "Shipped":
        return "shipped";
      case "Delivered":
        return "delivered";
      case "Cancelled":
        return "cancelled";
      case "Pending":
      default:
        return "pending";
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date
      .toLocaleString("en-GB", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
      })
      .replace(",", "")
      .replace(" ", "T")
      .substring(0, 16);
  };

  return (
    <div className="container container_orders">
      <h1>Orders</h1>
      <div className="table-responsive">
        <table className="table table-bordered table-hover table-collapse">
          <thead>
            <tr>
              <th>#</th>
              <th>Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((ord) => (
              <tr key={ord.id} className={getStatusClass(ord.status)}>
                <td>{ord.id}</td>
                <td>{formatDate(ord.date_order)}</td>
                <td>{ord.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminOrders;
