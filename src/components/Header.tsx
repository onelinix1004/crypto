// Header.tsx
import React from "react";

interface HeaderProps {
  searchQuery?: string;
  setSearchQuery?: (value: string) => void;
  coinName?: string;
  onBack?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
                                                searchQuery,
                                                setSearchQuery,
                                                coinName,
                                                onBack,
                                              }) => {
  return (
      <header className="header">
        <div className="header-content">
          <div className="logo-section">
            <h1>🚀 Crypto Tracker</h1>
            <p>Real-time cryptocurrency prices and market data</p>
          </div>

          {/* Nếu coinName tồn tại => Detail page */}
          {coinName ? (
              <div className="coin-header-controls">
                <button className="back-button" onClick={onBack}>
                  ← Back
                </button>
              </div>
          ) : (
              // Ngược lại => Home page, hiển thị search
              <div className="search-section">
                <input
                    type="text"
                    placeholder="Search cryptos..."
                    className="search-input"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery?.(e.target.value)}
                />
              </div>
          )}
        </div>
      </header>
  );
};
