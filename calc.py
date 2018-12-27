#!/usr/bin/python
#coding:utf-8

#每天听6小时，中等质量MP3

def mp3calc():
    day = 10

    albumnum = int(day)*6*60/4/12
    size = str(int(day)*6*60/1024)+'GB'

    print(albumnum)
    print(size)

def airticket():
    pass

def profit():
    days = 5
    cost = 30000
    rate = 9.2
    profit = cost*(rate/100)*(days/365)
    print(profit)

if __name__ == "__main__":
    profit()
