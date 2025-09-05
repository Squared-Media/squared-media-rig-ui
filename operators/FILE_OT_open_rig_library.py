import bpy
import os
import platform
import subprocess

from .. import properties


class FILE_OT_open_rig_library(bpy.types.Operator):
    bl_idname = "squaredmedia.open_rig_library"
    bl_label = "FILE_OT_open_rig_library"

    def execute(self, context):
        path = os.path.dirname(properties.Paths.default_lib_path)
        print(properties.Paths.default_lib_path)
        self.open_folder(path)
        
        return {"FINISHED"}



    def open_folder(self, path):
        """
        Opens the system file explorer at the given path.
        """
        path = os.path.abspath(path)

        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", path])
        else:  # Linux and other Unix-like
            subprocess.run(["xdg-open", path])