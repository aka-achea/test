


import os,re,configparser,sys,time
import urllib,shutil,coloredlogs,logging

from PIL import Image
import pytesseract,math
import codecs,fnmatch

import logging,coloredlogs
import inspect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



import win32con
import win32clipboard as wincld




txt = 'a1a1a1.live | a2a2a2.live | a3a3a3.live | gygygy.live | kgkgkg.live | nenene.live | bababa.live | bububu.live | gagaga.live | hehehe.live | 174.127.195.66 | 174.127.195.69 | 174.127.195.98 | 174.127.195.102 | 174.127.195.176 | 174.127.195.178 | 174.127.195.201 | 174.127.195.183 | 174.127.195.186 | 174.127.195.188 | 174.127.195.173 | 174.127.195.187 | 174.127.195.182 | 174.127.195.184 | 174.127.195.171 | 174.127.195.166 | 174.127.195.226 | 67.220.90.10 | 67.220.90.4 | 67.220.90.20 | 67.220.90.15 | 174.127.195.213 | 174.127.195.190 | 174.127.195.198 | 174.127.195.205 | a.1u2u3u4u.com'

def buildiplist(txt):
    iplist = re.split(' \| ',txt)
    return iplist

print(buildiplist(txt))