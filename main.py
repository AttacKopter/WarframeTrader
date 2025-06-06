import requests
import json

url = "https://api.warframe.market/v1/items"
response = requests.get(url)

items = json.loads(response.text)
for item in items:
    print(item)