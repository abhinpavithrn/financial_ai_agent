import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Trash2, TrendingUp, TrendingDown } from 'lucide-react'
import { getWatchlist, removeFromWatchlist, getStockQuote } from '../services/api'
import StockCard from '../components/StockCard'

const Watchlist = () => {
  const queryClient = useQueryClient()

  const { data: watchlist, isLoading } = useQuery({
    queryKey: ['watchlist'],
    queryFn: () => getWatchlist().then(res => res.data)
  })

  const [quotes, setQuotes] = useState({})

  // Fetch quotes for all watchlist items
  useEffect(() => {
    if (watchlist) {
      watchlist.forEach(async (item) => {
        try {
          const response = await getStockQuote(item.symbol)
          setQuotes(prev => ({
            ...prev,
            [item.symbol]: response.data
          }))
        } catch (error) {
          console.error(`Error fetching quote for ${item.symbol}:`, error)
        }
      })
    }
  }, [watchlist])

  const removeMutation = useMutation({
    mutationFn: removeFromWatchlist,
    onSuccess: () => {
      queryClient.invalidateQueries(['watchlist'])
    }
  })

  const handleRemove = (id) => {
    if (confirm('Remove this stock from your watchlist?')) {
      removeMutation.mutate(id)
    }
  }

  if (isLoading) {
    return <div className="text-center py-12">Loading watchlist...</div>
  }

  if (!watchlist || watchlist.length === 0) {
    return (
      <div className="card text-center py-12">
        <h2 className="text-2xl font-bold mb-4">Your Watchlist is Empty</h2>
        <p className="text-gray-600 mb-6">
          Start adding stocks to track their performance and get instant updates
        </p>
        <a href="/" className="btn-primary inline-block">
          Browse Stocks
        </a>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">My Watchlist</h1>
        <div className="text-gray-600">
          {watchlist.length} {watchlist.length === 1 ? 'stock' : 'stocks'}
        </div>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {watchlist.map((item) => (
          <div key={item.id} className="relative">
            <StockCard stock={item} quote={quotes[item.symbol]} />
            <button
              onClick={() => handleRemove(item.id)}
              className="absolute top-4 right-4 p-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors"
              title="Remove from watchlist"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Watchlist
