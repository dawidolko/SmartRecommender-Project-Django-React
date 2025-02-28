import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { format } from "date-fns";
import "./ClientOrderDetail.scss";

const ClientOrderDetail = () => {
    const { id } = useParams();
    const [order, setOrder] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem("access");
        axios
            .get(`http://127.0.0.1:8000/api/client/orders/${id}/`, {
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

    if (loading) return <div>Loading order details...</div>;
    if (error) return <div>{error}</div>;
    if (!order) return <div>No order found.</div>;

    return (
        <div className="container client-order-detail">
            <h2>Order #{order.id} Details</h2>
            <p>Date: {format(new Date(order.date_order), "dd MMM yyyy, HH:mm")}</p>
            <p>Status: {order.status}</p>
            <p>Total: ${order.total.toFixed(2)}</p>

            <h3>Products</h3>
            <table className="table table-hover">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Name</th>
                        <th>Quantity</th>
                        <th>Price (each)</th>
                    </tr>
                </thead>
                <tbody>
                    {order.order_products.map((op) => {
                        const product = op.product;
                        const imgSrc =
                            product.photos && product.photos.length > 0
                                ? `http://localhost:8000/media/${product.photos[0].path}`
                                : "https://via.placeholder.com/150";
                        return (
                            <tr key={op.id}>
                                <td>
                                    <img src={imgSrc} alt={product.name} style={{ width: "100px" }} />
                                </td>
                                <td>{product.name}</td>
                                <td>{op.quantity}</td>
                                <td>${product.price.toFixed(2)}</td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
};

export default ClientOrderDetail;
