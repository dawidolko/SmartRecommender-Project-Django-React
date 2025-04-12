import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";

const SalesTrendChart = ({ trend }) => {
  if (!trend || !trend.labels || !trend.data || trend.labels.length === 0) {
    return (
      <div className="bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700">
        <h2 className="text-xl font-semibold text-gray-100 mb-4">Sales Trend</h2>
        <div className="flex items-center justify-center" style={{ height: 300 }}>
          <p className="text-gray-400">No data to display</p>
        </div>
      </div>
    );
  }

  const data = trend.labels.map((label, index) => ({
    month: label,
    sales: trend.data[index],
  }));

  return (
    <div className="sales-trend-chart">
      <h2 className="text-xl font-semibold text-gray-100 mb-4">Sales Trend</h2>
      <div style={{ width: "90%", height: 300, margin: "0 auto" }}>
        <ResponsiveContainer>
          <LineChart data={data} margin={{ top: 20, right: 20, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="4 4" stroke="#374151" />
            <XAxis dataKey="month" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(31, 41, 55, 0.8)",
                borderColor: "#4B5563",
              }}
              itemStyle={{ color: "#E5E7EB" }}
            />
            <Legend />
            <Line type="monotone" dataKey="sales" stroke="#8B5CF6" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default SalesTrendChart;