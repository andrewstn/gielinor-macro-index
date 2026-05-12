import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Activity, TrendingUp } from 'lucide-react'

function App() {
  const [history, setHistory] = useState([])
  const [currentIndex, setCurrentIndex] = useState(null)
  const [basket, setBasket] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    try {
      // Fetch the historical graph data
      const historyRes = await fetch('http://127.0.0.1:8000/api/history')
      const historyData = await historyRes.json()
      
      // Fetch today's current index and basket breakdown
      const currentRes = await fetch('http://127.0.0.1:8000/api/pvm-index')
      const currentData = await currentRes.json()

      // We add a safety check here to guarantee Recharts always gets an array
      if (historyData.status === 'Success') {
        setHistory(Array.isArray(historyData.data) ? historyData.data : [])
      }
      
      if (currentData.status === 'Success') {
        setCurrentIndex(currentData.g500_index)
        setBasket(currentData.items)
      }
      setLoading(false)
    } catch (error) {
      console.error("Error fetching data:", error)
      setLoading(false)
    }
  }

  // Fetch data immediately when the page loads, and set up the 5-minute auto-refresh!
  useEffect(() => {
    fetchData()
    const interval = setInterval(() => {
      console.log("Auto-fetching latest market data...")
      fetchData()
    }, 300000) // 300,000 milliseconds = 5 minutes
    
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="min-h-screen bg-slate-950 text-emerald-400 flex items-center justify-center font-mono">Loading Market Data...</div>
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-8 font-mono">
      {/* Header */}
      <header className="mb-8 border-b border-slate-800 pb-4 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-emerald-400 flex items-center gap-2">
            <Activity size={28} />
            G-500 Macro Index
          </h1>
          <p className="text-slate-400 mt-1">OSRS PvM Blue-Chip Economy Tracker</p>
        </div>
        <div className="text-right">
          <p className="text-slate-400 text-sm mb-1">Current Index Value</p>
          <p className="text-4xl font-bold text-emerald-400">{currentIndex?.toFixed(2)}</p>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Chart Section */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 p-6 rounded-lg shadow-xl">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <TrendingUp size={20} className="text-emerald-400"/>
            Index Volatility (24h)
          </h2>
          <div className="h-96 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="time" stroke="#64748b" />
                <YAxis domain={['auto', 'auto']} stroke="#64748b" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#020617', borderColor: '#1e293b', color: '#34d399' }}
                  itemStyle={{ color: '#34d399' }}
                />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#34d399" 
                  strokeWidth={3}
                  dot={{ fill: '#020617', stroke: '#34d399', strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6, fill: '#34d399' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Basket Breakdown Section */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg shadow-xl">
          <h2 className="text-xl font-semibold mb-6">Basket Breakdown</h2>
          <div className="space-y-4">
            {basket.map((item, index) => (
              <div key={index} className="flex justify-between items-center border-b border-slate-800 pb-2">
                <span className="text-sm text-slate-300">{item.item}</span>
                <span className="text-sm font-semibold text-emerald-400">
                  {(item.price / 1000000).toFixed(1)}M
                </span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  )
}

export default App