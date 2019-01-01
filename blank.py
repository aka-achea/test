


import os,re,configparser
import urllib,shutil,coloredlogs,logging

confile = 'L:\\MUSIC\\xd.ini'
config = configparser.ConfigParser()
config.read(confile)
topdir = config['arch']['topdir']
archdir = config['arch']['archdir']
evadir = config['arch']['evadir']
coverdir = config['arch']['coverdir']
musicure = config['arch']['musicure']
logfile = config['log']['logfile']
logfilelevel = int(config['log']['logfilelevel'])

inventory =  config['arch']['inventory']

at = '久石譲'

with open(inventory,'r') as f:
    a = f.readlines()
    for i in a:
        m = re.search(at,i.strip())
        if m:
            print(i)