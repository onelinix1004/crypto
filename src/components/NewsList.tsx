import React from "react";
import type { NewsItem } from "../services/newsApi";
import { NewsCard } from "./NewsCard";

interface NewsListProps {
  newsList: NewsItem[];
}

export const NewsList: React.FC<NewsListProps> = ({ newsList }) => (
    <div className="news-list">
      {newsList.length === 0 ? (
          <p>No news found.</p>
      ) : (
          newsList.map((news) => <NewsCard key={news.id} news={news} />)
      )}
    </div>
);
