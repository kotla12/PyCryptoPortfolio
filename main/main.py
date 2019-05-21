from tkinter import *
import requests
import json
import sqlite3


#Create Tk() instatne
pycrypto = Tk()
pycrypto.title('Crypto Portfolio')
pycrypto.iconbitmap("img/favicon.ico")
updateImage = PhotoImage(file= "img/refresh.png").subsample(2,2)

# database sectoin
con = sqlite3.connect("coin.db")
cursorObj = con.cursor()
cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
con.commit()
#funciton to insert values:
def insert_coin (id,symbol, amount, price):
    cursorObj.execute("INSERT INTO coin VALUES(?,?,?,?)",(id,symbol, amount, price))
    con.commit()

#insert_coin(2,"BCH",100,420)
#insert_coin(3,"LTC",75,25)
#insert_coin(4,"XMR",10,100.05)

# function to display coins:
def my_portfolio():
    # Importing Data
    api_req = requests.get("https://api.coinmarketcap.com/v1/ticker/")

    api = json.loads(api_req.content)
    #Creating coins Dictionary:

    cursorObj.execute("SELECT * FROM coin")
    coins = cursorObj.fetchall()
    
    # font color
    def font_color(amount):
        if amount >= 0:
            return 'green'
        else:
            return 'red'

    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amount_paid = 0

    for i in range(0,100): # ge data from first 4 coins in API
        for coin in coins: #
            if api[i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3] # coins owned * inital price purchased at
                currnet_value = coin[2] * float(api[i]["price_usd"]) # coins owned * current price
                pl_percoin = float(api[i]["price_usd"]) - coin[2] # profit/loss current price - inital price
                total_pl_coin = pl_percoin * coin[2] # total profit/loss

                total_pl +=  total_pl_coin
                total_current_value += currnet_value
                total_amount_paid += total_paid

                #print(api[i]["name"] + " - " + api[i]["symbol"])
                #print("Price- ${0:.2f}".format(float(api[i]["price_usd"])))#
                #confert to float as api[i]['price_usd'] is a unicode and does
                #not accept fomart modifier
                #print("Number of Coin: ", coin[2])
                #print("Initial Price Purchased At: $", coin[3])
                #print("Total Amount Paid: ",
                #"${0:.2f}".format(float(total_paid)))
                #print("Current Value: ",
                #"${0:.2f}".format(float(currnet_value)))
                #print("Profit Loss Per Coin: ",
                #"${0:.2f}".format(float(pl_percoin)))
                #print("Total Profit Loss With Coin: ",
                #"${0:.2f}".format(float(total_pl_coin)))

                portfolio_id = Label(pycrypto, text= coin[0], bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                portfolio_id.grid(row= coin_row, column = 0, sticky=N + S + E + W)
                
                name = Label(pycrypto, text= api[i]["name"] + " - " + api[i]["symbol"], bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                name.grid(row= coin_row, column = 1, sticky=N + S + E + W)

                price = Label(pycrypto, text="${0:.2f}".format(float(api[i]["price_usd"])), bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                price.grid(row= coin_row, column = 2, sticky=N + S + E + W)

                no_coins = Label(pycrypto, text=coin[2], bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                no_coins.grid(row= coin_row, column = 3, sticky=N + S + E + W)

                amount_paid = Label(pycrypto, text="${0:.2f}".format(float(total_paid)), bg="#F3F4F6", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                amount_paid.grid(row= coin_row, column = 4, sticky=N + S + E + W)

                currnet_val = Label(pycrypto, text="${0:.2f}".format(float(currnet_value)), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(float(currnet_value)))), font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                currnet_val.grid(row= coin_row, column = 5, sticky=N + S + E + W)

                pl_coin = Label(pycrypto, text="${0:.2f}".format(float(pl_percoin)), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(float(pl_percoin)))), font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                pl_coin.grid(row= coin_row, column = 6, sticky=N + S + E + W)

                totalpl = Label(pycrypto, text="${0:.2f}".format(float(total_pl_coin)), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(float(total_pl_coin)))), font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                totalpl.grid(row= coin_row, column = 7, sticky=N + S + E + W)

                coin_row += 1


    totalap = Label(pycrypto, text="${0:.2f}".format(float(total_amount_paid)), bg="#F3F4F6", fg=f"black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
    totalap.grid(row= coin_row, column = 4, sticky=N + S + E + W)

    totalcv = Label(pycrypto, text="${0:.2f}".format(float(total_current_value)), bg="#F3F4F6", fg=f"black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
    totalcv.grid(row= coin_row, column = 5, sticky=N + S + E + W)

    totalpl = Label(pycrypto, text="${0:.2f}".format(float(total_pl)), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(float(total_pl)))), font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
    totalpl.grid(row= coin_row, column = 7, sticky=N + S + E + W)

    api = "" # clear the api so once update is clicked it will use the newest api ( refresh data)

    update = Button(pycrypto, text="Update", bg="#F3F4F6", image = updateImage, compound = 'top',command= my_portfolio, font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
    update.grid(row= coin_row + 1, column = 7, sticky=N + S + E + W)

# header section of the app
def app_header():
    portfolio_id = Label(pycrypto, text="Portfolio ID", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
    portfolio_id.grid(row= 0, column = 0, sticky=N + S + E + W)

    name = Label(pycrypto, text="Bitcoin", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
    name.grid(row= 0, column = 1, sticky=N + S + E + W)

    price = Label(pycrypto, text="Price", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
    price.grid(row= 0, column = 2, sticky=N + S + E + W)

    no_coins = Label(pycrypto, text="Coins Owned", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
    no_coins.grid(row= 0, column = 3, sticky=N + S + E + W)

    amount_paid = Label(pycrypto, text="Total Amount Paid", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
    amount_paid.grid(row= 0, column = 4, sticky=N + S + E + W)

    currnet_val = Label(pycrypto, text="Current Value", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
    currnet_val.grid(row= 0, column = 5, sticky=N + S + E + W)

    pl_coin = Label(pycrypto, text="P/L Per Coin", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
    pl_coin.grid(row= 0, column = 6, sticky=N + S + E + W)

    totalpl = Label(pycrypto, text="Total P/L With Coin", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
    totalpl.grid(row= 0, column = 7, sticky=N + S + E + W)

app_header()
my_portfolio()
pycrypto.mainloop()
cursorObj.close()
con.close()

print("Program Completed")
