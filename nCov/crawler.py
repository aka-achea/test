#!/usr/bin/python3
#coding:utf-8

import time
import re
from pprint import pprint
from bs4 import BeautifulSoup
import json
import requests
from pprint import pprint

# customized module
from openlink import op_requests,ran_header,op_simple
from conf import shsumary

api = 'https://weixin.sogou.com/weixin?query=%E5%81%A5%E5%BA%B7%E4%B8%8A%E6%B5%B712320'
web = 'https://weixin.sougou.com'

from selenium import webdriver  
# from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  


def get_detail():
    dxyapi = 'https://lab.isaaclin.cn/nCoV/api/area?latest=1&province=%E4%B8%8A%E6%B5%B7%E5%B8%82'
    header = ran_header()
    try:
        html = requests.get(dxyapi)
        # bsobj = BeautifulSoup(html,'html.parser').text
        j = json.loads(html.text)
    except json.decoder.JSONDecodeError:     
        print(html.text)
        print('Fail to update data')
        return False
    data = j['results'][0]
    confirmedCount = data['confirmedCount']
    curedCount = data['curedCount']
    deadCount = data['deadCount']
    detail = data['cities']
    detail = { d['cityName']:d['confirmedCount'] for d in detail }
    pprint(detail)
    with open(shsumary,'w',encoding='utf-8') as f:
        json.dump(detail,f,ensure_ascii=False,indent=2)
    return True


web = 'http://wsjkw.sh.gov.cn/xwfb/index.html'


def op_sel(web):
    '''Use selenium + chromedriver to scrap web
    Put chromedriver into Python folder
    Need to explicit driver.quit() after invocation
    '''
    chrome_options = Options()  
    chrome_options.add_argument("headless") 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # chrome_options.add_argument("no-sandbox") 
    # chrome_options.add_argument('user-data-dir="E:\\xm"')   
    # cpath = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    # chrome_options.binary_location = cpath    
    # if log != '':
    cd_arg = [f"--log-path=j:\c.log","--verbose"]
    # chrome_options.add_argument('log-path=j:\\c.log')
    # chrome_options.add_argument('verbose')
    driver = webdriver.Chrome(
            # executable_path="J:\\DOC\\GH\\test\\chromedriver.exe",
            # service_args=cd_arg,  # this work
            options=chrome_options)  
    driver.get(web)  
    time.sleep(2)
    # driver.get(web)  
    # driver.switch_to.frame('contentFrame')
    element = driver.find_elements_by_partial_link_text("上海新增")[0]
    link = element.get_attribute('href')
    print(link)
    driver.close()
    driver.get(link)
    time.sleep(2)
    items = driver.find_elements_by_partial_link_text("发现确诊病例")
    for x in items:
        title = x.text
        print(title)
    driver.quit()
    # return title


# print(op_sel(web))
# print(get_detail())


def crawl_wx_number(wx):
    html = requests.get(wx).text
    # print(html.text)
    obj = BeautifulSoup(html,'html.parser')
    content = obj.find('section',{'style':'max-width: 100%;box-sizing: border-box;word-wrap: break-word !important;'})
    # pprint(content)
    txt = content.text
    p1 = re.compile('发现确诊病例\d+例')
    if t := re.search(p1,txt):
        sumtotal = str(t).split('例')[1]
        pprint(sumtotal)
    else:
        raise
    p2 = re.compile('尚有\d+例疑似病例')
    if t := re.search(p2,txt):
        pending = str(t).split('例')[0].split('有')[-1]
        pprint(pending)
    else:
        raise   
    return int(sumtotal),int(pending)


def crawl_wx_location(wx):
    plist = []
    html = requests.get(wx).text
    # print(html.text)
    obj = BeautifulSoup(html,'html.parser')
    c = obj.find('section',{'data-tools':'135编辑器'})
    for p in c.find_all('p') :
        # pprint(p)
        # print('='*10)
        if p.strong:
            # pprint(p)
            # print('='*7)
            q = p.children
            q = [ y for y in q ]
            # print(q)
            if len(q) == 1 :                
                # pprint(p.text)
                tmp = p.text.split('：')
                district = tmp[0]
                place = tmp[1]
            else:
                # q = [ y for y in q ]
                # pprint(q)
                district = q[0].text.replace('：','')
                place = q[-1].text
            if '、' in place:
                for x in place.split('、'):
                    plist.append(district + x)
            else:
                plist.append(district + place)
    return plist


if __name__ == "__main__":
    
    wx = 'https://mp.weixin.qq.com/s/EpurrMKVG5yHUDmXRDukNQ'

    pprint(crawl_wx_location(wx))