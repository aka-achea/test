#!/usr/bin/python
#coding:utf-8
#Python3

s = r'M:\GH\test\s.txt'
with open(s,'r') as f:
    a = f.readlines()
    a = a[3:]
    for i in a:
        e = i.split()
        print(e[-1])