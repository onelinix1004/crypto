// Layout.tsx
import React from "react";
import { Header } from "../components/Header";
import { Footer } from "../components/Footer";

interface LayoutProps {
  children: React.ReactNode;
  searchQuery?: string;
  setSearchQuery?: (value: string) => void;
  coinName?: string;
  onBack?: () => void;
}

export const Layout: React.FC<LayoutProps> = ({
                                                children,
                                                searchQuery,
                                                setSearchQuery,
                                                coinName,
                                                onBack,
                                              }) => {
  return (
      <div className="app">
        <Header
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            coinName={coinName}
            onBack={onBack}
        />
        <main>{children}</main>
        <Footer />
      </div>
  );
};

