import bpy
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

        user_rig_list   = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.usr_file_path
        prefix          = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.lib_prefix
        dictionary = find_collections_in_directory(user_rig_list,prefix)

        rig_list = [
            (properties.Paths.default_rig_collection_name,properties.Paths.default_lib_path, "COLLECTION_COLOR_02"),
        ]

        for collection_name, collection_path in dictionary.items():
            rig_list.append((collection_name, collection_path, "COLLECTION_COLOR_05"))

        # Populate the rig list
        for rig in rig_list:
            rig_item = rig_props.rigs.add()
            rig_item.name = rig[0]
            rig_item.id = rig[1]
            rig_item.icon = rig[2]

        return {"FINISHED"}
