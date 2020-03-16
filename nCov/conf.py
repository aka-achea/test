#!/usr/bin/python3
#coding:utf-8

from configparser import ConfigParser
import os




class bkey():
    def __init__(self):
        baiduconf = r'M:\GH\_pri\baidu.ini'
        if not os.path.exists(baiduconf):
            baiduconf = r'C:\Business\GitHub\baidu.ini'
        config = ConfigParser()
        config.read(baiduconf)
        self.ak_geo = config.get('BaiduMap','ak_2020_srv') 
        self.sk_geo = config.get('BaiduMap','sk_2020_srv')
        self.ak_web = config.get('BaiduMap','ak_nCovApi_browser')
        self.ak_dev = config.get('BaiduMap','ak_dev_browser')


bucket = '2020-1301184162'
dest = 'render.html'
logbucket = 'log-1301184162'
workpath = r'M:\MyProject\nCov'
if not os.path.exists(workpath):
    workpath = r'C:\Business\GitHub\nCov'
qconf = os.path.join(workpath,'qcloud.ini')
outfile = os.path.join(workpath,dest)
logdir = os.path.join(workpath,'log','03')
geofile = os.path.join(workpath,'geo.json')
shsumary = os.path.join(workpath,'shsumary.txt')

#width:200px;height:50px;font-weight: bold;font-size: 20px;
#http://api.map.baidu.com/lbsapi/getpoint/index.html


if __name__ == "__main__":
    b = bkey()
    print(b.ak_web)