


import os,re,configparser,sys,time
import urllib,shutil,coloredlogs,logging


from PIL import Image
import pytesseract,math
import codecs,fnmatch


#!/usr/bin/python
#coding:utf-8
# Python3
# Version: 20181222

# CRITICAL    50
# ERROR   40
# WARNING 30
# INFO    20
# DEBUG   10
# NOTSET  0


import logging,coloredlogs
import inspect

# def get_funcname():
#     func = inspect.stack()[1][3]
#     mo = str(inspect.stack()[1][1]).split('/')[-1].split('.')[0]
#     mf = mo+'.'+func

#     lineno = inspect.stack()[1][2]
#     print(lineno)

#     return mf


# class mylogger():
#     def __init__(self,logfile,funcname,logfilelevel=10):
#         logging.basicConfig(level=logfilelevel,filename=logfile,filemode='w',
#                             datefmt='%m-%d %H:%M:%S',
#                             format='%(asctime)s <%(name)s>[%(levelname)s] %(message)s')
#         self.logger = logging.getLogger(funcname)
#         coloredlogs.DEFAULT_LEVEL_STYLES= {
#                                         #'debug': {'color': 'magenta','bold': True},
#                                         'info': {'color': 'green','bold': True},
#                                         'warning': {'color': 'yellow','bold': True},
#                                         'error': {'color': 'red','bold': True},
#                                         'critical': {'color': 'magenta','bold': True}
#                                             }
#         coloredlogs.DEFAULT_LOG_FORMAT = '%(message)s'
#         coloredlogs.install(level='info',logger=self.logger)  
#     def debug(self,msg):
#         self.logger.debug(msg)
#     def info(self,msg):
#         self.logger.info(msg)
#     def warning(self,msg):
#         self.logger.warning(msg)
#     def error(self,msg):
#         self.logger.error(msg)
#     def critical(self,msg):
#         self.logger.critical(msg)
#     def verbose(self,msg):
#         self.logger.debug(msg)

# # l = mylogger(logfile,funcname )





# # if __name__=='__main__': #Usage
#     # funcname = __name__
#     # logfilelevel = 10 # Debug
    
#     # l = mylogger(logfile,logfilelevel,funcname)   

#     # l = myconlog()   

#     # l.debug('This is Debug')
#     # l.info('ール・デ')
#     # l.error('error log')
#     # l.warning('warning log')
#     # l.critical("this is a critical message")
#     # l.verbose('vvvvv')

#     # logtest()


# def function_one():
#     time.sleep(1)
#     print(get_funcname())

# if __name__ == "__main__":
#     function_one()


    # import functools
    # logfile = 'E:\\app.log'
    # # def log(func):
    # #     @functools.wraps(func)
    # #     def wrapper(*args, **kw):
    # #         global l
    # #         l = mylogger(logfile,func.__name__)
    # #         return func(*args, **kw)
    # #     return wrapper

    # def log(logfile):
    #     def decorator(func):
    #         @functools.wraps(func)
    #         def wrapper(*args, **kw):
    #             global l
    #             l = mylogger(logfile,func.__name__)
    #             return func(*args, **kw)
    #         return wrapper
    #     return decorator

    
    # @log(logfile)
    # def logtest():
    #     l.info("gesge")
    #     l.info(get_current_function_name())

    # logtest()

    # with open(r'H:\av.txt','w',encoding='utf-8') as f:
    #     for dirpath, dirnames, files in os.walk('F:'):
    #         for name in files:
    #             name = name.lower()
    #             a = 0
    #             for e in ['*.jpg','*.jpeg','*.torrent','*.srt','*.htm']:
    #                 if fnmatch.fnmatch(name,e):
    #                     a = 1
    #             if a != 1:
    #                 p = os.path.join(dirpath,name)
    #                 s = str(os.path.getsize(p))
    #                 f.write(p +' - '+s+'\n')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rambo'

'''
Models for user, blog, comment.
'''

import orm
import asyncio,random,string
from models import User, Blog, Comment,next_id

def random_email():
    qq = random.randint(100000000, 999999999)
    return str(qq)+'@qq.com'

def random_name():
    return ''.join(random.sample(string.ascii_letters, 5))
async def test(loop):
    await orm.create_pool(loop=loop, user='root', password='luoshi123', db='awesome')

    u = User(name='Rambo', email='1434284872@qq.com', passwd='123456', image='about:blank')

    #1. 测试插入方法
    for x in range(100):
        u['id'] = next_id()
        u['email'] = random_email()
        u['name'] = random_name()
        await u.save()

    #2. 测试根据主键查询方法
    # u = await User.find('0015452734508517676e9987a094be6b017ef19f97e58db000')

    #3. 测试根据参数查询方法
    #u = await User.findAll(where='name like ?', args=['%a%'], orderBy='name asc', limit=(0, 10))

    #4. 测试findNumber方法，不知道这个方法有什么用
    #u = await User.findNumber('name')

    #5. 测试更新方法
    # u = await User.find('0015452734508517676e9987a094be6b017ef19f97e58db000')
    # u['passwd'] = '123'
    # await u.update()

    #6. 测试删除方法
    # u = await User.find('0015452782688867d6a4740601d4022b048312d2511dee4000')
    # await u.remove()

    print(u)

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test(loop))
    # loop.run_forever()

  