from fastapi import APIRouter, Query
import time
from database import get_db_connection
from services import calculate_current_index

router = APIRouter()

@router.get("/api/pvm-index")
def get_pvm_index():
    index_value, basket_data = calculate_current_index()
    if not index_value:
        return {"status": "Failed", "error": "Could not calculate index"}
    return {
        "status": "Success", 
        "g500_index": index_value,
        "items": basket_data
    }

@router.get("/api/history")
def get_history(hours: int = Query(24, description="Hours of history to fetch")):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Calculate how far back in time to look
    seconds_to_subtract = hours * 60 * 60
    cutoff_time = int(time.time()) - seconds_to_subtract
    
    # Grab all rows that happened AFTER the cutoff time
    cursor.execute('''
        SELECT timestamp, index_value 
        FROM index_history 
        WHERE timestamp >= ? 
        ORDER BY timestamp ASC
    ''', (cutoff_time,))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Format the data for our React graph
    history_data = [
        # If looking at 7 days, we might want to show Month/Day, but for now HH:MM is fine
        {"time": time.strftime('%H:%M', time.localtime(row[0])), "value": row[1]} 
        for row in rows
    ]
    
    return {"status": "Success", "data": history_data}