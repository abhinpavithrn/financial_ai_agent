import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Stock Data APIs
export const getStockQuote = (symbol) => 
  api.get(`/stock/${symbol}/quote`)

export const getStockProfile = (symbol) => 
  api.get(`/stock/${symbol}/profile`)

export const getStockNews = (symbol, days = 7) => 
  api.get(`/stock/${symbol}/news`, { params: { days } })

export const getStockEarnings = (symbol) => 
  api.get(`/stock/${symbol}/earnings`)

export const getStockFinancials = (symbol) => 
  api.get(`/stock/${symbol}/financials`)

export const getInsiderTransactions = (symbol) => 
  api.get(`/stock/${symbol}/insider-transactions`)

export const getRecommendations = (symbol) => 
  api.get(`/stock/${symbol}/recommendations`)

// AI Analysis APIs
export const getStockAnalysis = (symbol) => 
  api.get(`/stock/${symbol}/analysis`)

export const getAIRecommendation = (symbol) => 
  api.get(`/stock/${symbol}/recommendation`)

export const getMarketOverview = () => 
  api.get('/market/overview')

// Watchlist APIs
export const getWatchlist = () => 
  api.get('/watchlist')

export const addToWatchlist = (symbol, notes = null) => 
  api.post('/watchlist', { symbol, notes })

export const removeFromWatchlist = (watchlistId) => 
  api.delete(`/watchlist/${watchlistId}`)

// Search API
export const searchStocks = (query) => 
  api.get('/search', { params: { q: query } })

export default api
