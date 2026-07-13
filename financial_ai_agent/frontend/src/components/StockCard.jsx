import { TrendingUp, TrendingDown } from 'lucide-react'
import { Link } from 'react-router-dom'

const StockCard = ({ stock, quote }) => {
  const priceChange = quote ? ((quote.c - quote.pc) / quote.pc) * 100 : 0
  const isPositive = priceChange >= 0

  return (
    <Link to={`/stock/${stock.symbol}`}>
      <div className="card hover:shadow-lg transition-shadow cursor-pointer">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-lg font-bold text-gray-900">{stock.symbol}</h3>
            <p className="text-sm text-gray-500">{stock.name}</p>
          </div>
          {isPositive ? (
            <TrendingUp className="h-6 w-6 text-green-500" />
          ) : (
            <TrendingDown className="h-6 w-6 text-red-500" />
          )}
        </div>

        {quote && (
          <>
            <div className="space-y-2">
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-bold text-gray-900">
                  ${quote.c.toFixed(2)}
                </span>
                <span
                  className={`text-sm font-medium ${
                    isPositive ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {isPositive ? '+' : ''}
                  {priceChange.toFixed(2)}%
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <span className="text-gray-500">High:</span>
                  <span className="ml-2 font-medium">${quote.h.toFixed(2)}</span>
                </div>
                <div>
                  <span className="text-gray-500">Low:</span>
                  <span className="ml-2 font-medium">${quote.l.toFixed(2)}</span>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </Link>
  )
}

export default StockCard
