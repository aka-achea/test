#!/usr/bin/python3
#coding:utf-8

from configparser import ConfigParser
import os


baiduconf = r'M:\GH\_pri\baidu.ini'

def readconf(baiduconf):
    config = ConfigParser()
    config.read(baiduconf)
    ak_geo = config.get('BaiduMap','ak_2020_srv') 
    sk_geo = config.get('BaiduMap','sk_2020_srv')
    ak_web = config.get('BaiduMap','ak_nCovApi_browser')
    ak_dev = config.get('BaiduMap','ak_dev_browser')
    return ak_dev,ak_geo,ak_web,sk_geo

bucket = '2020-1301184162'
dest = 'render.html'
logbucket = 'log-1301184162'
# workpath = r'M:\MyProject\nCov'
workpath = r'C:\Business\GitHub\nCov'
qconf = os.path.join(workpath,'qcloud.ini')
outfile = os.path.join(workpath,dest)
logdir = os.path.join(workpath,'log')
geofile = os.path.join(workpath,'geo.json')
shsumary = os.path.join(workpath,'shsumary.txt')

#width:200px;height:50px;font-weight: bold;font-size: 20px;
#http://api.map.baidu.com/lbsapi/getpoint/index.html

