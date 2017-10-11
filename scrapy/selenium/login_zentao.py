from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

driver = webdriver.Firefox()
driver.get('http://172.30.6.71:81/zentao/user-login.html')

account = driver.find_element_by_name('account')
account.send_keys('shenweiwei')
password = driver.find_element_by_name('password')
password.send_keys('111111')
password.send_keys(Keys.RETURN)
time.sleep(5)

print('User: %s' % (driver.find_element_by_xpath('//*[@id="userMenu"]/a').text))

driver.close()