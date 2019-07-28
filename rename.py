#!/usr/bin/python
#coding:utf-8

# not in use

import os,fnmatch,shutil,re

from myfs import f_move


def modificate(text):
    #global loglevel
    #file_name = re.sub(r'\s*:\s*', u' - ', file_name)    # for FAT file system
    #if loglevel == 1 or loglevel == 2: before = text
    text = text.replace('[6v电影www.dy131.com]', '')      # for FAT file system
    text = text.replace('【更多美剧请去www.dy131.com】', '')
    text = text.replace('[66影视www.66ys.tv]', '')
    text = text.replace('[迅雷下载www.2tu.cc]', '')
    text = text.replace('[迅雷下载www.xunbo.cc]', '')
    text = text.replace('[电影天堂www.dy2018.net]', '')
    text = text.replace('[小调网-www.xiaopian.com]', '')
    text = text.replace('[电影天堂www.dygod.org]', '')
    text = text.replace('[阳光电影-www.ygdy8.com]', '')
    text = text.replace('【lol电影天堂www.loldytt.com】', '')
    text = text.replace('[最新电影www.6vhao.tv]', '')
    text = text.replace('【6v电影www.6vhao.net】', '')
    text = text.replace('[最新电影www.6vhao.tv]', '')
    text = text.replace('[www.66ys.org]','')
    text = text.replace('_副本', '')
    text = text.replace('(2)', '') 
    text = text.replace('dioguitar23.net_', '')
    text = text.replace('[电影天堂www.dy2018.com]', '')
    text = text.replace('javcn.net_', '')
    text = text.replace('【6v电影www.dy131.com】', '')
    text = text.replace('[最新电影www.66ys.tv]', '')
    text = text.replace('[最新电影www.hao6v.com]', '')
    text = text.replace('118', '')
    #text = text.replace('\'', u'＇')
    text = text.strip()
    #file_name = file_name.replace('$', '\\$')    # for command, see issue #7
    """if loglevel == 1 or loglevel == 2:
        after = text
        if before == after :
            pass
        else:
            print(color.verbose("Before modify: "+before))
            print(color.verbose("After modify: "+after))"""
    return text

# def f_move(src,dst):
#     if os.path.exists(dst):
#         print(os.path.getsize(dst))
#         print(os.path.getsize(src))
#         if os.path.getsize(dst) < os.path.getsize(src):
#             print('Replace small one')
#             os.remove(dst)
#             shutil.move(src,dst)
#         else:
#             print("Already have big one")
#             os.remove(src)
#     else:
#         shutil.move(src,dst)




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
            dst = os.path.join(path,modificate(pic))
            f_move(src,dst)


rename_pic(r'N:\LifeTrack\temp\巴尔干 - classic')
