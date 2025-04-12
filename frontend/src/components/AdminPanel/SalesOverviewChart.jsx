import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { motion } from "framer-motion";

const SalesOverviewChart = ({ data }) => {
  const chartData =
    data &&
    data.labels &&
    Array.isArray(data.labels) &&
    data.data &&
    Array.isArray(data.data)
      ? data.labels.map((label, index) => ({
          name: label,
          sales: Number(data.data[index] || 0),
        }))
      : [];

  return (
    <motion.div
      className="sales-overview-chart"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}>
      <h2 className="text-lg font-medium mb-4">Sales Overview</h2>

      {chartData.length === 0 ? (
        <div className="h-80 flex items-center justify-center">
          No sales data available
        </div>
      ) : (
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#4B5563" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis
                stroke="#9ca3af"
                domain={[0, data.y_axis_max || "auto"]}
                tickFormatter={(value) => `$${value}`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(31, 41, 55, 0.8)",
                  borderColor: "#4B5563",
                }}
                itemStyle={{ color: "#E5E7EB" }}
                formatter={(value) => [`$${value.toLocaleString()}`, "Sales"]}
              />
              <Line
                type="monotone"
                dataKey="sales"
                stroke="#6366F1"
                strokeWidth={3}
                dot={{ fill: "#6366F1", strokeWidth: 2, r: 6 }}
                activeDot={{ r: 8, strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </motion.div>
  );
};

export default SalesOverviewChart;
