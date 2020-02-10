#!/usr/bin/python3
#coding:utf-8

from urllib import parse
import hashlib
import requests
import json
from pprint import pprint

from conf import ak_geo,sk_geo

loc = [
'上海市浦东新区地杰国际城E欧泊时光',
'上海市浦东新区绿林路51弄',
'上海市浦东新区绿地崴廉公寓',
'上海市浦东新区浦东国际机场',
'上海市徐汇区地铁大木桥路站',
'上海市徐汇区地铁陕西南路站',
'上海市静安区闻喜路935弄',
'上海市普陀区西乡路91弄',
'上海市闵行区中华美路60弄',
'上海市闵行区爱博一村',
'上海市闵行区虹桥国际机场',
'上海市闵行区虹桥火车站',
'上海市闵行区地铁虹桥2号航站楼站',
'上海市闵行区大润发（华漕店）',
'上海市嘉定区光明D9空间',
'上海市嘉定区发祥路89号',
'上海市嘉定区永辉超市（嘉定宝龙广场店）',
'上海市松江区新凯家园一期',
]


def get_urt(address):
 
    # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=你的ak
    queryStr = f'/geocoder?address={address}&output=json&ak={ak_geo}' 
 
    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
 
    # 在最后直接追加上yoursk
    rawStr = encodedStr + sk_geo
 
    #计算sn
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
     
    #由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    url = parse.quote("http://api.map.baidu.com"+queryStr+"&sn="+sn, safe="/:=&?#+!$,;'@()*[]")  
    # print(url)
    return url


def get_coord(address):
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


if __name__ == "__main__":
    for x in loc:
        coord = get_coord(x)
        print(f'"{x}":{coord}')