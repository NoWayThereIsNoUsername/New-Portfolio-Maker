from vnstock3 import Vnstock
import matplotlib.pyplot as plt 
import pandas as pd
from vnstock3.explorer.misc.gold_price import *
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
df = pd.read_csv('C:/Users/Admin/Desktop/stock.csv')
file = open('C:/Users/Admin/Desktop/pricedata.csv', 'a')

plot_itemName_list = []
stockName_only = []
plot_itemData_list = []
itemData_list_without_cash = []
priceDiffPercent = []
priceDiff = []
ogPriceAll = []
itemName_without_cash = []
itemData_without_cash = []
url = "https://www.exchange-rates.org/Rate/USD/VND"
# Send a GET request to the URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
price_element = soup.find('span', {'class': 'rate-to'})
p = price_element.text.strip()
vnd = int(p[:2]) * 1000 + int(p[3:6])


def stock_price():
    global ogPrice
    ogPrice = []
    stock_counter = 0
    for names in df['stock name']:
        stockName_only.append(names)
        plot_itemName_list.append(names)
        itemName_without_cash.append(names)
        ogPriceAll.append(df['stock price og'][stock_counter] * df['share'][stock_counter] * 1000)
        stock_counter += 1
    try:
        stock = Vnstock().stock(symbol="ACB", source='VCI')
        price = stock.trading.price_board(stockName_only)
        for counter in range(0, len(stockName_only)):
            ogPrice.append(df['stock price og'][counter] * df['share'][counter] * 1000)
            priceData = price.iloc[counter][13] #match price 
            if priceData == 0:
                priceData = price.iloc[counter][3] #ref price
                plot_itemData_list.append(priceData * df['share'][counter])
                itemData_list_without_cash.append(priceData * df['share'][counter])
            else:
                plot_itemData_list.append(priceData * df['share'][counter])
                itemData_list_without_cash.append(priceData * df['share'][counter])
    except ConnectionError:
        stock = Vnstock().stock(symbol="ACB", source='TCBS')
        price = stock.trading.price_board(symbols_list=stockName_only)
        for counter in range(0, len(stockName_only)):
            ogPrice.append(df['stock price og'][counter] * df['share'][counter] * 1000)
            priceData = price['Giá'][counter] #match price 
            
            plot_itemData_list.append(priceData * df['share'][counter])
            itemData_list_without_cash.append(priceData * df['share'][counter])
            
    arr1 = np.array(ogPrice)
    arr2 = np.array(plot_itemData_list)
    
    percentage_diff = ((arr2 - arr1) / arr1) * 100
    value_diff = arr2-arr1
    for data in percentage_diff:
        priceDiffPercent.append(round(data,2))
    for d in value_diff:
        priceDiff.append(round(d))

def gold_price(): #Đơn vị: chỉ
    goldData = btmc_goldprice()
    goldPriceSJC = int(goldData['buy_price'][5]) * float(df['gold amount'][0])
    if pd.isna(df['gold amount'][0]):
        pass
    else:
        ogPriceAll.append(df['gold amount'][0] * df['gold og price'][0])
        plot_itemName_list.append('Gold')
        itemName_without_cash.append('Gold')
        plot_itemData_list.append(goldPriceSJC)
        itemData_list_without_cash.append(goldPriceSJC)
        percentdiff = (goldPriceSJC - df['gold amount'][0] * df['gold og price'][0]) / (df['gold amount'][0] * df['gold og price'][0]) * 100
        priceDiffPercent.append(round(percentdiff,2))
        valueDiff = goldPriceSJC - (df['gold amount'][0] * df['gold og price'][0]) 
        priceDiff.append(round(valueDiff))
        
        

def crypto_price():
    global ogCryptoPrice
    counter = 0
    ogCryptoPrice = []
    currenCryptoPrice = []
    for crypto in df['crypto name']:
        if pd.isna(crypto):
            break
        else:
            ogPriceAll.append(df['crypto og price'][counter] * df['crypto amount'][counter])
            ogCryptoPrice.append(df['crypto og price'][counter] * df['crypto amount'][counter])
            url = "https://api.coingecko.com/api/v3/simple/price?ids=" + str(crypto) + "&vs_currencies=usd"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception if request is unsuccessful
            dataCrypto = response.json()  # Parsing the JSON response
            cryptoPrice = dataCrypto[crypto]['usd'] * vnd * df['crypto amount'][counter]
            currenCryptoPrice.append(cryptoPrice)
            plot_itemData_list.append(cryptoPrice)
            itemData_list_without_cash.append(round(cryptoPrice))
            itemName_without_cash.append(crypto)
            plot_itemName_list.append(crypto)
            counter += 1
    

    arr1 = np.array(ogCryptoPrice)
    arr2 = np.array(currenCryptoPrice)
    percentage_diff = ((arr2 - arr1) / arr1) * 100
    value_diff = arr2-arr1
    
    for data in percentage_diff:
        priceDiffPercent.append(round(data))
    for datavalue in value_diff:
        priceDiff.append(round(datavalue))



def cashop():
    if df['cash'][0] == 0:
        pass
    else:
        plot_itemName_list.append('Available Cash')
        
        plot_itemData_list.append(round(df['cash'][0])) 
        
def mainControl():
    stock_price()
    gold_price()
    crypto_price()
    cashop()

    if pd.isna(df['gold amount'][0]):
        TOTAL_ASSET_ORIGINAL = sum(ogCryptoPrice) + sum(ogPrice) + df['cash'][0]
    else:
        TOTAL_ASSET_ORIGINAL = sum(ogCryptoPrice) + sum(ogPrice) + df['gold og price'][0] * df['gold amount'][0] + df['cash'][0]
    TOTAL_ASSET_CURRENT = sum(plot_itemData_list) 
    REVENUE = TOTAL_ASSET_CURRENT - TOTAL_ASSET_ORIGINAL
    REVENUE_PERCENT = REVENUE / TOTAL_ASSET_ORIGINAL * 100 
    color = "neutral"
    if REVENUE < 0:
        color = "red"
    if REVENUE >= 0:
        color = "green"
    text_to_display = str("ORIGINAL ASSET: " + str("{:,}".format(round(TOTAL_ASSET_ORIGINAL)).replace(",", ".")) + " VND\n" + "CURRENT ASSET: " + str("{:,}".format(round(TOTAL_ASSET_CURRENT)).replace(",", ".")) + " VND\n" + "Profit: " + str("{:,}".format(round(REVENUE)).replace(",", ".")) + " VND (" + str(round(REVENUE_PERCENT,2)) + "%)")

    plt.pie(plot_itemData_list, labels=plot_itemName_list, autopct='%1.1f%%', startangle=0)
    plt.axis('equal')  
    plt.text(-1,-1.4,text_to_display,color = color, fontsize = 11, ha = 'center')
    plt.title("Investment" + "\n")
    plt.savefig('C:/Users/Admin/Desktop/piechart.png', format = 'png', dpi = 300)
    


      # Replace with your actual saved date

    filedate = open('C:/Users/Admin/Desktop/dateyesterday.txt', 'r+')
    last_check = filedate.read()
    now = datetime.now()
    dateformat = "%Y-%m-%d"
    date_time_obj = datetime.strptime(last_check, dateformat)
    

    
    if now - date_time_obj >= timedelta(days=1):
        file = open('C:/Users/Admin/Desktop/pricedata.csv', 'a', newline='')
        filedate.seek(0)
        filedate.truncate()
        filedate.write(str(now.date()))
        writing = csv.writer(file)
        writing.writerow([now.date(), TOTAL_ASSET_CURRENT])
        
    else:
        print("Less than a day has passed.")
    

    write_counter = 0
    
    current_time = datetime.now()
    
    with open('C:/Users/Admin/Desktop/report.txt', "w") as file:
        for names in itemName_without_cash:
            file.write(names + " -> " + str("{:,}".format(priceDiffPercent[write_counter]).replace(",", ".")) + "%. Profit: " + str("{:,}".format(priceDiff[write_counter]).replace(",", ".")) + " VND. Original price: " + str("{:,}".format(round(ogPriceAll[write_counter])).replace(",", ".")) + " VND. Current price: " + str("{:,}".format(itemData_list_without_cash[write_counter]).replace(",", ".")) + " VND\n\n")
            write_counter += 1
        file.write('Available Cash: ' + str("{:,}".format(round(df['cash'][0])).replace(",", ".")) + " VND.\n\n")    
        file.write("======================================\n")
        file.write("Original asset: " + str("{:,}".format(round(TOTAL_ASSET_ORIGINAL)).replace(",", ".")) + " VND.\n")
        file.write("Current asset: " + str("{:,}".format(round(TOTAL_ASSET_CURRENT)).replace(",", ".")) +" VND.\n")
        file.write("Profit: " + str("{:,}".format(round(REVENUE)).replace(",", ".")) + " -> " + str("{:,}".format(round(REVENUE_PERCENT,2)).replace(",", ".")) + "%\n\n\n")
        file.write("Last updated at " + str(current_time) + "\n\n\n")
        file.write("An investment in knowledge pays the best interest. - Benjamin Franklin")
    
    

mainControl()


    
     
        