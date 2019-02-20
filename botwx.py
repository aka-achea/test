#!/usr/bin/python
#coding:utf-8
# python 3


from wxpy import *

msg = 'gjkalkej'


bot = Bot()
# bot = Bot(console_qr=2,cache_path=True)


JC = bot.friends().search(u'JASON')[0]
JC.send(msg)