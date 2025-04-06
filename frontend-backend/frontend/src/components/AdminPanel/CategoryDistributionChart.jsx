import React from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

const COLORS = ["#8B5CF6", "#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#EC4899"];

const CategoryDistributionChart = ({ category_distribution }) => {
  if (!category_distribution || !category_distribution.labels || !category_distribution.data) {
    return (
      <div className="bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700">
        <h2 className="text-xl font-semibold mb-4">Category Distribution</h2>
        <div className="flex items-center justify-center" style={{ height: 300 }}>
          <p className="text-gray-400">No data to display</p>
        </div>
      </div>
    );
  }

  const data = category_distribution.labels.map((label, index) => ({
    name: label,
    value: category_distribution.data[index],
  }));

  return (
    <div className="category-distribution-chart">
      <h2 className="text-xl font-semibold mb-4">Category Distribution</h2>
      <div style={{ width: "100%", height: 470 }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={true}
              outerRadius={150}
              fill="#8884d8"
              dataKey="value"
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(31, 41, 55, 0.8)",
                borderColor: "#4B5563",
              }}
              itemStyle={{ color: "#E5E7EB" }}
            />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default CategoryDistributionChart;