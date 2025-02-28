import React, { useEffect, useState } from "react";
import axios from "axios";
import CountUp from "react-countup";
import "./AdminPanel.scss";

const AdminDashboard = () => {
  const [orders, setOrders] = useState(0);
  const [clients, setClients] = useState(0);
  const [products, setProducts] = useState(0);
  const [complaints, setComplaints] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access");
    axios
      .get("http://127.0.0.1:8000/api/admin-stats/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setOrders(res.data.orders);
        setClients(res.data.clients);
        setProducts(res.data.products);
        setComplaints(res.data.complaints);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching admin stats:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div style={{ padding: "2rem" }}>Loading stats...</div>;
  }

  return (
    <div className="container">
      <h1>Admin Dashboard</h1>
      <p>Welcome to the administrative panel.</p>
      <div className="row mt-4">
        {/* Orders */}
        <div className="col-md-3">
          <div className="small-box bg-primary">
            <div className="inner">
              <h3>
                <CountUp end={orders} duration={1.5} />
              </h3>
              <p>Orders</p>
            </div>
          </div>
        </div>

        {/* Clients */}
        <div className="col-md-3">
          <div className="small-box bg-success">
            <div className="inner">
              <h3>
                <CountUp end={clients} duration={1.5} />
              </h3>
              <p>Customers</p>
            </div>
          </div>
        </div>

        {/* Products */}
        <div className="col-md-3">
          <div className="small-box bg-warning">
            <div className="inner">
              <h3>
                <CountUp end={products} duration={1.5} />
              </h3>
              <p>Products</p>
            </div>
          </div>
        </div>

        {/* Complaints */}
        <div className="col-md-3">
          <div className="small-box bg-danger">
            <div className="inner">
              <h3>
                <CountUp end={complaints} duration={1.5} />
              </h3>
              <p>Complaints</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
