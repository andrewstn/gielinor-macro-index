import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASKETS = {
    "PvM Blue-Chips": {
        "items": {
            "Twisted bow": 20997, "Scythe of vitur (uncharged)": 22325, "Tumeken's shadow (uncharged)": 27275,
            "Torva full helm": 26382, "Torva platebody": 26384, "Torva platelegs": 26386,
            "Masori body (f)": 27238, "Masori chaps (f)": 27240, "Zaryte crossbow": 26374,
            "Oathplate armour set": 30744 
        },
        "divisor": 5000000
    },
    "Consumables": {
        "items": {
            "Prayer potion(4)": 139, "Saradomin brew(4)": 6685, "Super restore(4)": 3024,
            "Manta ray": 391, "Shark": 383, "Anglerfish": 13441, "Karambwan": 253, "Monkfish": 126, "Lobster": 120, 
             "Swordfish": 150, "Super combat potion(4)": 4000, "Ranging potion(4)": 3000, "Magic potion(4)": 2500,
                "Stamina potion(4)": 1500, "Antifire potion(4)": 2000
        },
        "divisor": 50
    }
}

def calculate_index(basket_name):
    if basket_name not in BASKETS:
        return None, None

    basket_info = BASKETS[basket_name]
    items_dict = basket_info["items"]
    divisor = basket_info["divisor"]

    url = "https://prices.runescape.wiki/api/v1/osrs/latest"
    headers = {'User-Agent': os.getenv('WIKI_USER_AGENT')}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None, None
        
    data = response.json().get('data', {})
    index_total_value = 0
    basket_data = []

    for name, item_id in items_dict.items():
        str_id = str(item_id)
        if str_id in data:
            current_price = data[str_id].get('high', 0)
            if current_price == 0:
                 current_price = data[str_id].get('low', 0)
            
            index_total_value += current_price
            basket_data.append({"item": name, "price": current_price})
            
    if index_total_value == 0:
        return None, None
        
    g500_index_value = round(index_total_value / divisor, 2)
    basket_data.sort(key=lambda x: x['price'], reverse=True)
    
    return g500_index_value, basket_data