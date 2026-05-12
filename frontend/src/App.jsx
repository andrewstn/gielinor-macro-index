import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Activity, TrendingUp, Clock } from 'lucide-react'

function App() {
  const [history, setHistory] = useState([])
  const [currentIndex, setCurrentIndex] = useState(null)
  const [basket, setBasket] = useState([])
  const [loading, setLoading] = useState(true)
  
  const [timeframe, setTimeframe] = useState(24)
  const [activeTab, setActiveTab] = useState("PvM Blue-Chips")

  const fetchData = async () => {
    try {
      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

      // 1. Fetch History with BOTH timeframe and activeTab
      const historyUrl = `${API_BASE}/api/history?hours=${timeframe}&index_name=${encodeURIComponent(activeTab)}`;
      const historyRes = await fetch(historyUrl);
      const historyData = await historyRes.json();
      
      // 2. Fetch Current Index with activeTab
      const currentUrl = `${API_BASE}/api/index?index_name=${encodeURIComponent(activeTab)}`;
      const currentRes = await fetch(currentUrl);
      const currentData = await currentRes.json();

      if (historyData.status === 'Success') {
        setHistory(Array.isArray(historyData.data) ? historyData.data : [])
      } else {
        setHistory([])
      }
      
      if (currentData.status === 'Success') {
        setCurrentIndex(currentData.g500_index)
        setBasket(currentData.items)
      } else {
        setCurrentIndex(null)
        setBasket([])
      }
      
      setLoading(false)
    } catch (error) {
      console.error("Error fetching data:", error)
      setLoading(false)
    }
  }

  // The dependency array tells React to re-fetch when these variables change
  useEffect(() => {
    setLoading(true)
    fetchData()
    
    const interval = setInterval(() => {
      fetchData()
    }, 300000)
    
    return () => clearInterval(interval)
  }, [timeframe, activeTab])

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
      <header className="mb-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-emerald-400 flex items-center gap-2">
            <Activity size={28} />
            G-500 Macro Index
          </h1>
          <p className="text-slate-400 mt-1">OSRS Economy Sector Tracker</p>
        </div>
        <div className="text-left md:text-right">
          <p className="text-slate-400 text-sm mb-1">Current Index Value</p>
          <p className="text-4xl font-bold text-emerald-400">
            {currentIndex ? currentIndex.toFixed(2) : '---'}
          </p>
        </div>
      </header>

      {/* Economy Sector Tabs */}
      <div className="flex gap-4 border-b border-slate-800 mb-8 pb-px">
        {["PvM Blue-Chips", "Consumables", "Third Age", "Gilded", "Implings"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-3 px-2 text-sm font-semibold transition-colors border-b-2 ${
              activeTab === tab 
                ? 'border-emerald-400 text-emerald-400' 
                : 'border-transparent text-slate-500 hover:text-slate-300'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Chart Section */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 p-6 rounded-lg shadow-xl flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <TrendingUp size={20} className="text-emerald-400"/>
              Index Volatility
            </h2>
            
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
                    dot={false}
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
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg shadow-xl h-112.5 flex flex-col">
          <h2 className="text-xl font-semibold mb-6 shrink-0">Basket Breakdown</h2>
          
          <div className="space-y-4 overflow-y-auto pr-2 grow scrollbar-thin">
            {basket.length > 0 ? basket.map((item, index) => (
              <div key={index} className="flex justify-between items-center border-b border-slate-800 pb-2">
                <span className="text-sm text-slate-300">{item.item}</span>
                <span className="text-sm font-semibold text-emerald-400">
                  {item.price >= 1000000 
                    ? `${(item.price / 1000000).toFixed(1)}M` 
                    : `${(item.price / 1000).toFixed(1)}K`}
                </span>
              </div>
            )) : (
              [1,2,3,4,5,6,7].map(i => (
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