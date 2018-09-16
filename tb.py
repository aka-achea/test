#coding:utf-8
# https://www.cnblogs.com/zhaof/p/6953241.html

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()

#1st test

# browser.get("http://www.baidu.com")
# ## print(browser.page_source).encode('GB18030')
# a = str(browser.page_source).encode('GB18030')
# print(a)
# browser.close()

#test 2

# browser.get("http://www.taobao.com")
# input_first = browser.find_element_by_id("q")
# input_second = browser.find_element_by_css_selector("#q")
# input_third = browser.find_element_by_xpath('//*[@id="q"]')
# print(input_first)
# print(input_second)
# print(input_third)

# input_4 = browser.find_element(By.ID,"q")
# print(input_4)
# browser.close()

#test 3

# browser.get("http://www.taobao.com")
# lis = browser.find_elements_by_css_selector('.service-bd li')
# print(lis)
# lis2 = browser.find_elements(By.CSS_SELECTOR,'.service-bd li')
# browser.close()


# test 4

# browser.get("http://www.taobao.com")
# input_str = browser.find_element_by_id('q')
# input_str.send_keys("ipad")
# time.sleep(1)
# input_str.clear()
# input_str.send_keys("MakBook pro")
# button = browser.find_element_by_class_name('btn-search')
# button.click()

# test 5 交互动作

# url = "http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable"
# browser.get(url)
# browser.switch_to.frame('iframeResult')
# source = browser.find_element_by_css_selector('#draggable')
# target = browser.find_element_by_css_selector('#droppable')
# actions = ActionChains(browser)
# actions.drag_and_drop(source, target)
# actions.perform()


#test 6 执行JavaScript

# browser.get("http://www.zhihu.com/explore")
# browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# browser.execute_script('alert("To Bottom")')
# browser.close()

#test 7 获取ID，位置，标签名

# url = 'https://www.zhihu.com/explore'
# browser.get(url)
# logo = browser.find_element_by_id('zh-top-link-logo')
# print(logo)
# print(logo.get_attribute('class'))
# print(logo.text)
# input = browser.find_element_by_class_name('zu-top-add-question')
# print(input.text)
# print(input.id)
# print(input.location)
# print(input.tag_name)
# print(input.size)
# browser.close()

#test 8 Frame

# url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
# browser.get(url)
# browser.switch_to.frame('iframeResult')
# source = browser.find_element_by_css_selector('#draggable')
# print(source)
# try:
#     logo = browser.find_element_by_class_name('logo')
# except NoSuchElementException:
#     print('NO LOGO')
# browser.switch_to.parent_frame()
# logo = browser.find_element_by_class_name('logo')
# print(logo)
# print(logo.text)
# browser.close()

#test 9 隐式等待

# browser.implicitly_wait(10)
# browser.get('https://www.zhihu.com/explore')
# input = browser.find_element_by_class_name('zu-top-add-question')
# print(input)

# test 10  显示等待

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# browser.get('https://www.taobao.com/')
# wait = WebDriverWait(browser, 10)
# input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
# button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
# print(input, button)

#test 11 浏览器的前进和后退

# browser.get('https://www.baidu.com/')
# browser.get('https://www.taobao.com/')
# browser.get('https://www.python.org/')
# browser.back()
# time.sleep(1)
# browser.forward()
# browser.close()

#test 12  cookie操作


# browser.get('https://www.zhihu.com/explore')
# print(browser.get_cookies())
# browser.add_cookie({'name': 'name', 'domain': 'www.zhihu.com', 'value': 'zhaofan'})
# print(browser.get_cookies())
# browser.delete_all_cookies()
# print(browser.get_cookies())

#test 13 选项卡管理

# browser.get('https://www.baidu.com')
# browser.execute_script('window.open()')
# print(browser.window_handles)
# browser.switch_to_window(browser.window_handles[1])
# browser.get('https://www.taobao.com')
# time.sleep(1)
# browser.switch_to_window(browser.window_handles[0])
# # browser.get('https://python.org')

# # test 14 异常处理

# from selenium.common.exceptions import TimeoutException, NoSuchElementException

# try:
#     browser.get('https://www.baidu.com')
# except TimeoutException:
#     print('Time Out')
# try:
#     browser.find_element_by_id('hello')
# except NoSuchElementException:
#     print('No Element')
# finally:
#     browser.close()