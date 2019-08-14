#!/usr/bin/python3
#coding:utf-8
#tested in win


from urllib.error import URLError
# from urllib.parse import quote
import re,os,json, time, shutil,sys,sqlite3,argparse,random
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
from prettytable import PrettyTable , from_db_cursor
import requests

# customized module
from mylog import mylogger,get_funcname
from openlink import op_requests,ran_header
# from mytool import mywait


ignorelist = ['闭馆',\
            '南汇','闵行','嘉定','松江','奉贤','崇明','青浦','金山']
blacklist = ['徐汇华泾镇','中心馆分拣处',\
            '浦东洋泾','浦东新区新川沙','浦东沪东新村','杨浦长白新村','杨浦四平']
whitelist = ['普陀分馆','黄浦分馆','静安区图书馆(新闸路)','普陀宜川']

link = set() #link to library list of different pages
masterpath = 'E:\\UT\\'
logfile = masterpath+'library.log'
database = masterpath+'library.db'
wishlist = masterpath+'library.ini'
# basicquery = "http://ipac.library.sh.cn/ipac20/ipac.jsp?menu=search&aspect=basic_search&profile=sl&ri=&index=.TW&term="
queryapi = 'http://ipac.library.sh.cn/ipac20/ipac.jsp'

"""
TW = 题名
AW = 著者
SW = 主题
SE = 丛书名
PW = 出版者
"""

# class dec: # tracer
#     def __init__(self,func):
#         self.func = func
#     def __call__(self,*args, **kw):
#         # l.debug('>>>> Call %s()' % self.func.__name__)
#         #start = datetime.datetime.now().microsecond
#         result = self.func(*args, **kw)
#         #elapsed = (datetime.datetime.now().microsecond - start)
#         # l.debug('<<<< Exit %s()' % self.func.__name__)
#         #l.debug('++++ Function '+self.func.__name__+' spend ' +str(elapsed)
#         return result


# def modificate(text):
#     ml = mylogger(logfile,get_funcname()) 
#     #file_name = re.sub(r'\s*:\s*', u' - ', file_name)    # for FAT file system
#     text = str(text)
#     before = text
#     text = text.replace('&amp;', u'&')
#     text = text.strip()
#     #file_name = file_name.replace('$', '\\$')    # for command, see issue #7
#     after = text
#     if before != after :
#         ml.debug("Before modify >>>> "+before)
#         ml.debug("After modify >>>> "+after)
#     return text

def wantedlib(lib): 
    '''Filter library with ignore/black/white list'''
    #  map(lambda x:re.search(x,lib),ignorelist) :
    for s in ignorelist:
        if re.findall(s,lib):
            return False
    return False if lib in blacklist else True


class db():
    def create(self):
        ml = mylogger(logfile,get_funcname()) 
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cmd = 'create table inventory (SN varchar(20) primary key,\
                        book varchar(20),lib varchar(20),cat varchar(20)  )'
        ml.debug(cmd)
        cursor.execute(cmd)
        cursor.close()
        conn.close()

    def lib(self,lib):
        ml = mylogger(logfile,get_funcname())        
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        # cmd = 
        # ml.debug(cmd)
        cursor.execute('select distinct book as 图书, cat as 索书号 from inventory \
                        where lib = ? order by book' , (lib,))
        v = from_db_cursor(cursor)
        cursor.close()
        conn.close()
        return v

    def all(self):
        ml = mylogger(logfile,get_funcname())          
        ml.info(">>>>>>>显示所有图书<<<<<<<")
        ml.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select lib as 图书馆,book as 书,SN,cat as 索书号 from inventory')
        v = from_db_cursor(cursor)
        cursor.close()
        conn.close()
        return v

    def sum(self):
        ml = mylogger(logfile,get_funcname())          
        ml.info(">>显示书种类最多的图书馆<<")
        ml.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select lib as 图书馆,count(distinct(book)) as 本 from inventory \
                        group by 图书馆 having 本 > 1 order by 本 desc limit 10')
        v = from_db_cursor(cursor)
        cursor.close()
        conn.close()
        return v

    def book(self,book):
        ml = mylogger(logfile,get_funcname())          
        ml.info(">>>>显示有此书的图书馆<<<<")
        ml.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select distinct lib as 图书馆, book as 书,cat as 索书号 from inventory \
                        where book like ?', (book,))
        v = from_db_cursor(cursor)
        cursor.close()
        conn.close()
        return v

    def listbook(self):
        ml = mylogger(logfile,get_funcname())          
        ml.info(">>>>显示找到的图书列表<<<<")
        ml.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select distinct book, cat from inventory')
        values = cursor.fetchall()
        for i in values: ml.info(i)
        cursor.close()
        conn.close()

# @dec  #return version,verlink
def find_book_ver(queryapi,book,author=''):
    '''Get book of different version'''
    ml = mylogger(logfile,get_funcname())  
    para = [('menu','search'),
            ('index','.TW'),
            ('term',book),
            ('index','.AW'),
            ('term',author)]
    ml.debug(para)    
    try:
        vdict = {} # version dictionary
        html = op_requests(url=queryapi,para=para,header=ran_header())
        ml.debug(html.url)
        bsObj = BeautifulSoup(html.content,"html.parser")        
        if bsObj.find_all(string=re.compile("对不起")): # not find any book
            ml.error("对不起, 不能找到任何命中书目")
            return None
        else:
            vbook = bsObj.find_all("a",{"class":"mediumBoldAnchor"})
            if vbook: 
            # mediumBoldAnchor >= 1 , different version find, only scan 1st page
                ml.debug('Find book version below')
                for v in vbook:
                    ml.debug(v)
                    n = v
                    for i in range(7): n = n.parent                  
                    # ml.debug(n)
                    n = n.previous_sibling.text.strip()
                    # ml.debug(n)  # sample n :  "1."
                    bookname = str(v).split('<')[1].split('>')[-1].strip()
                    # ml.info(bookname)
                    if bookname == book:
                        ml.debug(n+bookname)
                        ml.debug(v["href"])
                        vdict[n] = v["href"]
                    else:
                        ml.warning(n+bookname+'--> not match')
                        if input("Sure (Y)? >>>") in ['y','Y']:
                            ml.info('Add to search candidate')
                            vdict[n] = v["href"]
                        else:
                            ml.warning('ignored')
                if vdict == {}: #there is book, but no name match
                    if input("都不符合，翻页？(Y)")  in ['y','Y']:
                        nextpage = bsObj.find_all(text="下页")[0].parent
                        np = nextpage.attrs['href']
                        print('oooops')
                    else:
                        return None  # all none
            else: # mediumBoldAnchor = 0 , search directly
                ml.debug("没其他版本，直接搜!")
                vdict['0.'] = html.url  
    except AttributeError as e:
        print(e)
    ml.debug(vdict)
    return vdict

# @dec #return other library link
def find_other_lib(weblink):
    '''Get link of other library'''
    ml = mylogger(logfile,get_funcname())      
    ml.debug(weblink)
    global link
    try:
        #find other library tag 
        bsObj = BeautifulSoup(op_requests(weblink,header=ran_header()).content,"html.parser")
        other = bsObj.find("input",{"value":"其它馆址"})
        if other :
            ml.debug(other)
            ol = (str(other).split(" "))
            ml.debug(ol)
            # other_lib = modificate(ol[2][30:-2])
            other_lib = ol[2][30:-2].replace('&amp;', u'&').strip()
            ml.debug(f"Other lib is -->  {other_lib}")
            link.add(other_lib)
            #go to other_lib
            bsObj = BeautifulSoup(op_requests(other_lib,header=ran_header()).content,"html.parser")
            more_other_lib(bsObj)
            # except IndexError as e:
            #     ml.error(e)
        else:
            more_other_lib(bsObj)
            link.add(weblink)

    except AttributeError as e:
        print(e)
    ml.debug(f"Other lib list --> {link}")


def more_other_lib(bsObj):  
    global link
    lk = bsObj.find_all(href=re.compile("staffonly=$"))
    if lk:
        for i in lk : link.add(i["href"]) 


#馆址	馆藏地	索书号	状态	应还日期 馆藏类型 馆藏条码
# @dec
def find_library(liblink,book):
    '''Find libary details'''
    ml = mylogger(logfile,get_funcname())  
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    bsObj = BeautifulSoup(op_requests(liblink,header=ran_header()).content,"html.parser")
    for i in bsObj.find_all("tr",{"height":"15"}):
        ml.debug('='*10)
        library = i.td
        lib = library.text
        ml.debug("馆址:"+lib)  
        if wantedlib(lib):
            room = library.next_sibling
            ml.debug("馆藏地:"+room.text)
            catalog = room.next_sibling
            cat = catalog.text
            ml.debug("索引号:"+cat)
            status = catalog.next_sibling
            if status.text == "归还":      
                if bsObj.find(title="应还日期") :
                    #print("find 应还日期")
                    #index = room.next_sibling
                    #print(index.text)
                    btype = status.next_sibling.next_sibling
                else:
                    btype = status.next_sibling
                ml.debug("馆藏类型:"+btype.text)        
                if btype.text == "普通外借资料":
                    SN = btype.next_sibling.text
                    ml.debug("馆藏条码:"+SN)
                    try:
                        cursor.execute("insert into inventory values (?,?,?,?)", (SN,book,lib,cat))
                    except sqlite3.IntegrityError as e:
                        ml.debug(e)
                        ml.error(f"Duplicate: {SN} {book} {lib}")
            else:
                ml.debug(lib+status.text)
        else:
            ml.debug('Not recommaned library')

    cursor.close()
    conn.commit()
    conn.close()

# @dec
def single(book,author=''):
    '''Search single book'''
    ml = mylogger(logfile,get_funcname())  
    ml.info("搜寻图书："+book)
    if author:
        ml.info("作者："+author)
    vdict = find_book_ver(queryapi,book,author)
    if vdict:
        ml.info("Scan version")
        for v in vdict:
            ml.info(v + book)
            find_other_lib(vdict[v])
        ml.debug("all link find below")
        for liblink in link:
            ml.debug(liblink)
            find_library(liblink,book)
    

def main():
    ml = mylogger(logfile,get_funcname())  
    parser = argparse.ArgumentParser(description = 'Library search tool')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m','--multiple',help='Search multiple books',action='store_true')
    group.add_argument('-c','--clean',help='Clean database',action='store_true')
    group.add_argument('-q',help='Query all|libary|single book|best',choices=['a','l','s','b'])
    parser.add_argument('-b','--book',help='Search book ')
    parser.add_argument('-a','--author',help='Search author')
    args = parser.parse_args()

    if args.book:
        book = args.book
        single(book,args.author if args.author else '')
      
    elif args.multiple:
        ml.info('Search multiple books')
        with open(wishlist, 'r') as w:
            for i in w:
                book = i.strip()
                single(book)
    
    elif args.clean:
        ml.info('Clean up database')
        if os.path.isfile(database): os.remove(database)
        r = db()
        r.create()

    elif args.q == 'a':
        ml.info('all find')
        r = db()
        v = r.all()
        ml.info(v.get_string(fields = ['图书馆','书','SN','索书号']))

    elif args.q == 's':
        book = input('>>')
        ml.info('Search : '+book)
        r = db()
        v = r.book(book)
        ml.info(v.get_string(fields = ['图书馆','索书号']))

    elif args.q == 'l':
        lib = input('>>')
        ml.info(lib)
        r = db()
        v = r.lib(lib)
        ml.info(v.get_string(fields = ['图书','索书号']))

    elif args.q == 'b':
        # print('best')
        r = db()
        v = r.sum()
        ml.info(v.get_string(fields = ['图书馆','本']))

    else:
        parser.print_help()


if __name__=='__main__':
    if os.path.exists(logfile):
        os.remove(logfile)
    try:
        main()
    except KeyboardInterrupt:
        print('ctrl + c')



"""
Changelog:
2019.3.28 fix other lib bug v2.7
2019.3.13 add filter lib function v2.6
2019.3.11 Add author search key v2.5
2019.1.22 optimize argparse v2.4
2018.12.25 add keyinterrupt v2.3
2018.12.24 use argparse,prettytable v2.2
2018.1.15 add DB class v2.1
2018.1.13 fix log bug, optimize DB query v2.0
2018.1.4 add logger, dec v1.9
2017.11.5 update usage comment v1.8
2017.7.29 optimize sql query v1.7
2017.7.28 build multiple book query v1.6
2017.7.27 isolate single book query v1.5
2017.7.26 fix timeout issue v1.4
2017.7.25 add DB query v1.3
2017.7.24 enable logging, re-org structure v1.2
2017.7.23 add link search, fix column issue v1.1
2017.7.22 basic query funtion v1.0
"""