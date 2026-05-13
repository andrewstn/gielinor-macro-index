from fastapi import APIRouter, Query, HTTPException
import time
from database import get_db_connection
from services import calculate_index, BASKETS

router = APIRouter()

@router.get("/api/index")
def get_current_index(index_name: str = Query("PvM Blue-Chips")):
    if index_name not in BASKETS:
        raise HTTPException(status_code=404, detail="Index not found")
        
    index_value, basket_data = calculate_index(index_name)
    if not index_value:
        return {"status": "Failed", "error": "Could not calculate index"}
        
    # --- NEW: 24-Hour Change Logic ---
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Calculate what the timestamp was exactly 24 hours ago
    target_time = int(time.time()) - (24 * 60 * 60)
    
    # Grab the closest data point from *before* that target time
    cursor.execute('''
        SELECT index_value FROM index_history 
        WHERE index_name = ? AND timestamp <= ?
        ORDER BY timestamp DESC LIMIT 1
    ''', (index_name, target_time))
    
    row = cursor.fetchone()
    conn.close()
    
    change_24h = None
    if row:
        old_value = row[0]
        # Standard percentage change formula: ((New - Old) / Old) * 100
        if old_value > 0:
            change_24h = round(((index_value - old_value) / old_value) * 100, 2)

    return {
        "status": "Success", 
        "g500_index": index_value,
        "change_24h": change_24h, # Send the new math to React!
        "items": basket_data
    }

@router.get("/api/history")
def get_history(
    hours: int = Query(24), 
    index_name: str = Query("PvM Blue-Chips") 
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cutoff_time = int(time.time()) - (hours * 60 * 60)
    
    # We now filter the database by the specific sector name
    cursor.execute('''
        SELECT timestamp, index_value 
        FROM index_history 
        WHERE timestamp >= ? AND index_name = ?
        ORDER BY timestamp ASC
    ''', (cutoff_time, index_name))
    
    rows = cursor.fetchall()
    conn.close()
    
    history_data = [{"time": time.strftime('%H:%M', time.localtime(row[0])), "value": row[1]} for row in rows]
    return {"status": "Success", "data": history_data}