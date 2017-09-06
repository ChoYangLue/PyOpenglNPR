from PIL import (Image, ImageDraw, ImageFont)
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

VS = ['''
    varying vec3 normal;
    void main() {
        normal = gl_NormalMatrix * gl_Normal;
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
    ''']
FS = ['''
    varying vec3 normal;
    void main() {
        float intensity;
        vec4 color;
        vec3 n = normalize(normal);
        vec3 l = normalize(gl_LightSource[0].position).xyz;
 
        // quantize to 5 steps (0, .25, .5, .75 and 1)
        intensity = (floor(dot(l, n) * 4.0) + 1.0)/4.0;
        color = vec4(intensity*1.0, intensity*0.5, intensity*0.5,
            intensity*1.0);
 
        gl_FragColor = color;
    }
    ''']


''' 文字の描画 '''
class DrawString:
    def __init__(self, string):
        print(pygame.display.get_surface().get_size())
        self.hx = pygame.display.get_surface().get_size()[0]
        self.hy = pygame.display.get_surface().get_size()[1]
        print(pygame.display.get_surface().get_size()[0])
        self.string = string
        self.string_color = 'white'
        self.bgcolor = [0, 0, 0, 255]
        self.size = 144
        self.initsize=256
        self.text0 = -1
        #self.vertex_shade_code = VS
        #self.fragment_shader_code = FS

        #self.program = compileProgram(
        #    compileShader( vertex_shade_code,GL_VERTEX_SHADER),
        #    compileShader( fragment_shader_code,GL_FRAGMENT_SHADER),)

        self.TextUpdate(self.string)

    def TextUpdate(self, string):
        img = Image.new('RGBA', (self.initsize, self.initsize),
                        (self.bgcolor[0], self.bgcolor[1], self.bgcolor[2], self.bgcolor[3]))
        draw = ImageDraw.Draw(img)
        fnt = ImageFont.truetype('HGRME.TTC', self.size)
        ext = draw.textsize(string, font=fnt)
        draw.text((0, 0), string, font=fnt, fill=self.string_color)
        # (left, upper, right, lower)-tuple
        imgcr = img.crop((0, 0, ext[0], ext[1] + 16))
        self.string = string
        # TODO: Use the power of two value that is the closest
        # to each component of img.size.
        img = imgcr.resize((self.initsize, self.initsize), Image.ANTIALIAS)
        self.Send_openGL(img)

    def Send_openGL(self, img):
        self.text0 = glGenTextures(1) #テクスチャ領域確保
        glMatrixMode(GL_TEXTURE)
        glBindTexture(GL_TEXTURE_2D, self.text0)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,img.size[0], img.size[1],0, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())

    def Draw(self,x,y):
        AspectRaito = self.hx/self.hy
        x=x*2*AspectRaito
        y=y*2
        dx0 = x/self.hx -1.0*AspectRaito
        dy0 = -y/self.hy +1.0 -self.size/self.hy
        dx1 = (x+self.size)/self.hx -1.0*AspectRaito
        dy1 = -(y-self.size)/self.hy +1.0 -self.size/self.hy
        #dx0 = -1*AspectRaito
        #dy0 = -1
        #dx1 = 1*AspectRaito
        #dy1 = 1
        glEnable(GL_TEXTURE_2D)# テクスチャマップを有効にする
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);# alphaを有効にする
        glEnable(GL_BLEND) #blendを有効にする
        glBindTexture(GL_TEXTURE_2D, self.text0)
        #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,img.size[0], img.size[1],0, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glBegin(GL_POLYGON)
        """
        glTexCoord2f(0.0, 1.0) # テクスチャ画像での位置を指定
        glVertex3f(-1.0, -1.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0, -1.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0, 1.0, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, 1.0, 0.0)
        """
        glTexCoord2f(0.0, 1.0) # テクスチャ画像での位置を指定
        glVertex3f(dx0, dy0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(dx1, dy0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(dx1, dy1, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(dx0, dy1, 0.0)
        glEnd()
        glFlush()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND) #blendを有効にする

''' 画像の描画 '''
class LoadGraphScreen:
    def __init__(self, name, tf = False):
        self.x = 0
        self.y = 0
        self.GraphName = name
        self.TransFlag = tf
        self.text0 = -1

    def Send_openGL(self, img):
        self.text0 = glGenTextures(1) #テクスチャ領域確保
        glMatrixMode(GL_TEXTURE)
        glBindTexture(GL_TEXTURE_2D, self.text0)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,img.size[0], img.size[1],0, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())


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
