#!/usr/bin/python
#coding:utf-8
#Python3

from urllib.error import URLError
from urllib.parse import quote
import re,os,json, time, shutil,sys,sqlite3,coloredlogs,logging,argparse,random
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
from prettytable import PrettyTable , from_db_cursor


headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml; " \
        "q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"text/html",
    "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
    "Content-Type":"application/x-www-form-urlencoded",
    "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 "\
        "(KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
}

plink = set() #link to different pages of version list
num = [] #link to book version number
version = [] #link to different book version
link = set() #link to library list of different pages
D = {}
fail = []
masterpath = 'E:\\UT\\'
logfilelevel = 10
logfile = masterpath+'book.log'
database = masterpath+'book.db'
wishlist = masterpath+'book.ini'
blacklist = masterpath+'blacklistlib.txt'
QueryURL = "http://ipac.library.sh.cn/ipac20/ipac.jsp?menu=search&aspect=basic_search&profile=sl&ri=&index=.TW&term="


class mylogger(): # Version: 20181222
    def __init__(self,logfile,logfilelevel,funcname):
        self.funcname = funcname
        logging.basicConfig(level=logfilelevel,filename=logfile,filemode='w',
                            datefmt='%m-%d %H:%M:%S',
                            format='%(asctime)s <%(name)s>[%(levelname)s] %(message)s')
        self.logger = logging.getLogger(funcname)
        coloredlogs.DEFAULT_LEVEL_STYLES= {
                                        #'debug': {'color': 'magenta','bold': True},
                                        'info': {'color': 'green','bold': True},
                                        'warning': {'color': 'yellow','bold': True},
                                        'error': {'color': 'red','bold': True},
                                        'critical': {'color': 'magenta','bold': True}
                                            }
        coloredlogs.DEFAULT_LOG_FORMAT = '%(message)s'
        coloredlogs.install(level='info',logger=self.logger)  
    def debug(self,msg):
        self.logger.debug(msg)
    def info(self,msg):
        self.logger.info(msg)
    def warning(self,msg):      
        self.logger.warning(msg)
    def error(self,msg):      
        self.logger.error(msg)
    def critical(self,msg):  
        self.logger.critical(msg)
    def verbose(self,msg):     
        self.logger.debug(msg)


# class dec: # tracer
#     def __init__(self,func):
#         self.func = func
#     def __call__(self,*args, **kw):
#         # l.verbose('>>>> Call %s()' % self.func.__name__)
#         #start = datetime.datetime.now().microsecond
#         result = self.func(*args, **kw)
#         #elapsed = (datetime.datetime.now().microsecond - start)
#         # l.verbose('<<<< Exit %s()' % self.func.__name__)
#         #l.verbose('++++ Function '+self.func.__name__+' spend ' +str(elapsed)
#         return result

# def open_link(URL):
#     funcname = __name__
#     l = mylogger(logfile,logfilelevel,funcname)
#     l.debug(URL)
#     req = Request(URL,headers=headers)
#     try:
#         html = urlopen(req)
#         time.sleep(3)
#         #l.verbose(html.info())
#         l.verbose(html.getcode())
#     except HTTPError as e:
#         l.error(e) #5xx,4xx
#     return html

def op_simple(URL): # use built-in
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml; " \
            "q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"text/html",
        "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
        "Content-Type":"application/x-www-form-urlencoded",
        # "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 "\
        #     "(KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
    req = Request(URL,headers=headers)
    try:
        html = urlopen(req)
        time.sleep(random.uniform(2,4))
        #l.verbose(html.info())
        #l.debug(html.getcode())
        status = html.getcode()
    except HTTPError as e:
        status = e #5xx,4xx
        html = 0
    except URLError as e:
        print('Host no response, try again')
        time.sleep(30)
        try:
            html = urlopen(req)
        except:
            status = e 
            html = 0
    return html,status #return array object

def modificate(text):
    funcname = __name__
    l = mylogger(logfile,logfilelevel,funcname)    
    #file_name = re.sub(r'\s*:\s*', u' - ', file_name)    # for FAT file system
    text = str(text)
    before = text
    text = text.replace('&amp;', u'&')
    text = text.strip()
    #file_name = file_name.replace('$', '\\$')    # for command, see issue #7
    after = text
    if before == after :
        pass
    else:
        l.debug("Before modify >>> "+before)
        l.debug("After modify >>> "+after)
    return text

def search_link(book):
    funcname = __name__
    l = mylogger(logfile,logfilelevel,funcname)     
    l.debug("Transalte to Web code")
    l.debug(quote(book))
    qweb = QueryURL+quote(book)
    return qweb

class db():
    def create(self):
        funcname = __name__
        l = mylogger(logfile,logfilelevel,funcname) 
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('create table inventory (SN varchar(20) primary key,\
                        book varchar(20),lib varchar(20),cat varchar(20)  )' )
        cursor.close()
        conn.close()

    def lib(self,lib):
        funcname = __name__
        l = mylogger(logfile,logfilelevel,funcname)         
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select distinct book as 图书, cat as 索书号 from inventory \
                        where lib = ? order by book' , (lib,))
        v = from_db_cursor(cursor)
        cursor.close()
        conn.close()
        return v

    def all(self):
        funcname = __name__
        l = mylogger(logfile,logfilelevel,funcname)         
        l.info(">>>>>>>显示所有图书<<<<<<<")
        l.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select lib as 图书馆,book as 书,SN,cat as 索书号 from inventory ')
        v = from_db_cursor(cursor)
        cursor.close()
        conn.close()
        return v

    def sum(self):
        funcname = __name__
        l = mylogger(logfile,logfilelevel,funcname)         
        l.info(">>显示书种类最多的图书馆<<")
        l.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select lib as 图书馆,count(distinct(book)) as 本 from inventory \
                        group by 图书馆 having 本 > 1 order by 本 desc limit 10')
        v = from_db_cursor(cursor)
        cursor.close()
        conn.close()
        return v

    def book(self,book):
        funcname = __name__
        l = mylogger(logfile,logfilelevel,funcname)         
        l.info(">>>>显示有此书的图书馆<<<<")
        l.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select distinct lib as 图书馆, book as 书,cat as 索书号 from inventory \
                        where book like ?', (book,))
        v = from_db_cursor(cursor)
        cursor.close()
        conn.close()
        return v

    def listbook(self):
        funcname = __name__
        l = mylogger(logfile,logfilelevel,funcname)         
        l.info(">>>>显示找到的图书列表<<<<")
        l.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select distinct book, cat from inventory')
        values = cursor.fetchall()
        for i in values: l.info(i)
        cursor.close()
        conn.close()

# @dec  #return version,num
def find_book_ver(qweb,book):
    funcname = __name__
    l = mylogger(logfile,logfilelevel,funcname) 
    try:
        global version,num
        html = op_simple(qweb)[0]
        bsObj = BeautifulSoup(html,"html.parser")
        nobook = bsObj.find_all(string=re.compile("对不起"))
        if nobook: # not find any book
            l.err("对不起, 不能找到任何命中书目")
            pass
            #sys.exit()
        else:
            l.debug("Find some book")
        vbook = bsObj.find_all("a",{"class":"mediumBoldAnchor"})
        #l.info(vbook)
        if vbook: # mediumBoldAnchor >= 1 , different version find, only scan 1st page
            for v in vbook:
                #l.debug(v)
                bookname = str(v).split('<')[1].split('>')[-1].strip()
                l.info(bookname)
                if bookname == book:
                    n = v
                    for i in range(7):
                        n = n.parent
                        l.debug(n)
                    n = n.previous_sibling.text.strip()
                    l.debug(n)
                    l.verbose(n+bookname)
                    num.append(n)
                    l.verbose(v["href"])
                    version.append(v["href"])
                else:
                    l.info(bookname)
                    #sys.exit()
                    pass
            if version == []: #there is book, but name doesn't match
                l.error("请确认书名")
                sys.exit()
            else:
                for i in version : l.debug(i)
        else: # mediumBoldAnchor = 0 , search directly
            version = 0
    except AttributeError as e:
        print(e)
    return version,num

# @dec #return other library link
def find_other_lib(v):
    funcname = __name__
    l = mylogger(logfile,logfilelevel,funcname)     
    try:
        global link
        #bookname = bsObj.find("a",{"class":"largeAnchor"})
        #print(bookname)
        #for i in bookname:  print(i["title"])
        #l.info(bookname["title"])
        T = 20
        while T != 0:  #find other library
            html = op_simple(v)[0]
            bsObj = BeautifulSoup(html,"html.parser")
            other = bsObj.find("input",{"value":"其它馆址"})
            l.verbose(other)
            if other :
                T = 0
            else:
                T = T - 1
                l.error("重新加载网页")
        ol = (str(other).split(" "))
        l.debug(ol)
        try:
            other_lib = modificate(ol[2][30:-2])
            l.debug("Other lib is : ")
            l.debug(other_lib)
            link.add(other_lib)
            #go to other_lib
            bsObj = BeautifulSoup(op_simple(other_lib)[0],"html.parser")
            # find more page of other lib
            lk = bsObj.find_all(href=re.compile("staffonly=$"))
            for i in lk :  link.add(i["href"])
            l.debug("Other lib list : ")
            l.debug(link)
        except IndexError as e:
            l.error("没有其他馆址")
    except AttributeError as e:
        print(e)
    #time.sleep(3)
    #find_library(bsObj)
    #print(link)
    return link

#馆址	馆藏地	索书号	状态	应还日期 馆藏类型 馆藏条码
# @dec
def find_library(bsObj,book):
    funcname = __name__
    l = mylogger(logfile,logfilelevel,funcname) 
    global D, fail
    for i in bsObj.find_all("tr",{"height":"15"}):
        status = i.td.next_sibling.next_sibling.next_sibling.text
        l.verbose("="*10)
        if status == "归还":
            library = i.td
            l.verbose("馆址:"+library.text)
            lib = library.text
            room = library.next_sibling
            l.verbose("馆藏地:"+room.text)
            catalog = room.next_sibling
            l.verbose("索引号:"+catalog.text)
            cat = catalog.text
            if bsObj.find(title="应还日期") :
                #print("find 应还日期")
                #index = room.next_sibling
                #print(index.text)
                btype = room.next_sibling.next_sibling.next_sibling.next_sibling
            else:
                btype = room.next_sibling.next_sibling.next_sibling
            bt = btype.text
            l.verbose("馆藏类型:"+btype.text)
            label = btype.next_sibling
            l.verbose("馆藏条码:"+label.text)
            SN = label.text
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            if btype.text == "普通外借资料":
                try:
                    cursor.execute("insert into inventory values (?,?,?,?)", (SN,book,lib,cat))
                except sqlite3.IntegrityError as e:
                    l.verbose(e)
                    l.error("Duplicate: "+SN+" "+book+" "+lib)
            cursor.close()
            conn.commit()
            conn.close()
        else:
            l.info(status)

# @dec
def single(book):
    funcname = __name__
    l = mylogger(logfile,logfilelevel,funcname) 
    l.info("搜寻图书："+book)
    #l.info("Link>> " + link)
    qweb = search_link(book)
    version,num = find_book_ver(qweb,book)
    if version == 0:
        l.debug("没其他版本，直接搜!")
        link = find_other_lib(qweb)
    else:
        D = {num[i]:version[i] for i in range(len(version))}
        l.debug(D)
        if version:
            l.debug("Scan version")
            for v in D:
                l.info(v + book)
                link = find_other_lib(D[v])
    l.debug("all link find below")
    for lib in link:
        l.debug(lib)
        bsObj = BeautifulSoup(op_simple(lib)[0],"html.parser")
        find_library(bsObj,book)

def main():
    funcname = __name__
    l = mylogger(logfile,logfilelevel,funcname) 
    parser = argparse.ArgumentParser(description = 'Library search tool')
    parser.add_argument('-s','--single',help='Search single book ')
    parser.add_argument('-m','--multiple',help='Search multiple books',action='store_true')
    parser.add_argument('-c','--clean',help='Clean database',action='store_true')
    parser.add_argument('-qa',help='Query all find',action='store_true')
    parser.add_argument('-ql',help='Query one library')
    parser.add_argument('-qs',help='Query one book')
    parser.add_argument('-qb',help='Query best library',action='store_true')
    args = parser.parse_args()

    if args.single:
        book = args.single
        single(book)

    elif args.multiple == True:
        l.info('Search multiple books')
        with open(wishlist, 'r') as l:
            for i in l:
                book = i.strip()
                single(book)
    
    elif args.clean == True:
        l.info('Clean up database')
        if os.path.isfile(database): os.remove(database)
        r = db()
        r.create()

    elif args.qa == True:
        l.info('all find')
        r = db()
        v = r.all()
        l.info(v.get_string(fields = ['图书馆','书','SN','索书号']))

    elif args.qs:
        book = args.qs
        l.info('Search : '+book)
        r = db()
        v = r.book(book)
        l.info(v.get_string(fields = ['图书馆','索书号']))

    elif args.ql:
        lib = args.ql
        print(lib)
        r = db()
        v = r.lib(lib)
        l.info(v.get_string(fields = ['图书','索书号']))

    elif args.qb == True:
        # print('best')
        r = db()
        v = r.sum()
        l.info(v.get_string(fields = ['图书馆','本']))

    else:
        parser.print_help()


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('ctrl + c')

"""
Changelog:
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


Flow chart:
search_link find_book_ver  find_other_lib  find_library       query
    |             |               |              |              |
q2 ---> qweb ---------> [version] ---> link ------------> lib ---> Result
"""
