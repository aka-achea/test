
import os
from myfs import f_move

# question = r'L:\Music\_Jazz\cc.txt'
# target = r'L:\Music\mc.txt'


# with open(target,'r') as q:
#     questions = q.readlines()
#     adict = { x.strip().split('\\')[-1]:x.strip() for x in questions} 

# # print(adict)
os_dict = {
    'w':'Windows (WSOE)',
    'l':'Linux (LSOE)',
    'v':'VMware (VSOE)',
    's':'Suse (SSOE)'
}
hw_dict = {
    'r10':'HP DL380 G10',
    'b10':'HP BL460 G10',
    'b9':'HP BL460 G9'
}

a = tuple(hw_dict[x] for x in hw_dict.keys())
print(a)
# with open(question,'r') as q:
#     questions = q.readlines()
#     for x in questions:
#         a = x.strip().split('\\')[-1]
#         if a in adict.keys():
#             print(x.strip())
#             print(adict[a])
#             # print(f_move(x.strip(),adict[a]))



# for x in os.listdir(target):
#     av = os.path.basename(x).upper()
#     if av[-3:] == 'JPG':
#         # print(av[:-4])
#         q = os.path.join(hd,av)
#         if os.path.exists(q):
#             print(q)



# import shutil

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