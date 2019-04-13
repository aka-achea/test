


import os,re,configparser,sys,time
import urllib,shutil,coloredlogs,logging

from PIL import Image
import pytesseract,math
import codecs,fnmatch

import logging,coloredlogs
import inspect
from flask import Flask
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

def find_album(album):
    with open(albumlist,'r',encoding='utf-8') as f:        
        for i in f.readlines():
            if album == i.strip():
                return True

albumlist = r'L:\Music\album.txt'
a = find_album('The Roots - 2010 - How I Got Over')
print(a)