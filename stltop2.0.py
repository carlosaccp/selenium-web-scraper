# Created by carlosaccp all rights reserved. The following code was written in MacOS Catalina 10.15.16

# The aim of this program is to scrape designer data from STLTop and store it in an sqlite file so it can be uploaded to Metabase
# THIS PROGRAM IS MEANT TO BE RAN EVERY 24 HOURS, IF NOT THE DATA GATHERED IS USELESS!

# Importing all of the necessary packages for the webscraper, make sure all of them are installed

import selenium
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

# Create a date variable and set it to today's date and time
date = datetime.date(datetime.now())

# Define the options for when the chromedriver opens, which for me is set the window size to my monitor's size (fullscreen not working for some reason)
chrome_options = Options()
chrome_options.add_argument("window-size=1680,1050")

# Tell Python to locate the Webdriver, as well as the options we want it to run. In my case, I had it in the same folder as the code so this is enough
driver = webdriver.Chrome(executable_path=r"./chromedriver", options=chrome_options)
# Open the website we want to scrape. I wanted to scrape www.stltop.com/
driver.get("https://www.stltop.com/")

# Things start to become specific to www.stltop.com, and may change a considerable amount when scraping other websites
# For context, I am interested in scraping all of the designers listed in STLTop's names and patron numbers, and there are 6 designers lister per page

# My preferred way of location elements is to locate them by XPath, but there are many other ways to do it such as locating it by id, name, tag name...

# Create a variable and define it so when its ran it closes the 'allow cookies' window. 
fuckcookies = driver.find_element_by_xpath(r"/html/body/div/div/div/div/div[2]/div[2]/button").click()
# Count the number of elements I want to scrape. I did this by finding the total number of Patrons listed on STLTop (Which came as 'xxx PATRONS'
# and then stripping ' PATRONS' from the string
elements = int(driver.find_element_by_xpath(r"/html/body/section[2]/div/div[1]/div/div/a").text.strip(' PATREONS'))
# Create an empty array to which I will append another array consisting of a designer's name and patron number
patronlist = []
# Create a pgcounter variable which will be useful later on to count how many pages we have cycled through
pgcounter = 1

#Create a for loop that loops from when number == 1 to when number == elements
for number in range (1 , elements+1):
    # Redefine the counter variable as number % 6. This means that we will know what element of a page the program is scraping as there are 6 elements per page.
    counter = number % 6
    # If counter != 0 <==> if the last element of the page hasn't been reached and pgcounter != math.floor(elements/6+1) <==> we are not on the last page, so
    # we need to scrape 6 times, not any less as on the last page there is a 5/6 chance that there are < 6 elements, so we need to find a way to find how many
    # elements are on the last page to only scrape said elements, not more as that leads to error
    if (counter != 0) and pgcounter != math.floor(elements/6 + 1):
            # Locate the name by xpath and store it in a variable. Note that I have formatted the XPath; this is because the XPath is correlated to the element 
            # number, so we can format the counter (which tells us which element of a page we are scraping) into the XPath to scrape the nth element.
            name = driver.find_element_by_xpath('/html/body/section[2]/div/div[4]/div[{}]/div[2]/div/div[1]/div/div/h5'.format(counter)).text
            # Do the same thing as with name, except this time we use a list comprehension to only extract the integer of the string scraped, as that's what we want
            patrons = [int(s) for s in driver.find_element_by_xpath('/html/body/section[2]/div/div[4]/div[{}]/div[2]/div/div[1]/div/div/p'.format(counter)).text.split() if s.isdigit()][0]
            # Create an array called number in which we append the date and time the data was scraped as well as the name and the patron number
            info = [date, name, patrons]
            # Append the info array to the patronlist array
            patronlist.append(sp.array(info))
            
    # Else if counter == 0 <==> we are on the 6th element of the page <==> we need to go onto the next page after scraping this element. Moreover
    # pgcounter != math.floor(elements/6 + 1) <==> we are not on the last page so we don't need to worry about having < 6 elements in the page
    elif (counter == 0) and pgcounter != math.floor(elements/6 + 1):
            # Locate the designer's name, same as before except that this time as we are on the 6th element we don't need to format the counter 
            # as counter == 6 always
            name = driver.find_element_by_xpath('/html/body/section[2]/div/div[4]/div[6]/div[2]/div/div[1]/div/div/h5').text
            # Locate the designers' patrons with the same twist as the previous line, no formatting this time
            patrons = [int(s) for s in driver.find_element_by_xpath('/html/body/section[2]/div/div[4]/div[6]/div[2]/div/div[1]/div/div/p').text.split() if s.isdigit()][0]
            # Create an array with all of the designer's info we want
            info = [date, name, patrons]
            # Append the info array containing the designer's info to the patronlist array
            patronlist.append(sp.array(info))
            # Add 1 to the page counter as we are done with this page
            pgcounter += 1
            # Go to the next page via URL, as we can format pgcounter into stltop's URL. 
            # V1 did this differently, as the 'next page' button was clicked, but the owner changed said XPath and now it changes in every page
            driver.get("https://stltop.com/?page={}".format(pgcounter))          
            # Call fuckcookies again as we are navigating to another page where we might be faced with another 'Allow cookies' prompt
            fuckcookies
    
    # Else if pgcounter == math.floor(elements/6 + 1) <==> we are on the last page
    elif pgcounter == math.floor(elements/6 + 1):
            # Find the designer's name by using counter and formatting it to the XPath
            name = driver.find_element_by_xpath('/html/body/section[2]/div/div[4]/div[{}]/div[2]/div/div[1]/div/div/h5'.format(counter)).text
            # Find the designer's patron number by using counter and formatting it to the XPath
            patrons = [int(s) for s in driver.find_element_by_xpath('/html/body/section[2]/div/div[4]/div[{}]/div[2]/div/div[1]/div/div/p'.format(counter)).text.split() if s.isdigit()][0]
            # Add all the info into one info array
            info = [date,name,patrons]
            # Append the info array into the patronlist array
            patronlist.append(sp.array(info))
            
    # else <==> if something goes wrong:
    else:
        # Print ERROR and my contact email so I can fix the code
        print("")
        print("ERROR contact carlos@myminifactory.com")
        print("")
        # Close the driver if something goes wrong
        driver.close()

# Close the driver (Chromium) to free up memory
driver.close()
# Create a pandas dataframe from the patronlist array where all of a designer's details are stored with headings "Date", "Name" and "Patrons"
df = pd.DataFrame(patronlist, columns=["Date", "Name", "Patrons"])
# Convert the 'Patrons' column from a string to an int so it's doesn't cause any problems with Metabase and SQL
df['Patrons'] = df['Patrons'].astype(int)
# Create an database in the local directory to save SQL tables.
engine = create_engine('sqlite:///STLTop data.db', echo=True)
# Connect to the engine
sqlite_connection = engine.connect()
# Create an SQLite table in which today's date is shown to distinguish between days
sqlite_table = "STLTop data {}".format(date)
# Turn the dataframe into an SQLite file with sqlite_table as its name. It will be saved to sqlite_connection.
df.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
# Close the connection after the whole process is finished
sqlite_connection.close()
