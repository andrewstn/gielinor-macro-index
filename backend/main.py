from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the G-500 Backend!"}

@app.get("/api/test-osrs")
def test_osrs_api():
    # This is the official OSRS Wiki API endpoint for the latest prices
    url = "https://prices.runescape.wiki/api/v1/osrs/latest"
    
    # We must include a custom User-Agent so the Wiki knows who is requesting data
    headers = {
        'User-Agent': 'G500-Dashboard-Project - @andrewstn'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return {"status": "Success", "data_points": len(data['data'])}
    else:
        return {"status": "Failed", "code": response.status_code}