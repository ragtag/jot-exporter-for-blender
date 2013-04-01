#!BPY

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# LIMITATIONS!
# - Exporting crease info will not work on multires or subdiv models. It will only export the crease info for the edge in the basemesh. This is not a limit of the exporter, but of how creases and subdivs are handled. The workaround is to Apply subdiv modifiers, and add creases to the subdivided mesh.
# - Rendering to file does not work when you export without animation. As a workaround you can export a single frame of animation.

# RUNNING JOT ON LINUX USING WINE
# - Modify jot/batch/jot-config.bat so that JOT_ROOT points to where jot is installed in wine (e.g. C:\jot if installed in ~/.wine/drvie_c/jot).
# - Run cmd.exe in wine (e.g. wine /usr/lib/i386-linux-gnu/wine/fakedlls/cmd.exe )
# - cd to jot/batch and run jot-config.bat from cmd.exe
# - Go to where your .jot file is
# - Run jot (jotq myJotFile.jot )
# - Sometimes on quitting jot the cmd.exe will seem to hang. Use Ctrl-Z to put it in the background, and fg to put it back in the foreground. Now you should be able to type new commmands.
# - Yes its hacky and complicated. :)

bl_info = {
    "name": "Export to Jot Stylized Renderer (.jot)",
    "author": "Ragnar Brynjulfsson",
    "version": (0, 9, 0),
    "blender": (2, 6, 6),
    "location": "File > Import-Export > Jot Stylized Renderer (.jot)",
    "description": "Export selected models to Jot, a WYSIWYG NPR interactive stylized renderer (.jot)",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}

if "bpy" in locals():
    import imp
    if "export_jot" in locals():
        imp.reload(export_jot)

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
            default=False)
    start = IntProperty(
            name="Start Frame",
            description="Starting frame for the animation",
            default=1
            )
    end   = IntProperty(
            name="End Frame",
            description="End frame for the animation",
            default=100
            )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        from . import export_jot
        builder = export_jot.BuildJot(context, self.filepath, self.anim, self.start, self.end)
        return {'FINISHED'}

    def invoke(self, context, event):
        # Extend ExportHelper invoke function to support dynamic default values (thanks to CoDEmanX)
        self.start = context.scene.frame_start
        self.end = context.scene.frame_end
        return super().invoke(context, event)


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


