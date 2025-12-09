import React, { useEffect, useState } from "react";
import {useNavigate, useParams} from "react-router-dom";
import {fetchCoinData, fetchChartData, type ChartData} from "../services/coinGecko";
import type { CoinData } from "../services/coinGecko";
import { Loading } from "../components/Loading";
import { NoResults } from "../components/NoResults";
import { PriceSection } from "../components/PriceSection";
import { ChartSection } from "../components/ChartSection";
import { StatsGrid } from "../components/StatsGrid";
import {Layout} from "../layout/MainLayout.tsx";

interface ChartPoint {
  time: string;
  price: number;
}

export const CoinDetail: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [coin, setCoin] = useState<CoinData | null>(null);
  const [chartData, setChartData] = useState<ChartPoint[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    const loadData = async () => {
      try {
        const coinData = await fetchCoinData(id);
        const chart: ChartData = await fetchChartData(id);

        const formattedChart: ChartPoint[] = chart.prices.map(
            (p: [number, number]) => ({
              time: new Date(p[0]).toLocaleDateString("en-US", {
                month: "short",
                day: "numeric",
              }),
              price: Number(p[1].toFixed(2)),
            })
        );

        setCoin(coinData);
        setChartData(formattedChart);
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [id]);

  if (isLoading) return <Loading />;
  if (!coin) return <NoResults />;

  return (
      <Layout coinName={coin.name} onBack={() => navigate("/")}>
        <div className="coin-detail">
          <div className="coin-header">
            <div className="coin-title">
              <img src={coin.image?.large} alt={coin.name} />
              <div>
                <h1>{coin.name}</h1>
                <p className="symbol">{coin.symbol.toUpperCase()}</p>
              </div>
            </div>
            <span className="rank">Rank #{coin.market_data?.market_cap_rank}</span>
          </div>

          <PriceSection coin={coin} />
          <ChartSection chartData={chartData} />
          <StatsGrid coin={coin} />
        </div>
      </Layout>
  );
};
