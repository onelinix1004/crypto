# Technical Documentation

## crypto

### Architecture Overview

The `crypto` project is a modern, real-time cryptocurrency tracking application built with React, TypeScript, and Vite. The application fetches and displays real-time cryptocurrency data using the CoinGecko API. The project is structured to be modular and maintainable, with clear separation of concerns between components, services, and utilities.

### Setup & Installation

#### Prerequisites

- **Node.js** 18.x or higher
- **npm** or **yarn**

#### Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/you
```

2. **Navigate to the project directory**

```bash
cd crypto
```

3. **Install dependencies**

```bash
npm install
```

4. **Run the development server**

```bash
npm run dev
```

5. **Open the application in your browser**

```bash
http://localhost:5173
```

### API Documentation

#### CoinGecko API

The application uses the CoinGecko API to fetch cryptocurrency data. The API endpoints used are:

- **Fetching top 100 cryptocurrencies by market cap**

```bash
GET /coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false
```

- **Fetching detailed coin data**

```bash
GET /coins/{id}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false
```

- **Fetching 7-day price chart data**

```bash
GET /coins/{id}/market_chart?vs_currency=usd&days=7
```

### Database Schema (if applicable)

The application does not use a traditional database. Instead, it fetches data from the CoinGecko API and stores it in memory. If you need to persist data, you can use a database like SQLite or PostgreSQL.

### Configuration

#### Environment Variables

The application uses environment variables to configure API keys and other settings. The `.env.example` file provides a template for these variables. To use the application, create a `.env` file and fill in the necessary values.

```env
# CoinGecko API (currently using public endpoints, no key needed)
# If you have a Pro account, add your API key here:
# VITE_COINGECKO_API_KEY=your_api_key_here

# CoinGecko API Base URL (optional, defaults to public API)
# VITE_COINGECKO_BASE_URL=https://api.coingecko.com/api/v3

# App Title (optional)
# VITE_APP_TITLE=Crypto Tracker

# Auto-refresh interval in milliseconds (default: 2000ms = 2 seconds)
# VITE_REFRESH_INTERVAL=2000

# Number of cryptos to fetch (default: 100)
# VITE_CRYPTO_LIMIT=100

# Enable/disable news feature (optional)
# VITE_ENABLE_NEWS=false

# Enable/disable portfolio feature (optional, for future use)
# VITE_ENABLE_PORTFOLIO=false

# Enable debug mode (shows console logs)
# VITE_DEBUG_MODE=false
```

### Development Guidelines

#### Code Style

- **TypeScript**: Use explicit types and avoid implicit `any`.
- **React Components**: Prefer functional components with TypeScript.
- **Linting**: Use ESLint with the recommended configuration.

#### Testing

- **Unit Tests**: Write unit tests for individual components and services.
- **Integration Tests**: Test the integration between components and services.

### Deployment Instructions

#### Production Build

1. **Build the project**

```bash
npm run build
```

2. **Serve the production build**

```bash
npm run preview
```

3. **Deploy to a web server**

You can deploy the production build to a web server like Nginx or Apache. Make sure to configure the server to serve the static files in the `dist` directory.

### File Structure

```
crypto/
├── public/                    # File tĩnh (logo, favicon)
│   └── vite.svg
├── src/
│   ├── components/            # UI components
│   ├── pages/                 # Pages
│   ├── services/              # API services
│   ├── utils/                 # Utility functions
│   ├── styles/                # CSS styles
│   ├── App.tsx                # Main application component
│   ├── index.css              # Global styles
│   ├── main.tsx               # Entry point
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── CHANGELOG.md               # Changelog
├── CONTRIBUTING.md            # Contributing guidelines
├── LICENSE                    # License
├── package.json               # Project dependencies
├── README.md                  # Project documentation
├── tsconfig.app.json          # TypeScript configuration for app
├── tsconfig.json              # TypeScript configuration
├── tsconfig.node.json         # TypeScript configuration for node
├── vite.config.ts             # Vite configuration
├── WORKFLOW-GUIDE.md          # Workflow guide
```

### Conclusion

The `crypto` project is a comprehensive and well-structured application for tracking cryptocurrencies in real-time. With a focus on modularity, maintainability, and developer usability, the project provides a solid foundation for building and extending cryptocurrency tracking features.
