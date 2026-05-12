import requests

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
INDEX_DIVISOR = 5000000

def calculate_current_index():
    url = "https://prices.runescape.wiki/api/v1/osrs/latest"
    headers = {'User-Agent': 'G500-Dashboard-Project - @YourGitHubUsername'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None, None
        
    data = response.json().get('data', {})
    index_total_value = 0
    basket_data = []

    for name, item_id in PVM_BLUE_CHIPS.items():
        str_id = str(item_id)
        if str_id in data:
            current_price = data[str_id].get('high', 0)
            if current_price == 0:
                 current_price = data[str_id].get('low', 0)
            
            index_total_value += current_price
            basket_data.append({"item": name, "price": current_price})
            
    if index_total_value == 0:
        return None, None
        
    g500_index_value = round(index_total_value / INDEX_DIVISOR, 2)
    return g500_index_value, basket_data