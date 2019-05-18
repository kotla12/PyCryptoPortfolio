from tkinter import *
import requests
import json



#Create Tk() instatne
pycrypto = Tk()
pycrypto.title('Crypto Portfolio')
pycrypto.iconbitmap("img/favicon.ico")

# function to display coins:
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
                 },
        {
         "symbol": "LTC",
         "amount_owned": 75,
         "price_per_coin": 25
            },
            {
         "symbol": "XMR",
         "amount_owned": 10,
         "price_per_coin": 40.05
            }
                 ]
    total_pl = 0
    coin_row = 1
    total_current_value = 0

    for i in range(0,100): # ge data from first 4 coins in API
        for coin in coins: #
            if api[i]["symbol"] == coin["symbol"]:
                total_paid = coin['amount_owned'] * coin['price_per_coin'] # coins owned * inital price purchased at
                currnet_value = coin["amount_owned"] * float(api[i]["price_usd"]) # coins owned * current price
                pl_percoin = float(api[i]["price_usd"]) - coin["price_per_coin"] # profit/loss current price - inital price
                total_pl_coin = pl_percoin * coin["amount_owned"] # total profit/loss
                total_pl = total_pl + total_pl_coin
                total_current_value= total_current_value + currnet_value

                #print(api[i]["name"] + " - " + api[i]["symbol"])
                #print("Price- ${0:.2f}".format(float(api[i]["price_usd"])))# confert to float as api[i]['price_usd'] is a unicode and does not accept fomart modifier
                #print("Number of Coin: ", coin["amount_owned"])
                #print("Initial Price Purchased At: $", coin['price_per_coin'])
                #print("Total Amount Paid: ", "${0:.2f}".format(float(total_paid)))
                #print("Current Value: ", "${0:.2f}".format(float(currnet_value)))
                #print("Profit Loss Per Coin: ", "${0:.2f}".format(float(pl_percoin)))
                #print("Total Profit Loss With Coin: ", "${0:.2f}".format(float(total_pl_coin)))

                name = Label(pycrypto, text= api[i]["name"] + " - " + api[i]["symbol"], bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                name.grid(row= coin_row, column = 0, sticky=N + S + E + W)

                price = Label(pycrypto, text="${0:.2f}".format(float(api[i]["price_usd"])), bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                price.grid(row= coin_row, column = 1, sticky=N + S + E + W)
    
                no_coins = Label(pycrypto, text=coin["amount_owned"], bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                no_coins.grid(row= coin_row, column = 2, sticky=N + S + E + W)
    
                amount_paid = Label(pycrypto, text="${0:.2f}".format(float(total_paid)), bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                amount_paid.grid(row= coin_row, column = 3, sticky=N + S + E + W)
    
                currnet_val = Label(pycrypto, text="${0:.2f}".format(float(currnet_value)), bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                currnet_val.grid(row= coin_row, column = 4, sticky=N + S + E + W)
    
                pl_coin = Label(pycrypto, text="${0:.2f}".format(float(pl_percoin)), bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                pl_coin.grid(row= coin_row, column = 5, sticky=N + S + E + W)
    
                totalpl = Label(pycrypto, text="${0:.2f}".format(float(total_pl_coin)), bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                totalpl.grid(row= coin_row, column = 6, sticky=N + S + E + W)

                coin_row = coin_row+1

                totalcv = Label(pycrypto, text="${0:.2f}".format(float(total_current_value)), bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                totalcv.grid(row= coin_row, column = 6, sticky=N + S + E + W)

                totalpl = Label(pycrypto, text="${0:.2f}".format(float(total_pl)), bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                totalpl.grid(row= coin_row, column = 2, sticky=N + S + E + W)



name = Label(pycrypto, text="Bitcoin", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
name.grid(row= 0, column = 0, sticky=N + S + E + W)

price = Label(pycrypto, text="Price", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
price.grid(row= 0, column = 1, sticky=N + S + E + W)
    
no_coins = Label(pycrypto, text="Coins Owned", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
no_coins.grid(row= 0, column = 2, sticky=N + S + E + W)
    
amount_paid = Label(pycrypto, text="Total Amount Paid", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
amount_paid.grid(row= 0, column = 3, sticky=N + S + E + W)
    
currnet_val = Label(pycrypto, text="Current Value", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
currnet_val.grid(row= 0, column = 4, sticky=N + S + E + W)
    
pl_coin = Label(pycrypto, text="P/L Per Coin", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
pl_coin.grid(row= 0, column = 5, sticky=N + S + E + W)
    
totalpl = Label(pycrypto, text="Total P/L With Coin", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
totalpl.grid(row= 0, column = 6, sticky=N + S + E + W)

my_portfolio()
pycrypto.mainloop()   
print("Program Completed")


    
