from tkinter import *
import requests
import json



#Create Tk() instatne
pycrypto = Tk()
pycrypto.title('Crypto Portfolio')


name = Label(pycrypto, text="Bitcoin", bg="black", fg="white")
name.grid(row= 0, column = 0, sticky=N + S + E + W)

price = Label(pycrypto, text="Price", bg="black", fg="white")
price.grid(row= 0, column = 1, sticky=N + S + E + W)
    
no_coins = Label(pycrypto, text="Coins Owned", bg="black", fg="white")
no_coins.grid(row= 0, column = 2, sticky=N + S + E + W)
    
amount_paid = Label(pycrypto, text="Total Amout Paid", bg="black", fg="white")
amount_paid.grid(row= 0, column = 3, sticky=N + S + E + W)
    
currnet_val = Label(pycrypto, text="Current Value", bg="black", fg="white")
currnet_val.grid(row= 0, column = 4, sticky=N + S + E + W)
    
pl_coin = Label(pycrypto, text="P/L Per Coin", bg="black", fg="white")
pl_coin.grid(row= 0, column = 5, sticky=N + S + E + W)
    
totalpl = Label(pycrypto, text="Total P/L With Coin", bg="black", fg="white")
totalpl.grid(row= 0, column = 6, sticky=N + S + E + W)

pycrypto.mainloop()   
print("Program Completed")

def my_portfolio():
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
                 }]
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
                total_pl = total_pl + total_pl_coin

                print(api[i]["name"] + " - " + api[i]["symbol"])
                print("Price- ${0:.2f}".format(float(api[i]["price_usd"])))# confert to float as api[i]['price_usd'] is a unicode and does not accept f
                                                                           # fomart
                                                                                                                                                      # modifier
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

    
