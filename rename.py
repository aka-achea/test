#!/usr/bin/python
#coding:utf-8

# not in use

import os,fnmatch,shutil,re

from myfs import f_move



def rename_mfwguide(path):
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, '*.pdf'):
            print(file)
            a = file[:-4].split
            print(a)
            if a.find('蚂蜂窝'):
                a.split('蚂蜂窝')
                print(a)
            nfile = modificate(file)
            dst = path+"\\"+nfile
            #print(dst)2

            #f_move(src,dst)


def rename_pic(path):
    for pic in os.listdir(path):
        if re.findall(' \(2\)',pic):
            print(pic)
            src = os.path.join(path,pic)
            dst = os.path.join(path,pic.replace('_副本', ''))
            f_move(src,dst)


rename_pic(r'N:\新建文件夹\新西兰 - classic')
