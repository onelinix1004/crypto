# 🚀 Crypto Tracker

A modern, real-time cryptocurrency tracking application built with React, TypeScript, and Vite. Track the latest prices, market data, and trends of the top 100 cryptocurrencies.

![React](https://img.shields.io/badge/React-19.x-61DAFB?style=flat&logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?style=flat&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7.x-646CFF?style=flat&logo=vite&logoColor=white)

## ✨ Features

- 📊 **Real-time Data**: Auto-refresh prices every 2 seconds
- 🔍 **Smart Search**: Search cryptocurrencies by name or symbol
- 📈 **Price Charts**: 7-day price history with interactive charts
- 🎨 **Modern UI**: Glassmorphism design with dark theme
- 📱 **Responsive**: Works seamlessly on desktop, tablet, and mobile
- ⚡ **Fast**: Built with Vite for lightning-fast development and builds
- 🔄 **Sorting Options**: Sort by rank, name, price, market cap, or 24h change
- 👁️ **View Modes**: Toggle between grid and list views
- 💰 **Detailed Stats**: Market cap, volume, supply, and more

## 🖼️ Screenshots

### Home Page - Grid View

Display of top 100 cryptocurrencies with real-time prices and market data.

### Coin Detail Page

Detailed information with 7-day price chart and comprehensive statistics.

## 🛠️ Tech Stack

| Technology           | Version | Purpose                 |
| -------------------- | ------- | ----------------------- |
| **React**            | 19.x    | UI Library              |
| **TypeScript**       | 5.9.x   | Type-safe JavaScript    |
| **Vite**             | 7.x     | Build tool & dev server |
| **React Router DOM** | 7.x     | Client-side routing     |
| **Recharts**         | 3.x     | Chart visualization     |
| **CoinGecko API**    | v3      | Cryptocurrency data     |

## 📦 Installation

### Prerequisites

- **Node.js** 18.x or higher
- **npm** or **yarn**

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/crypto-tracker.git

# Navigate to project directory
cd crypto

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

## 🚀 Usage

### Development

```bash
# Start dev server with hot reload
npm run dev
```

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Linting

```bash
# Run ESLint
npm run lint
```

## 📁 Project Structure

```
crypto/
├── public/                 # Static assets
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── ChartSection.tsx
│   │   ├── Controls.tsx
│   │   ├── CryptoCard.tsx
│   │   ├── CryptoList.tsx
│   │   ├── Footer.tsx
│   │   ├── Header.tsx
│   │   ├── Loading.tsx
│   │   ├── NoResults.tsx
│   │   ├── PriceSection.tsx
│   │   └── StatsGrid.tsx
│   ├── layout/            # Layout components
│   │   └── MainLayout.tsx
│   ├── pages/             # Page components
│   │   ├── CoinDetail.tsx
│   │   ├── CryptoNews.tsx
│   │   └── Home.tsx
│   ├── services/          # API services
│   │   ├── coinGecko.ts
│   │   └── newsApi.ts
│   ├── utils/             # Utility functions
│   │   └── formatter.ts
│   ├── styles/            # Additional CSS
│   ├── App.tsx           # Main App component
│   ├── main.tsx          # Entry point
│   └── index.css         # Global styles
├── docs/                  # Documentation
│   └── HUONG_DAN_TAO_DU_AN.md
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## 🔑 Key Features Explained

### Real-time Price Updates

The app automatically fetches fresh data from CoinGecko API every 2 seconds:

```typescript
useEffect(() => {
  fetchCryptoData();
  const interval = setInterval(fetchCryptoData, 2000);
  return () => clearInterval(interval);
}, []);
```

### Flexible Sorting

Sort cryptocurrencies by:

- Market Cap Rank (default)
- Name (A-Z)
- Price (Low to High / High to Low)
- 24h Change
- Market Cap

### Interactive Charts

Built with Recharts for smooth, responsive price charts showing 7-day historical data.

## 🎨 Design Philosophy

- **Glassmorphism**: Modern frosted glass effect with backdrop blur
- **Dark Theme**: Eye-friendly dark background with vibrant accents
- **Light Blue Accent**: #ADD8E6 for primary actions and highlights
- **Smooth Animations**: Hover effects and transitions for better UX
- **Responsive Grid**: Auto-adjusting layout for all screen sizes

## 🌐 API Reference

### CoinGecko API Endpoints Used

| Endpoint                   | Purpose                              |
| -------------------------- | ------------------------------------ |
| `/coins/markets`           | Get list of top 100 cryptocurrencies |
| `/coins/{id}`              | Get detailed coin information        |
| `/coins/{id}/market_chart` | Get 7-day price history              |

> [!NOTE]
> CoinGecko's free API has a rate limit of **30 requests/minute**. For higher limits, consider getting an API key.

## 🔧 Configuration

### Vite Config

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
});
```

### TypeScript Config

The project uses three TypeScript config files:

- `tsconfig.json` - Base configuration
- `tsconfig.app.json` - Application code
- `tsconfig.node.json` - Build scripts

## 🚧 Roadmap

Future enhancements planned:

- [ ] Portfolio tracking
- [ ] Price alerts
- [ ] Favorites/Watchlist
- [ ] Multi-currency support (EUR, VND, etc.)
- [ ] Historical price comparison
- [ ] News integration
- [ ] PWA support
- [ ] Dark/Light theme toggle
- [ ] Export data to CSV

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [CoinGecko](https://www.coingecko.com/) for providing free cryptocurrency API
- [Recharts](https://recharts.org/) for beautiful chart components
- [Vite](https://vitejs.dev/) for the amazing build tool

## 📚 Documentation

- 🇻🇳 [Vietnamese Setup Guide](docs/HUONG_DAN_TAO_DU_AN.md) - Hướng dẫn chi tiết bằng tiếng Việt
- 🇬🇧 [API Documentation](docs/API.md) - API reference and usage

## 💬 Support

If you have any questions or run into issues:

1. Check existing [Issues](https://github.com/yourusername/crypto-tracker/issues)
2. Create a new issue with detailed description
3. Contact the maintainer

---

**Made with ❤️ using React + TypeScript + Vite**

**⭐ Star this repo if you find it helpful!**
