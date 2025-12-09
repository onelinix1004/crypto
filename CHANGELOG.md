# 📝 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🎯 Planned

- Portfolio tracking feature
- Price alerts
- Favorites/Watchlist
- Multi-currency support (EUR, VND)
- News integration
- PWA support
- Dark/Light theme toggle

---

## [1.0.0] - 2024-12-08

### 🎉 Initial Release

#### ✨ Added

- **Core Features**

  - Display top 100 cryptocurrencies by market cap
  - Real-time price updates every 2 seconds
  - Search functionality by coin name or symbol
  - Sort by multiple criteria (rank, name, price, market cap, 24h change)
  - Grid and List view modes
  - Detailed coin information page
  - 7-day price chart using Recharts
  - Responsive design for all devices

- **Components**

  - `Header` - App header with search and navigation
  - `Footer` - Simple footer component
  - `CryptoCard` - Individual crypto display card
  - `CryptoList` - Grid/List container for crypto cards
  - `Controls` - Sort and view mode controls
  - `Loading` - Loading spinner component
  - `NoResults` - Empty state component
  - `PriceSection` - Current price with 24h high/low
  - `ChartSection` - Interactive 7-day price chart
  - `StatsGrid` - Market data statistics grid

- **Pages**

  - `Home` - Main page with crypto list
  - `CoinDetail` - Detailed coin information page
  - `CryptoNews` - News page (placeholder)

- **Services**

  - `coinGecko.ts` - CoinGecko API integration
  - `newsApi.ts` - News API integration (placeholder)

- **Utils**

  - `formatter.ts` - Price and market cap formatting

- **Styling**

  - Dark theme with glassmorphism effects
  - Light blue (#ADD8E6) accent color
  - Smooth animations and transitions
  - Responsive layout with CSS Grid
  - Mobile-first design approach

- **Documentation**
  - English README with full project documentation
  - Vietnamese setup guide (HUONG_DAN_TAO_DU_AN.md)
  - Quick start guide (QUICK_START.md)
  - API reference documentation (API_REFERENCE.md)
  - Contributing guidelines (CONTRIBUTING.md)
  - Environment variables template (.env.example)

#### 🛠️ Technical Stack

- React 19.2.0
- TypeScript 5.9.3
- Vite 7.2.4
- React Router DOM 7.10.1
- Recharts 3.5.1
- CoinGecko API v3

#### 🔧 Configuration

- ESLint for code quality
- TypeScript strict mode
- Vite for fast builds
- Modern CSS with CSS Grid and Flexbox

---

## Version History

- **1.0.0** (2024-12-08) - Initial release with core features
- **0.0.0** - Project initialization

---

## 📌 Notes

### Breaking Changes

None yet - this is the initial release.

### Deprecations

None yet.

### Security

- No known security vulnerabilities
- Using HTTPS for all API calls
- No sensitive data stored in client

### Migration Guides

Not applicable for initial release.

---

## 🔗 Links

- [GitHub Repository](https://github.com/OWNER/crypto-tracker)
- [Documentation](./README.md)
- [Vietnamese Guide](./docs/HUONG_DAN_TAO_DU_AN.md)
- [API Reference](./docs/API_REFERENCE.md)

---

**Legend:**

- 🎉 Major release
- ✨ New feature
- 🐛 Bug fix
- 🔧 Configuration
- 📝 Documentation
- 🎨 Styling
- ⚡ Performance
- 🔒 Security
