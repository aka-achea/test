# import binascii
import os
from PIL import Image

from tkinter import Tk, Canvas
import numpy as np

dot_matrix = np.array([[0,0,0,0,0,0,0],
                       [0,0,1,1,1,0,0],
                       [0,1,0,0,0,1,0],
                       [0,0,0,0,0,1,0],
                       [0,0,0,0,1,0,0],
                       [0,0,0,1,0,0,0],
                       [0,0,1,0,0,0,0],
                       [0,1,1,1,1,1,0],
                       [0,0,0,0,0,0,0]])

master = Tk()
canvas = Canvas(master, bg="black", width=200, height=200)
canvas.pack()

def display_matrix(matrix):
    h,l = matrix.shape
    for i in range(h):
        for j in range(l):
            if matrix[i,j]:
                canvas.create_oval(5 + 12*j , 5 + 12*i, 15 + 12*j, 15 + 12*i, fill="red")

<<<<<<< HEAD
        #读取HZK16汉字库文件
        with open(HZK16, "rb") as f:
            #找到目标汉字的偏移位置
            f.seek(offset)
            #从该字模数据中读取32字节数据
            font_rect = f.read(32)
            print( font_rect )
=======
display_matrix(dot_matrix)
>>>>>>> 5f441a75f09c6f0251bfca6b40bcec986d277acf

master.mainloop()



if __name__=="__main__":
    #将想转化的字赋给字符串
    inpt = "二零一九新年快乐！"

    #将字转化为汉字库的点阵数据
    outlist = char2bit(inpt)

    #获取当前文件夹路径
    workspace = os.getcwd()

    #用于拼接的图片所在文件夹名称
    user = "TED"
    #获取图片文件夹所在路径
    folder = "{}\\{}".format(workspace,user)

    #若读取图片失败，用于替代的备用图片路径
    self=workspace+"\\"+"TED.jpg"
    #运行后将生成 user_输出 文件夹
    head2char(workspace,folder,self,outlist)
    print("Well done!")