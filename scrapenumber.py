import unittest
from secrets import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")
mainUrl = 'https://www.puregym.com/login/'
driver.get(mainUrl)

loginField = driver.find_element_by_xpath('//*[@id="email"]')
passwordField = driver.find_element_by_xpath('//*[@id="pin"]')
submitButton = driver.find_element_by_xpath('//*[@id="login-submit"]')
loginField.send_keys(username)
passwordField.send_keys(userpassword)
submitButton.click()

# implicit wait
driver.implicitly_wait(10)
currPop = driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/div/div/div[1]/div/div/div/div[1]/div/p[1]/span')

#regex to find the number portion of the captured text
pattern = re.compile('\d?\d\d')
matchedNumber = pattern.match(currPop.text)
print matchedNumber.group()


# try:
#     currPopString = WebDriverWait(driver, 10).until(EC.presence_of_element_located(driver.find_element_by_xpath(
#         '//*[@id="main-content"]/div[2]/div/div/div[1]/div/div/div/div[1]/div/p[1]/span')))
#     print currPopString.text
# finally:
#     driver.quit()



















