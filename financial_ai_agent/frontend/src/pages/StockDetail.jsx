import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { 
  TrendingUp, 
  TrendingDown, 
  Plus, 
  ExternalLink,
  Sparkles,
  Activity
} from 'lucide-react'
import {
  getStockQuote,
  getStockProfile,
  getStockNews,
  getStockAnalysis,
  getRecommendations,
  addToWatchlist
} from '../services/api'
import { useWebSocket } from '../hooks/useWebSocket'

const StockDetail = () => {
  const { symbol } = useParams()
  const [activeTab, setActiveTab] = useState('overview')
  const { data: wsData, isConnected } = useWebSocket(symbol)

  const { data: profile, isLoading: profileLoading } = useQuery({
    queryKey: ['profile', symbol],
    queryFn: () => getStockProfile(symbol).then(res => res.data)
  })

  const { data: news } = useQuery({
    queryKey: ['news', symbol],
    queryFn: () => getStockNews(symbol).then(res => res.data)
  })

  const { data: analysis, isLoading: analysisLoading } = useQuery({
    queryKey: ['analysis', symbol],
    queryFn: () => getStockAnalysis(symbol).then(res => res.data)
  })

  const { data: recommendations } = useQuery({
    queryKey: ['recommendations', symbol],
    queryFn: () => getRecommendations(symbol).then(res => res.data)
  })

  const [quote, setQuote] = useState(null)

  useEffect(() => {
    if (wsData?.data) {
      setQuote(wsData.data)
    }
  }, [wsData])

  const handleAddToWatchlist = async () => {
    try {
      await addToWatchlist(symbol)
      alert('Added to watchlist!')
    } catch (error) {
      alert('Error adding to watchlist')
    }
  }

  if (profileLoading) {
    return <div className="text-center py-12">Loading...</div>
  }

  const priceChange = quote ? ((quote.c - quote.pc) / quote.pc) * 100 : 0
  const isPositive = priceChange >= 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl font-bold">{symbol}</h1>
              {isConnected && (
                <span className="flex items-center gap-1 text-xs text-green-600">
                  <Activity className="h-3 w-3" />
                  Live
                </span>
              )}
            </div>
            <p className="text-xl text-gray-600">{profile?.name}</p>
            <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
              {profile?.exchange && <span>{profile.exchange}</span>}
              {profile?.finnhubIndustry && <span>• {profile.finnhubIndustry}</span>}
            </div>
          </div>
          
          <button
            onClick={handleAddToWatchlist}
            className="btn-primary flex items-center gap-2"
          >
            <Plus className="h-4 w-4" />
            Add to Watchlist
          </button>
        </div>

        {quote && (
          <div className="mt-6 border-t pt-6">
            <div className="flex items-baseline gap-4">
              <span className="text-4xl font-bold">${quote.c?.toFixed(2)}</span>
              <span
                className={`text-xl font-semibold flex items-center gap-1 ${
                  isPositive ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {isPositive ? <TrendingUp className="h-5 w-5" /> : <TrendingDown className="h-5 w-5" />}
                {isPositive ? '+' : ''}
                {priceChange.toFixed(2)}%
              </span>
            </div>

            <div className="grid grid-cols-4 gap-6 mt-6">
              <div>
                <div className="text-sm text-gray-500">Open</div>
                <div className="text-lg font-semibold">${quote.o?.toFixed(2)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-500">High</div>
                <div className="text-lg font-semibold">${quote.h?.toFixed(2)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-500">Low</div>
                <div className="text-lg font-semibold">${quote.l?.toFixed(2)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-500">Prev Close</div>
                <div className="text-lg font-semibold">${quote.pc?.toFixed(2)}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <div className="flex gap-4">
          {['overview', 'analysis', 'news', 'recommendations'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`pb-3 px-2 font-medium capitalize transition-colors ${
                activeTab === tab
                  ? 'border-b-2 border-primary-600 text-primary-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="grid md:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-lg font-bold mb-4">Company Profile</h3>
            <div className="space-y-3 text-sm">
              {profile?.marketCapitalization && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Market Cap:</span>
                  <span className="font-semibold">${profile.marketCapitalization}M</span>
                </div>
              )}
              {profile?.shareOutstanding && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Shares Outstanding:</span>
                  <span className="font-semibold">{profile.shareOutstanding}M</span>
                </div>
              )}
              {profile?.weburl && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Website:</span>
                  <a
                    href={profile.weburl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary-600 hover:underline flex items-center gap-1"
                  >
                    Visit <ExternalLink className="h-3 w-3" />
                  </a>
                </div>
              )}
            </div>
          </div>

          {profile?.logo && (
            <div className="card">
              <h3 className="text-lg font-bold mb-4">Company Logo</h3>
              <img src={profile.logo} alt={profile.name} className="max-h-32" />
            </div>
          )}
        </div>
      )}

      {activeTab === 'analysis' && (
        <div className="card">
          {analysisLoading ? (
            <div className="text-center py-8">Generating AI analysis...</div>
          ) : analysis ? (
            <>
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="h-6 w-6 text-primary-600" />
                <h3 className="text-lg font-bold">AI-Generated Analysis</h3>
              </div>
              <div className="prose prose-gray max-w-none">
                <p className="whitespace-pre-wrap text-gray-700">{analysis.summary}</p>
              </div>
            </>
          ) : (
            <p className="text-gray-500">No analysis available</p>
          )}
        </div>
      )}

      {activeTab === 'news' && (
        <div className="space-y-4">
          {news?.news?.slice(0, 10).map((article, index) => (
            <a
              key={index}
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="card hover:shadow-lg transition-shadow block"
            >
              <div className="flex gap-4">
                {article.image && (
                  <img
                    src={article.image}
                    alt=""
                    className="w-32 h-20 object-cover rounded-lg flex-shrink-0"
                  />
                )}
                <div className="flex-1 min-w-0">
                  <h4 className="font-semibold text-gray-900 mb-1 line-clamp-2">
                    {article.headline}
                  </h4>
                  <p className="text-sm text-gray-600 line-clamp-2 mb-2">
                    {article.summary}
                  </p>
                  <div className="text-xs text-gray-500">
                    {article.source} • {new Date(article.datetime * 1000).toLocaleDateString()}
                  </div>
                </div>
              </div>
            </a>
          ))}
        </div>
      )}

      {activeTab === 'recommendations' && (
        <div className="card">
          <h3 className="text-lg font-bold mb-4">Analyst Recommendations</h3>
          {recommendations?.recommendations?.length > 0 ? (
            <div className="space-y-4">
              {recommendations.recommendations.slice(0, 3).map((rec, index) => (
                <div key={index} className="border-b last:border-b-0 pb-4 last:pb-0">
                  <div className="text-sm text-gray-500 mb-2">{rec.period}</div>
                  <div className="grid grid-cols-5 gap-2 text-sm">
                    <div>
                      <div className="text-gray-600">Strong Buy</div>
                      <div className="font-bold text-green-600">{rec.strongBuy}</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Buy</div>
                      <div className="font-bold text-green-500">{rec.buy}</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Hold</div>
                      <div className="font-bold text-gray-600">{rec.hold}</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Sell</div>
                      <div className="font-bold text-red-500">{rec.sell}</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Strong Sell</div>
                      <div className="font-bold text-red-600">{rec.strongSell}</div>
                    </div>
                  </div>
                </div>
              ))}

              {recommendations.priceTarget && (
                <div className="mt-6 pt-6 border-t">
                  <h4 className="font-semibold mb-3">Price Targets</h4>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <div className="text-sm text-gray-500">Target High</div>
                      <div className="text-lg font-bold text-green-600">
                        ${recommendations.priceTarget.targetHigh?.toFixed(2)}
                      </div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Target Mean</div>
                      <div className="text-lg font-bold">
                        ${recommendations.priceTarget.targetMean?.toFixed(2)}
                      </div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Target Low</div>
                      <div className="text-lg font-bold text-red-600">
                        ${recommendations.priceTarget.targetLow?.toFixed(2)}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <p className="text-gray-500">No recommendations available</p>
          )}
        </div>
      )}
    </div>
  )
}

export default StockDetail
