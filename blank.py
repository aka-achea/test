import os,sys

# wkdir = r'E:\jpg'
# MAX_WORKERS = 10 
# bfile = os.path.join(wkdir,'blacklist.txt')
# flist = os.path.join(wkdir,'faillist.txt')

# def blacklist(bfile):
#     with open(bfile,'r') as b:
#         bl = [i.strip() for i in b.readlines()]
#     return bl
# coding=utf-8
import os
import sys
from loguru import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

log_file_path = os.path.join(BASE_DIR, 'Log/my.log')
err_log_file_path = os.path.join(BASE_DIR, 'Log/err.log')

# # logger.add(s)
# logger.add(log_file_path, rotation="500 MB", encoding='utf-8')  # Automatically rotate too big file
# logger.add(err_log_file_path, rotation="500 MB", encoding='utf-8',
#            level='ERROR')  # Automatically rotate too big file
# logger.info("That's it, beautiful and simple logging!")
# logger.debug("中文日志可以不")
# logger.error("严重错误")
logger.level("foobar", no=33, icon="🤖", color="<blue>")

logger.log("foobar", "A message")





c = find_code('恒医药')
print(c)