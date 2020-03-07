

# import json
from myfs import g_fsize,jdump,jload
from itertools import product
from pprint import pprint

a = [
[r'O:',r'd:\avnomask.txt'],
[r'H:',r'd:\av1.txt'],
[r'I:',r'd:\av2.txt'],
[r'K:',r'd:\av3.txt'],
[r'D:\H',r'd:\maskd.txt'],
[r'E:\AV',r'd:\ave.txt'],
[r'J:\decode',r'd:\avj.txt'],
[r'F:',r'd:\avhd.txt']
]

def create_dump():
    for x in a:
        data = g_fsize(x[0])
        jdump(x[1],data)

# create_dump()

def compare_dump():
    p = []
    for x in a:
        keys = jload(x[1]).keys()
        kk = [ k[:-4] for k in keys if k[-3:] not in ['JPG','INI','PEG'] ]
        p.append({x[0]:kk})
    dk = ( (x,y) for x in p for y in p if x != y )
    for x in dk:
        # if x[0] != x[1]:
        m = [ s for s in x[0].values() ][0]
        n = [ s for s in x[1].values() ][0]
        mk = [ s for s in x[0].keys() ][0]
        nk = [ s for s in x[1].keys() ][0]
        if dup := set(m) & set(n):
            print(f'{mk} & {nk} : {dup}' )

def murge_dump():
    m = {}
    for x in a:
        m.update(jload(x[1]))
    jdump(r'd:\all.txt',m)


# murge_dump()


from urllib import parse

s = 'ed2k://|file|%E7%8B%99%E5%87%BB%E7%B2%BE%E8%8B%B1%EF%BC%9A%E5%B7%85%E5%B3%B0%E5%AF%B9%E5%86%B3.720p.BD%E4%B8%AD%E8%8B%B1%E5%8F%8C%E5%AD%97[%E6%9C%80%E6%96%B0%E7%94%B5%E5%BD%B1www.6vhao.tv].mp4|1474483384|3A62C00F7790D779AC879C7F6A3FB86B|h=N2D6HC2QWPNGCAAVHFGTV3J4RBCZQKCB|/'

t = parse.unquote(s)

print(t)