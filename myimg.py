#!/usr/bin/python3
#coding:utf-8
# tested in win

from PIL import Image
import imageio
import numpy as np
import os

def gifsplit(pic,outfolder):
    images = imageio.mimread(pic)
    #把上面的每帧图片进行保存
    for i, img in enumerate(images):
        img = np.asarray(img)
        imageio.imwrite(os.path.join(outfolder,"%d.png" % i), img)

def gifmake(folder,gifname):
    fileOrder = sorted([int(os.path.splitext(x)[0]) for x in os.listdir(folder)])
    # print(fileOrder)
    frames = []
    for order in fileOrder:
        filename = str(order)+ '.png'
        filePath = os.path.join(folder,filename)
        frames.append(imageio.imread(filePath))
    gifpath = os.path.join(folder,gifname)
    imageio.mimsave(gifpath, frames, 'GIF', duration = 0.1)

if __name__ == "__main__":
    pic = r'M:\MyProject\ocr\t.gif'
    outfolder = r'M:\MyProject\ocr'
    # gifsplit(pic,outfolder)
    gifname = 'g.gif'
    gifmake(outfolder,gifname)