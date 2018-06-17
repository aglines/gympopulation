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

# get to the URL
try:
    mainUrl = 'https://www.puregym.com/login/'
    driver.get(mainUrl)
except:
    errorLog = 'Error while getting mainURL'
    logEvent(errorLog)

# log in
try:
    loginField = driver.find_element_by_xpath('//*[@id="email"]')
    passwordField = driver.find_element_by_xpath('//*[@id="pin"]')
    submitButton = driver.find_element_by_xpath('//*[@id="login-submit"]')
    loginField.send_keys(username)
    passwordField.send_keys(userpassword)
    submitButton.click()
except:
    errorLog = 'Error during login'
    logEvent(errorLog)

driver.implicitly_wait(5)

# get past survey if it exists
try:
    skipButton = driver.find_element_by_xpath('//*[@id="canSkip"]')
    skipButton.click()
    notActuallyAnError = 'Survey found. '
    # logEvent(notActuallyAnError)
except:
    errorLog = 'survey not encountered, nothing to log'
    # logEvent(errorLog)

# scrape data
try:
    currPop = driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/div/div/div[1]/div/div/div/div[1]/div/p[1]/span')
except:
    errorLog = 'Error during data scrape'
    logEvent(errorLog)

pattern = re.compile('\d+')
patternFewer = re.compile('Fewer than 20 people')
patternMore = re.compile('More than .')

matchedNumber = pattern.match(currPop.text)
matchedFewer = patternFewer.match(currPop.text)
matchedMore = patternMore.match(currPop.text)

if (matchedNumber):
    currPop = matchedNumber.group()
elif (matchedFewer):
    currPop = matchedFewer.group()
elif (matchedMore) :
    currPop = matchedMore.group()
    
try:
    currTime = time.time()
    stringifiedCurrTime = str(datetime.now())
    cursor.execute('''INSERT INTO times (timestamp, pop, readabletimestamp)
                    VALUES (?,?,?)''', (currTime, currPop, stringifiedCurrTime))
    db.commit()
    logEvent('All OK. Current pop: ' + currPop)
except:
    errorLog = 'error during db insert statement'
    logEvent(errorLog)

#shut it down
db.close()
driver.quit()
