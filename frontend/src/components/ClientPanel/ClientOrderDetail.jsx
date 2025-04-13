import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import { format } from "date-fns";
import "./ClientPanel.scss";
import config from "../../config/config";

const ClientOrderDetail = () => {
  const { id } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
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
      .get(`${config.apiUrl}/api/client/orders/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setOrder(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching order details:", err);
        setError("Failed to fetch order details");
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div className="loading-spinner"></div>;
  if (error) return <div>{error}</div>;
  if (!order) return <div>No order found.</div>;

  return (
    <div className="container client-order-detail">
      <h2>Order #{order.id} Details</h2>
      <p>
        <strong>Date: </strong>
        {format(new Date(order.date_order), "dd MMM yyyy, HH:mm")}
      </p>
      <p>
        <strong>Status: </strong>
        <span className={getStatusClass(order.status)}>{order.status}</span>
      </p>
      <p>
        <strong>Total:</strong>${order.total.toFixed(2)}
      </p>

      <h3 style={{ marginTop: "1rem" }}>Ordered Products:</h3>
      <table className="table table-hover">
        <thead>
          <tr>
            <th style={{ textAlign: "center" }}>Image</th>
            <th style={{ textAlign: "center" }}>Name</th>
            <th style={{ textAlign: "center" }}>Quantity</th>
            <th style={{ textAlign: "center" }}>Price (each)</th>
          </tr>
        </thead>
        <tbody>
          {order.order_products.map((op) => {
            const product = op.product;
            const imgSrc =
              product.photos && product.photos.length > 0
                ? `${config.apiUrl}/media/${product.photos[0].path}`
                : "https://via.placeholder.com/150";
            return (
              <tr key={op.id}>
                <td
                  style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    border: "none",
                    borderBottom: "1px solid #ddd",
                  }}>
                  <img
                    src={imgSrc}
                    alt={product.name}
                    style={{ width: "100px" }}
                  />
                </td>
                <td style={{ textAlign: "center" }}>{product.name}</td>
                <td style={{ textAlign: "center" }}>{op.quantity}</td>
                <td style={{ textAlign: "center" }}>
                  ${Number(product.price).toFixed(2)}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <button
        className="btn btn-primary back_button btn-main-client"
        onClick={() => navigate(-1)}>
        Back to Complaints
      </button>
    </div>
  );
};

export default ClientOrderDetail;
