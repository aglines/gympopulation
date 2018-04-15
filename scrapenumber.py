import unittest
from secrets import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import sqlite3
import time
from datetime import datetime


db = sqlite3.connect(dbLocation)
cursor = db.cursor()


def logEvent(currEventStatus):
    stringifiedCurrTime = str(datetime.now())
    cursor.execute('''INSERT INTO eventlog (timestamp, event)
                VALUES (?,?)''', (stringifiedCurrTime, currEventStatus))
    db.commit()


# get webdriver/chrome to start
try:
    driver = webdriver.Chrome(driverLocation)
except:
    logEvent('webdriver error')


# get to the URL, log in, get data
try:
    mainUrl = 'https://www.puregym.com/login/'
    driver.get(mainUrl)
    loginField = driver.find_element_by_xpath('//*[@id="email"]')
    passwordField = driver.find_element_by_xpath('//*[@id="pin"]')
    submitButton = driver.find_element_by_xpath('//*[@id="login-submit"]')
    loginField.send_keys(username)
    passwordField.send_keys(userpassword)
    submitButton.click()
    # implicit wait
    driver.implicitly_wait(5)
    currPop = driver.find_element_by_xpath(
        '//*[@id="main-content"]/div[2]/div/div/div[1]/div/div/div/div[1]/div/p[1]/span')
    #regex to find the number portion of the captured text
    pattern = re.compile('\d+')
    matchedNumber = pattern.match(currPop.text)
    # print matchedNumber.group()
    currPop = matchedNumber.group()
    logEvent('logged in, found currPop element: ' + currPop)
except:
    errorLog = 'Error during url get, login, or data scrape'
    logEvent(errorLog)

try:
    currTime = time.time()
    stringifiedCurrTime = str(datetime.now())
    #print "curr time = ", stringifiedCurrTime
    cursor.execute('''INSERT INTO times (timestamp, pop, readabletimestamp)
                    VALUES (?,?,?)''', (currTime, currPop, stringifiedCurrTime))
    db.commit()
except:
    errorLog = 'error during db insert statement'
    logEvent(errorLog)

# look at stored data once it's captured
# cursor.execute("SELECT timestamp FROM times WHERE id = 2")
# result = cursor.fetchone()[0]
# print "new result = ", datetime.datetime.fromtimestamp(result)

#SHUT IT DOWN
db.close()
driver.quit()
