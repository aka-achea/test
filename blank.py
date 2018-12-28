

import progressbar as pbar

import os,re
import urllib

def get_pdf(html):
    """ xxx"""
    reg = r'href="(.+?\.pdf)">pdf'
    pdfre = re.compile(reg)
    pdflist = re.findall(pdfre, html)
    dir_name = 'COLT2016'
    if os.path.exists(dir_name) is False:
        os.mkdir(dir_name)
    maxrows = len(pdflist)
    pbar = prgbar.ProgressBar(total=maxrows)
    for idx, pdfurl in enumerate(pdflist):
        filename = dir_name + '/' + pdfurl
        pbar.log('http://jmlr.org/proceedings/papers/v49/' + pdfurl)
        if os.path.exists(filename) is True:
            pbar.log('Exist')
        else:
            urllib.urlretrieve(
                'http://jmlr.org/proceedings/papers/v49/' + pdfurl, filename)
        pbar.update(index=(idx + 1))
    pbar.finish() 


