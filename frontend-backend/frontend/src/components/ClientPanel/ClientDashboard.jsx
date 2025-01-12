import React, { useEffect, useState } from "react";
import axios from "axios";
import CountUp from "react-countup";
import "./ClientPanel.scss";

const ClientDashboard = () => {
  const [purchasedItems, setPurchasedItems] = useState(0);
  const [complaints, setComplaints] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/client-stats/")
      .then((res) => {
        setPurchasedItems(res.data.purchased_items);
        setComplaints(res.data.complaints);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching client stats:", error);
        setError("Failed to fetch data. Please try again.");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div style={{ padding: "2rem" }}>Loading stats...</div>;
  }

  if (error) {
    return <div style={{ padding: "2rem", color: "red" }}>{error}</div>;
  }

  return (
    <div className="container">
      <h1>Client Dashboard</h1>
      <div className="row mt-4">
        {/* Purchased Items */}
        <div className="col-md-6">
          <div className="small-box bg-primary">
            <div className="inner">
              <h3>
                <CountUp end={purchasedItems} duration={1.5} />
              </h3>
              <p>Purchased Items</p>
            </div>
          </div>
        </div>

        {/* Complaints */}
        <div className="col-md-6">
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

export default ClientDashboard;
