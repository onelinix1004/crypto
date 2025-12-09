import React from "react";
import { useNavigate } from "react-router-dom";

export const NoResults: React.FC = () => {
  const navigate = useNavigate();
  return (
      <div className="app">
        <div className="no-results">
          <p>Coin not found</p>
          <button onClick={() => navigate("/")}>Go Back</button>
        </div>
      </div>
  );
};
