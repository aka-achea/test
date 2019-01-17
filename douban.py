#!/usr/bin/python
#coding:utf-8
#Python3

from urllib.parse import quote
import re,os,json, time, wget,shutil,sys,sqlite3,requests
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,HTTPError,unquote
from html.parser import HTMLParser
from colorama import init, Fore, Back, Style

headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml; " \
        "q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"text/html",
    "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
    "Content-Type":"application/x-www-form-urlencoded",
    "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 "\
        "(KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
}
loglevel = 0

exh = "https://shanghai.douban.com/events/week-exhibition"
mus = 'https://shanghai.douban.com/events/week-music'

db = 'douban.db'
e_title = ""
e_time = ""
e_place = ""
e_cost = ""
e_link = ""
e_cover = ""
event_link_list = set()
workfolder = "D:\douban"
os.chdir(workfolder)

"""Color Theme"""
init(autoreset=True)
class Colored(object):
    #  前景色:红色  背景色:默认
    def warning(self, s):
        s = str(s)
        return Fore.RED + Style.BRIGHT + s + Fore.RESET
    #  前景色:绿色  背景色:默认
    def info(self, s):
        s = str(s)
        return Fore.GREEN + Style.BRIGHT + s + Fore.RESET
    #  前景色:黄色  背景色:默认
    def verbose(self, s):
        s = str(s)
        return Fore.YELLOW + Style.BRIGHT + s + Fore.RESET
    def debug(self, s):
        s = str(s)
        return Fore.YELLOW + Style.BRIGHT + Back.CYAN + s + Fore.RESET + Back.RESET
color = Colored()
"""Color Theme"""

def open_link(URL):
    if loglevel == 1 or loglevel == 2:
        print(color.verbose(">>>>Enter open_link()"))
    if loglevel == 2:
        print(color.debug(URL))
    req = Request(URL,headers=headers)
    try:
        html = urlopen(req)
        #time.sleep(3)
        #print(color.verbose(html.info()))
        if loglevel == 1 or loglevel == 2:
            print(color.verbose(html.getcode()))
    except HTTPError as e:
        print(color.warning(e)) #5xx,4xx
    if loglevel == 1 or loglevel == 2:
        print(color.verbose("<<<<Exit open_link()"))
    return html

def download(file_url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(file_url)
        # write to file
        file.write(response.content)

def modificate(text):
    #file_name = re.sub(r'\s*:\s*', u' - ', file_name)    # for FAT file system
    if loglevel == 1 or loglevel == 2: before = text
    text = text.replace('?', u'？')      # for FAT file system
    text = text.replace('/', u'／')
    text = text.replace('|', '')
    text = text.replace(':', u'∶')    # for FAT file system
    text = text.replace('*', u'×')
    text = text.replace('\n', '')
    #text = text.replace('&amp;', u'&')
    #text = text.replace('&#039;', u'\'')
    #text = text.replace('\'', u'＇')
    text = text.replace('\\', u'＼')
    text = text.replace('"', u'＂')
    #text = text.replace('\'', u'＇')
    text = text.strip()
    #file_name = file_name.replace('$', '\\$')    # for command, see issue #7
    if loglevel == 1 or loglevel == 2:
        after = text
        if before == after :
            pass
        else:
            print(color.verbose("Before modify: "+before))
            print(color.verbose("After modify: "+after))
    return text


def get_page_list(url):
    if loglevel == 1 or loglevel == 2 :
        print(color.verbose(">>>>Entering get_page_list()"))
        print(color.verbose("Scan page:"))
        print(color.verbose(url))
    page_list = set()
    err = 0
    next_page = ""
    while err == 0:
        try:
            link = url + next_page
            if loglevel == 1 or loglevel == 2 :print(link)
            bsObj = BeautifulSoup(open_link(link),"html.parser") #;print(bsObj)
            next_page = bsObj.find("span",{"class":"next"}).link["href"]
            page_list.add(link)
            if loglevel == 2 :print(next_page)
        except:
            err = 1
            link = url + next_page
            page_list.add(link)
            print(color.info("End of page list"))
    if loglevel == 1 or loglevel == 2:
        print(color.verbose("Page list:"))
        for i in page_list: print(color.verbose(i))
        print(color.verbose("<<<<Exit get_page_list()"))
    return page_list

def get_event_in_page(page):
    if loglevel == 1 or loglevel == 2 :
        print(color.verbose(">>>>Entering get_event_in_page()"))
        print(color.verbose("Analyzing event link from page:"))
        print(color.verbose(page))
    try:
        global event_link_list
        bsObj = BeautifulSoup(open_link(page),"html.parser") #;print(bsObj)
        list_entry = bsObj.find_all("div",{"class":"pic"})
        for l in list_entry:
            event = l.a["href"]
            event_link_list.add(event)
    except AttributeError as e:
        print(e)
    if loglevel == 1 or loglevel == 2:
        print(color.verbose("Event in this page:"))
        for i in event_link_list: print(color.verbose(i))
        print(color.verbose("<<<<Exit get_event_in_page()"))
    return event_link_list

def get_event_detail(event):
    if loglevel == 1 or loglevel == 2 :
        print(color.verbose(">>>>Entering get_event_detail()"))
        print(color.verbose("Analyzing event detail from page:"))
        print(color.verbose(event))
    global e_title,e_time,e_cost,e_place,e_link
    try:
        bsObj = BeautifulSoup(open_link(event),"html.parser") #;print(bsObj)
        e_link = event
        e_title = bsObj.find("h1",{"itemprop":"summary"}).text.strip()
        e_title = e_title.replace('官方售票','').strip()
        e_title = e_title.replace('即将开始','').strip()
        e_time = bsObj.find("li",{"class":"calendar-str-item"}).text.strip()
        #location = bsObj.find("span",{"itemprop":"locality"}).text.strip()
        e_place = bsObj.find("span",{"itemprop":"street-address"}).text.strip()
        #e_place = location + street
        e_cost = bsObj.find("span",{"itemprop":"ticketAggregate"}).text[3:].strip()
        e_cover = bsObj.find("div",{"class":"poster"}).a["href"]
        e_id = e_link.split('/')[-2]
        if loglevel == 1 or loglevel == 2 :
            print(color.verbose("ID："+e_id))
            print(color.verbose("展览："+e_title))
            print(color.verbose("时间："+e_time))
            print(color.verbose("地点："+e_place))
            print(color.verbose("费用："+e_cost))
            print(color.verbose("链接："+e_link))
            print(color.verbose("封面："+e_cover))

        download(e_cover, modificate(e_title)+".jpg")
        conn = sqlite3.connect('douban.db')
        cursor = conn.cursor()
        try:
            cursor.execute("insert into show values (?,?,?,?,?)",(e_id,e_title,e_place,e_time,e_cost))
        except sqlite3.IntegrityError as e:
            if loglevel == 1 or loglevel == 2 : print(color.verbose(e))
            print(color.warning("Duplicate: "+e_id+" "+e_title))
        cursor.close()
        conn.commit()
        conn.close()

    except AttributeError as e:
        print(e)
    if loglevel == 1 or loglevel == 2:
        print(color.verbose("Event in this page:"))
        #for i in event_link: print(color.verbose(i))
        print(color.verbose("<<<<Exit get_event_detail()"))

def create_db(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute('create table show (ID varchar(20) primary key,\
                        title varchar(40),place varchar(50),\
                        time varchar(20),cost varchar(20) )' )
    except sqlite3.OperationalError as e:
        print(color.warning(e))
    cursor.close()
    conn.close()

def query_db(q):
    if loglevel == 1 or loglevel == 2:
        print(color.verbose(">>>>Enter query_db()"))
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    if q == 's':
        t = input("Show name >>>>")
        cursor.execute('select ID,time,place,cost  from show where title = ?',(t,))
    elif q == 'a':
        cursor.execute('select ID,title from show')
    elif q == 'id':
        cursor.execute('select ID,title,time,place,cost from show')


    values = cursor.fetchall()
    for i in values: print(i)
    cursor.close()
    conn.close()
    if loglevel == 1 or loglevel == 2:
        print(color.verbose("<<<<Exit query( )"))

if sys.argv[-1] == 'v':
    print(color.verbose("Enable verbose log"))
    loglevel = 1
elif sys.argv[-1] == 'vv':
    print(color.verbose("Enable debug log"))
    loglevel = 2


if sys.argv[1] == 'show':
    if sys.argv[2] == 'u':
        create_db(db)
        page_list = get_page_list(exh)
        for page in page_list:
            event_link = get_event_in_page(page)
        for event in event_link:
            #print(event)
            get_event_detail(event)
    elif sys.argv[2] == 'q':
        if sys.argv[3] == 'a':
            query_db('a')
        elif sys.argv[3] == 's':
            query_db('s')
    else:
        print(color.warning("SHOW WHAT"))
elif sys.argv[1] == 'music':
    if sys.argv[2] == 'u':
        create_db(db)
        page_list = get_page_list(mus)
        for page in page_list:
            event_link = get_event_in_page(page)
        for event in event_link:
            #print(event)
            get_event_detail(event)
    elif sys.argv[2] == 'q':
        if sys.argv[3] == 'a':
            query_db('a')
        elif sys.argv[3] == 's':
            query_db('s')
    else:
        print(color.warning("SHOW WHAT"))
else:
    pass

"""
Changelog:
2017.8.22 basic query funtion for exhibition v1.0
2018.1.2 add music function v1.1
"""
