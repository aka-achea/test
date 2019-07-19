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
    auto.screenshot(png,region=(15,450,1040,1360))  # for bookshelf
    # time.sleep(0.2)
    auto.keyDown('ctrl')
    auto.keyDown('pagedown')
    auto.keyUp('ctrl')
    auto.keyUp('pagedown')

 

if __name__ == "__main__":
    try:
        path = r'E:\daka'
        # name = input('Book Name: ')
        # pages = input('Total page: ')
        name = 'A5.5'
        pages = '880'

        bp = os.path.join(path,name)
        if os.path.isdir(bp):
            print('Book folder exist')
        else:
            os.mkdir(bp)
        os.chdir(bp)

        width, height = auto.size()
        # print(width,height)
        auto.PAUSE = 1
        # auto.click(150,150,button='left') # for kindle
        auto.click(800,800,button='left') # for bookshelf

        for p in range(572,int(pages)):
            scan_bookshelf(name,p)

        print('finish book capture')

    except KeyboardInterrupt:
        print("Stop")



"""
change log:
2019.7.19 add bookshelf for aws v1.2
2018.12.7 resize with new screen v1.1
2017.6.21 build basic screenshot funciton v1.0
"""