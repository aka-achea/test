
import os
from myfs import f_move

# question = r'L:\Music\_Jazz\cc.txt'
# target = r'L:\Music\mc.txt'


# with open(target,'r') as q:
#     questions = q.readlines()
#     adict = { x.strip().split('\\')[-1]:x.strip() for x in questions} 

# # print(adict)




# with open(question,'r') as q:
#     questions = q.readlines()
#     for x in questions:
#         a = x.strip().split('\\')[-1]
#         if a in adict.keys():
#             print(x.strip())
#             print(adict[a])
#             # print(f_move(x.strip(),adict[a]))


hd = r'H:\HD'
target = r'H:\_Mask\VA'
question = r'D:\H\_Mask\1\桜空もも'
cover = r'D:\H\_Mask\cover' 

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
