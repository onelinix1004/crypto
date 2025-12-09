import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import {Home} from "./pages/Home.tsx";
import {CoinDetail} from "./pages/CoinDetail.tsx";
import {CryptoNews} from "./pages/CryptoNews.tsx";

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/coin/:id" element={<CoinDetail />} />
          <Route path="/news" element={<CryptoNews />} />
        </Routes>
      </BrowserRouter>
  )
}

export default App
