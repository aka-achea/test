


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



import win32con
import win32clipboard as wincld


def get_text():
    wincld.OpenClipboard()
    text_result = wincld.GetClipboardData(win32con.CF_UNICODETEXT)
    # wincld.EmptyClipboard()
    wincld.CloseClipboard()
    return text_result



# read clipboard
print(get_text())