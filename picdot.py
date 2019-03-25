#!/usr/bin/python3
#coding:utf-8
# tested in win

import os
from PIL import Image
import numpy as np
import pyfiglet

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

heart = np.array([
    [0,1,0,0,0,1,0],
    [1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1],
    [0,1,1,1,1,1,0],
    [0,0,1,1,1,0,0],
    [0,0,0,1,0,0,0], ])

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
    [0,0,0,0,0],
    [0,1,1,1,0],
    [0,0,1,0,0],
    [0,0,1,0,0],
    [0,0,1,0,0],
    [0,0,1,0,0],
    [0,0,1,0,0],
    [0,1,1,1,0],
    [0,0,0,0,0],  ])

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

zeorarr = np.zeros(( len(base),1 )) # for concatenate array

mapdic = { 'C':C,'E':E,'H':H,'I':I,'L':L,'O':O,'R':R,'U':U,'V':V }

ascii_char = list("@B%8&WM*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1[]?-_+~<>i!;:,^'")

# word = word.replace(' ','_')

#背景着色：  dodgerblue, FFFACD黄色 F0FFFF白 BFEFFF蓝 b7facd青色 ffe7cc浅橙色 fbccff浅紫色 d1ffb8淡绿 febec0淡红 E0EEE0灰
colorlist = ['#1E90FF','#FFFACD','#F0FFFF','#BFEFFF','#b7facd','#ffe7cc','#fbccff','#d1ffb8','#febec0','#E0EEE0']
#index用来改变不同字的背景颜色
index = 0

def pastepic(arr,canvas,picfolder):
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
            if arr[row][col] == 1:
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

def figletter(word):  # create geek letter
    result = pyfiglet.figlet_format(str(word), font = "standard"  ) 
    print(result)

def pix2char(r,b,g,alpha=256):
    if alpha == 0:
        return ' '
    gray = int(0.2126*r+0.7152*g+0.0722*b)
    unit = (256.0+1)/len(ascii_char)
    return ascii_char[int(gray/unit)]

def pic2char(img):
    width,height = 300,300    
    img = Image.open(img)
    img = img.resize((width,height),Image.NEAREST)
    txt = ""
    for y in range(height):
        for x in range(width):
            txt += pix2char(*img.getpixel((x,y)))
        txt += '\n'
    print(txt)
    return txt

    # if out:
    #     with open(out,'w') as f:
    #         f.write(txt)


def main(word,picfolder,out):
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

    totalx = 50*len(arr[0])
    totaly = 50*len(arr)
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
    main(word,picfolder,outpic)

    # txt = pic2char(back)

    # with open(r"e:\out.txt",'w') as f:
    #     f.write(txt)