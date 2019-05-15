import requests
import json

api_req = requests.get("https://api.coinmarketcap.com/v1/ticker/")

api = json.loads(api_req.content)

print(api[0]["symbol"])
print(api[0]["price_usd"])