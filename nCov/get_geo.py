#!/usr/bin/python3
#coding:utf-8

from urllib import parse
import hashlib
import requests
import json
from pprint import pprint

from conf import bkey,geofile
from crawler import crawl_wx_location



def get_urt(address):
    '''Build API request'''
    bk = bkey()
    # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=你的ak
    queryStr = f'/geocoder?address={address}&output=json&ak={bk.ak_geo}' 
 
    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
 
    # 在最后直接追加上yoursk
    rawStr = encodedStr + bk.sk_geo
 
    #计算sn
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
     
    #由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    url = parse.quote("http://api.map.baidu.com"+queryStr+"&sn="+sn, safe="/:=&?#+!$,;'@()*[]")  
    # print(url)
    return url


def get_coord(address):
    '''Get coordinate from address'''
    try:
        url = get_urt(address)
        resp = requests.get(url).text
        js = json.loads(resp)
        # pprint(js)
        coord = js['result']['location']
        coord = [ coord['lng'],coord['lat'] ]
    except:
        raise
    return coord


def update_geo(wx):
    '''Update geo json'''
    loc = crawl_wx_location(wx)
    with open(geofile,'r',encoding='utf-8') as f:
        j = json.loads(f.read())
        # pprint(j)
    for x in loc:
        if x not in j.keys():
            coord = get_coord('上海市'+x)
            if ( coord[0] > 120 and coord[0] < 123 and
                coord[1] >29 and coord[1] < 32 )  :
                print(f'"{x}":{coord}')
                j[x] = coord
            else:
                print(f'Cannot find {x}')
    # pprint(j)
    with open(geofile,'w',encoding='utf-8') as f:
        json.dump(j,f,ensure_ascii=False,indent=2)


if __name__ == "__main__":

    wx = 'https://mp.weixin.qq.com/s/Yf5f_f7EldzjCZwuJRJNrw'

    update_geo(wx)