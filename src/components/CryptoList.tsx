import React from "react";
import { CryptoCard } from "../components/CryptoCard";
import type {Crypto} from "../pages/Home";

interface CryptoListProps {
  cryptos: Crypto[];
  viewMode: "grid" | "list";
}

export const CryptoList: React.FC<CryptoListProps> = ({ cryptos, viewMode }) => (
    <div className={`crypto-container ${viewMode}`}>
      {cryptos.map((crypto) => (
          <CryptoCard crypto={crypto} key={crypto.id} />
      ))}
    </div>
);
