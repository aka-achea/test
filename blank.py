


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


import asyncio

from aiohttp import web

async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()