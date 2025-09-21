import bpy #type: ignore
import os
from ..msc.utils import find_collections_in_directory
from .. import properties


class SCENE_OT_RefreshRigList(bpy.types.Operator):
    bl_idname = "squaredmedia.load_rigs"
    bl_label = "Refresh Rig List"
    bl_description = "Refresh the list of rigs available for importing"
    

    def execute(self, context):
        scene = context.scene
        rig_props = scene.rigs

        # Clear the list
        rig_props.rigs.clear()

        addons = bpy.context.preferences.addons
        addon_preferences = properties.AddonProperties.module_name


        user_rig_list   = addons[addon_preferences].preferences.usr_file_path
        default_rig_dir = os.path.dirname(properties.Paths.default_lib_path)
        prefix          = addons[addon_preferences].preferences.lib_prefix
        user_rig_dict   = find_collections_in_directory(user_rig_list,prefix)

        rig_list = []

        default_rig_dict = find_collections_in_directory(default_rig_dir, prefix)

        # Then default rigs
        for name, path in default_rig_dict.items():
            rig_list.append((name, path, "COLLECTION_COLOR_07"))
 
        # First user rigs
        for name, path in user_rig_dict.items():
            rig_list.append((name, path, "COLLECTION_COLOR_05"))

       
        # Populate the rig list
        for rig in rig_list:
            rig_item = rig_props.rigs.add()
            rig_item.name = rig[0]
            rig_item.id = rig[1]
            rig_item.icon = rig[2]

        return {"FINISHED"}
