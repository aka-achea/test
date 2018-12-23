#!/usr/bin/python
#coding:utf-8
#Python3

from urllib.parse import quote
import re,os,json, time, wget,shutil,sys,sqlite3,coloredlogs,logging
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser


Usage = "Note: Pls clean up db first\n\
Usage:\n\
book s BOOKNAME [vv] -- Search single book\n\
book m [vv] -- Search all book from list\n\
book c [vv] -- clear DB \n\
book q a [vv] -- query all library \n\
book q s -- query best library\n\
book q l LIBRARY -- query one libary\n\
book q b BOOK -- query one book\n\
book q ll -- list all book found\n\
"

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
masterpath = 'D:\\doc\\OneDrive\\script\\'
logfile = masterpath+'book.log'
database = masterpath+'book.db'
wishlist = masterpath+'book.ini'
QueryURL = "http://ipac.library.sh.cn/ipac20/ipac.jsp?menu=search&aspect=basic_search&profile=sl&ri=&index=.TW&term="


"""Logger Setup"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create a file handler
if os.path.isfile(logfile):os.remove(logfile)
handler = logging.FileHandler(logfile)
handler.setLevel(logging.DEBUG)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the l
logger.addHandler(handler)
#l.addHandler(console_handler)

class myconsolelog():
    def __init__(self):
        coloredlogs.DEFAULT_LEVEL_STYLES= {
                                            'debug': {'color': 'magenta','bold': True},
                                            'info': {'color': 'yellow','bold': True},
                                            'warning': {'color': 'green','bold': True},
                                            'error': {'color': 'red','bold': True}
                                            }
        coloredlogs.DEFAULT_LOG_FORMAT = '%(message)s'
        coloredlogs.install(level='warning',logger=logger)
    def info(self,m): #default
        logger.warning(m)
    def debug(self,m): #vv
        logger.debug(m)
    def verbose(self,m): #v
        logger.info(m)
    def err(self,m):
        logger.error(m)
l = myconsolelog()
"""Logger Setup"""

class dec: # tracer
    def __init__(self,func):
        self.func = func
    def __call__(self,*args, **kw):
        l.verbose('>>>> Call %s()' % self.func.__name__)
        #start = datetime.datetime.now().microsecond
        result = self.func(*args, **kw)
        #elapsed = (datetime.datetime.now().microsecond - start)
        l.verbose('<<<< Exit %s()' % self.func.__name__)
        #l.verbose('++++ Function '+self.func.__name__+' spend ' +str(elapsed)
        return result

@dec
def open_link(URL):
    l.debug(URL)
    req = Request(URL,headers=headers)
    try:
        html = urlopen(req)
        time.sleep(3)
        #l.verbose(html.info())
        l.verbose(html.getcode())
    except HTTPError as e:
        l.err(e) #5xx,4xx
    return html

@dec
def modificate(text):
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

@dec
def search_link(book):
    l.debug("Transalte to Web code")
    l.debug(quote(book))
    qweb = QueryURL+quote(book)
    return qweb

"""
@dec
def create_db():
    conn = sqlite3.connect('db')
    cursor = conn.cursor()
    cursor.execute('create table inventory (SN varchar(20) primary key,\
                    book varchar(20),lib varchar(20),cat varchar(20) )' )
    cursor.close()
    conn.close()
"""

@dec
class db:
    def create(self):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('create table inventory (SN varchar(20) primary key,\
                        book varchar(20),lib varchar(20),cat varchar(20)  )' )
        cursor.close()
        conn.close()
    def lib(self,lib):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select distinct cat,  book from inventory where lib = ? order by cat' , (lib,))
        values = cursor.fetchall()
        for i in values: l.info(i)
        cursor.close()
        conn.close()
    def all(self):
        l.info(">>>>>>>显示所有图书<<<<<<<")
        l.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select lib,book,SN,cat from inventory ')
        values = cursor.fetchall()
        for i in values: l.info(i)
        cursor.close()
        conn.close()
    def sum(self):
        l.info(">>显示书种类最多的图书馆<<")
        l.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select lib,count(distinct(book)) as c from inventory group by lib having c > 1 order by c desc limit 10')
        values = cursor.fetchall()
        for i in values: l.info(i)
        cursor.close()
        conn.close()
    def book(self,book):
        l.info(">>>>显示有此书的图书馆<<<<")
        l.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select distinct lib, book,cat from inventory where book like ?', (book,))
        values = cursor.fetchall()
        for i in values: l.info(i)
        cursor.close()
        conn.close()
    def list(self):
        l.info(">>>>显示找到的图书列表<<<<")
        l.info("="*26)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('select distinct book, cat from inventory')
        values = cursor.fetchall()
        for i in values: l.info(i)
        cursor.close()
        conn.close()

@dec  #return version,num
def find_book_ver(qweb,book):
    try:
        global version,num
        html = open_link(qweb)
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
                l.err("请确认书名")
                sys.exit()
            else:
                for i in version : l.debug(i)
        else: # mediumBoldAnchor = 0 , search directly
            version = 0
    except AttributeError as e:
        print(e)
    return version,num

@dec #return other library link
def find_other_lib(v):
    try:
        global link
        #bookname = bsObj.find("a",{"class":"largeAnchor"})
        #print(bookname)
        #for i in bookname:  print(i["title"])
        #l.info(bookname["title"])
        T = 20
        while T != 0:  #find other library
            html = open_link(v)
            bsObj = BeautifulSoup(html,"html.parser")
            other = bsObj.find("input",{"value":"其它馆址"})
            l.verbose(other)
            if other :
                T = 0
            else:
                T = T - 1
                l.err("重新加载网页")
        ol = (str(other).split(" "))
        l.debug(ol)
        try:
            other_lib = modificate(ol[2][30:-2])
            l.debug("Other lib is : ")
            l.debug(other_lib)
            link.add(other_lib)
            #go to other_lib
            bsObj = BeautifulSoup(open_link(other_lib),"html.parser")
            # find more page of other lib
            lk = bsObj.find_all(href=re.compile("staffonly=$"))
            for i in lk :  link.add(i["href"])
            l.debug("Other lib list : ")
            l.debug(link)
        except IndexError as e:
            l.err("没有其他馆址")
    except AttributeError as e:
        print(e)
    #time.sleep(3)
    #find_library(bsObj)
    #print(link)
    return link

#馆址	馆藏地	索书号	状态	应还日期 馆藏类型 馆藏条码
@dec
def find_library(bsObj,book):
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
                    l.err("Duplicate: "+SN+" "+book+" "+lib)
            cursor.close()
            conn.commit()
            conn.close()
        else:
            l.info(status)

@dec
def single(book):
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
        bsObj = BeautifulSoup(open_link(lib),"html.parser")
        find_library(bsObj,book)

"""
@dec
def query():
    conn = sqlite3.connect('db')
    cursor = conn.cursor()

    l.info("="*26)

    values = cursor.fetchall()
    for i in values: l.info(i)
    l.info("="*26)

    l.info(">>显示书数量最多的图书馆<<")
    l.info("="*26)
    cursor.execute('select lib,count(SN) as c from inventory group by lib having c > 1 order by c desc ')
    values = cursor.fetchall()
    for i in values: l.info(i)
    l.info("="*26)

    l.info(">>显示书种类最多的图书馆<<")
    l.info("="*26)
    cursor.execute('select lib,count(distinct(book)) as c from inventory group by lib having c > 1 order by c desc')
    values = cursor.fetchall()
    for i in values: l.info(i)
    l.info("="*26)

    library = (values[0][0])
    l.info(library)
    cmd = 'select distinct(book) from inventory where lib = "'+ library + '"'
    #l.info(cmd)
    cursor.execute(cmd)
    values = cursor.fetchall()
    for i in values: l.info(i[0])
    l.info("="*26)

    cursor.close()
    conn.close()
"""


def main():
    if len(sys.argv) < 2:
        l.info(Usage)
        sys.exit()

    if sys.argv[-1] == 'v':
        l.verbose("Enable verbose log")

    elif sys.argv[-1] == 'vv':
        l.debug("Enable debug log")


    if sys.argv[1] == 's':
        if sys.argv[2]:
            book = sys.argv[2]
            single(book)
        else:
            l.err("Book Name pls")
    elif sys.argv[1] == 'm':
        for i in open(wishlist,'r'):
            book = i.strip()
            single(book)
    elif sys.argv[1] == 'q':
        if len(sys.argv) < 3:
            l.info(Usage)
            sys.exit()
        elif sys.argv[2] == 'a': #all book with library
            r = db()
            r.all()
        elif sys.argv[2] == 'b': #one book
            if len(sys.argv) < 4:
                l.info(Usage)
                sys.exit()
            else:
                r = db()
                r.book(sys.argv[3])
        elif sys.argv[2] == 'l': #one libary
            if len(sys.argv) < 4:
                l.info(Usage)
                sys.exit()
            else:
                r = db()
                r.lib(sys.argv[3])
        elif sys.argv[2] == 's': # summary
            r = db()
            r.sum()
        elif sys.argv[2] == 'll':
            r = db()
            r.list()
        else:
            l.info(Usage)
        l.info("="*26)
    elif sys.argv[1] == 'c':
        if os.path.isfile(database): os.remove(database)
        r = db()
        r.create()
    else:
        l.info(Usage)

if __name__=='__main__':
    main()

"""
Changelog:
2017.7.22 basic query funtion v1.0
2017.7.23 add link search, fix column issue v1.1
2017.7.24 enable logging, re-org structure v1.2
2017.7.25 add DB query v1.3
2017.7.26 fix timeout issue v1.4
2017.7.27 isolate single book query v1.5
2017.7.28 build multiple book query v1.6
2017.7.29 optimize sql query v1.7
2017.11.5 update usage comment v1.8
2018.1.4 add logger, dec v1.9
2018.1.13 fix log bug, optimize DB query v2.0
2018.1.15 add DB class v2.1

Flow chart:
search_link find_book_ver  find_other_lib  find_library     query
    |             |              |              |              |
q2 ---> qweb ---------> [version] ---> link --------------> lib ---> Result
"""
