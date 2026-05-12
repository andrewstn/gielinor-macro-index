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
            "Oathplate armour set": 30744, "Dragon claws": 13652, "Elder maul": 21003, "Abyssal tentacle": 4151,
            "Dragon hunter crossbow": 21012, "Dragon hunter lance": 22978, "Kodai wand": 21006, "Eye of ayak (uncharged)": 31115,
            "Avernic treads": 31088, "Avernic defender hilt": 22477,  "Seers' ring (i)": 21006, "Archers' ring (i)": 21012, "Warrior ring (i)": 21003,
            "Ultor ring": 28307, "Amulet of rancour": 29801
        },
        "divisor": 5000000
    },
    "Consumables": {
        "items": {
            "Prayer potion(4)": 139, "Saradomin brew(4)": 6685, "Super restore(4)": 3024,
            "Manta ray": 391, "Shark": 383, "Anglerfish": 13441, "Karambwan": 253, "Monkfish": 126, "Lobster": 120, 
             "Swordfish": 373, "Super combat potion(4)": 12695, "Ranging potion(4)": 2444, "Magic potion(4)": 3040,
            "Stamina potion(4)": 12625, "Antifire potion(4)": 2452, "Divine super combat potion(4)": 23685, "Divine ranging potion(4)": 23733,
            "Bastion potion(4)": 22461, "Divine bastion potion(4)": 23685
        },
        "divisor": 100
    },
    "Third Age": {
        "items": {
            "3rd age pickaxe": 20014, "3rd age axe": 20011, "3rd age longsword": 12426,
            "3rd age full helmet": 10350, "3rd age platebody": 10348, "3rd age platelegs": 10346,
            "3rd age kiteshield": 10352, "3rd age cloak": 12437, "3rd age amulet": 10344,
            "3rd age range coif": 10334, "3rd age vambraces": 10336, "3rd age robe top": 10338, "3rd age robe": 10340
        },
        "divisor": 10000000
    },
    "Gilded": {
        "items": {
            "Gilded full helm": 3486, "Gilded platebody": 3481, "Gilded platelegs": 3483,
            "Gilded kiteshield": 3488, "Gilded scimitar": 12389, "Gilded axe": 23279,
            "Gilded pickaxe": 23276, "Gilded hasta": 20161, "Gilded spear": 20158, "Gilded spade": 23282,
            "Gilded boots": 12391, "Gilded coif": 23258
        },
        "divisor": 1000000
    },
    "Implings": {
        "items": {
            "Baby impling jar": 11238, "Young impling jar": 11240, "Gourmet impling jar": 11242,
            "Earth impling jar": 11244, "Essence impling jar": 11246, "Eclectic impling jar": 11248,
            "Nature impling jar": 11250, "Magpie impling jar": 11252, "Ninja impling jar": 11254,
            "Dragon impling jar": 11256
        },
        "divisor": 10000
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