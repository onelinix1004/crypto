import React from "react";
import { formatPrice } from "../utils/formatter";
import type { CoinData } from "../services/coinGecko";

interface PriceSectionProps {
  coin: CoinData;
}

export const PriceSection: React.FC<PriceSectionProps> = ({ coin }) => {
  const priceChange = coin.market_data?.price_change_percentage_24h || 0;
  const isPositive = priceChange >= 0;

  return (
      <div className="coin-price-section">
        <div className="current-price">
          <h2>{formatPrice(coin.market_data?.current_price.usd || 0)}</h2>
          <span className={`change-badge ${isPositive ? "positive" : "negative"}`}>
          {isPositive ? "↑" : "↓"} {Math.abs(priceChange).toFixed(2)}%
        </span>
        </div>

        <div className="price-ranges">
          <div className="price-range">
            <span className="range-label">24h High</span>
            <span className="range-value">{formatPrice(coin.market_data?.high_24h.usd || 0)}</span>
          </div>
          <div className="price-range">
            <span className="range-label">24h Low</span>
            <span className="range-value">{formatPrice(coin.market_data?.low_24h.usd || 0)}</span>
          </div>
        </div>
      </div>
  );
};
