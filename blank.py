
import os
from myfs import f_move

# for x in os.listdir(target):
#     av = os.path.basename(x).upper()
#     if av[-3:] == 'JPG':
#         # print(av[:-4])
#         q = os.path.join(hd,av)
#         if os.path.exists(q):
#             print(q)


q = r'F:\HD'
avf = r'i:\av.txt'

def g_fsize(folderpath): 
    '''get all file size dict'''
    adict = {}
    for root, dirs, files in os.walk(folderpath):
        for name in files:
            size = os.path.getsize(os.path.join(root, name))
            if name[-3:].upper() not in ['JPG','SRT','HTM','PEG','ENT']: 
                print(name,size)
                adict[name] = size
    return adict

# with open(avf,'w',encoding='utf-8') as f:
#     adict = g_fsize(q)
#     for a in adict:
#         f.write(f'{a} {adict[a]} \n')

av = set()
with open(avf,'r',encoding='utf-8') as f:
    for a in f.readlines():
        av.add(a.split()[0][:-4])

b = set()
for v in os.listdir(r'D:\H\_Mask\1'):
    b.add(v[:-4])

print(av&b)

# for x in os.listdir(cover):
#     if x[-3:] == 'JPG':
#         name = checkcovername(x)
#         print(name)
#         src = os.path.join(cover,x)        
#         dst = os.path.join(cover,name)        
#         shutil.move(src,dst)


# for x in a.split():
#     print(x)
# a = {'ge':'s'}
# print(hash(a))

from dis import dis

# dis(a['ge'])

# print(id(a))


print(__file__)