# coding: utf-8

import os, datetime, pygame
#import tkinter as tk
from tkinter import *
import tkinter.filedialog
from PIL import (Image, ImageDraw, ImageFont)

pi2 = 3.149265358979 

# このプログラムが読まれた時点でUIが構築される

"""---------- モデルの管理クラス --------------"""
class Model_info:
    def __init__(self):
        self.model_file_path = ""
        self.path_name = ""
        self.changeFlag = False
        self.addFlag = False
        self.save_path = os.getcwd()
        self.surface = None
        self.render = 0
        self.file_type = "obj"
        self.shad_line = 12.0
        self.shad_dot = 18.0
        self.ld_type = 0.0

    def SetSuface(self, sur):
        self.surface = sur

"""---------ボタンのコールバック関数-------------"""

def ff():
    """
    if MI.render < 1:
        MI.render = MI.render + 1
    elif MI.render == 1:
        MI.render =0
    """
    MI.render=Radio_Value0.get()
    print("MI.render:")
    print(MI.render)

    if MI.render == 2:
        # ボタンを有効化
        shad_button.configure(state=NORMAL)
    else:
        shad_button.configure(state=DISABLED)

# レンダリング画像の保存
def Capture():
    d = datetime.datetime.today()
    save_file_name = str(d.month)+"-"+str(d.day)+"-"+str(d.minute)+"-"+str(d.second) + ".png"
    #pygame.image.save(screen, "output.png")
    pygame.image.save(MI.surface, "scs/"+save_file_name)
    print(save_file_name)
    print("{}を保存しました。".format(save_file_name))

# ファイルの選択
def load_file():
    global image_data, path_name
    path_name = os.getcwd()
    filename = tkinter.filedialog.askopenfilename(filetypes = [
        ('objファイル', ('.obj')),
        ('xファイル', '.x'),
        ('MMDファイル', '.pmd','.pmx')],
                                                  initialdir = path_name)
    if filename != "":
        MI.path_name = os.path.dirname(filename)
        #print(filename)
        #del model_file_path[:]
        #model_file_path.append(filename)
        MI.model_file_path = filename
        #print(model_file_path[:])
        MI.changeFlag = True
        typef = filename.split(".")
        if typef[1] == "pmd":
            MI.file_type = "pmd"
        elif typef[1] == "obj":
            MI.file_type = "obj"
        print(MI.path_name)
        print(MI.file_type)
        print(MI.model_file_path)
        #image_data = PhotoImage(file = filename)
        #label.configure(image = image_data)

# ライン間隔
def line_len(n):
    #label.configure(bg='#%02x0000' % scale1.get())
    MI.shad_line = float(scale1.get())
    print("MI.shad_line:",MI.shad_line)

# ドット間隔
def dot_len(n):
    MI.shad_dot = float(scale2.get())
    print("MI.shad_dot:",MI.shad_dot)

# ハーフトーンとドットを切り替える
def ld_c():
    if MI.ld_type == 0.0:
        MI.ld_type = 1.0
    else:
        MI.ld_type = 0.0
    print("MI.ld_type:",MI.ld_type)

def shad():
    tki = Tk()
    canvas1=Canvas(tki,width=200,height=10,bd=0)# canvas作成
    canvas1.pack()
    tki.title(u'設定') # タイトル

    ld_button = Button(tki, text = '切り替え', compound=TOP, command=ld_c)
    ld_button.pack(side="top", fill="both")

    #global label
    #label = Label(tki, text='press button', fg='#ffffff')
    #label.pack()

    global scale1
    scale1 = Scale(tki, label='斜線間隔', orient='h', from_= 0, to=pi2, resolution=0.1, command=line_len)
    scale1.pack()

    global scale2
    scale2 = Scale(tki, label='ドット間隔', orient='h', from_= 0, to=pi2, resolution=0.1, command=dot_len)
    scale2.pack()
    
        
root = Tk() #tkinter初期化
# canvas作成
canvas=Canvas(root,width=800,height=600,bd=0)
canvas.pack(side = LEFT)
root.title(u'ノンフォトリアリスティックレンダー') # タイトル

MI = Model_info() # 管理用オブジェクト

Radio_Value0 = IntVar()
Radio_Value0.set(0)

#Radio_Value1 = tkinter.IntVar()
#Radio_Value1.set(0)

cam_icon = PhotoImage(file='camera48.png')
fol_icon = PhotoImage(file='folder48.png')
        
Radiobutton(root,text='通常',variable=Radio_Value0,value=0,command = ff).pack()
Radiobutton(root,text='アニメ',variable=Radio_Value0,value=1,command = ff).pack()
Radiobutton(root,text='漫画',variable=Radio_Value0,value=2,command = ff).pack()
#button = Button(root, text = 'レンダー切り替え', command = ff)
#button.pack(side="top", fill="both")
f_button = Button(root, image=fol_icon, text = 'ファイルの選択', compound=TOP, command = load_file)
f_button.pack(side="top", fill="both")
cap_button = Button(root, image=cam_icon, text = '保存', compound=TOP, command = Capture)
cap_button.pack(side="top", fill="both")

shad_button = Button(root, text = '設定', compound=TOP, command=shad ,state=DISABLED)
shad_button.pack(side="top", fill="both")

"""
def draw_text(text, initsize=256, point=144, bgcolor='black', forecolor='white'):
    # Create a larger canvas.
    #img = Image.new('RGBA', (initsize, initsize), bgcolor)
    img = Image.new('RGBA', (initsize, initsize), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('HGRME.TTC', point)

    ext = draw.textsize(text, font=fnt)
    draw.text((0, 0), text, font=fnt, fill=forecolor)

    # (left, upper, right, lower)-tuple
    imgcr = img.crop((0, 0, ext[0], ext[1] + 16))

    # TODO: Use the power of two value that is the closest
    # to each component of img.size.
    return imgcr.resize((initsize, initsize), Image.ANTIALIAS)
"""


