import time
from services import calculate_current_index
from database import get_db_connection

def background_fetch_and_store():
    index_value, _ = calculate_current_index()
    if index_value:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO index_history (timestamp, index_value) VALUES (?, ?)", 
                       (int(time.time()), index_value))
        conn.commit()
        conn.close()
        print(f"[{time.strftime('%H:%M:%S')}] Saved new index value: {index_value}")