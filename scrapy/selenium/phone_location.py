from selenium import webdriver

import time

driver = webdriver.Firefox()
driver.get('http://www.showji.com/search.htm?m=1813522')
time.sleep(5)
print('Province: %s' % (driver.find_element_by_id('txtProvince').text,))

driver.close()