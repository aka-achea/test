import os,sys

# wkdir = r'E:\jpg'
# MAX_WORKERS = 10 
# bfile = os.path.join(wkdir,'blacklist.txt')
# flist = os.path.join(wkdir,'faillist.txt')

# def blacklist(bfile):
#     with open(bfile,'r') as b:
#         bl = [i.strip() for i in b.readlines()]
#     return bl


# import os
# import sys
# from loguru import logger

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# log_file_path = os.path.join(BASE_DIR, 'Log/my.log')
# err_log_file_path = os.path.join(BASE_DIR, 'Log/err.log')

# # logger.add(s)
# logger.add(log_file_path, rotation="500 MB", encoding='utf-8')  # Automatically rotate too big file
# logger.add(err_log_file_path, rotation="500 MB", encoding='utf-8',
#            level='ERROR')  # Automatically rotate too big file
# logger.info("That's it, beautiful and simple logging!")
# logger.debug("中文日志可以不")
# logger.error("严重错误")
# logger.level("foobar", no=33, icon="🤖", color="<blue>")

# logger.log("foobar", "A message")

#coding:utf-8

from pprint import pprint
a= {"songid":127433973,"songmid":"002IvRV43ybv7F","songtype":0,"songname":"孤独的角落","songtitle":"孤独的角落 (TV Version)","songsubtitle":"","type":0,"cdIdx":0,"interval":105,"isonly":0,"language":0,"genre":0,"singer":[{"id":2283050,"mid":"004CnOhH2F3zqD","name":"韦正","title":"韦正","type":0,"uin":0}],"albumid":0,"albummid":"","albumname":"","strMediaMid":"0007GX6X4bFwNT","sizeape":0,"preview":{"trybegin":0,"tryend":0,"trysize":0},"pay":{"payalbumprice":0,"payplay":0,"timefree":0},"msgid":0,"switch":81683,"alertid":11,"action":{"play_lq":1,"play_hq":0,"play_sq":0,"down_lq":1,"down_hq":0,"down_sq":0,"soso":0,"fav":1,"share":1,"bgm":1,"ring":1,"sing":1,"radio":1,"try":0,"give":0,"play":1},"tryPlay":0,"anyPlay":1,"tryIcon":0,"disabled":0,"sosoFlag":0,"formatted":1,"mtype":"qqmusic","songurl":"","mid":"127433973","singername":"韦正","singerid":2283050,"singermid":"004CnOhH2F3zqD","fav":""}
pprint(a)