#!BPY

bl_info = {
    "name": "Jot Stylized Renderer (.jot) - beta",
    "author": "Ragnar Brynjulfsson",
    "version": (0, 0, 0),
    "blender": (2, 6, 3),
    "location": "File > Import-Export > Jot Stylized Renderer (.jot)",
    "description": "Export to Jot, a WYSIWYG NPR interactive stylized renderer (.jot)",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}

if "bpy" in locals():
    import imp
    if "io_export_jot" in locals():
        imp.reload(io_export_jot)

import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.props import IntProperty
from bpy.props import BoolProperty


class ExportJot(Operator, ExportHelper):
    # Export the file to .jot, readable by Jot WYSIWIG stylistic rendere.
    bl_idname       = "jot_wysiwyg_renderer.jot";
    bl_label        = "Export JOT";
    bl_options      = {'PRESET'};

    filename_ext    = ".jot";

    filter_glob = StringProperty(default="*.jot", options={'HIDDEN'})
    anim = BoolProperty(
            name="Export animation",
            description="Export animation, not just model.",
            default=True)
    start = IntProperty(
            name="Start Frame",
            description="Starting frame for the animation",
            default=bpy.context.scene.frame_start,
            )
    end   = IntProperty(
            name="End Frame",
            description="End frame for the animation",
            default=bpy.context.scene.frame_end,
            )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        from . import export_jot
        builder = export_jot.BuildJot(context, self.filepath, self.anim, self.start, self.end)
        return {'FINISHED'}



def menu_func(self, context):
    self.layout.operator(ExportJot.bl_idname, text="Jot Stylized Renderer (.jot)");

def register():
    bpy.utils.register_module(__name__);
    bpy.types.INFO_MT_file_export.append(menu_func);

def unregister():
    bpy.utils.unregister_module(__name__);
    bpy.types.INFO_MT_file_export.remove(menu_func);


if __name__ == "__main__":
    register()


# TODO!
# - Add support for animation.
# - Test with a riggeed and animated character.
# - Fix the camera.
# - Add support for exporting model, while keeping Jot annotation.
# - Learn how to use Jot. :)
# - Compile the damn thing on 64bit Linux. :P

# LIMITATIONS!
# - Exporting crease info will not work on multires or subdiv models. It will only export the crease info for the edge in the basemesh. This is not a limit of the exporter, but of how creases and subdivs are handled. The workaround is to Apply subdiv modifiers, and add creases to the subdivided mesh.
