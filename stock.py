#!/usr/bin/python
#coding:utf-8
#Python3

import openpyxl

s = r'D:\Profile\Desktop\wt.txt'
xl = r'J:\DOC\我的坚果云\newstock.xlsx'


def readtransaction(s):
    with open(s,'r') as f:
        a = f.readlines()[3:] 
        # a = a[3:]
        t = {}
        n = 0
        for i in a:
            e = i.split()
            x = -1 if e[5] == '买入' else 1
            v = [e[0],e[4],e[5],e[8],float(e[9])*x,float(e[9])*x*float(e[8])]
            # print(v)
            t[n] = v
            n += 1
    return t

def stock(xl,t):
    wb = openpyxl.load_workbook(xl)
    sheet = wb['Sheet2']
    max = sheet.max_row
    for i in range(len(t)):
        # print(t[i])                    
        for n in range(6) :
            # print(t[i][n])
            sheet.cell(row=(max+i+1),column=(n+1)).value = t[i][n] 
    wb.save(xl)

try:
    t = readtransaction(s)
    stock(xl,t)
except PermissionError as e:
    print(e)
    print('Is file being opened?')