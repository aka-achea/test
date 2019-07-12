#!/usr/bin/python3
#coding:utf-8
#tested in win
"""
SCAN eBOOK on kindle
"""

import time , os
import pyautogui as auto



def scan_kindle(name,p):
    png = name+"_"+str(p)+".png"
    auto.screenshot(png,region=(125,90, 620, 815))  # for kindle
    time.sleep(1)
    auto.typewrite(['right'])

def scan_bookshelf(name,p): 
    '''in middle monitor'''
    png = name+"_"+str(p)+".png"
    auto.screenshot(png,region=(15,460,1040,1365))  # for bookshelf
    time.sleep(0.2)
    auto.keyDown('ctrl')
    auto.keyDown('pagedown')
    auto.keyUp('ctrl')
    auto.keyUp('pagedown')

 

if __name__ == "__main__":

    path = r'E:\daka'
    # name = input('Book Name: ')
    # pages = input('Total page: ')
    name = 'TE'
    pages = '103'

    bp = os.path.join(path,name)
    if os.path.isdir(bp):
        print('Book folder exist')
    else:
        os.mkdir(bp)
    os.chdir(bp)

    width, height = auto.size()
    print(width,height)
    auto.PAUSE = 1
    # auto.click(150,150,button='left') # for kindle
    auto.click(800,800,button='left') # for bookshelf

    for p in range(59,int(pages)):
        scan_bookshelf(name,p)

    print('finish book capture')



"""
change log:
2018.12.7 resize with new screen v1.1
2017.6.21 build basic screenshot funciton v1.0
"""