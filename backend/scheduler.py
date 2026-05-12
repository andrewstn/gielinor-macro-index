import time
from services import calculate_index, BASKETS
from database import get_db_connection

def background_fetch_and_store():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Loop through every basket we defined!
    for basket_name in BASKETS.keys():
        index_value, _ = calculate_index(basket_name)
        if index_value:
            # Save the name AND the value
            cursor.execute(
                "INSERT INTO index_history (timestamp, index_name, index_value) VALUES (?, ?, ?)", 
                (int(time.time()), basket_name, index_value)
            )
            print(f"[{time.strftime('%H:%M:%S')}] Saved {basket_name}: {index_value}")
            
    conn.commit()
    conn.close()