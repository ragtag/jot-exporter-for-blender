#!BPY

import bpy
import os.path
from mathutils import Vector, Euler
from math import tan, radians
from bpy_extras.io_utils import axis_conversion

class BuildJot():
    # Build a jot file.
    
    
    def __init__(self,context, filepath, anim, start, end, y_correct):
        # Export Jot files(s) to disk.
        self.anim = anim
        self.start = start
        self.end = end
        self.y_correct = y_correct
        
        self.filepath = filepath
        self.basepath = os.path.splitext(filepath)[0]
        self.basename = os.path.splitext(os.path.basename(filepath))[0]
        # Open file for writing.
        self.file = open(self.filepath, 'w')
        self.file.write('#jot\n')
        # Loop through the scene and find all meshes.
        bpy.ops.object.mode_set(mode='OBJECT');
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                self.texbody(obj, self.file, self.filepath)
        # Export the camera settings.
        self.camera(self.file)
        # Set window and view size
        self.window()
        # Create the view settings.
        self.view()
        # Close the file and finish.
        self.file.close()
        # Export animation data
        current = bpy.context.scene.frame_current
        if self.anim:
            for i in range(self.start, self.end+1):
                bpy.context.scene.frame_set(i)
                filepath = ('%s[%05d].jot' % (self.basepath, i) )
                file = open(filepath, 'w')
                file.write('#jot\n')
                for obj in bpy.context.scene.objects:
                    if obj.type == 'MESH':
                        self.texbody(obj, file, filepath, True)
                self.camera(file)
                file.close()

    def vertices(self, obj, file):
        # Write vertices to file.
        file.write('      vertices {{ ')
        depsgraph = bpy.context.evaluated_depsgraph_get()
        m = obj.evaluated_get(depsgraph)
        for vert in m.data.vertices:
            file.write('{ %s %s %s }' % ( vert.co.x, vert.co.y, vert.co.z ) )
        file.write('  }}\n')
        m.user_clear()
        obj.to_mesh_clear()


    def faces(self, obj, file):
        # Triangulate faces and write to file.
        file.write('      faces {{ ')
        depsgraph = bpy.context.evaluated_depsgraph_get()
        m = obj.evaluated_get(depsgraph)
        for tface in m.data.polygons:
            vert_index = tface.vertices
            if len(vert_index) == 3:
                file.write('{ %s %s %s }' % ( vert_index[0], vert_index[1], vert_index[2] ) )
            else:
                file.write('{ %s %s %s }' % ( vert_index[0], vert_index[1], vert_index[2] ) )
                file.write('{ %s %s %s }' % ( vert_index[0], vert_index[2], vert_index[3] ) )
        file.write('  }}\n')
        m.user_clear()
        obj.to_mesh_clear()

    def creases(self, obj, file):
        # Write creased edges to file.
        file.write('       creases {{ ')
        for edge in obj.data.edges:
            if edge.crease > 0.0:
                file.write('{ %s %s }' % ( edge.vertices[0], edge.vertices[1] ) )
        file.write('  }}\n')

    def uvs(self, obj, file):
        # Write UV's to file.
        try:
            file.write('       texcoords2 {{ ')
            depsgraph = bpy.context.evaluated_depsgraph_get()
            m = obj.evaluated_get(depsgraph)
            face_count = 0
            # This fails if object has no UV's.
            for tex_face in m.data.polygons.tessface_uv_textures.active.data:
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
            obj.to_mesh_clear()
        except:
            file.write(' }}\n')

    def patch(self, obj, file):
        # Write npr shader data to file.
        file.write('       patch {\n')
        file.write('         Patch {\n')
        file.write('           cur_tex     0\n')
        file.write('           patchname     patch-0\n')
        file.write('           texture {\n')
        file.write('             NPRTexture {\n')
        file.write('               npr_data_file { %s_%s }\n' % ( self.basename, obj.name ) )
        file.write('             }\n')
        file.write('           }\n')
        file.write('         }\n') 
        file.write('       }\n')


    def texbody(self, obj, file, filepath, update=False):
        # Write the TEXBODY for obj to file.
        if update:
            file.write('\nUPDATE_GEOM { %s' % obj.name)
        file.write('\nTEXBODY {\n')
        file.write('  name  %s\n' % obj.name)
        if self.y_correct:
            temp_matrix = axis_conversion(from_forward = '-Y', from_up = 'Z', to_forward = 'Z', to_up = 'Y').to_4x4() @ obj.matrix_world
        else:
            temp_matrix = obj.matrix_world
        file.write('  xform {{%s %s %s %s}{%s %s %s %s}{%s %s %s %s}{0 0 0 1}}\n' % ( \
                temp_matrix[0][0], temp_matrix[0][1], temp_matrix[0][2], temp_matrix[0][3], \
                temp_matrix[1][0], temp_matrix[1][1], temp_matrix[1][2], temp_matrix[1][3], \
                temp_matrix[2][0], temp_matrix[2][1], temp_matrix[2][2], temp_matrix[2][3] ))
        file.write('  xfdef  { DEFINER\n')
        file.write('    DEFINER {\n')
        file.write('      out_mask  1\n')
        file.write('      inputs    { }\n')
        file.write('    }\n')
        file.write('  }\n')
        file.write('  color {1 1 1}\n')
        if self.anim:
            smfilename = ( '%s_%s.sm' % ( self.basename, obj.name ) )
            if update:
                smfilename = ( '%s_%s[%05d].sm' % ( self.basename, obj.name, bpy.context.scene.frame_current ) )
            smfilepath = os.path.join(os.path.split(filepath)[0], smfilename)
            if update:
                file.write('  mesh_data_update_file { %s }' % smfilename)
            else:
                file.write('  mesh_data_file { %s }' % smfilename)                
            smfile = open(smfilepath, 'w')
            smfile.write('    LMESH {\n')
            self.vertices(obj, smfile)
            if not update:
                self.faces(obj, smfile)
                self.creases(obj, smfile)
                self.uvs(obj, smfile)
                self.patch(obj, smfile)
            smfile.write('    }\n')
            smfile.close()
        else:
            file.write('  mesh_data {\n')
            file.write('    LMESH {\n')
            obj.data.update(calc_edges=True)
            # Vertices
            self.vertices(obj, file)
            # Faces
            self.faces(obj, file)
            # Creases
            self.creases(obj, file)
            # UV's
            self.uvs(obj, file)
            # Patch NPR data
            self.patch(obj, file)
            # Closing LMESH, mesh_data and TEXBODY and creating it.
            file.write('    }\n')
            file.write('  }\n')
        file.write('}\n')
        if update:
            file.write('}\n')
        else:
            file.write('CREATE { %s }\n\n' % obj.name)

    def camera(self, file):
        # Write the camera to file.
        cam = bpy.context.scene.camera
        if not cam:
            return False
        file.write('\nCHNG_CAM {\n')
        # from_point
        if self.y_correct:
            from_point = (axis_conversion(from_forward = '-Y', from_up = 'Z', to_forward = 'Z', to_up = 'Y').to_4x4() @ cam.matrix_world).col[3]
        else:
            from_point = cam.matrix_world.col[3]
        file.write('{ %s %s %s }' % ( from_point.x, from_point.y, from_point.z ) )
       # at_point
        if self.y_correct:
            at_point = (axis_conversion(from_forward = '-Y', from_up = 'Z', to_forward = 'Z', to_up = 'Y').to_4x4() @ cam.matrix_world).col[2]
        else:
            at_point = cam.matrix_world.col[2]
        at_point = at_point * -1
        at_point = at_point + from_point
        file.write('{ %s %s %s }' % ( at_point.x, at_point.y, at_point.z ) )
        # up_point
        if self.y_correct:
            up_point = (axis_conversion(from_forward = '-Y', from_up = 'Z', to_forward = 'Z', to_up = 'Y').to_4x4() @ cam.matrix_world).col[1]
        else:
            up_point = cam.matrix_world.col[1]
        up_point = up_point + from_point
        file.write('{ %s %s %s }' % ( up_point.x, up_point.y, up_point.z ) )
        # center_point (that the camera will rotate about).
        file.write('{ %s %s %s }' % ( at_point.x, at_point.y, at_point.z ) )
        # focal length ( 0.1/2 / tan(x/2) = F ) 
        scene = bpy.context.scene
        focal_length = 0.1/2 / tan(cam.data.angle/2)
        # Blender uses width to calculate angle of view, while jot uses the shortes of width and height.
        aspect = scene.render.resolution_x / scene.render.resolution_y
        if aspect > 1:
            focal_length = focal_length * ( scene.render.resolution_x / scene.render.resolution_y )
            file.write(' %s 1 2.25 }\n' % ( focal_length ) )
        else:
            focal_length = focal_length * ( scene.render.resolution_y / scene.render.resolution_x )
            file.write(' %s 1 2.25 }\n' % ( focal_length ) )
        # The second to last value is perspective/orthographic. The exporter doesn't support ortographics cameras yet.
        # The last value is interocular distance for 3D cameras, which is not used by jot.
                
    def window(self):
        # Set the window size, based on the resolution in blender.
        scene = bpy.context.scene
        width  = int(scene.render.resolution_x * scene.render.resolution_percentage / 100)
        height = int(scene.render.resolution_y * scene.render.resolution_percentage / 100)
        self.file.write('CHNG_WIN { 32 32 %s %s }\n' % ( width, height ) )

    def view(self):
        # Defines the view, such as frame range and background.
        self.file.write('CHNG_VIEW {\n')
        self.file.write('  VIEW {\n')
        self.file.write('    view_animator {\n')
        self.file.write('      Animator {\n')
        if self.anim:
            self.file.write('        fps            %s\n' % bpy.context.scene.render.fps)
            self.file.write('        start_frame    %s\n' % self.start)
            self.file.write('        end_frame      %s\n' % self.end)
            self.file.write('        name { %s } \n' % self.basename)
        else:
            self.file.write('        fps            -1\n')
            self.file.write('        start_frame    -1\n')
            self.file.write('        end_frame      -1\n')
            self.file.write('        name { NULL_STR } \n')
        self.file.write('      }\n')
        self.file.write('    }\n')
        # TODO! This causes view data to be written to the .jot file, and not a .view file. Don't know if this is important.
        self.file.write('    view_data_file { NULL_STR }\n')
        self.file.write('  }\n')
        self.file.write('}\n')
            
