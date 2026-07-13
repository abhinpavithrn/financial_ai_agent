import { useEffect, useState, useRef } from 'react'

const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

export const useWebSocket = (symbol) => {
  const [data, setData] = useState(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState(null)
  const wsRef = useRef(null)

  useEffect(() => {
    if (!symbol) return

    const ws = new WebSocket(`${WS_BASE_URL}/ws/stock/${symbol}`)
    wsRef.current = ws

    ws.onopen = () => {
      setIsConnected(true)
      setError(null)
      console.log(`WebSocket connected for ${symbol}`)
    }

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)
        setData(message)
      } catch (err) {
        console.error('Error parsing WebSocket message:', err)
      }
    }

    ws.onerror = (err) => {
      setError('WebSocket error occurred')
      console.error('WebSocket error:', err)
    }

    ws.onclose = () => {
      setIsConnected(false)
      console.log(`WebSocket disconnected for ${symbol}`)
    }

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close()
      }
    }
  }, [symbol])

  return { data, isConnected, error }
}
