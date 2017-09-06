# coding: utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GLUT import *
# PyOpenGL 3.0.1 introduces this convenience module...
from OpenGL.GL.shaders import *
import sys

class SetGLSL:
    def __init__(self, VS_path=None, FS_path=None):
        self.vertex_shader_file = VS_path # バーテックスシェーダーパス
        self.fragment_shader_file = FS_path # フラグメントシェーダーパス
        
        if VS_path==None and FS_path==None:
            self.vertex_shader_file = 'toon1.vert' # バーテックスシェーダーパス
            self.fragment_shader_file = 'toon1.frag' # フラグメントシェーダーパス
            
        self.vertex_shade_code = '\n'.join(open(self.vertex_shader_file,'r').readlines())
        self.fragment_shader_code = '\n'.join(open(self.fragment_shader_file,'r').readlines())

        # シェーダーのコンパイル
        self.program = compileProgram(
            compileShader(self.vertex_shade_code,GL_VERTEX_SHADER),
            compileShader(self.fragment_shader_code,GL_FRAGMENT_SHADER),)

        glUseProgram(self.program) # シェーダーの有効化

        #print("lineScale:",glGetUniformLocation(self.program, 'lineScale'))
        #print("shadetype:",glGetUniformLocation(self.program, 'shadetype'))

    def SendUniformValue(self, name, val):
        loc = glGetUniformLocation(self.program, name)
        if loc == -1:
            print(name+"が定義されていません。")
            return -1
        if len(val) == 1:
            glUniform1f( loc, val[0])
        elif len(val) == 2:
            glUniform2f( loc, val[0], val[1])
        

    def SetShader(self, bl):
        if self.program:
            if bl:
                glUseProgram(self.program) # シェーダーの有効化
            else:
                glUseProgram(0) # シェーダーの有効化
        else:
            print("シェーダーが定義されていない")
