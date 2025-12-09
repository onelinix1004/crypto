import { useEffect, useState } from "react";
import { fetchCryptos } from "../services/coinGecko";
import type {Crypto} from "../services/coinGecko";
import { Controls } from "../components/Controls";
import { CryptoList } from "../components/CryptoList";
import { Loading } from "../components/Loading";
import {Layout} from "../layout/MainLayout.tsx";

export const Home: React.FC = () => {
  const [cryptoList, setCryptoList] = useState<Crypto[]>([]);
  const [filteredList, setFilteredList] = useState<Crypto[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [sortBy, setSortBy] = useState<
      "market_cap_rank" | "name" | "price" | "price_desc" | "change" | "market_cap"
  >("market_cap_rank");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    const interval = setInterval(fetchCryptoData, 2000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    filterAndSort();
  }, [sortBy, cryptoList, searchQuery]);

  const fetchCryptoData = async () => {
    try {
      const data: Crypto[] = await fetchCryptos();
      setCryptoList(data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const filterAndSort = () => {
    const filtered = cryptoList.filter(
        (crypto) =>
            crypto.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            crypto.symbol.toLowerCase().includes(searchQuery.toLowerCase())
    );

    filtered.sort((a, b) => {
      switch (sortBy) {
        case "name":
          return a.name.localeCompare(b.name);
        case "price":
          return a.current_price - b.current_price;
        case "price_desc":
          return b.current_price - a.current_price;
        case "change":
          return a.price_change_percentage_24h - b.price_change_percentage_24h;
        case "market_cap":
          return a.market_cap - b.market_cap;
        default:
          return a.market_cap_rank - b.market_cap_rank;
      }
    });

    setFilteredList(filtered);
  };

  return (
      <Layout searchQuery={searchQuery} setSearchQuery={setSearchQuery}>
        <Controls
            sortBy={sortBy}
            setSortBy={setSortBy}
            viewMode={viewMode}
            setViewMode={setViewMode}
        />
        {isLoading ? (
            <Loading />
        ) : (
            <CryptoList cryptos={filteredList} viewMode={viewMode} />
        )}
      </Layout>
  );
};
