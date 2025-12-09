import React from "react";
import type { CoinData } from "../services/coinGecko";
import { formatMarketCap } from "../utils/formatter";

interface StatsGridProps {
  coin: CoinData;
}

export const StatsGrid: React.FC<StatsGridProps> = ({ coin }) => (
    <div className="stats-grid">
      <div className="stat-card">
        <span className="stat-label">Market Cap</span>
        <span className="stat-value">${formatMarketCap(coin.market_data?.market_cap.usd || 0)}</span>
      </div>
      <div className="stat-card">
        <span className="stat-label">Volume (24h)</span>
        <span className="stat-value">${formatMarketCap(coin.market_data?.total_volume.usd || 0)}</span>
      </div>
      <div className="stat-card">
        <span className="stat-label">Circulating Supply</span>
        <span className="stat-value">{coin.market_data?.circulating_supply?.toLocaleString() || "N/A"}</span>
      </div>
      <div className="stat-card">
        <span className="stat-label">Total Supply</span>
        <span className="stat-value">{coin.market_data?.total_supply?.toLocaleString() || "N/A"}</span>
      </div>
    </div>
);
