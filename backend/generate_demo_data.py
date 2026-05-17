import sqlite3
import time
import random

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

    cursor.execute("DELETE FROM index_history")

    now = int(time.time())
    days_to_generate = 7
    interval = 5 * 60  
    start_time = now - (days_to_generate * 24 * 60 * 60)

    # Configured baselines tailored to your divisors
    baskets = {
        "PvM Blue-Chips": {"value": 650.00, "volatility": 1.5},
        "Consumables": {"value": 140.00, "volatility": 0.4},
        "Third Age": {"value": 1200.00, "volatility": 4.5},
        "Gilded": {"value": 320.00, "volatility": 1.1},
        "Implings": {"value": 95.00, "volatility": 0.3}
    }

    data_to_insert = []
    current_time = start_time

    print(f"Calculating 7 days of market history across {len(baskets)} dynamic sectors...")

    while current_time <= now:
        for basket_name, stats in baskets.items():
            change = random.gauss(0, stats["volatility"])
            
            # 1% chance of a high-volume trading cascade
            if random.random() < 0.01:
                change *= random.uniform(4, 7)
                
            stats["value"] += change
            
            if stats["value"] < 10:
                stats["value"] += abs(change) * 2

            data_to_insert.append((current_time, basket_name, round(stats["value"], 2)))
        
        current_time += interval

    cursor.executemany(
        "INSERT INTO index_history (timestamp, index_name, index_value) VALUES (?, ?, ?)",
        data_to_insert
    )

    conn.commit()
    conn.close()

    print(f"Success! Injected {len(data_to_insert)} records into g500.db")

if __name__ == "__main__":
    generate_market_data()