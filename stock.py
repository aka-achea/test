#!/usr/bin/python
#coding:utf-8
#Python3

import openpyxl

s = r'D:\Profile\Desktop\wt.txt'
xl = r'J:\DOC\我的坚果云\newstock.xlsx'

#印花税：单向收取，卖出成交金额的千分之一（1‰）。 
#过户费：按成交股票的金额×0.02‰收取，单位：元。双向收取（仅上海股票收取）。
#手续费： 5元 


def readtransaction(s):
    with open(s,'r') as f:
        a = f.readlines()[3:] 
        # a = a[3:]
        t = {}
        n = 0
        for i in a:
            e = i.split() 
            if e[5] in ['买入','卖出']:
                x = -1 if e[5] == '买入' else 1
                ttime = e[0]
                stock = e[4]
                ty = e[5]
                price = round(float(e[8]),2)
                qty = float(e[9])
                tprice = round(qty*float(e[8]),2)
                guohu = tprice*0.00002 if e[-1] == '上海A股' else 0
                tax = tprice*0.001 if e[5] == '卖出' else 0
                shouxufei = 0 if stock in ['广发500','300ETF'] else 5
                total = round((x*tprice - tax - guohu - shouxufei),2)
                v = [ttime,stock,ty,price,x*qty,x*tprice,total]
                # print(v)
                t[n] = v
                n += 1
    # print(t)
    return t

def stock(xl,t):
    wb = openpyxl.load_workbook(xl)
    sheet = wb['Sheet2']
    max = sheet.max_row
    for i in range(len(t)):
        # print(t[i])                    
        for n in range(7) :
            # print(t[i][n])
            sheet.cell(row=(max+i+1),column=(n+1)).value = t[i][n] 
    wb.save(xl)

try:
    t = readtransaction(s)
    stock(xl,t)
except PermissionError as e:
    print(e)
    print('Is file being opened?')