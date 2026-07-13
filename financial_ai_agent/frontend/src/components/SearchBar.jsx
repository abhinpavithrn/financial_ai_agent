import { useState } from 'react'
import { Search } from 'lucide-react'
import { searchStocks } from '../services/api'
import { useNavigate } from 'react-router-dom'

const SearchBar = () => {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isOpen, setIsOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSearch = async (value) => {
    setQuery(value)
    
    if (value.length < 1) {
      setResults([])
      setIsOpen(false)
      return
    }

    setLoading(true)
    try {
      const response = await searchStocks(value)
      setResults(response.data.results || [])
      setIsOpen(true)
    } catch (error) {
      console.error('Search error:', error)
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  const handleSelect = (symbol) => {
    navigate(`/stock/${symbol}`)
    setQuery('')
    setResults([])
    setIsOpen(false)
  }

  return (
    <div className="relative w-full max-w-xl">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
          placeholder="Search stocks by symbol or name..."
          className="input w-full pl-10"
        />
      </div>

      {isOpen && (
        <div className="absolute z-50 w-full mt-2 bg-white rounded-lg shadow-lg border border-gray-200 max-h-96 overflow-y-auto">
          {loading ? (
            <div className="p-4 text-center text-gray-500">Searching...</div>
          ) : results.length > 0 ? (
            <ul>
              {results.map((result) => (
                <li
                  key={result.symbol}
                  onClick={() => handleSelect(result.symbol)}
                  className="px-4 py-3 hover:bg-gray-50 cursor-pointer border-b last:border-b-0"
                >
                  <div className="font-semibold text-gray-900">
                    {result.symbol}
                  </div>
                  <div className="text-sm text-gray-500">
                    {result.description}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <div className="p-4 text-center text-gray-500">
              No results found
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default SearchBar
