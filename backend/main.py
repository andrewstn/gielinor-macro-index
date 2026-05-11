from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the G-500 Backend!"}

# Our basket of Blue-Chip PvM Items
# We map the item name to its official OSRS Wiki Item ID
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

# The Divisor is crucial in index funds.
# If we just add all the prices together, the number is too big (~5 Billion GP).
# Dividing by a base number makes it look like a real stock index (e.g., "1045.32")
INDEX_DIVISOR = 5000000 

@app.get("/api/pvm-index")
def get_pvm_index():
    url = "https://prices.runescape.wiki/api/v1/osrs/latest"
    headers = {
        'User-Agent': 'G500-Dashboard-Project - @andrewstn'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"status": "Failed", "error": "Could not fetch from Wiki API"}
        
    data = response.json()['data']
    
    index_total_value = 0
    basket_data = []

    # Loop through our chosen items
    for name, item_id in PVM_BLUE_CHIPS.items():
        str_id = str(item_id) # The API returns IDs as strings, not integers
        
        # Check if the item is actively trading right now
        if str_id in data:
            # We use the 'high' price (the instant-buy price) to reflect current active demand
            current_price = data[str_id].get('high', 0) 
            
            # Fallback: If 'high' is missing (nobody is instant-buying), use 'low' (instant-sell)
            if current_price == 0:
                 current_price = data[str_id].get('low', 0)

            index_total_value += current_price
            
            # Save the individual item data so our React frontend can display a breakdown
            basket_data.append({
                "item": name,
                "price": current_price
            })
            
    # Calculate the final index number
    g500_index_value = index_total_value / INDEX_DIVISOR

    return {
        "status": "Success", 
        "g500_index": round(g500_index_value, 2),
        "total_basket_gp": index_total_value,
        "items": basket_data
    }