#!/usr/bin/python3
#coding:utf-8
#tested in win

from matplotlib import pyplot as plt
from PIL import Image
import pytesseract
import os
import cv2
import difflib
import numpy as np

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

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
    return cv2.GaussianBlur(img,(n,n),0)

def denoise_cv_bilat(img):
    return cv2.bilateralFilter(img,9,75,75)

def denoise_cv_med(img,n):
    return cv2.medianBlur(img,n)

def denoise_cv_fNM(img):
    return cv2.fastNlMeansDenoising(img)

def cv2plt(img):
    b,g,r = cv2.split(img)
    return cv2.merge([r,g,b])

def myocr_cv(pic):
    img = cv2.imread(pic,0)

    dgaus5 = denoise_cv_gaus(img,5)
    dgaus7 = denoise_cv_gaus(img,7)
    dbi = denoise_cv_bilat(img)
    dmed5 = denoise_cv_med(img,5)
    fNM = denoise_cv_fNM(img)

    tgaus5 = pytesseract.image_to_string(dgaus5,lang='chi_sim')
    print(f'Gaus5:\n {tgaus5}')
    tgaus7 = pytesseract.image_to_string(dgaus7,lang='chi_sim')
    print(f'Gaus7:\n {tgaus7}')
    tbi = pytesseract.image_to_string(dbi,lang='chi_sim')
    print(f'Bilateral:\n {tbi}')  
    tmed5 = pytesseract.image_to_string(dmed5,lang='chi_sim')
    print(f'Median:\n {tmed5}')  

    tfNM = pytesseract.image_to_string(fNM,lang='chi_sim')
    print(f'fNM:\n {tfNM}')  
      

    # cv2.imshow('denoised',denoised)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # plt.imshow(img2, cmap = 'gray', interpolation = 'bicubic')
    # plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    # plt.show()
    return {'gaus5':tgaus5,'gaus7':tgaus7,'bilat':tbi,'med5':tmed5,'fNM':tfNM}


if __name__ == "__main__":
    path = r'M:\MyProject\ocr'
    output = r'E:\jj\out.txt'

    pic = r'E:\jj\a.jpg'
    tpil = readimg_pil(pic,threshold)

    tdic = myocr_cv(pic)
    # print(tdic)
    g5m = difflib.SequenceMatcher(a=tdic['gaus5'],b=tdic['med5']).ratio()
    # g5b = difflib.SequenceMatcher(a=tdic['gaus5'],b=tdic['bilat']).ratio()
    fm = difflib.SequenceMatcher(a=tdic['fNM'],b=tdic['med5']).ratio()
    # pb = difflib.SequenceMatcher(a=tpil,b=tdic['bilat']).ratio()
    fg5 = difflib.SequenceMatcher(a=tdic['fNM'],b=tdic['gaus5']).ratio()
    # mb = difflib.SequenceMatcher(a=tdic['med5'],b=tdic['bilat']).ratio()

    print(g5m,fm,fg5)

    # for k in tdic:
    #     print(tdic[k])

