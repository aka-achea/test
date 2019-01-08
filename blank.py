


import os,re,configparser
import urllib,shutil,coloredlogs,logging


from PIL import Image
import pytesseract,math
import codecs



f = codecs.open('e:/intimate.txt','a','utf-8')#这里表示把intimate.txt文件从utf-8编码转换为unicode，就可以对其进行unicode读写了
f.write(u'中文')#直接写入unicode
s = '中文'
f.write(s.decode('gbk'))#先把gbk的s解码成unicode然后写入文件
f.close()

f = codecs.open('e:/intimate.txt','r','utf-8')
s = f.readlines()
f.close()
for line in s:
    print(line.encode('gbk'))