from fastapi import APIRouter
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
def get_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, index_value FROM index_history ORDER BY timestamp DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()
    
    history_data = [
        {"time": time.strftime('%H:%M', time.localtime(row[0])), "value": row[1]} 
        for row in reversed(rows)
    ]
    
    return {"status": "Success", "data": history_data}