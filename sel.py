#!/usr/bin/python
#coding:utf-8

import os  ,time
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  

web = 'https://www.python.org/'

chrome_options = Options()  
chrome_options.add_argument("headless") 
# chrome_options.add_argument("no-sandbox") 
# chrome_options.add_argument('user-data-dir="E:\\xm"')  
# cpath = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
# chrome_options.binary_location = cpath    

cd_arg = ["--log-path=e:\qc.log","--verbose"]

driver = webdriver.Chrome(
    executable_path="chromedriver.exe",
    service_args=[cd_arg[0]],
    chrome_options=chrome_options)  
driver.get(web)  

# time.sleep(5)
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('chromedriver')
# search_box.submit()
# time.sleep(5)
#driver.close()
driver.quit()

#