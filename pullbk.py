#!/usr/bin/python3
#coding:utf-8

__version__ = 20210301

from bs4 import BeautifulSoup as bs
from openlink import op_simple,ran_header

header = ran_header()

def analyze_page(url):
    bsobj = bs(op_simple(url,header)[0],'html.parser')
    repo = bsobj.find_all('span',{'class':'repository-name'}).text
    print(repo)


if __name__ == "__main__":
    url = ''
    analyze_page(url)