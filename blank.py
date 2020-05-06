

# import json
from myfs import g_fsize,jdump,jload
from itertools import product
from pprint import pprint


# def unquote_url(url):
#     from urllib import parse
#     return parse.unquote(url)

# from bs4 import BeautifulSoup
# from hyper import HTTPConnection
# from urllib.parse import urlparse,parse_qs

# conn = HTTPConnection('v.douyin.com')
# conn.request('GET', '/7uCmaC/')
# resp = conn.get_response()
# html = resp.read().decode('utf-8')
# bsObj = BeautifulSoup(html,"html.parser")
# newlink = bsObj.a['href']
# print(newlink)

# # newlink = 'https://www.iesdouyin.com/share/video/6807957042163174664/?region=CN&mid=6807920732866120452&u_code=dfi2hi3f619&titleType=title&timestamp=1585151579&utm_campaign=client_share&app=aweme&utm_medium=ios&tt_from=more&utm_source=more'
# result = urlparse(newlink)
# print(result)
# # query_dict = parse_qs(result.query)
# # print(query_dict)
# path = result.path+'?'+result.query
# print(path)
# conn.request('GET',path)
# resp = conn.get_response()
# html = resp.read().decode('utf-8')
# print(html)

from PIL import Image
import math,os ,csv,codecs
from prettytable import PrettyTable 
# from pathlib import PureWindowsPath as pp
import time
import openpyxl
from pprint import pprint

from mystr import batchremovestr
from myocr import init_client,ocr_baidu

'''
1. iPhone wx screen shot
2. Picsew 长截图
3. wx 转原图
4. Baidu OCR
'''


path = r'M:\MyProject\JiJin'
# xls = r'M:\MyProject\JiJin\t.xlsx'
xls = r'N:\Doc\财务统计.xlsx'




class jijin():
    def __init__(self,name):
        self.name = name
        self.rate = None
        self.days = None
        self.amount = None
        self.match = None


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def modificate(text):
    rlist = ['假期收益已提前发放','预约中',',','支持','零钱通','买入','净值型','智能','NEW','灵活申赎','随买随取最快当到账','HOT']
    return batchremovestr(rlist,text)

def readjj(ocrclient,jdict,path):
    '''Crop the image every 271 pix'''
    img = os.path.join(path,'j.png')
    im = Image.open(img).convert('L') 
    try:    
        # ni.show()
        im.save('tmp.png', 'PNG')
        data = get_file_content('tmp.png')
        txtlist = ocr_baidu(ocrclient,data)
        pprint(txtlist)
        # name = modificate(txtlist[0])
        # rateday = txtlist[1].split('%')
        # rate = rateday[0]
        # if '天' in rateday[1]:
        #     days = rateday[1].replace('天','')
        # elif '个月' in rateday[1]:
        #     days = rateday[1].replace('个月','')
        # else:
        #     days = txtlist[2].replace('天','')
        # if modificate(days) == '':
        #     days = 1
        # if name not in jdict.keys():
        #     j = jijin(name)
        #     jdict[name] = j
        # jdict[name].rate = rate
        # jdict[name].days = days
        # if txtlist == []:
        #     break
        # n += 1
        # time.sleep(1)
    except:
        raise
    # pprint(jdict) # details
    return jdict

def formattable_jj(jdict):
    t = PrettyTable()
    t.field_names = ['基金','天数','利率','数量','Match']
    t.align['基金'] = 'l'
    t.sortby = '基金'
    for k in jdict.keys():
        jj = jdict[k]
        t.add_row([ jj.name,jj.rate,jj.days,jj.amount,jj.match ])
    print(t)


ocr = init_client()
jdict = {}
jdict = readjj(ocr,jdict,path)
# formattable_jj(jdict)
