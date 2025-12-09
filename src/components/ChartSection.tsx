import React from "react";
import { LineChart, ResponsiveContainer, CartesianGrid, XAxis, YAxis, Line, Tooltip } from "recharts";

interface ChartPoint {
  time: string;
  price: number;
}

interface ChartSectionProps {
  chartData: ChartPoint[];
}

export const ChartSection: React.FC<ChartSectionProps> = ({ chartData }) => (
    <div className="chart-section">
      <h3>Price Chart (7 Days)</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
          <XAxis dataKey="time" stroke="#9ca3af" style={{ fontSize: "12px" }} />
          <YAxis stroke="#9ca3af" style={{ fontSize: "12px" }} domain={["auto", "auto"]} />
          <Tooltip
              contentStyle={{
                backgroundColor: "rgba(20, 20, 40, 0.95)",
                border: "1px solid rgba(255, 255, 255, 0.1)",
                borderRadius: "8px",
                color: "#e0e0e0",
              }}
          />
          <Line type="monotone" dataKey="price" stroke="#ADD8E6" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
);
