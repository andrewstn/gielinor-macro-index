import sqlite3
import time

def init_db():
    connection = sqlite3.connect("g500.db")
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS index_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            index_name TEXT, 
            index_value REAL
        )
    ''')
    connection.commit()
    connection.close()

def get_db_connection():
    return sqlite3.connect("g500.db")

def cleanup_old_data(days=30):
    """Deletes rows older than the specified number of days."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Calculate what the timestamp was 30 days ago
    seconds_in_a_day = 24 * 60 * 60
    cutoff_time = int(time.time()) - (days * seconds_in_a_day)
    
    # Execute the deletion
    cursor.execute("DELETE FROM index_history WHERE timestamp < ?", (cutoff_time,))
    deleted_count = cursor.rowcount # See how many rows were actually deleted
    
    conn.commit()
    conn.close()
    
    if deleted_count > 0:
        print(f"[{time.strftime('%H:%M:%S')}] Database Cleanup: Removed {deleted_count} expired records.")