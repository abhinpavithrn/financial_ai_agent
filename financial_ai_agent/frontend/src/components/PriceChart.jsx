import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const PriceChart = ({ data, symbol }) => {
  if (!data || data.length === 0) {
    return (
      <div className="card">
        <h3 className="text-lg font-bold mb-4">Price Chart</h3>
        <p className="text-gray-500">No chart data available</p>
      </div>
    )
  }

  return (
    <div className="card">
      <h3 className="text-lg font-bold mb-4">{symbol} Price Chart</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="time" 
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
          />
          <YAxis 
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
            domain={['auto', 'auto']}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
            }}
          />
          <Line 
            type="monotone" 
            dataKey="price" 
            stroke="#0284c7" 
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default PriceChart
