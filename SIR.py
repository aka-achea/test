#!/usr/bin/python
#coding:utf-8

import time,os
from docx import Document

SIR = 'E:\\UT\\SIR Blade.docx'
doc = Document(SIR)

# name = 'ggggg'
# SN =  'sgeserger'
# site = 'Singapore'
# loc = 'IDX2/A24/GSHFRB024A2/Bay79'
d = time.strftime('%Y-%m-%d',time.localtime(time.time()))

name = input('Server Name: ')
SN = input('Serial Number: ')
site = input('Default Shanghai  ')
if site == '': site = 'Shanghai'
loc = input('eg:IDX2/A24/GSHFRB024A2/Bay7  ')


"""
Serial Number:          6CU830G700
Site:   SHANGHAI
Area/Building/Room:
IDX2/A24/GSHFRB024A2/Bay9
"""

tables = doc.tables

t0 = tables[0]
cName = t0.cell(0,0)
cName.text = 'System Name:      '+name
cSN = t0.cell(0,1)
cSN.text = 'Serial Number:          '+SN
cSite = t0.cell(1,0)
cSite.text = 'Site:   '+site
cloc = t0.cell(1,1)
cloc.text = 'Area/Building/Room:\n'+loc

t1 = tables[3]
cdate = t1.cell(1,1)
cdate.text = d

try:
    doc.save(SIR)
except PermissionError as e:
    print(e)
    print('Is file being opened?')

os.startfile(SIR,'print')