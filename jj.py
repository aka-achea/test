#!/usr/bin/python
#coding:utf-8



from PIL import Image
import pytesseract,math,os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
img = 'e:\\t1.png'
path = 'e:\\'
# box = (0,300,655,1230)
box1 = (0,300,655,530)
box2 = (0,530,655,760)
box3 = (0,760,655,990)
box4 = (0,990,655,1220)
box = [box1,box2,box3,box4]
# jump = 230
#(750, 1334)
# print(im.size)

def initTable(threshold=150):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

def format_data(dlist):
    ddict = {}
    s = 0
    for i in range(n):
        name = dlist[s].split(' ')[0]
        r = dlist[s+1].split(' ')  #  '4.7540%', '366天'
        j = [name,r[0][:4],r[-1]]
        ddict[i] = j
        s += 3
    return ddict



im = Image.open(img).convert('L')

ddict = {}

for b in range(4):
    out = os.path.join(path,str(b)+'.jpg')
    # print(out)
    ni = im.crop(box[b])
    ni = ni.point(initTable(195),'1')
    # ni.save(out,'jpeg')
    t = pytesseract.image_to_string(ni,lang='chi_sim')
    # print(t)
    dlist = []
    t = t.split('\n')
    for i in t:
        if i != '' and i != ' ':
            dlist.append(i)

    # n = len(dlist)
    name = dlist[0].split(' ')[0]
    rate = dlist[1][:4]
    for i in range(2,len(dlist)):
        if '天' in dlist[i]: 
            days = dlist[i][:-1]
            break
        else:
            days = 1

    j = [name,rate,days]
    ddict[b] = j


for i in range(len(ddict)):
    print(ddict[i])

# n = math.floor(/3)
# ddict = format_data(dlist)

# for i in range(n):
#     print(ddict[i])

