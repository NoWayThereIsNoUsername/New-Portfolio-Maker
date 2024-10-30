from vnstock3 import Vnstock
import matplotlib.pyplot as plt 
import pandas as pd
from vnstock3.explorer.misc.gold_price import *
df = pd.read_csv('C:/Users/giahi/OneDrive/Desktop/stock.csv')


plot_itemName_list = []
stockName_only = []
plot_itemData_list = []
price_difference = {"value": [], "percentage": []}


def stock_price():
    
    for names in df['stock name']:
        stockName_only.append(names)
        plot_itemName_list.append(names)
    stock = Vnstock().stock(symbol="ACB", source='VCI')
    price = stock.trading.price_board(stockName_only)
    for counter in range(0, len(stockName_only)):
        priceData = price.iloc[counter][13] #match price 
        if priceData == 0:
            priceData = price.iloc[counter][3] #ref price
            
            plot_itemData_list.append(priceData * df['share'][counter] * 1000)
        else:
            
            plot_itemData_list.append(priceData * df['share'][counter] * 1000)
    

stock_price()
print(plot_itemData_list)