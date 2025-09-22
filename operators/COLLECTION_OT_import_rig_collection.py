import bpy  # type: ignore
import os
from .. import properties
from ..msc.utils import get_preferences

# this is a test


class COLLECTION_OT_import_rig_collection(bpy.types.Operator):
    """imports the skin, armature and boneshapes into the current file according to Default Import Options in the properties"""

    bl_idname = "squaredmedia.import_rig"
    bl_label = "Check Rig File"
    bl_description = "imports the skin, armature and boneshapes into the current file according to Default Import Options in the properties"
    bl_options = {"REGISTER", "UNDO"}

    collection_name: bpy.props.StringProperty(
        name="Collection Name", default="SQM Character Rig"
    )  # type: ignore
    rig_path: bpy.props.StringProperty(
        name="Rig Path", default=properties.Paths.default_lib_path
    )  # type: ignore

    invert = False

    def execute(self, context):
        # sanity checks
        if not self.sanity_checks():
            return {"CANCELLED"}

        preferences = get_preferences(context)
        import_method = preferences.DefaultImportOption

        method_map = {"LINK": self.link_rig, "APPEND": self.append_rig}

        if self.invert:
            method_map = {"LINK": self.append_rig, "APPEND": self.link_rig}
        import_function = method_map.get(import_method)

        if import_function is None:
            return {"CANCELLED"}

        import_function()

        return {"FINISHED"}

    def sanity_checks(self) -> bool:
        if not os.path.exists(self.rig_path):
            self.report({"ERROR"}, f"Blend file not found: {self.rig_path}")
            return False

        if bpy.data.filepath == self.rig_path:
            self.report({"ERROR"}, "cannot import rig into its own source file!")
            return False

        return True

    def link_rig(self):
        bpy.ops.wm.link(
            filepath=self.rig_path,
            directory=self.rig_path + "/Collection/",
            filename=self.collection_name,
        )
        bpy.ops.object.make_override_library()

    def append_rig(self):
        bpy.ops.wm.append(
            filepath=self.rig_path,
            directory=self.rig_path + "/Collection/",
            filename=self.collection_name,
        )

    def invoke(self, context, event):
        if event.alt:
            self.invert = True
        return self.execute(context)
