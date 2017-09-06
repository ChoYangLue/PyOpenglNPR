import pygame, os, sys
from OpenGL.GL import *

def MTL(filename):
    contents = {}
    mtl = None
    # , encoding="UTF-8"
    if sys.version_info.major == 2:
        ofile = open(filename, "r")
    else:
        ofile = open(filename, "r", encoding="UTF-8")
    for line in ofile:
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError( "mtl file doesn't start with newmtl stmt")
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            #mtl[values[0]] = values[1]
            mtl['map_Kd'] = values[1]
            #print(mtl['map_Kd'])   #os.path.join('data', mtl['map_Kd'])
            a=os.path.dirname(filename)
            path = os.path.join(a, mtl['map_Kd'])
            #surf = pygame.image.load(path.encode('cp932'))
            #image = pygame.image.tostring(surf, 'RGBA', True)
            #ix, iy = surf.get_rect().size
            try:
                #surf = pygame.image.load(t)
                surf = pygame.image.load(path)
                image = pygame.image.tostring(surf, 'RGBA', True)
                ix, iy = surf.get_rect().size
            except:
                # 日本語ファイルが読めないのでPILで読む
                from PIL import Image
                #surf = Image.open(t, 'r')
                surf = Image.open(path, 'r')
                surf = surf.transpose(Image.FLIP_TOP_BOTTOM)
                image = surf.convert('RGBA').tobytes()
                ix, iy = surf.size[0], surf.size[1]
            texid = mtl['texture_Kd'] = glGenTextures(1)
            #print(texid)
            glMatrixMode(GL_TEXTURE)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,GL_REPEAT)
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,GL_MIRRORED_REPEAT)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, image)
        elif values[0] == 'map_d':
            pass
        else:
            mtl[values[0]] = list(map(float, values[1:]))
            #mtl[values[0]] = values[1:]
    return contents

class OBJ:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        a=os.path.dirname(filename)

        material = None
        if sys.version_info.major == 2:
            ofile = open(filename, "r")
        else:
            ofile = open(filename, "r", encoding="UTF-8")
        for line in ofile:
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                #v = map(float, values[1:4])
                v = list(map(float, values[1:4]))
                #v = [float(i) for i in values]
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                #v = map(float, values[1:4])
                v = list(map(float, values[1:4]))
                #v = [float(i) for i in values]
                
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                #self.texcoords.append(map(float, values[1:3]))
                self.texcoords.append(list(map(float, values[1:3])))
                #v = [float(i) for i in values]
                #self.texcoords.append(v)
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                path = os.path.join(a, values[1])
                print(path)
                self.mtl = MTL(path)
                #print(self.mtl)
                #self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

    def DeleteOBJ(self):
        #pass
        glDeleteLists(self.gl_list,1)


"""
self.mtl = MTL()=
{'Material.001':
{'Ka': [1.0, 1.0, 1.0],
'Ke': [0.0, 0.0, 0.0],
'Ks': [0.5, 0.5, 0.5],
'Ni': [1.0],
'Ns': [96.078431],
'Kd': [0.64, 0.64, 0.64],
'illum': [2.0],
'texture_Kd': 2,
'map_Kd': 'testobj.png',
'd': [1.0]}}
"""
