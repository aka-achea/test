#!/usr/bin/python3
#coding:utf-8
#tested in win


from PIL import Image
import pytesseract
import os


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

threshold = 120

def initTable(threshold=150):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


def readimg(imgpath,threshold):
    # print(img)
    im = Image.open(imgpath).convert('L')  #灰度图 
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
        text = readimg(imgpath,threshold)
        print(text)

# with open(out,'w',newline='',encoding='utf8') as c:
#     writer = csv.writer(c)
#     for i in range(len(ddict)):
#         writer.writerow(ddict[i+1])

if __name__ == "__main__":
    path = r'M:\MyProject\ocr'
    output = r'E:\jj\out.txt'
    myocr_pil(path)