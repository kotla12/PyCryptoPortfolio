
import requests
import json

# Importing Data
api_req = requests.get("https://api.coinmarketcap.com/v1/ticker/")

api = json.loads(api_req.content)




#Creating coins Dictionary:

coins = [{ # dictionary to store info on each coin
    "symbol": "BTC",
    "amount_owned": 2,
    "price_per_coin": 3200 # hybothetical price purchased as
    },
    {
     "symbol": "BCH",
    "amount_owned": 100,
    "price_per_coin": 2.05
             }
         ]
total_pl = 0

print("-----------") # indicate the beginning of print statements
print('Crypto Profile Info....')
print("-----------")

for i in range(0,5): # ge data from first 4 coins in API
    for coin in coins: #
        if api[i]["symbol"] == coin["symbol"]:
            total_paid = coin['amount_owned'] * coin['price_per_coin'] # coins owned * inital price purchased at 
            currnet_value = coin["amount_owned"] * float(api[i]["price_usd"]) # coins owned * current price
            pl_percoin = float(api[i]["price_usd"]) - coin["price_per_coin"] # profit/loss current price - inital price
            total_pl_coin = pl_percoin * coin["amount_owned"] # total profit/loss
            total_pl= total_pl + total_pl_coin

            print(api[i]["name"]+" - "+api[i]["symbol"])
            print("Price- ${0:.2f}".format(float(api[i]["price_usd"])))# confert to float as api[i]['price_usd'] is a unicode and does not accept f fomart modifier
            print("Number of Coin: ", coin["amount_owned"])
            print("Initial Price Purchased At: $", coin['price_per_coin'])
            print("Total Amount Paid: ", "${0:.2f}".format(float(total_paid)))
            print("Current Value: ", "${0:.2f}".format(float(currnet_value)))
            print("Profit Loss Per Coin: ", "${0:.2f}".format(float(pl_percoin)))
            print("Total Profit Loss With Coin: ", "${0:.2f}".format(float(total_pl_coin)))

            print("-----------")

print("********************************************")
print("Total Profit/Loss for Portifolio ${0:.2f}".format(float(total_pl)))
print("********************************************\n\n")

