
import os,requests
from bs4 import BeautifulSoup

from openlink import op_simple,ran_header

def main(link):
    bsObj = BeautifulSoup(op_simple(link,ran_header())[0],"html.parser") #;print(bsObj)    
    for x in bsObj.find_all('tr'):
        try:
            bt = x.td.a["href"]
            print(bt)
        except TypeError:
            pass



if __name__ == "__main__":
    link = r'http://www.6vhao.com/rj/2019-08-02/33714.html'
    main(link)