
import os,requests
from bs4 import BeautifulSoup

from openlink import op_simple,ran_header

def main(link):
    bsObj = BeautifulSoup(op_simple(link,ran_header())[0],"html.parser") #;print(bsObj)    
    for x in bsObj.find_all('tr'):
        bt = x.td.a["href"]
        print(bt)



if __name__ == "__main__":
    link = r'http://so.hao6v.com/rj/2019-06-29/33499.html'
    main(link)