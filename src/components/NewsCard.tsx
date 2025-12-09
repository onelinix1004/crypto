import React from "react";
import type { NewsItem } from "../services/newsApi";

interface NewsCardProps {
  news: NewsItem;
}

export const NewsCard: React.FC<NewsCardProps> = ({ news }) => (
    <div className="news-card">
      {news.image && <img src={news.image} alt={news.title} />}
      <div className="news-content">
        <a href={news.url} target="_blank" rel="noopener noreferrer">
          <h3>{news.title}</h3>
        </a>
        <p className="news-source">{news.source}</p>
        <p className="news-date">{new Date(news.publishedAt).toLocaleString()}</p>
      </div>
    </div>
);
