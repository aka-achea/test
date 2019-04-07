#!/usr/bin/python3
#coding:utf-8
#tested in win

from matplotlib import pyplot as plt
from PIL import Image
import pytesseract
import os,sys
import cv2
import difflib
import numpy as np

from mytool import remove_emptyline 

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

threshold = 120

def initTable(threshold=150):
    table = []
    for i in range(256): 
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

def readimg_pil(pic,threshold):
    # print(img)
    im = Image.open(pic).convert('L')  #灰度图 
    # im.show()
    ni = im.point(initTable(threshold),'1')
    # ni.save(out,'jpeg')
    ni.show()
    text = pytesseract.image_to_string(ni,lang='chi_sim')
    # print(t)
    return text

def myocr_pil(path):
    for j in os.listdir(path):
        imgpath = os.path.join(path,j)
        text = readimg_pil(imgpath,threshold)
        print(text)

# with open(out,'w',newline='',encoding='utf8') as c:
#     writer = csv.writer(c)
#     for i in range(len(ddict)):
#         writer.writerow(ddict[i+1])

def denoise_cv_gaus(img,n):
    print(f'高斯过滤 Size {n}')
    return cv2.GaussianBlur(img,(n,n),0)

def denoise_cv_bilat(img):
    print(f'双边过滤')
    return cv2.bilateralFilter(img,9,75,75)

def denoise_cv_med(img,n):
    print(f'中值消噪 Size {n}')
    return cv2.medianBlur(img,n)

def denoise_cv_fNM(img):
    print(f'fastNlMeansDenoising')
    return cv2.fastNlMeansDenoising(img)

def denoise_cv_gausthrold(img):
    print('高斯二值化')
    return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,7,2)

def cv2plt(img):
    b,g,r = cv2.split(img)
    return cv2.merge([r,g,b])

def myocr_cv(pic,book=False):
    img = cv2.imread(pic,0)        #灰度图

    if book == True:
        img = denoise_cv_med(img,5)    #中值消噪    
        img = denoise_cv_gaus(img,5)   #高斯过滤
        img = denoise_cv_bilat(img)    #双边过滤
        img = denoise_cv_gausthrold(img)    #高斯二值化               
        img = denoise_cv_gaus(img,5)   #高斯过滤
        img = denoise_cv_med(img,5)    #中值消噪   

    # img = denoise_cv_bilat(img)    #双边过滤
    # ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

    # cv2.imshow('denoised',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
 
    print('='*10)
    text = pytesseract.image_to_string(img,lang='chi_sim')
    text = remove_emptyline(text)
    print(text)

    # plt.imshow(img,'gray')
    # plt.xticks([]),plt.yticks([])
    # plt.show()

    return text

def main():
    # print(len(sys.argv))
    if len(sys.argv) == 1:
        book = False
    elif sys.argv[1] == 'b':
        book = True
    else:
        book = False    

    pic = input(">>")
    text = myocr_cv(pic,book)



if __name__ == "__main__":
    path = r'M:\MyProject\ocr'
    output = r'E:\jj\out.txt'
    
    main()
    # pic = r'M:\MyProject\ocr\IMG_9507.JPG'
    # tpil = readimg_pil(pic,threshold)


