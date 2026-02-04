import requests
import json

url = "http://localhost:8000/generate"
payload = {
    "name": "Super Coffee",
    "target": "Tired Developers",
    "benefit": "Infinite Energy"
}

try:
    print(f"Testing API at {url}...")
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    print("✅ API Success!")
    print("Response snippet:", data["result"][:100])
except Exception as e:
    print(f"❌ API Failed: {e}")
