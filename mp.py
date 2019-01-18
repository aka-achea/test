from multiprocessing import Pool
import  random
from openlink import mytimer
import sys , os , shutil ,datetime , math
from urllib.parse import urlparse
from urllib import error
import urllib.request as req


# def long_time_task(i):
#     url = 'https://epass.icbc.com.cn/ICBCChromeExtension.msi'
#     # print('Run task %s (%s)...' % (i, os.getpid()))
    
#     print(i)
#     print('\n'*i)
#     myget.dl(url,out=str(i))
    

def filename_from_url(url):
    fname = os.path.basename(urlparse(url).path)
    if len(fname.strip(" \n\t.")) == 0:
        return None
    return fname


def mbar(blocks, block_size, total_size):
    if not total_size or total_size < 0:
        sys.stdout.write(str(block_size*blocks)+'\r')
    else:
        dlsize = block_size*blocks
        if dlsize > total_size: dlsize = total_size
        rate = dlsize/total_size
        percentrate = str(math.floor(100*rate))+'%'  
        # width = get_console_width()-8
        width = 40
        dots = int(math.floor(rate*width))
        bar = '▇'*dots+'--'*(width-dots)
        if total_size > (1024*1024):
            ts = str(total_size/(1024*1024))[:4]
            ds = str(dlsize/(1024*1024))[:4]
            unit = 'MB'
        elif total_size > 1024:
            ts = str(total_size/1024)[:4]
            ds = str(dlsize/1024)[:4]
            unit = 'KB' 
        else:
            ts = str(total_size)
            ds = str(dlsize) 
            unit = 'B'          
        e = '\n' if rate == 1 else '\r'
        sys.stdout.write('\n'*ind*2+out+bar+' '+percentrate+' '+ds+'/'+ts+unit+e)
    sys.stdout.flush()


def mdl(url,index,out=None,mbar=mbar):     
    # detect of out is a directory
    outdir = None
    if out and os.path.isdir(out):
        outdir = out
        out = None
    print('begin'+str(ind))
    fn = out if out else filename_from_url(url)
    if os.path.exists(fn):
        print('Already download --> Pass')
    else:
        now = str(datetime.datetime.utcnow()).replace(':','')
        tmpname = fn+now+'.tmp'   
        try:
            local_filename, headers = req.urlretrieve(url,tmpname,mbar )
        except error.ContentTooShortError as e:
            mytimer(5)
            local_filename, headers = req.urlretrieve(url,tmpname,mbar )

        shutil.move(tmpname,out) if out else shutil.move(tmpname,fn)

def mp(urllist):
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(len(urllist)):
        url = urllist[i]
        print(url)
        global ind
        global out 
        ind = i
        out = str(i+10)
        p.apply_async(mdl, args=(url,))
    # print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')


if __name__=='__main__':
    a = 'https://epass.icbc.com.cn/ICBCChromeExtension.msi'
    urllist = [a,a,a,a]
    mp(urllist)





