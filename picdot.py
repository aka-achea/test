#!/usr/bin/python3
#coding:utf-8
# tested in win

import os
from PIL import Image
import numpy as np
from myimg import squaresize,mapdic,zeorarr


ascii_char = list("@B%8&WM*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1[]?-_+~<>i!;:,^'")

# word = word.replace(' ','_')

#背景着色：  dodgerblue, FFFACD黄色 F0FFFF白 BFEFFF蓝 b7facd青色 ffe7cc浅橙色 fbccff浅紫色 d1ffb8淡绿 febec0淡红 E0EEE0灰
colorlist = ['#1E90FF','#FFFACD','#F0FFFF','#BFEFFF','#b7facd','#ffe7cc','#fbccff','#d1ffb8','#febec0','#E0EEE0']
#index用来改变不同字的背景颜色
index = 0


def pastepic(arr,canvas,picfolder):
    '''Paste picture on position 1'''
    piclist = os.listdir(picfolder)
    x,y = 0,0
    count = 0
    for row in range(len(arr)):
        # print(r)
        for col in range(len(arr[0])):
            # print(c)
            x,y = 50*col,50*row
            if len(piclist) == 0:
                piclist = os.listdir(picfolder)
            if arr[row][col] == 1:
                count += 1
                # print(x,y)                
                pic = os.path.join(picfolder,piclist[0])
                del piclist[0]
                img = squaresize(pic)
                # img = Image.open(pic)    
                # wpercent = (50/float(img.size[0]))
                # hsize = int((float(img.size[1])*float(wpercent)))
                # img = img.resize((50,hsize),Image.LANCZOS)
                canvas.paste(img,(x,y))
    print('Total use {} picture'.format(count))
    

def picdot(word,back,picfolder,out):
    '''Stack the charactor'''
    for n in range(len(word)):
        # print(word[n])
        if n == 0:
            arr = mapdic[word[n]]
        elif word[n] not in mapdic:
            arr = np.hstack(( arr,zeorarr  ))
        else:
            arr = np.hstack(( arr,mapdic[word[n]][::,1:] ))
    # arr = arr[::,1:] # remove 1st column
    # print(arr)

    totalx,totaly = 50*len(arr[0]),50*len(arr)
    canvas = Image.new('RGB',(totalx,totaly),'#0066cc')  # 新建画布
    bg = Image.open(back)
    bg = bg.resize((totalx,totaly),Image.LANCZOS)
    canvas.paste(bg,(0,0))
    pastepic(arr,canvas,picfolder)
    canvas.show()
    canvas.save(out)


if __name__ == "__main__":
    picfolder = r'C:\Users\chenj82.RMOASIA\Downloads\WhoKnows'
    # front = r'E:\bang.png'
    back = r'E:\b.jpg'
    outpic = r'E:\out.jpg'
    word = 'ROCHE'    
    picdot(word,picfolder,outpic)

