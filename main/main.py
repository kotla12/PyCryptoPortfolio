from tkinter import *
import tkinter as tk
import requests
import json
import sqlite3
from tkinter import messagebox, Menu


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

##Hoover Section stackoverflowp
class HoverLabel(tk.Label):
    def __init__(self, master, **kw):
        tk.Label.__init__(self,master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>",self.on_enter)
        self.bind("<Leave>",self.on_exit)
    def on_enter(self, e):
        self["background"] = self["activebackground"]
    def on_exit(self, e):
        self["background"] = self.defaultBackground

# function to refresh the frame:
def refresh():
    for frame in pycrypto.winfo_children(): # winfo_children() calls the widgets inside root pycrypto
        frame.destroy()# this loop destroy all widgets 
    #call back new header & protfolio
    app_header()
    app_nav()
    my_portfolio()

# function for menu
def app_nav():

    def close_app(): # to close the app
        pycrypto.destroy()

    menu = Menu(pycrypto) # create a menu variable that holds all the items file, edit, help ...

    item = Menu(menu) # create an item and assign it to that above menu
    item.add_command(label= "Show Coins List") # subitem
    item.add_command(label= "Close App", command = close_app) # subitem

    menu.add_cascade(label= "File", menu = item) # use this thethod to add items inside the menu
    pycrypto.config(menu = menu) # assign menu as the menu for pycrypto frame

# function to display coins:
def my_portfolio():
    # Importing Data
    api_req = requests.get("https://api.coinmarketcap.com/v1/ticker/")

    api = json.loads(api_req.content)

    cursorObj.execute("SELECT * FROM coin")
    coins = cursorObj.fetchall()
    
    # font color
    def font_color(amount):
        if amount >= 0:
            return 'green'
        else:
            return 'red'
    # background color
    def bg_color(amount):
        if amount >= 0:
            return '#c6f5c7'
        else:
            return '#f5c6cd'
    
    #funciton to insert values:
    def insert_coin():
        cursorObj.execute("INSERT INTO coin (symbol, price, amount) VALUES(?,?,?)",(symbol_text.get(), price_text.get(), amount_text.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Coin " + symbol_text.get() +" Added To Portfolio Successfuly")
        refresh()
    
    #funciton to update values:
    def update_coin():
        cursorObj.execute("UPDATE  coin SET symbol=?, price=? ,amount=? WHERE id=?",(symbol_update.get(), price_update.get(), amount_update.get(),portId_update.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Coin " + symbol_update.get().upper() +" Updated Successfuly")
        refresh()
    
    #funciton to delete values:
    def delete_coin():
        ans = messagebox.askyesno("DELETING COIN","Do You Want To Delete This Coin?" )
        if ans:
            cursorObj.execute("DELETE FROM coin WHERE id=?",(portId_delete.get(),))
            con.commit()
            refresh()

    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amount_paid = 0

    for i in range(0,100): # ge data from first 4 coins in API
        for coin in coins: #
            if api[i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3] # coins owned * inital price purchased at
                currnet_value = coin[2] * float(api[i]["price_usd"]) # coins owned * current price
                pl_percoin = float(api[i]["price_usd"]) - coin[3] # profit/loss current price - inital price
                total_pl_coin = pl_percoin * coin[2] # total profit/loss

                total_pl +=  total_pl_coin
                total_current_value += currnet_value
                total_amount_paid += total_paid

                portfolio_id = HoverLabel(pycrypto, text= coin[0], activebackground="#b7b7b7", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                portfolio_id.grid(row= coin_row, column = 0, sticky=N + S + E + W)
                
                name = HoverLabel(pycrypto, text= api[i]["name"] + " - " + api[i]["symbol"], activebackground="#b7b7b7", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                name.grid(row= coin_row, column = 1, sticky=N + S + E + W)

                price = HoverLabel(pycrypto, text="${0:.2f}".format(float(api[i]["price_usd"])),  activebackground="#b7b7b7", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                price.grid(row= coin_row, column = 2, sticky=N + S + E + W)

                no_coins = HoverLabel(pycrypto, text=coin[2],  activebackground="#b7b7b7", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                no_coins.grid(row= coin_row, column = 3, sticky=N + S + E + W)

                amount_paid = HoverLabel(pycrypto, text="${0:.2f}".format(float(total_paid)),  activebackground="#b7b7b7", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                amount_paid.grid(row= coin_row, column = 4, sticky=N + S + E + W)

                currnet_val = HoverLabel(pycrypto, text="${0:.2f}".format(float(currnet_value)),  activebackground="#b7b7b7", fg="black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                currnet_val.grid(row= coin_row, column = 5, sticky=N + S + E + W)

                pl_coin = HoverLabel(pycrypto, text="${0:.2f}".format(float(pl_percoin)), bg=bg_color(float("{0:.2f}".format(float(pl_percoin)))), fg=font_color(float("{0:.2f}".format(float(pl_percoin)))), font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                pl_coin.grid(row= coin_row, column = 6, sticky=N + S + E + W)

                totalpl = HoverLabel(pycrypto, text="${0:.2f}".format(float(total_pl_coin)), bg=bg_color(float("{0:.2f}".format(float(total_pl_coin)))), fg=font_color(float("{0:.2f}".format(float(total_pl_coin)))), font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
                totalpl.grid(row= coin_row, column = 7, sticky=N + S + E + W)

                coin_row += 1

    #insert Data
    symbol_text = Entry(pycrypto, borderwidth = 2, relief = "groove")
    symbol_text.grid(row= coin_row + 1, column = 1)
    
    price_text = Entry(pycrypto, borderwidth = 2, relief = "groove")
    price_text.grid(row= coin_row + 1, column = 2)
    
    amount_text = Entry(pycrypto, borderwidth = 2, relief = "groove")
    amount_text.grid(row= coin_row + 1, column = 3)

    add_coin = Button(pycrypto, text= "Add Coin", bg = "#1c7071",fg= "white", command = insert_coin , font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")

    add_coin.grid(row= coin_row + 1, column = 4, sticky = N + S + E + W) #---End of insert Data---

    #Update Data
    portId_update = Entry(pycrypto, borderwidth = 2, relief = "groove")
    portId_update.grid(row= coin_row + 2, column = 0)
    
    symbol_update = Entry(pycrypto, borderwidth = 2, relief = "groove")
    symbol_update.grid(row= coin_row + 2, column = 1)

    price_update = Entry(pycrypto, borderwidth = 2, relief = "groove")
    price_update.grid(row= coin_row + 2, column = 2)
    
    amount_update = Entry(pycrypto, borderwidth = 2, relief = "groove")
    amount_update.grid(row= coin_row + 2, column = 3)

    update_coin = Button(pycrypto, text= "Update Coin", bg = "#1c7071",fg= "white", command = update_coin , font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")

    update_coin.grid(row= coin_row + 2, column = 4, sticky = N + S + E + W) #---End of Update Data---

    #Delete Data
    portId_delete = Entry(pycrypto, borderwidth = 2, relief = "groove")
    portId_delete.grid(row= coin_row + 3, column = 0)

    delete_coin = Button(pycrypto, text= "Delete Coin", bg = "#1c7071",fg= "white", command = delete_coin , font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")

    delete_coin.grid(row= coin_row + 3, column = 4, sticky = N + S + E + W) #---End of Delete Data---

    totalap = HoverLabel(pycrypto, text="${0:.2f}".format(float(total_amount_paid)), activebackground="#b7b7b7", fg=f"black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
    totalap.grid(row= coin_row, column = 4, sticky=N + S + E + W)

    totalcv = HoverLabel(pycrypto, text="${0:.2f}".format(float(total_current_value)), activebackground="#b7b7b7", fg=f"black", font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
    totalcv.grid(row= coin_row, column = 5, sticky=N + S + E + W)

    totalpl = HoverLabel(pycrypto, text="${0:.2f}".format(float(total_pl)),activebackground= bg_color(float("{0:.2f}".format(float(total_pl)))) , fg=font_color(float("{0:.2f}".format(float(total_pl)))), font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
    totalpl.grid(row= coin_row, column = 7, sticky=N + S + E + W)

    api = "" # clear the api so once update is clicked it will use the newest api ( refresh
             # data)


    update = Button(pycrypto, text="Refresh", bg="#F3F4F6", image = updateImage, compound = 'left',command= refresh, font= "Lato 12 ", padx = "2", pady= "2",borderwidth=2, relief= "groove")
    update.grid(row= coin_row + 1, column = 7, sticky=N + S + E + W)

# header section of the app
def app_header():
    portfolio_id = Label(pycrypto, text="Portfolio ID", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
    portfolio_id.grid(row= 0, column = 0, sticky=N + S + E + W)

    name = Label(pycrypto, text="Bitcoin", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
    name.grid(row= 0, column = 1, sticky=N + S + E + W)

    price = Label(pycrypto, text="Current Price", bg="#1c7071", fg="white", font= "Lato 12 bold", padx = "5", pady= "5",borderwidth=2, relief= "groove")
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
app_nav()
my_portfolio()
pycrypto.mainloop()
cursorObj.close()
con.close()

print("Program Completed")
