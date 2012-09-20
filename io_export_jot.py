#!BPY
#
# Blender export for JOT NPR render.

bl_info = {
    "name": "Jot Stylized Renderer (.jot)",
    "author": "Ragnar Brynjulfsson",
    "version": (0, 0, 0),
    "blender": (2, 6, 3),
    "location": "File > Import-Export > Jot Stylized Renderer (.jot)",
    "description": "Export to Jot, a WYSIWYG NPR interactive stylized renderer (.jot)",
    "category": "Import-Export"}

import bpy
from bpy_extras.io_utils import ExportHelper

class ExportJot(bpy.types.Operator, ExportHelper):
    bl_idname       = "jot_wysiwyg_renderer.jot";
    bl_label        = "Export JOT";
    bl_options      = {'PRESET'};
    
    filename_ext    = ".jot";
    
    def execute(self, context):
        # Writes the jot file to disk.
        self.file = open(self.filepath, 'w')
        self.file.write('#jot')
        self.file.write('\n\n')
        # Loop through the scene and find all meshes
        bpy.ops.object.mode_set(mode='OBJECT');
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                self.exportMesh(obj)
        # Close the file and finish.
        self.file.close()
        return {'FINISHED'}

    def exportMesh(self, obj):
        # Add a mesh to the file.
        self.file.write('TEXBODY {\n')
        self.file.write('  name  %s\n' % obj.name)
        self.file.write('  xform {{1 0 0 0}{0 1 0 0}{0 0 1 0}{0 0 0 1}}\n')
        self.file.write('  xdef  { DEFINER\n')
        self.file.write('    DEFINER {\n')
        self.file.write('      out_mask  1\n')
        self.file.write('      inputs    { }\n')
        self.file.write('    }\n')
        self.file.write('  }\n')
        self.file.write('  color {1 1 1}\n')
        self.file.write('  mesh_data {\n')
        self.file.write('    LMESH {\n')
        self.file.write('      vertices {{ ')
        for v in obj.data.vertices:
            self.file.write('{ %s %s %s }' % ( v.co.x, v.co.y, v.co.z ) )
        self.file.write('\n  }}\n')
        self.file.write('}\n')
        self.file.write('CREATE { %s }' % obj.name)

#CREATE	{ cactus_dancingCactus
        

def menu_func(self, context):
    self.layout.operator(ExportJot.bl_idname, text="Jot Stylized Renderer (.jot)");

def register():
    bpy.utils.register_module(__name__);
    bpy.types.INFO_MT_file_export.append(menu_func);
    
def unregister():
    bpy.utils.unregister_module(__name__);
    bpy.types.INFO_MT_file_export.remove(menu_func);

def write(filename):
    out = open(filename, "w")
    sce= bpy.data.scenes.active
    for ob in sce.objects:
        out.write(ob.type + ": " + ob.name + "\n")
    out.close()

if __name__ == "__main__":
    register()


#TEXBODY	{
#	name	cactus_dancingCactus
#	xform	{{1 0 0 0}{0 1 0 0}{0 0 1 0}{0 0 0 1}}
#	xfdef	{ DEFINER
#		DEFINER	{
#			out_mask	1
#			inputs	{ }
#			} }
#	color	{1 1 1}
#	mesh_data_file	{ cactus_dancingCactus.sm }
#	}
#CREATE	{ cactus_dancingCactus
#	}


