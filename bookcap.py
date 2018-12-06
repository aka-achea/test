#!/usr/bin/python
#coding:utf-8
"""
SCAN eBOOK
"""

import time , os
import pyautogui as auto


auto.size()
width, height = auto.size()
print(width,height)
auto.PAUSE = 1
auto.click(150,150,button='left')

name = input('Book Name: ')
pages = input('Total page: ')

def scan(name,p):
    auto.screenshot(name+"_"+p+".png",region=(125,90, 620, 815))

for p in range(1,pages):
    scan(name,str(p))
    time.sleep(1)
    auto.typewrite(['right'])
