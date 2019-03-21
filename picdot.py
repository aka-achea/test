#!/usr/bin/python3
#coding:utf-8
# tested in win


import os
from PIL import Image
import numpy as np

picfolder = r'C:\Users\chenj82.RMOASIA\Downloads\WhoKnows'
# front = r'E:\bang.png'
back = r'E:\blank.png'
out = r'E:\out.jpg'

base = np.array([
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],  ])


C = np.array([
    [0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,1,0,0,0,1,0],
    [0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0],  ])

E = np.array([
    [0,0,0,0,0,0,0],
    [0,1,1,1,1,1,0],
    [0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,1,1,1,1,1,0],
    [0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0],  ])

H = np.array([
    [0,0,0,0,0,0,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,1,1,1,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,0,0,0,0,0,0],  ])

I = np.array([
    [0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0],  ])

L = np.array([
    [0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0],  ])

O = np.array([
    [0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0],  ])

R = np.array([
    [0,0,0,0,0,0,0],
    [0,1,1,1,1,0,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,1,1,1,0,0],
    [0,1,0,1,0,0,0],
    [0,1,0,0,1,0,0],
    [0,1,0,0,0,1,0],
    [0,0,0,0,0,0,0],  ])

U = np.array([
    [0,0,0,0,0,0,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0],  ])

V = np.array([
    [0,0,0,0,0,0,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,0,1,0,1,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0],  ])





mapdic = { 'R':R,'O':O,'C':C,'H':H,'E':E }

word = 'ROCHE'

#背景着色：  dodgerblue, FFFACD黄色 F0FFFF白 BFEFFF蓝 b7facd青色 ffe7cc浅橙色 fbccff浅紫色 d1ffb8淡绿 febec0淡红 E0EEE0灰
colorlist = ['#1E90FF','#FFFACD','#F0FFFF','#BFEFFF','#b7facd','#ffe7cc','#fbccff','#d1ffb8','#febec0','#E0EEE0']
#index用来改变不同字的背景颜色
index = 0

totalx = 50*( len(word)*len(base[0]) )
totaly = 50*len(base)
canvas = Image.new('RGB',(totalx,totaly),'#0066cc')  # 新建画布

def pastepic(arr,picfolder):
    piclist = os.listdir(picfolder)
    x,y = 0,0
    count = 0
    for row in range(len(arr)):
        # print(r)
        for col in range(len(arr[0])):
            # print(c)
            x = 50*col
            y = 50*row
            if len(piclist) == 0:
                piclist = os.listdir(picfolder)
            if arr[row][col] != 1:
                count += 1
                # print(x,y)                
                pic = os.path.join(picfolder,piclist[0])
                del piclist[0]
                img = cropresize(pic)
                # img = Image.open(pic)    
                # wpercent = (50/float(img.size[0]))
                # hsize = int((float(img.size[1])*float(wpercent)))
                # img = img.resize((50,hsize),Image.LANCZOS)
                canvas.paste(img,(x,y))
    print('Total use {} picture'.format(count))
    
def cropresize(pic):
    img = Image.open(pic)   
    width, height = img.size
    newsize = width if width < height else height 
    left = (width - newsize)/2
    top = (height - newsize)/2
    right = (width + newsize)/2
    bottom = (height + newsize)/2
    img.crop((left, top, right, bottom))
    img = img.resize((50,50),Image.LANCZOS)
    return img


zeorarr = np.zeros(( len(base),1 )) # for concatenate array

for n in range(len(word)):
    if n == 0:
        arr = np.hstack(( zeorarr,mapdic[word[n]]))
    # elif n == len(word):
    #     arr = np.hstack(( arr,zeorarr  ))
    else:
        arr = np.hstack(( arr,mapdic[word[n]] ))

arr = arr[::,1:]
# print(arr)

pastepic(arr,picfolder)

canvas.show()

