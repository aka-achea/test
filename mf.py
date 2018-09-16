#!/usr/bin/python
#coding:utf-8
#Python3

import os  ,time
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  

lg = 'https://passport.mafengwo.cn'

user = 'https://m.mafengwo.cn'
dk = "https://m.mafengwo.cn/activity/daka"


pt = "akaachea@163.com"
pd = "5021529"
mobileEmulation = {'deviceName': 'iPhone 6'}


chrome_options = Options()  
# chrome_options.add_argument("headless") 
# chrome_options.add_argument("no-sandbox") 
# chrome_options.add_argument('user-data-dir="E:\\xm"')  
# cpath = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
# chrome_options.binary_location = cpath  
chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)  

cd_arg = ["--log-path=e:\qc.log","--verbose"]

driver = webdriver.Chrome(
    executable_path="J:\\DOC\\GH\\test\\chromedriver.exe",
    service_args=[cd_arg[0]],
    chrome_options=chrome_options)  

driver.get(lg)  
time.sleep(5)
u = driver.find_element_by_name("passport") 
# print(u)
u.send_keys(pt)
p = driver.find_element_by_name("password") 
p.send_keys("5021529")
submit = driver.find_element_by_css_selector("button.btn") 
submit.click()

# driver.get_cookies()
time.sleep(5)

dk = driver.find_element_by_link_text("打卡")
dk.click()

time.sleep(5)
dk = driver.find_element_by_css_selector("div.btn-card")
dk.click()

# search_box = driver.find_element_by_name('q')
# search_box.send_keys('chromedriver')
# search_box.submit()
# time.sleep(5)
# driver.close()
# driver.quit()






























# headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
#             "Accept-Encoding":"gzip",
#             "Accept-Language":"zh-CN,zh;q=0.8",
#             # "Referer":"http://www.example.com/",
#             "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
#             }

# s = requests.Session()
# lg = s.post(lg, data=data, headers=headers)
# res2 = s.get(user,cookies = lg.cookies, verify = False)

# print(res2.content) #获得二进制响应内容
# print(res2.raw) #获得原始响应内容,需要stream=True
# print(res2.raw.read(50))
# print(type(res2.text))#返回解码成unicode的内容
# # print(res2.url)
# print(res2.history)#追踪重定向

# # print(lg.cookies)
# print(res2.cookies)
# # print(res2.cookies['example_cookie_name'])
# print(res2.headers)
# print(res2.headers['Content-Type'])
# print(res2.headers.get('content-type'))
# print(res2.json)#讲返回内容编码为json
# print(res2.encoding)#返回内容编码
# print(res2.status_code)#返回http状态码
# print(res2.raise_for_status())#返回错误状态码





