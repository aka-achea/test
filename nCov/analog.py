#!/usr/bin/python3
#coding:utf-8

from pprint import pprint
from collections import Counter
import os
import datetime

from cos import download_cos
from conf import logdir,logbucket

myip = ['101.80.91.59','101.87.14.107','101.87.13.250','101.87.14.204','101.80.89.20','101.87.12.7','101.87.10.87']
iplist = []
timelist = []

def downloadyesterdaylog():
    yesterday = datetime.date.today()-datetime.timedelta(days=1)
    yesterdate = str(yesterday)[-2:]
    targetdir = os.path.join(logdir,yesterdate)
    try:
        os.mkdir(targetdir)
    except FileExistsError:
        pass
    finally:
        os.chdir(targetdir)
    objfolder = f"cos-access-log/{str(yesterday).replace('-','/')}"
    result = download_cos(logbucket,objfolder)
    print(result)
    return targetdir


def ana_all():
    for d in os.listdir(logdir):
        ldir = os.path.join(logdir,d)
        ana_log(ldir)
    a = list(Counter(iplist))
    pprint(sorted(a))

def ana_log(ldir):   
    for logs in os.listdir(ldir):
        with open(os.path.join(ldir,logs),'r') as f:
            for x in f.readlines():
                data = x.split()
                if data[6] not in myip:
                    iplist.append(data[6])
                    timelist.append(data[3])
    t = [ t.split('T')[1][:-1] for t in timelist ]
    h = [ x[:2] for x in t ]
    # pprint(Counter(h))


def ana_yesterday():    
    targetdir = downloadyesterdaylog()    
    ana_log(targetdir)
    a = list(Counter(iplist))
    pprint(sorted(a))


if __name__ == "__main__":
    ana_yesterday()