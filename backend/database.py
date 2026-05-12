import sqlite3

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

def get_db_connection():
    """A helper function so other files can easily grab a connection."""
    return sqlite3.connect("g500.db")