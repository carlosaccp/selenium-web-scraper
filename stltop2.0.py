import selenium
import urllib
import time
import scipy as sp
import math
import datetime
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


date = datetime.date(datetime.now())
chrome_options = Options()
chrome_options = Options()
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1680,1050")

driver = webdriver.Chrome(executable_path=r"/usr/bin/chromedriver", options=chrome_options)
driver.get("https://stltop.com/")
fuckcookies = driver.find_element_by_xpath(r"/html/body/div/div/div/div/div[2]/div[2]/button").click()
elements = int(driver.find_element_by_xpath(r"/html/body/section[2]/div/div[1]/div/div/a").text.strip(' PATREONS'))
patronlist = []
counter = 0
pgcounter = 1

for number in range (1 , elements+1):
    counter = number%6
    if (counter != 0) and pgcounter != math.floor(elements/6 + 1):
            name = driver.find_element_by_xpath('/html/body/section[2]/div/div[4]/div[{}]/div[2]/div/div[1]/div/div/h5'.format(counter))
            patrons = [int(s) for s in driver.find_element_by_xpath('/html/body/section[2]/div/div[4]/div[{}]/div[2]/div/div[1]/div/div/p'.format(counter)).text.split() if s.isdigit()][0]
            counter += 1
            info = [date,name.text,int(patrons)]
            patronlist.append(sp.array(info))

    elif (counter == 0) and pgcounter != math.floor(elements/6 + 1):
            name = driver.find_element_by_xpath('/html/body/section[2]/div/div[4]/div[6]/div[2]/div/div[1]/div/div/h5')
            patrons = [int(s) for s in driver.find_element_by_xpath('/html/body/section[2]/div/div[4]/div[6]/div[2]/div/div[1]/div/div/p').text.split() if s.isdigit()][0]
            info = [date,name.text,int(patrons)]
            patronlist.append(sp.array(info))
            pgcounter += 1
            driver.get("https://stltop.com/?page={}".format(pgcounter))            
            fuckcookies

    elif pgcounter == math.floor(elements/6 + 1):
            name = driver.find_element_by_xpath('/html/body/section[2]/div/div[4]/div[{}]/div[2]/div/div[1]/div/div/h5'.format(counter))
            patrons = [int(s) for s in driver.find_element_by_xpath('/html/body/section[2]/div/div[4]/div[{}]/div[2]/div/div[1]/div/div/p'.format(counter)).text.split() if s.isdigit()][0]
            info = [date,name.text,int(patrons)]
            patronlist.append(sp.array(info))
            driver.close()

    else:
        print("")
        print("ERROR contact carlos@myminifactory.com")
        print("")
        driver.close()

df = pd.DataFrame(patronlist, columns=["Date","Name", "Patrons"])
df['Patrons'] = df['Patrons'].astype(int)
engine = create_engine('sqlite:///STLTop data.db', echo=True)
sqlite_connection = engine.connect()
sqlite_table = "STLTop data {}".format(date)
df.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
sqlite_connection.close()



