#!/usr/bin/python3
#coding:utf-8
# tested in win

from PIL import Image
import pytesseract
import os
import cv2
import numpy as np


def gifsplit(pic):
    gif = Image.open(pic)

    
    mypalette = gif.getpalette()
    gif.putpalette(mypalette)
    im = Image.new('RGBA',gif.size)
    im.paste(gif)
    # im.save('image\\{}.png'.format(str(i)))


if __name__ == "__main__":
    pic = r'M:\MyProject\ocr\t.gif'
    gifsplit(pic)