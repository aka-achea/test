#!/usr/bin/python
#coding:utf-8



from PIL import Image
import pytesseract,math,os ,csv,codecs
from prettytable import PrettyTable 
from pathlib import PureWindowsPath as pp
import time



from mystr import splitall


'''
1. iPhone wx screen shot
2. Picsew
3. Tesseract
'''


ocr = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd =ocr

path = r'E:\UT\JiJin'
cf = r'j.csv'
threshold = 189



tdir = os.path.join(path,'t')
height = 245

# (left, upper, right, lower)
# The right can also be represented as (left+width)
# and lower can be represented as (upper+height)

# jump = 230
#(750, 1334)
# print(im.size)
jdict = {}


def modificate(text):
    text = str(text)    
    text = text.replace('，','')   
    text = text.replace('预约中','')
    text = text.replace('”','')
    text = text.strip()
    return text


def initTable(threshold=150):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


    
def formattable(jdict):
    t = PrettyTable()
    t.field_names = ['基金','利率','天数']
    t.align['基金'] = 'l'
    t.sortby = '基金'
    for i in range(len(jdict)):
        t.add_row(jdict[i])
    print(t)


def readimg(path,threshold):
    seplist = ['\n',' ',]
    n = 0
    for x in os.listdir(path):
        if x.split('.')[-1] == 'PNG':          
            img = os.path.join(path,x)
            im = Image.open(img).convert('L') 
            while True:
                try:    
                    print('='*40)
                    box = (0,height*n,800,height*(n+1))
                    ni = im.crop(box)
                    ni = ni.point(initTable(threshold),'1')
                    # out = os.path.join(path,str(b)+'.jpg')
                    # ni.save(out,'jpeg')
                    content = pytesseract.image_to_string(ni,lang='chi_sim')
                    content = splitall(seplist,content)
                    # print(content)
                    name = content[0]
                    for z in range(1,len(content)):
                        if '.' in content[z]: 
                            rate = content[z].split('%')[0]
                            break
                    for z in range(2,len(content)):
                        if '天' in content[z]: 
                            days = content[z].split('天')[0]
                            break
                        else:
                            days = 1
                    j = [name,rate,days]
                    print(j) # details
                    jdict[n] = j
                    if content == []: break
                    n += 1
                except IndexError:
                    break
    return jdict


# print('threshold '+str(threshold))
jdict = readimg(path,190)
formattable(jdict)

# with open(cf,'w',newline='',encoding='utf-8-sig') as c:
#     writer = csv.writer(c)
#     for i in range(len(jdict)):
#         writer.writerow(jdict[i+1])

# n = math.floor(/3)
# jdict = format_data(content)


    

"""
change log
2018.1.8 add csv output v1.2
2018.1.4 add pretty table v1.1
2018.1.3 build core function v1.0

"""