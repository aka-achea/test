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
    '''focus need to be in middle monitor'''
    png = name+"_"+str(p)+".png"
    auto.screenshot(png,region=(15,440,1040,1360))  # for bookshelf
    # time.sleep(0.2)
    auto.keyDown('ctrl')
    auto.keyDown('pagedown')
    auto.keyUp('ctrl')
    auto.keyUp('pagedown')


def scan_pbb(name,p):
    '''Capture PBB'''
    png = name+"_"+str(p)+'.png'
    print(f'Page {p}')
    time.sleep(2)
    auto.screenshot(png,region=(10,90,1090,930)) # for pbb

if __name__ == "__main__":
    try:
        path = r'O:'
        # name = input('Book Name: ')
        # pages = input('Total page: ')
        name = 'SAP'
        pages = '100'

        bp = os.path.join(path,name)
        if os.path.isdir(bp) is False:
            os.mkdir(bp)
        os.chdir(bp)

        width, height = auto.size()
        # print(width,height)
        auto.PAUSE = 1
        # auto.click(150,150,button='left') # for kindle
        # auto.click(100,200,button='left') # for bookshelf

        for p in range(1,int(pages)+1):
            scan_pbb(name,p)
        print('finish book capture')
    except KeyboardInterrupt:
        print("Stop")


