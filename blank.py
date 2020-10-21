

# import json
from myfs import g_fsize,jdump,jload
from itertools import product
from pprint import pprint

q='magnet:?xt=urn:btih:2UVRVPWZV7FMBD3GULCY4TMNML24NSAE&dn=%e5%8d%87%e7%ba%a7%2e1080p%2eBD%e4%b8%ad%e8%8b%b1%e5%8f%8c%e5%ad%97%5b%e6%9c%80%e6%96%b0%e7%94%b5%e5%bd%b1www%2e66ys%2etv%5d%2emp4&tr=udp%3a%2f%2f9%2erarbg%2eto%3a2710%2fannounce&tr=udp%3a%2f%2f9%2erarbg%2eme%3a2710%2fannounce&tr=http%3a%2f%2ftr%2ecili001%2ecom%3a8070%2fannounce&tr=http%3a%2f%2ftracker%2etrackerfix%2ecom%3a80%2fannounce&tr=udp%3a%2f%2fopen%2edemonii%2ecom%3a1337&tr=udp%3a%2f%2ftracker%2eopentrackr%2eorg%3a1337%2fannounce&tr=udp%3a%2f%2fp4p%2earenabg%2ecom%3a1337'

def unquote_url(url):
    from urllib import parse
    return parse.unquote(url)

# print(unquote_url(q))
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

import json,pprint
ffile = r'N:\MyProject\BM\ff.log'
# ff = {1: {'email': 'CJYRB@hotmail.com',
#      'link': 'https://mp.weixin.qq.com/s/11OPqElE8vXjGs2E1GTHGw',
#      'tag': '史',
#      'timestamp': '2020-10-21 09:59:32'}}
# with open(ffile,'w',encoding='utf-8') as x:
#     json.dump(ff,x,ensure_ascii=False,indent=2)

with open(ffile,'r',encoding='utf-8') as f:
    ff = json.loads(f.read())
    pprint.pprint(ff)