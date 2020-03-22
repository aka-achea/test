

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


def unquote_url(url):
    from urllib import parse
    return parse.unquote(url)


from contextlib import contextmanager

@contextmanager
def tag(name):
    print(f"<{name}>")
    yield
    print(f"</{name}>")

with tag("h1"):
    print("This is Title.")


def a():
    print(a.__module__)

a()