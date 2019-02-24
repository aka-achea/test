#!/usr/bin/python3
#coding:utf-8
# tested in win

# from urllib.parse import quote
import os,sqlite3,requests,argparse
from bs4 import BeautifulSoup
# from urllib.request import urlopen,Request,HTTPError,unquote
# from html.parser import HTMLParser
# from colorama import init, Fore, Back, Style

# customized module
from mylog import mylogger,get_funcname
from openlink import op_simple

logfilelevel = 10
logfile = 'db.log'
workfolder = r"M:\MyProject\Douban"
os.chdir(workfolder)

headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml; " \
        "q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"text/html",
    "Accept-Language":"en-US,en;q= 0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
    "Content-Type":"application/x-www-form-urlencoded",
    "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 "\
        "(KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
}


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

def download(file_url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(file_url)
        # write to file
        file.write(response.content)

def modificate(text):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    #file_name = re.sub(r'\s*:\s*', u' - ', file_name)    # for FAT file system
    before = text
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
    after = text
    if before != after :
        l.debug("Before modify: "+before)
        l.debug("After modify: "+after)
    return text

def get_page_list(url):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    page_list = set()
    err = 0
    next_page = ""
    while err == 0:
        try:
            link = url + next_page
            l.debug(link)
            bsObj = BeautifulSoup(op_simple(link)[0],"html.parser") #;print(bsObj)
            next_page = bsObj.find("span",{"class":"next"}).link["href"]
            page_list.add(link)
            l.debug(next_page)
        except:
            err = 1
            link = url + next_page
            page_list.add(link)
            l.info("End of page list")
    l.debug("Page list >>>>")
    l.debug(page_list)
    return page_list

def get_event_in_page(page):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    try:
        global event_link_list
        bsObj = BeautifulSoup(op_simple(page)[0],"html.parser") #;print(bsObj)
        list_entry = bsObj.find_all("div",{"class":"pic"})
        for i in list_entry:
            event_link = i.a["href"]
            # l.debug(event_link)
            event_link_list.add(event_link)
    except AttributeError as e:
        l.warning(e)
    # l.debug("Event link in this page:")
    # l.debug(event_link_list)
    return event_link_list

def get_event_detail(event):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    global e_title,e_time,e_cost,e_place,e_link
    try:
        bsObj = BeautifulSoup(op_simple(event)[0],"html.parser") #;print(bsObj)
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
        l.debug("ID："+e_id)
        l.debug("展览："+e_title)
        l.debug("时间："+e_time)
        l.debug("地点："+e_place)
        l.debug("费用："+e_cost)
        l.debug("链接："+e_link)
        l.debug("封面："+e_cover)
        download(e_cover, modificate(e_title)+".jpg")
        conn = sqlite3.connect('douban.db')
        cursor = conn.cursor()
        try:
            cursor.execute("insert into show values (?,?,?,?,?)",(e_id,e_title,e_place,e_time,e_cost))
        except sqlite3.IntegrityError as e:
            l.debug(e)
            l.warning("Duplicate: "+e_id+" "+e_title)
        cursor.close()
        conn.commit()
        conn.close()
    except AttributeError as e:
        l.warning(e)
    l.debug("Event in this page:" + e_title)
    # l.debug(event_link)

def create_db(db):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute('create table show (ID varchar(20) primary key,\
                        title varchar(40),place varchar(50),\
                        time varchar(20),cost varchar(20) )' )
    except sqlite3.OperationalError as e:
        l.warning(e)
    cursor.close()
    conn.close()

def query_db(q):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
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
    for i in values: l.info(i)
    cursor.close()
    conn.close()

  
def ana_douban(web):
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    page_list = get_page_list(web)
    for page in page_list:
        l.debug('Analyze page: '+page)
        event_link_list = get_event_in_page(page)        
    for event in event_link_list:
        l.debug(event)
        get_event_detail(event) 

def main():
    l = mylogger(logfile,logfilelevel,get_funcname()) 
    parser = argparse.ArgumentParser(description = 'douban search tool')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s','--show',help='Search show event',choices=['n','q'])
    group.add_argument('-m','--music',help='Search music event',choices=['n','q'])
    group.add_argument('-c','--clean',help='Clean database',action='store_true')
    parser.add_argument("-v", "--verbosity",action="count",default=0,help="increase output verbosity")
    args = parser.parse_args()

    if args.show == 'n':
        l.info('Search new show event')
        create_db(db)
        ana_douban(exh)

    elif args.show == 'q':
        l.info('Query show event')
        query_db('a')

    elif args.music == 'n':
        l.info('Search new music event')
        create_db(db)
        ana_douban(mus)    
        
    elif args.music == 'q':
        l.info('Query music event')
        query_db('a')

    elif args.clean:
        pass

    else:
        parser.print_help()


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('ctrl + c')



"""
Changelog:
2019.1.21 use argparser,mylogger v1.2
2018.1.2 add music function v1.1
2017.8.22 basic query funtion for exhibition v1.0
"""
