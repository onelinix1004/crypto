import React from "react";

interface ControlsProps {
  sortBy: "market_cap_rank" | "name" | "price" | "price_desc" | "change" | "market_cap";
  setSortBy: React.Dispatch<React.SetStateAction<"market_cap_rank" | "name" | "price" | "price_desc" | "change" | "market_cap">>;
  viewMode: "grid" | "list";
  setViewMode: React.Dispatch<React.SetStateAction<"grid" | "list">>;
}

export const Controls: React.FC<ControlsProps> = ({ sortBy, setSortBy, viewMode, setViewMode }) => (
    <div className="controls">
      <div className="filter-group">
        <label>Sort by:</label>
        <select
            value={sortBy}
            onChange={(e) =>
                setSortBy(e.target.value as
                    "market_cap_rank" | "name" | "price" | "price_desc" | "change" | "market_cap"
                )
            }
        >
        <option value="market_cap_rank">Rank</option>
          <option value="name">Name</option>
          <option value="price">Price (Low to High)</option>
          <option value="price_desc">Price (High to Low)</option>
          <option value="change">24h Change</option>
          <option value="market_cap">Market Cap</option>
        </select>
      </div>

      <div className="view-toggle">
        <button
            className={viewMode === "grid" ? "active" : ""}
            onClick={() => setViewMode("grid")}
        >
          Grid
        </button>
        <button
            className={viewMode === "list" ? "active" : ""}
            onClick={() => setViewMode("list")}
        >
          List
        </button>
      </div>
    </div>
);
