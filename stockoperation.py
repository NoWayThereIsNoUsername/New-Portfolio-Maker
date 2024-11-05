from vnstock3 import Vnstock
import pandas as pd
import csv

from datetime import datetime, timedelta
file = open('C:/Users/Admin/Desktop/pricedata.csv', 'a')
asset = 123000000

def updatetable():


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
        writing.writerow([now.date(), asset])
        
    else:
        print("Less than a day has passed.")

def news():
    df = pd.read_csv('C:/Users/Admin/Desktop/stock.csv')
    file = open("C:/Users/Admin/Desktop/news.txt", "w", encoding='utf-8')
    for names in df['stock name']:
        company = Vnstock().stock(symbol=names, source='TCBS').company
        news = company.news()['title'].iloc[0]
        file.write(news + "\n\n")
updatetable()

