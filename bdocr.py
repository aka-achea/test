#!/usr/bin/python3
#coding:utf-8

__version__ = 20200223

from pprint import pprint
from PIL.ImageGrab import grabclipboard


from myocr import init_client,ocr_baidu

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def murge_txt(txtlist:list):
    baselen = max(len(x) for x in txtlist)-4
    output = []
    tmpstr = ''
    for x in txtlist:
        if len(x) < baselen and tmpstr != '':
            output.append(tmpstr)
            tmpstr = ''
            output.append(x)
        elif len(x) < baselen and tmpstr == '':
            output.append(x)
        elif len(x) >= baselen :
            tmpstr += x
    return output


def main(murge=True,pic=None):
    client = init_client()
    if pic:
        img = get_file_content(pic)
    else:
        img = grabclipboard()
    img.save('tmp.png', 'PNG')
    data = get_file_content('tmp.png')
    txtlist = ocr_baidu(client,data)
    if murge:
        txtlist = murge_txt(txtlist)
    for x in txtlist:
        print(x)


if __name__ == "__main__":
    main(murge=True)