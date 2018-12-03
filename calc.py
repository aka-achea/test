#!/usr/bin/python
#coding:utf-8

#每天听6小时，中等质量MP3

day = 10

albumnum = int(day)*6*60/4/12
size = str(int(day)*6*60/1024)+'GB'

print(albumnum)
print(size)