
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

a = '''
8055770
8055736
8055648
8054914
8054375
8054264
8054914
8054625
8054622
8053218
8052893
8052893
8052860
8051528
8051458
8051428
8050642
8050641
8050534
8050331
8050260
8049327
8049056
8049004
8048123
8048121
8048120
8048119
8047851
8047772
8046653
8046459
8046444
8046313
8045154
8045040
8044968
8044066
8044065
8044064
8044061
8043992
8042548
8042287
8042178
8041726
8040905
8040780
8043615
8066516
8066142
8066142
8064719
8064313
8063382
8063381
8063377
8063152
8063017
8062266
8061892
8061463
8060950
8060214
8060110
8059790
8058570
8058488
8057376
8057373
8057161
8057046
8057007
8055770
8055736
8055648
8054914
8054625
8054622
8054375
8054264
8053218
8052893
8052860
8051528
8051458
8051428
8050642
8050641
8090385
8088971
8088438
8086876
8085057
8084789
8083637
8084789
8083637
8082563
8081532
8081236
8080048
8079517
8078425
8078424
8078422
8078420
8078418
8078415
8074703
8073576
8073528
8073526
8073525
8073523
8073521
8073518
8073266
8072672
8072094
8071281
8071280
8071272
8071270
8071269
8070863
8069909
8069659
8068582
8068579
8068574
8068416
8093868
8092573
8091994
8091360
8107187
8105596
8103789
8103787
8103785
8103783
8103789
8103787
8103785
8103783
8103771
8103632
8103410
8103407
8103404
8103402
8103399
8103393
'''

for x in a.split():
    print(x)
