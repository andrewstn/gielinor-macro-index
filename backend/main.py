from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
import requests
import sqlite3
import time

# Constants 
PVM_BLUE_CHIPS = {
    "Twisted bow": 20997,
    "Scythe of vitur (uncharged)": 22325,
    "Tumeken's shadow (uncharged)": 27275,
    "Torva full helm": 26382,
    "Torva platebody": 26384,
    "Torva platelegs": 26386,
    "Masori body (f)": 27238,
    "Masori chaps (f)": 27240,
    "Zaryte crossbow": 26374,
    "Oathplate armour set": 30744 
}
INDEX_DIVISOR = 5000000

# Database Setup
def init_db():
    conn = sqlite3.connect("g500.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS index_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            index_value REAL
        )
    ''')
    conn.commit()
    conn.close()

# Core Logic: Fetching prices and calculating the index
def calculate_current_index():
    url = "https://prices.runescape.wiki/api/v1/osrs/latest"
    headers = {'User-Agent': 'G500-Dashboard-Project - @andrewstn'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None, None
        
    data = response.json().get('data', {})
    index_total_value = 0
    basket_data = []

    for name, item_id in PVM_BLUE_CHIPS.items():
        str_id = str(item_id)
        if str_id in data:
            current_price = data[str_id].get('high', 0)
            if current_price == 0:
                 current_price = data[str_id].get('low', 0)
            
            index_total_value += current_price
            basket_data.append({"item": name, "price": current_price})
            
    if index_total_value == 0:
        return None, None
        
    g500_index_value = round(index_total_value / INDEX_DIVISOR, 2)
    return g500_index_value, basket_data

def background_fetch_and_store():
    index_value, _ = calculate_current_index()
    if index_value:
        conn = sqlite3.connect("g500.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO index_history (timestamp, index_value) VALUES (?, ?)", 
                       (int(time.time()), index_value))
        conn.commit()
        conn.close()
        print(f"[{time.strftime('%H:%M:%S')}] Saved new index value: {index_value}")

# App Lifespan (Startup/Shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run DB setup
    init_db()
    
    # Start the background timer
    scheduler = BackgroundScheduler()
    scheduler.add_job(background_fetch_and_store, 'interval', minutes=5)
    scheduler.start()
    
    # Run it immediately once on startup so we don't have to wait 5 minutes
    background_fetch_and_store()
    
    yield
    scheduler.shutdown()

# App Initialization & CORS
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows our future React app to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
@app.get("/api/pvm-index")
def get_pvm_index():
    index_value, basket_data = calculate_current_index()
    if not index_value:
        return {"status": "Failed", "error": "Could not calculate index"}
    return {
        "status": "Success", 
        "g500_index": index_value,
        "items": basket_data
    }

@app.get("/api/history")
def get_history():
    conn = sqlite3.connect("g500.db")
    cursor = conn.cursor()
    # Fetch the last 50 data points, newest first
    cursor.execute("SELECT timestamp, index_value FROM index_history ORDER BY timestamp DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()
    
    # Recharts (our React graphing library) needs a list of dictionaries. 
    # We reverse it here so the graph draws from oldest -> newest (Left to Right).
    history_data = [
        {"time": time.strftime('%H:%M', time.localtime(row[0])), "value": row[1]} 
        for row in reversed(rows)
    ]
    
    return {"status": "Success", "data": history_data}