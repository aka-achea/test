#!/usr/bin/python
#coding:utf-8



from PIL import Image
import pytesseract,math,os ,csv,codecs
from prettytable import PrettyTable 

# ocr = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
ocr = r'C:\Users\chenj82\AppData\Local\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd =ocr

path = r'E:\UT\JiJin'
cf = r'E:\UT\JiJin\j.csv'
threshold = 189


tdir = os.path.join(path,'t')
# box = (0,300,655,1230)
box1 = (0,300,655,530)
box2 = (0,530,655,760)
box3 = (0,760,655,990)
box4 = (0,990,655,1220)
box = [box1,box2,box3,box4]
# jump = 230
#(750, 1334)
# print(im.size)
ddict = {}


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

def formattable(ddict):
    t = PrettyTable()
    t.field_names = ['基金','利率','天数']
    t.align['基金'] = 'l'
    t.sortby = '基金'
    for i in range(len(ddict)):
        t.add_row(ddict[i+1])
    print(t)

def readimg(path,threshold):
    n = 1
    for i in os.listdir(path):
        img = os.path.join(path,i)
        # print(img)
        im = Image.open(img).convert('L')   
        for b in range(4):
            # out = os.path.join(path,str(b)+'.jpg')
            # print(out)
            ni = im.crop(box[b])
            ni = ni.point(initTable(threshold),'1')
            # ni.save(out,'jpeg')
            t = pytesseract.image_to_string(ni,lang='chi_sim')
            # print(t)
            dlist = []
            for i in t.split('\n'):
                if i != '' and i != ' ':
                    dlist.append(i)
            # n = len(dlist)
            name = modificate(dlist[0].split(' ')[0])
            rate = dlist[1].replace('+','')[:4]
            for i in range(2,len(dlist)):
                if '天' in dlist[i]: 
                    days = dlist[i][:-1]
                    break
                else:
                    days = 1
            j = [name,rate,days]
            # print(j) # details
            ddict[n] = j
            n += 1
    return ddict


# print('threshold '+str(threshold))
ddict = readimg(path,threshold)
# formattable(ddict)

with open(cf,'w',newline='',encoding='utf-8-sig') as c:
    writer = csv.writer(c)
    for i in range(len(ddict)):
        writer.writerow(ddict[i+1])

# n = math.floor(/3)
# ddict = format_data(dlist)


    

"""
change log
2018.1.8 add csv output v1.2
2018.1.4 add pretty table v1.1
2018.1.3 build core function v1.0

"""