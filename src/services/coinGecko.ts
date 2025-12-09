const BASE_URL = "https://api.coingecko.com/api/v3";

export interface Crypto {
  id: string;
  symbol: string;
  name: string;
  image: string;
  current_price: number;
  market_cap: number;
  market_cap_rank: number;
  price_change_percentage_24h: number;
  total_volume: number;
}

export interface CoinData {
  id: string;
  symbol: string;
  name: string;
  description: {
    en: string;
  };
  market_data: {
    current_price: {
      usd: number;
    };
    market_cap: {
      usd: number;
    };
    price_change_percentage_24h: number;
    market_cap_rank: number;
    high_24h:{
      usd: number;
    }
    low_24h: {
      usd: number;
    };
    total_volume: {
      usd: number;
    };
    circulating_supply: number;
    total_supply: number;
  };
  image: {
    thumb: string;
    small: string;
    large: string;
  };
}

export interface ChartData {
  prices: [number, number][];
}


export const fetchCryptos = async (): Promise<Crypto[]> => {
  const response = await fetch(
      `${BASE_URL}/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch cryptos");
  }

  return response.json();
};

export const fetchCoinData = async (id: string): Promise<CoinData> => {
  const response = await fetch(
      `${BASE_URL}/coins/${id}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false`
  );
  if (!response.ok) {
    throw new Error("Failed to fetch coin data");
  }
  return response.json();
};

export const fetchChartData = async (id: string): Promise<ChartData> => {
  const response = await fetch(
      `${BASE_URL}/coins/${id}/market_chart?vs_currency=usd&days=7`
  );
  if (!response.ok) {
    throw new Error("Failed to fetch chart data");
  }
  return response.json();
};
