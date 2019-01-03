


import os,re,configparser
import urllib,shutil,coloredlogs,logging


from PIL import Image
import pytesseract,math

img = 'e:\\t.jpg'
out = 'e:\\n.jpg'

im = Image.open(img)
im = im.convert('L')


def initTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

ni = im.point(initTable(195),'1')
ni.save(out,'jpeg')

# img = 'e:\\n140.jpg'

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
t = pytesseract.image_to_string(Image.open(out),lang='chi_sim')



get = []
t = t.split('\n')
for i in t:
    if i != '' and i != ' ':
        # print(i.strip())
        get.append(i)

print(get)
# # n = math.floor(len(get)/3)

