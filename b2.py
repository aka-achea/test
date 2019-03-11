
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

from mylog import mylogger,get_funcname

from openlink import op_requests

book = '黄金时代'
author = '王小波'
para = [('menu','search'),
        ('index','.TW'),
        ('term',book),
        ('index','.AW'),
        ('term',author)]
        

queryapi = 'http://ipac.library.sh.cn/ipac20/ipac.jsp'

html = op_requests(url=queryapi,para=para)
print(html.url)
bsObj = BeautifulSoup(html.content,"html.parser")


vbook = bsObj.find_all("a",{"class":"mediumBoldAnchor"})
print(vbook)
# if vbook: # mediumBoldAnchor >= 1 , different version find, only scan 1st page
#     for v in vbook:
#         print(v)
#         bookname = str(v).split('<')[1].split('>')[-1].strip()
#         print(bookname)
#         if bookname == book:
#             n = v
#             for i in range(7):
#                 n = n.parent
#                 print(n)0000000
#             n = n.previous_sibling.text.strip()
#             print(n)
#             print(n+bookname)
#             # num.append(n)
#             print(v["href"])
#             # version.append(v["href"])
#         else:
#             print(bookname)
#             #sys.exit()
#             # pass
