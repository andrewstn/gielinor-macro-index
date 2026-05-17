import sqlite3
import time
import random
from services import calculate_index, BASKETS

def generate_market_data():
    conn = sqlite3.connect("g500.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS index_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            index_name TEXT, 
            index_value REAL
        )
    ''')

    # Clear old artifact data
    cursor.execute("DELETE FROM index_history")

    now = int(time.time())
    days_to_generate = 7
    interval = 5 * 60  
    start_time = now - (days_to_generate * 24 * 60 * 60)

    print("Fetching real-time market data to anchor the simulation...")
    
    # Grab the actual live prices right now to act as our starting point
    anchors = {}
    for basket_name in BASKETS.keys():
        live_val, _ = calculate_index(basket_name)
        
        # Fallback just in case the Wiki API is down during generation
        if live_val is None:
            live_val = 500.00 
            
        # Keep our original volatility settings
        volatility = 1.5 if basket_name == "PvM Blue-Chips" else \
                     4.5 if basket_name == "Third Age" else \
                     1.1 if basket_name == "Gilded" else \
                     0.4 if basket_name == "Consumables" else 0.3
        
        anchors[basket_name] = {"value": live_val, "volatility": volatility}

    data_to_insert = []
    current_time = now

    print(f"Calculating 7 days of historical data working BACKWARDS from live prices...")

    # Step BACKWARDS in time
    while current_time >= start_time:
        for basket_name, stats in anchors.items():
            
            # Record the state
            data_to_insert.append((current_time, basket_name, round(stats["value"], 2)))
            
            # Apply the random walk for the *previous* time step
            change = random.gauss(0, stats["volatility"])
            if random.random() < 0.01:
                change *= random.uniform(4, 7)
                
            # SUBTRACT the change because we are moving in reverse
            stats["value"] -= change
            
            # Prevent impossible negative market crashes
            if stats["value"] < 10:
                stats["value"] += abs(change) * 2

        current_time -= interval

    # Sort chronologically (oldest to newest) before saving to SQLite
    data_to_insert.sort(key=lambda x: x[0])

    cursor.executemany(
        "INSERT INTO index_history (timestamp, index_name, index_value) VALUES (?, ?, ?)",
        data_to_insert
    )

    conn.commit()
    conn.close()

    print(f"Success! Injected {len(data_to_insert)} perfectly smoothed records.")

if __name__ == "__main__":
    generate_market_data()