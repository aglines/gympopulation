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
import datetime

driver = webdriver.Chrome(driverLocation)
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
currPop = driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/div/div/div[1]/div/div/div/div[1]/div/p[1]/span')

#regex to find the number portion of the captured text
pattern = re.compile('\d+')
matchedNumber = pattern.match(currPop.text)
# print matchedNumber.group()
currPop = matchedNumber.group()

#sounds like db will be best route
db = sqlite3.connect(dbLocation)
cursor = db.cursor()
currTime = time.time()
cursor.execute('''INSERT INTO times (timestamp, pop)
                VALUES (?,?)''', (currTime, currPop))
db.commit()

# look at stored data once it's captured
# cursor.execute("SELECT timestamp FROM times WHERE id = 2")
# result = cursor.fetchone()[0]
# newresult = datetime.datetime.fromtimestamp(result)
# print "newresult = ", newresult

driver.quit()
db.close()
