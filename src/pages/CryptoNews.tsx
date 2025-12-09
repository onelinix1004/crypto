import React, { useEffect, useState } from "react";
import { fetchNews, type NewsItem } from "../services/newsApi";
import { NewsList } from "../components/NewsList";
import { Header } from "../components/Header";
import "../styles/news.css";

export const CryptoNews: React.FC = () => {
  const [newsList, setNewsList] = useState<NewsItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadNews = async () => {
      try {
        const data = await fetchNews();
        setNewsList(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load news");
      } finally {
        setIsLoading(false);
      }
    };

    loadNews();
  }, []);

  return (
      <div className="app">
        <Header /> {/* Nếu muốn thêm search riêng cho news, có thể truyền prop */}

        <div className="news-page">
          <h1>📢 Crypto News</h1>
          {isLoading && <p>Loading news...</p>}
          {error && <p className="error">{error}</p>}
          {!isLoading && !error && <NewsList newsList={newsList} />}
        </div>
      </div>
  );
};
