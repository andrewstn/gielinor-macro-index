import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Activity, TrendingUp, Clock } from 'lucide-react'

function App() {
  const [history, setHistory] = useState([])
  const [currentIndex, setCurrentIndex] = useState(null)
  const [basket, setBasket] = useState([])
  const [loading, setLoading] = useState(true)
  
  // NEW: State to track which timeframe the user is looking at (defaults to 24 hours)
  const [timeframe, setTimeframe] = useState(24) 

  const fetchData = async () => {
    try {
      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

      // NEW: We pass the timeframe to the Python API
      const historyRes = await fetch(`${API_BASE}/api/history?hours=${timeframe}`)
      const historyData = await historyRes.json()
      
      const currentRes = await fetch(`${API_BASE}/api/pvm-index`)
      const currentData = await currentRes.json()

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

  // Notice we added `timeframe` to the dependency array at the bottom.
  // This tells React: "If the user clicks a new timeframe button, instantly run this effect again!"
  useEffect(() => {
    setLoading(true) // Show skeletons when changing timeframes
    fetchData()
    
    const interval = setInterval(() => {
      fetchData()
    }, 300000)
    
    return () => clearInterval(interval)
  }, [timeframe])

  // NEW: The Skeleton Loader UI
  if (loading && !currentIndex) {
    return (
      <div className="min-h-screen bg-slate-950 p-8">
        <div className="animate-pulse flex flex-col gap-8">
          <div className="h-16 bg-slate-900 rounded-lg w-1/3"></div>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 h-96 bg-slate-900 rounded-lg"></div>
            <div className="h-96 bg-slate-900 rounded-lg"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-8 font-mono">
      {/* Header */}
      <header className="mb-8 border-b border-slate-800 pb-4 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-emerald-400 flex items-center gap-2">
            <Activity size={28} />
            G-500 Macro Index
          </h1>
          <p className="text-slate-400 mt-1">OSRS PvM Blue-Chip Economy Tracker</p>
        </div>
        <div className="text-left md:text-right">
          <p className="text-slate-400 text-sm mb-1">Current Index Value</p>
          <p className="text-4xl font-bold text-emerald-400">
            {currentIndex ? currentIndex.toFixed(2) : '---'}
          </p>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Chart Section */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 p-6 rounded-lg shadow-xl flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <TrendingUp size={20} className="text-emerald-400"/>
              Index Volatility
            </h2>
            
            {/* NEW: Interactive Timeframe Controls */}
            <div className="flex bg-slate-950 rounded-lg p-1 border border-slate-800">
              {[
                { label: '1H', value: 1 },
                { label: '24H', value: 24 },
                { label: '7D', value: 168 }
              ].map((btn) => (
                <button
                  key={btn.label}
                  onClick={() => setTimeframe(btn.value)}
                  className={`px-3 py-1 text-sm rounded-md transition-colors ${
                    timeframe === btn.value 
                      ? 'bg-emerald-500 text-slate-950 font-bold' 
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {btn.label}
                </button>
              ))}
            </div>
          </div>
          
          <div className="grow min-h-75">
            {loading ? (
               <div className="w-full h-full animate-pulse bg-slate-800/50 rounded flex items-center justify-center">
                 <Clock className="text-slate-600 animate-spin" size={32} />
               </div>
            ) : history.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={history}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="time" stroke="#64748b" minTickGap={30} />
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
                    dot={false} // Turned off dots to make the line look cleaner when viewing large timeframes!
                    activeDot={{ r: 6, fill: '#34d399' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="w-full h-full flex items-center justify-center text-slate-500">
                Not enough data collected for this timeframe yet.
              </div>
            )}
          </div>
        </div>

        {/* Basket Breakdown Section */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg shadow-xl h-fit">
          <h2 className="text-xl font-semibold mb-6">Basket Breakdown</h2>
          <div className="space-y-4">
            {basket.length > 0 ? basket.map((item, index) => (
              <div key={index} className="flex justify-between items-center border-b border-slate-800 pb-2">
                <span className="text-sm text-slate-300">{item.item}</span>
                <span className="text-sm font-semibold text-emerald-400">
                  {(item.price / 1000000).toFixed(1)}M
                </span>
              </div>
            )) : (
              // Skeleton for the basket items
              [1,2,3,4,5].map(i => (
                 <div key={i} className="animate-pulse flex justify-between border-b border-slate-800 pb-2">
                    <div className="h-4 bg-slate-800 rounded w-32"></div>
                    <div className="h-4 bg-slate-800 rounded w-12"></div>
                 </div>
              ))
            )}
          </div>
        </div>

      </div>
    </div>
  )
}

export default App