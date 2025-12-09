export interface NewsItem {
  id: string;
  title: string;
  source: string;
  url: string;
  publishedAt: string;
  image?: string;
}

const NEWS_API_URL = "https://api.example.com/crypto-news"; 

export const fetchNews = async (): Promise<NewsItem[]> => {
  const res = await fetch(NEWS_API_URL);
  if (!res.ok) throw new Error("Failed to fetch news");
  const data = await res.json();
  return data.articles || []; // tùy API
};
