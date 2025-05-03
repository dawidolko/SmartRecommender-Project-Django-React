import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { motion } from "framer-motion";

const SalesOverviewChart = ({ data }) => {
  const defaultData = [
    { name: "Jan", sales: 4000 },
    { name: "Feb", sales: 3000 },
    { name: "Mar", sales: 5000 },
    { name: "Apr", sales: 2780 },
    { name: "May", sales: 1890 },
    { name: "Jun", sales: 2390 },
    { name: "Jul", sales: 3490 },
  ];

  let chartData = defaultData;

  if (
    data &&
    data.labels &&
    Array.isArray(data.labels) &&
    data.data &&
    Array.isArray(data.data)
  ) {
    if (data.labels.length > 0 && data.data.length > 0) {
      chartData = data.labels.map((label, index) => ({
        name: label,
        sales: Number(data.data[index] || 0),
      }));
    }
  }

  return (
    <motion.div
      className="sales-overview-chart"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}>
      <h2>Sales Overview</h2>

      {!chartData || chartData.length === 0 ? (
        <div
          style={{
            height: "300px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#9ca3af",
          }}>
          No sales data available
        </div>
      ) : (
        <div style={{ height: "300px", width: "100%" }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{ top: 20, right: 30, left: 20, bottom: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#4B5563" />
              <XAxis
                dataKey="name"
                stroke="#9ca3af"
                tick={{ fill: "#9ca3af" }}
              />
              <YAxis
                stroke="#9ca3af"
                tick={{ fill: "#9ca3af" }}
                domain={[0, "auto"]}
                tickFormatter={(value) => `$${value}`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(31, 41, 55, 0.8)",
                  borderColor: "#4B5563",
                  color: "#E5E7EB",
                }}
                labelStyle={{ color: "#E5E7EB" }}
                itemStyle={{ color: "#E5E7EB" }}
                formatter={(value) => [`$${value.toLocaleString()}`, "Sales"]}
              />
              <Legend
                verticalAlign="top"
                wrapperStyle={{ paddingBottom: "10px", color: "#9ca3af" }}
              />
              <Line
                name="Sales Amount"
                type="monotone"
                dataKey="sales"
                stroke="#6366F1"
                strokeWidth={3}
                dot={{ fill: "#6366F1", strokeWidth: 2, r: 6 }}
                activeDot={{ r: 8, strokeWidth: 2 }}
                isAnimationActive={true}
                animationDuration={1500}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </motion.div>
  );
};

export default SalesOverviewChart;
