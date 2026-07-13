import { useQuery } from '@tanstack/react-query'
import { Sparkles, TrendingUp, ExternalLink } from 'lucide-react'
import { getMarketOverview } from '../services/api'

const MarketOverview = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['marketOverview'],
    queryFn: () => getMarketOverview().then(res => res.data)
  })

  if (isLoading) {
    return <div className="text-center py-12">Loading market overview...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <TrendingUp className="h-8 w-8 text-primary-600" />
        <h1 className="text-3xl font-bold">Market Overview</h1>
      </div>

      {/* AI-Generated Overview */}
      {data?.overview && (
        <div className="card">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="h-6 w-6 text-primary-600" />
            <h2 className="text-xl font-bold">AI Market Analysis</h2>
          </div>
          <div className="prose prose-gray max-w-none">
            <p className="whitespace-pre-wrap text-gray-700 leading-relaxed">
              {data.overview}
            </p>
          </div>
        </div>
      )}

      {/* Market News */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Latest Market News</h2>
        <div className="space-y-4">
          {data?.news?.slice(0, 15).map((article, index) => (
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
                    className="w-40 h-28 object-cover rounded-lg flex-shrink-0"
                  />
                )}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <h3 className="font-bold text-gray-900 line-clamp-2 flex-1">
                      {article.headline}
                    </h3>
                    <ExternalLink className="h-4 w-4 text-gray-400 flex-shrink-0" />
                  </div>
                  <p className="text-sm text-gray-600 line-clamp-3 mb-3">
                    {article.summary}
                  </p>
                  <div className="flex items-center gap-3 text-xs text-gray-500">
                    {article.source && <span className="font-medium">{article.source}</span>}
                    {article.datetime && (
                      <>
                        <span>•</span>
                        <span>{new Date(article.datetime * 1000).toLocaleDateString()}</span>
                      </>
                    )}
                  </div>
                </div>
              </div>
            </a>
          ))}
        </div>
      </div>
    </div>
  )
}

export default MarketOverview
