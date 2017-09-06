import os, pygame
import pymeshio.pmd.reader
#import pymeshio.pmx.reader
from OpenGL.GL import *
from OpenGL.GLU import *

class MMDloader:
    def __init__(self, model_path, path_name):
        self.model_obj=pymeshio.pmd.reader.read_from_file(model_path)
        self.vertices=[]
        self.mesh_face_indices=[]
        self.mesh_face_materials=[]
        self.used_vertices=set()
        self.normal = []
        self.tex_dir = path_name
        self.textureMap={}
        self.imageMap={}
        self.index=0
        self.gl_list=None
        self.mtl = {}
        self.mtl_name = []
        self.uv_array = []
        self.bone_index = []
        self.bone_weight = []
        self.bones = {}
        
        self.load_vertex()
        self.load_face()
        self.load_material()
        self.send_opengl()
        self.load_bone()

    def convert_coord(self, pos):
        """
        Left handed y-up to Right handed z-up
        """
        return (pos.x, pos.y, -pos.z)
        return (pos.x, pos.z, pos.y)

    def degenerate(self, i0, i1, i2):
        """
        縮退しているか？
        """
        return i0==i1 or i1==i2 or i2==i0

    def load_vertex(self):
        # リストの初期化
        del self.vertices[:]

        i=0
        # リストに頂点情報を代入
        for v in self.model_obj.each_vertex():
            self.vertices.append(self.convert_coord(v.pos))
            self.normal.append(self.model_obj.vertices[i].normal)
            i=i+1

        amari = len(self.vertices)%len(self.vertices[0])
        if amari == 0:
            loop_max = len(self.vertices)
        elif amari == 1:
            loop_max = len(self.vertices)-1
        elif amari == 2:
            loop_max = len(self.vertices)-2
        # UV座標
        for x in range(0, loop_max, len(self.vertices[0])):
            uv0 = self.model_obj.vertices[x].uv
            uv1 = self.model_obj.vertices[x+1].uv
            uv2 = self.model_obj.vertices[x+2].uv
            triangle=[uv0, uv1, uv2]
            for y in triangle:
                self.uv_array.append(y)
        for ss in range(amari):
            self.uv_array.append(self.model_obj.vertices[loop_max+ss])

    def load_face(self):
        # 各マテリアルの開始頂点インデックスを記録する
        face_map={}
        face_count=0
        for i, m in enumerate(self.model_obj.materials):
            face_map[i]=face_count
            face_count+=m.vertex_count
            
        for material_index, m in enumerate(self.model_obj.materials):
            face_offset=face_map[material_index]
            material_faces=self.model_obj.indices[face_offset:face_offset+m.vertex_count]

            for j in range(0, len(material_faces), 3):
                i0=material_faces[j]
                i1=material_faces[j+1]
                i2=material_faces[j+2]
                # flip
                #triangle=[i2, i1, i0]
                #triangle=[i2, i0, i1]
                #triangle=[i1, i2, i0]
                #triangle=[i1, i0, i2]
                #triangle=[i0, i1, i2]
                triangle=[i0, i2, i1]
                if self.degenerate(*triangle):
                    continue
                self.mesh_face_indices.append(triangle[0:3])
                self.mesh_face_materials.append(material_index)
                self.used_vertices.add(i0)
                self.used_vertices.add(i1)
                self.used_vertices.add(i2)

    def load_material(self):
        for material_index, m in enumerate(self.model_obj.materials):

            name="m_%02d" % material_index
            self.mtl[name] = {}
            self.mtl_name.append(name)
            
            # diffuse
            diffuse_color=[m.diffuse_color.r, m.diffuse_color.g, m.diffuse_color.b]
            self.mtl[name]["Kd"] = diffuse_color
            self.mtl[name]["Tr"] = m.alpha
            # specular
            specular_color=[m.specular_color.r, m.specular_color.g, m.specular_color.b]
            specular_toon_size=m.specular_factor * 0.1
            self.mtl[name]["Ks"] = specular_color
            # ambient
            mirror_color=[m.ambient_color.r, m.ambient_color.g, m.ambient_color.b]
            self.mtl[name]["Ka"] = mirror_color
            # flag
            #subsurface_scattering.use=True if m.edge_flag==1 else False
            #material.preview_render_type='FLAT'
            #material.use_transparency=True
  
            # main texture
            texture_name=m.texture_file.decode('cp932')
            if texture_name!='':
                for i, t in enumerate(texture_name.split('*')):
                    if t in self.textureMap:
                        texture=self.textureMap[t]
                    else:
                        path0=os.path.join(self.tex_dir, t)
                        print(t)
                        main_path = os.path.dirname(os.path.abspath( __file__ ))
                        #print(main_path)
                        path = os.path.join(main_path,path0)
                        print(path0)
                        self.mtl[name]['map_Kd'] = path
                        try:
                            #surf = pygame.image.load(t)
                            surf = pygame.image.load(path0)
                            image = pygame.image.tostring(surf, 'RGBA', True)
                            ix, iy = surf.get_rect().size
                        except:
                            # 日本語ファイルが読めないのでPILで読む
                            from PIL import Image
                            print("Import PIL")
                            #surf = Image.open(t, 'r')
                            surf = Image.open(path0, 'r')
                            image = surf.convert('RGBA').tobytes()
                            ix, iy = surf.size[0], surf.size[1]
                        texid = self.mtl[name]['texture_Kd'] = glGenTextures(1)
                        #texture, image=path, path
                        #self.textureMap[texture_name]=texture
                        #self.imageMap[material_index]=image
                        glMatrixMode(GL_TEXTURE)
                        glBindTexture(GL_TEXTURE_2D, texid)
                        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_LINEAR)
                        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_LINEAR)
                        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
                        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
                        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                            GL_UNSIGNED_BYTE, image)
                    #texture_index=bl.material.addTexture(material, texture)
                    if t.endswith('sph'):
                        # sphere map
                        print("sphere map")
                        #setSphereMap(material, texture_index)
                    elif t.endswith('spa'):
                        # sphere map
                        print("sphere map")
                        #setSphereMap(material, texture_index, 'ADD')
            self.index+=1
        #print(self.mtl)

    def load_bone(self):

        # create vertex group
        for v in self.model_obj.each_vertex():
            # bone weight
            w1=float(v.weight0)/100.0
            w2=1.0-w1
            self.bone_weight.append([w1,w2]) # 重みづけ
            self.bone_index.append([v.bone0, v.bone1]) # ボーンインデックス

        for b in self.model_obj.bones:
            name=b.name.decode('cp932')
            #print(name)
            position = b.pos
            #print(position)
            if b.parent_index!=0xFFFF:
                Pindex = b.parent_index
                #print("parent_index:{}".format(Pindex))
            if b.tail_index!=0 and b.tail_index!=0xFFFF and b.type!=pymeshio.pmd.Bone.TWEAK:
                #if b.tail_index!=0 and b.tail_index!=0xFFFF:
                tail=b.tail_index
                #print("tail:{}".format(tail))
  
        """
        # fix
        boneNameMap={}
        for b in self.model_obj.bones:
            name=pymeshio.englishmap.getEnglishBoneName(b.name.decode('cp932'))
            name=englishmap.getEnglishBoneName(b.name.decode('cp932'))
            if not name:
                name=b.name.decode('cp932')
            boneNameMap[name]=b
        for b in armature.bones.values():
            if boneNameMap[b.name].type==pmd.Bone.UNVISIBLE:
                b.hide=True
        """

        
        """
        # assign bone to group
        for b_index, g_index in self.model_obj.bone_display_list:
            # bone
            b=self.model_obj.bones[b_index]
            #print(b)
            bone_name=b.name.decode('cp932')
            #print(bone_name)
            # group
            g=self.model_obj.bone_group_list[g_index-1]
            group_name=self.get_group_name(g.name)
            #print(g)
            #print(group_name)
            #print("-----------------")
        """
        
        """
        for i, v, mvert in zip(range(len(self.model_obj.vertices)),self.model_obj.each_vertex(), 3):
            # bone weight
            w1=float(v.weight0)/100.0
            w2=1.0-w1
            #bl.object.assignVertexGroup(meshObject, get_bone_name(l, v.bone0),i,  w1)
            #bl.object.assignVertexGroup(meshObject, get_bone_name(l, v.bone1),i,  w2)
        """
        #print(self.vertex_groups)

    def get_bone_name(self, l, index):
        if index==-1:
            return l.bones[0].name.decode('cp932')
  
        if index < len(l.bones):
            #name=englishmap.getEnglishBoneName(l.bones[index].name.decode('cp932'))
            name=l.bones[index].name.decode('cp932')
            if name:
                return name
            return l.bones[index].name.decode('cp932')
        print('invalid bone index', index)
        return l.bones[0].name.decode('cp932')

    def get_group_name(self, g):
        #group_name=englishmap.getEnglishBoneGroupName(g.decode('cp932').strip())
        group_name=g.decode('cp932').strip()
        if not group_name:
            group_name=g.decode('cp932').strip()
        return group_name

    def send_opengl(self):
        #print(glGenLists(1))
        gl_list = glGenLists(1)
        glNewList(gl_list, GL_COMPILE)
        self.gl_list = gl_list
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        ind = 0
        for face in self.mesh_face_indices:
            mat_ind = self.mesh_face_materials[ind]
            #print(self.mtl_name[mat_ind])
            #mtl = self.mtl["m_01"]
            mtl = self.mtl[self.mtl_name[mat_ind]]
            mtlFlag = False
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
                mtlFlag = True
                glColor(*mtl['Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])
            
            glBegin(GL_POLYGON)
            for i in range(len(self.vertices[0])):
                #if normals[i] > 0:
                #    glNormal3fv(self.normals[normals[i] - 1])
                #if texture_coords[i] > 0:
                #    glTexCoord2fv(self.uv_array[face[i]])
                #print(self.uv_array[face[i]].x, self.uv_array[face[i]].y)
                #print(self.uv_array[face[i]][i].x)
                glNormal3f(self.normal[face[i]].x, self.normal[face[i]].y, self.normal[face[i]].z)
                if mtlFlag:
                    glTexCoord2f(self.uv_array[face[i]].x, self.uv_array[face[i]].y)
                glVertex3fv(self.vertices[face[i]])
            glEnd()
            ind = ind + 1
        glDisable(GL_TEXTURE_2D)
        glEndList()


def createPmdMaterial(m, index):
    material = bpy.data.materials.new("Material")
    # diffuse
    material.diffuse_shader='FRESNEL'
    material.diffuse_color=([m.diffuse_color.r, m.diffuse_color.g, m.diffuse_color.b])
    material.alpha=m.alpha
    # specular
    material.specular_shader='TOON'
    material.specular_color=([m.specular_color.r, m.specular_color.g, m.specular_color.b])
    material.specular_toon_size=m.specular_factor * 0.1
    # ambient
    material.mirror_color=([m.ambient_color.r, m.ambient_color.g, m.ambient_color.b])
    # flag
    material.subsurface_scattering.use=True if m.edge_flag==1 else False
    # other
    material.name="m_%02d" % index
    material.preview_render_type='FLAT'
    material.use_transparency=True
    return material
  
"""        
text0 = glGenTextures(1) #テクスチャ領域確保
mmd=MMDloader('レーシングミク2012_アノマロ5th.pmd')
print(mmd.vertices[8])
print(mmd.mesh_face_indices[8])
print(mmd.mesh_face_materials[2])
"""


# http://pythonhosted.org/pymeshio/
# http://nullege.com/codes/show/src@b@l@blenderpython-HEAD@scripts@addons_extern@blender26-meshio@export_pmx.py/78/pymeshio.pmx.Vertex
