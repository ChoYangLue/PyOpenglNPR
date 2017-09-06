import sys, pygame, os
if sys.version_info.major == 2:
    import Tkinter as tk
    from Tkinter import *
    import Tkinter.filedialog
else:
    import tkinter as tk
    from tkinter import *
    import tkinter.filedialog
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

# IMPORT MY LIB
from objloader import *
from mmdloader import *
from gui import *
from GLSL import *
from GL2d import *

# 画面の統合
os.environ['SDL_WINDOWID'] = str(canvas.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
pygame.display.init() # pygame初期化
viewport = (800,600) # pyopenglのビューポート
hx,hy = viewport[0]/2,viewport[1]/2
screen = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)# pygame+pyopengl
glViewport(0, 0, viewport[0], viewport[1])# pyopenglのビューポート有効化

MI.SetSuface(screen)
World_Model =[]

# ライティングの設定
glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))  # 光源の位置設定
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0) # ０番目の光源 (GL_LIGHT0 - 必ず用意されている) を有効
glEnable(GL_LIGHTING)# 陰影付けを有効
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH) # スムースシェーディングの有効化

#img = DrawString('賢')

glClearDepth(1.0)
glDepthFunc(GL_LESS)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(45.0, float(width)/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)

gluLookAt(3.0, 4.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        
glEnable(GL_BLEND)
glEnable(GL_CULL_FACE) # 陰面消去しておくとより顕著にわかりやすく見えるのでEnableにした
glFrontFace(GL_CCW)

for wm in World_Model:
    print(wm.gl_list)
    print(wm.texcoords)


tt = -1

glsl = SetGLSL('toon0.vert','toon0.frag') # GLSL初期化

glsl2 = SetGLSL('cartoon.vert','cartoon.frag') # GLSL初期化

#fxaa = SetGLSL(viewport[0],viewport[1],'fxaa.vert','fxaa.frag') # GLSL初期化

count = 0

clock = pygame.time.Clock() # 固定FPS用
rx, ry = (0,0)
tx, ty = (0,0)
zpos = 5
rotate = move = False
paramove = False
lx,ly = -40,200
while 1:
    if MI.changeFlag:
        MI.changeFlag = False
        """
        for wm in World_Model:
            wm.DeleteOBJ
        del World_Model[:]
        """
        if MI.file_type == "obj":
            World_Model.append(OBJ(MI.model_file_path, swapyz=False)) # ファイル読み込み
        elif MI.file_type == "pmd":
            World_Model.append(MMDloader(MI.model_file_path, MI.path_name)) # ファイル読み込み
        # ライティングの設定
        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))  # 光源の位置設定
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0) # ０番目の光源 (GL_LIGHT0 - 必ず用意されている) を有効
        glEnable(GL_LIGHTING)# 陰影付けを有効
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH) # スムースシェーディングの有効化
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = viewport
        gluPerspective(90.0, width/float(height), 0.5, 100.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        
        glEnable(GL_BLEND)
        glEnable(GL_CULL_FACE) # 陰面消去しておくとより顕著にわかりやすく見えるのでEnableにした
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)# フレーム
        glHint(GL_POLYGON_SMOOTH_HINT,GL_NICEST)
        glEnable(GL_POLYGON_SMOOTH)   
        
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()# Pygameの終了(画面閉じられる)
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            pygame.quit()# Pygameの終了(画面閉じられる)
            sys.exit()
        elif e.type == KEYDOWN:
            # 矢印キー
            if e.key == K_LEFT:
                lx = lx - 10
            if e.key == K_RIGHT:
                lx = lx + 10
            if e.key == K_UP:
                ly = ly + 10
            if e.key == K_DOWN:
                ly = ly - 10
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: zpos = max(1, zpos-1)
            elif e.button == 5: zpos += 1
            elif e.button == 1: rotate = True
            elif e.button == 3: move = True
            elif e.button == 2: paramove = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
            elif e.button == 3: move = False
            elif e.button == 2: paramove = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j
            if paramove:
                #data = glReadPixels( 0,0, viewport[0], viewport[1], GL_RGBA, GL_UNSIGNED_BYTE)
                #im = Image.frombuffer("RGBA", (viewport[0], viewport[1]), data, "raw", "RGBA", 0, 0)
                #im.save("asmo.png")
                #print("ammo")
                #pygame.image.save(srf, "output.png")
                pass

    if MI.render == 0:
        glsl.SetShader(False)
        glsl2.SetShader(False)
        glClearColor(0.5,0.5,0.5,1.0) #カラーバッファのクリアの色(背景色)
    elif MI.render == 1:
        glsl2.SetShader(False)
        glsl.SetShader(True)
        glClearColor(0.5,0.5,0.5,1.0) #カラーバッファのクリアの色(背景色)
    elif MI.render == 2:
        glsl.SetShader(False)
        glsl2.SetShader(True)
        glsl2.SendUniformValue('lineScale', [MI.shad_line])
        glsl2.SendUniformValue('dotScale', [MI.shad_dot])
        glsl2.SendUniformValue('shadetype', [MI.ld_type])
        glClearColor(0.9,0.9,0.9,1.0) #カラーバッファのクリアの色(背景色)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glLightfv(GL_LIGHT0, GL_POSITION,  (lx, ly, 100, 0.0))  # 光源の位置設定

    #glClearColor(0.5,0.5,0.5,1.0) #カラーバッファのクリアの色(背景色)

    glLoadIdentity() # 座標系をリセット(単位行列を代入)
    
    # RENDER OBJECT
    glTranslate(tx/20., ty/20., -zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    if len(World_Model)>0:
        for wm in World_Model:
            glCallList(wm.gl_list)
    #glCallList(mmd.gl_list)

    glsl.SetShader(False)
    glsl2.SetShader(False)
    
    glLoadIdentity() # 座標系をリセット(単位行列を代入)
    glTranslate(0, 0, -1)
    glRotate(0, 1, 0, 0)
    glRotate(0, 0, 1, 0)
    #img.Draw(10,10)

    pygame.display.flip()

    root.update_idletasks()
    root.update()

    #count += 1
    #print(count)

