#!BPY

import bpy
from mathutils import Vector, Euler
from math import tan, radians

class BuildJot():
    # Build a jot file.
    
    
    def __init__(self,context, filepath, anim, start, end):
        # Export Jot files(s) to disk.
        self.anim = anim
        self.start = start
        self.end = end
        self.filepath = filepath
        # Open file for writing.
        self.file = open(self.filepath, 'w')
        self.file.write('#jot\n')
        # Loop through the scene and find all meshes
        bpy.ops.object.mode_set(mode='OBJECT');
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                self.texbody(obj)
        # Export the camera settings.
        self.camera()
        # Set window and view size
        self.window()
        # Close the file and finish.
        self.file.close()


    def vertices(self, obj, file=False):
        # Write vertices to file.
        if not file:
            file = self.file
        file.write('      vertices {{ ')
        m = obj.to_mesh(bpy.context.scene, True, 'PREVIEW')
        for vert in m.vertices:
            file.write('{ %s %s %s }' % ( vert.co.x, vert.co.y, vert.co.z ) )
        file.write('  }}\n')
        m.user_clear()
        bpy.data.meshes.remove(m)


    def faces(self, obj, file=False):
        # Triangulate faces and write to file.
        if not file:
            file = self.file
        file.write('      faces {{ ')
        m = obj.to_mesh(bpy.context.scene, True, 'PREVIEW')
        for tface in m.tessfaces:
            vert_index = tface.vertices
            if len(vert_index) == 3:
                file.write('{ %s %s %s }' % ( vert_index[0], vert_index[1], vert_index[2] ) )
            else:
                file.write('{ %s %s %s }' % ( vert_index[0], vert_index[1], vert_index[2] ) )
                file.write('{ %s %s %s }' % ( vert_index[0], vert_index[2], vert_index[3] ) )
        file.write('  }}\n')
        m.user_clear()
        bpy.data.meshes.remove(m)

    def creases(self, obj, file=False):
        # Write creased edges to file.
        if not file:
            file = self.file
        file.write('       creases {{ ')
        for edge in obj.data.edges:
            if edge.crease > 0.0:
                file.write('{ %s %s }' % ( edge.vertices[0], edge.vertices[1] ) )
        file.write('  }}\n')

    def uvs(self, obj, file=False):
        # Write UV's to file.
        if not file:
            file = self.file
        try:
            file.write('       texcoords2 {{ ')
            m = obj.to_mesh(bpy.context.scene, True, 'PREVIEW')
            face_count = 0
            # This fails if object has no UV's.
            for tex_face in m.tessface_uv_textures.active.data:
                uvs = tex_face.uv
                if len(uvs) == 3:
                    file.write('{ %s { %s %s }{ %s %s }{ %s %s } }' % ( face_count, uvs[0][0], uvs[0][1], uvs[1][0], uvs[1][1], uvs[2][0], uvs[2][1] ) )
                    face_count += 1
                else:
                    file.write('{ %s { %s %s }{ %s %s }{ %s %s } }' % ( face_count, uvs[0][0], uvs[0][1], uvs[1][0], uvs[1][1], uvs[2][0], uvs[2][1] ) )
                    face_count += 1
                    file.write('{ %s { %s %s }{ %s %s }{ %s %s } }' % ( face_count, uvs[0][0], uvs[0][1], uvs[2][0], uvs[2][1], uvs[3][0], uvs[3][1] ) )
                    face_count += 1
            file.write(' }}\n')
            m.user_clear()
            bpy.data.meshes.remove(m)
        except:
            file.write(' }}\n')


    def texbody(self, obj):
        # Write the TEXBODY for obj to file.
        self.file.write('\nTEXBODY {\n')
        self.file.write('  name  %s\n' % obj.name)
        self.file.write('  xform {{%s %s %s %s}{%s %s %s %s}{%s %s %s %s}{0 0 0 1}}\n' % ( \
                obj.matrix_local[0][0], obj.matrix_local[0][1], obj.matrix_local[0][2], obj.matrix_local[0][3], \
                obj.matrix_local[1][0], obj.matrix_local[1][1], obj.matrix_local[1][2], obj.matrix_local[1][3], \
                obj.matrix_local[2][0], obj.matrix_local[2][1], obj.matrix_local[2][2], obj.matrix_local[2][3] ))
        self.file.write('  xfdef  { DEFINER\n')
        self.file.write('    DEFINER {\n')
        self.file.write('      out_mask  1\n')
        self.file.write('      inputs    { }\n')
        self.file.write('    }\n')
        self.file.write('  }\n')
        self.file.write('  color {1 1 1}\n')
        self.file.write('  mesh_data {\n')
        self.file.write('    LMESH {\n')
        obj.data.update(calc_tessface=True)
        # Vertices
        self.vertices(obj)
        # Faces
        self.faces(obj)
        # Creases
        self.creases(obj)
        # UV's
        self.uvs(obj)
        # Closing LMESH, mesh_data and TEXBODY and creating it.
        self.file.write('    }\n')
        self.file.write('  }\n')
        self.file.write('}\n')
        self.file.write('CREATE { %s }\n\n' % obj.name)

    def camera(self):
        # Write the camera to file. TODO! Does not work correctly.
        cam = bpy.context.scene.camera
        self.file.write('\nCHNG_CAM {\n')
        # from_point
        from_point = cam.matrix_world.col[3]
        self.file.write('{ %s %s %s }' % ( from_point.x, from_point.y, from_point.z ) )
       # at_point
        at_point = cam.matrix_world.col[2]
        at_point = at_point * -1
        at_point = at_point + from_point
        self.file.write('{ %s %s %s }' % ( at_point.x, at_point.y, at_point.z ) )
        # up_point
        up_point = cam.matrix_world.col[1]
        up_point = up_point + from_point
        self.file.write('{ %s %s %s }' % ( up_point.x, up_point.y, up_point.z ) )
        # center_point (that the camera will rotate about).
        self.file.write('{ %s %s %s }' % ( at_point.x, at_point.y, at_point.z ) )
        # focal length ( 0.1/2 / tan(x/2) = F ) 
        # TODO! Incorrect formula.
        focal_length = 0.1/2 / tan(radians(cam.data.angle)/2)
        # focal length, perspective, inter-ocular distance (not used)
        self.file.write(' %s 1 2.25 }\n' % ( 0.2 ) )
        
                
    def window(self):
        # Set the window size, based on the resolution in blender.
        scene = bpy.context.scene
        width  = int(scene.render.resolution_x * scene.render.resolution_percentage / 100)
        height = int(scene.render.resolution_y * scene.render.resolution_percentage / 100)
        self.file.write('CHNG_WIN { 32 32 %s %s }\n' % ( width, height ) )

    def unused(self):
        pass
        # CAMERA & VIEW
        # Export Camera
        # TODO! Aim at location, up vector and field of view.
        # TODO! Camera is seemingly pointing in the right direction, but model is facing differently. Find out what axis jot is using for up.
        # Set Windows size TODO! Don't know if this is needed.
        #self.file.write('CHNG_WIN { 30 34 480 580 }\n')
        # Set the View TODO! Don't know if this is needed, and insert correct data.
        #self.file.write('CHNG_VIEW {\n')
        #self.file.write('  VIEW {\n')
        #self.file.write('    view_animator {\n')
        #self.file.write('      Animator {\n')
        #self.file.write('        fps            -1\n')
        #self.file.write('        start_frame    -1\n')
        #self.file.write('        end_frame      -1\n')
        #self.file.write('        name { NULL_STR } \n')
        #self.file.write('      }\n')
        #self.file.write('    }\n')
        #self.file.write('    view_data_file { NULL_STR }\n')
        #self.file.write('  }\n')
        #self.file.write('}\n')
                
