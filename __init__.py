import bpy
import tomllib
import os

#Operators
from .operators.OBJECT_OT_FK_to_IK_snapper            import OBJECT_OT_FK_to_IK_snapper  
from .operators.SCENE_OT_Open_Preset                  import SCENE_OT_Open_Preset, ConfirmOpenBlendFileOperator
from .operators.IMAGE_OT_                             import IMAGE_OT_pack, IMAGE_OT_reload
from .operators.SCENE_OT_RefreshRigList               import SCENE_OT_RefreshRigList
from .operators.OBJECT_OT_keyframe_all_properties     import OBJECT_OT_keyframe_all_properties
from .operators.EXPERIMENTAL_                         import EXPERIMENTAL_OT_Null, EXPERIMENTAL_OT_set_pose
from .operators.OBJECT_OT_keyframe_all_properties     import OBJECT_OT_keyframe_all_properties
from .operators.COLLECTION_OT_import_rig_collection   import COLLECTION_OT_import_rig_collection
from .operators.SCENE_OT_toggle_face_camera           import SCENE_OT_toggle_face_camera

#UI
from .panels.VIEW3D_PT_ui_Main                        import VIEW3D_PT_ui_Main
from .panels.VIEW3D_PT_VisibilitySettings             import VIEW3D_PT_visibility_settings
from .panels.VIEW3D_CameraGizmo                       import VIEW3D_CameraGizmo
from .panels.VIEW3D_PT_RigListPanel                   import VIEW3D_PT_RigListPanel
from .panels.MyFancyPanel                             import TestPanel

#misc       
from .msc.DATA_list_setup                             import RigListProperties, RigItem, RigListUI
from .msc.Preferences                                 import SQM_Rig_Preferences


toml_path = os.path.join(os.path.dirname(__file__), "blender_manifest.toml")
with open(toml_path, "rb") as f:
    manifest = tomllib.load(f)
version_str = manifest.get("version", "0.0.0")
version_tuple = tuple(int(x) for x in version_str.split("."))


bl_info = {
    "name": "Squared Media Rig UI Addon",
    "description": "Adds RIG UI for Supported Rigs",
    "author": "Squared Media, Fxnarji",
    "version": version_tuple, 
    "blender": (4, 3, 2),
    "location": "Npanel > SQMDefaultRig",
    "support": "COMMUNITY",
    "category": "UI",
}

classes = [
        # Properties
        SQM_Rig_Preferences,
        RigItem,
        RigListUI,
        RigListProperties,

        # Operator classes
        IMAGE_OT_pack,
        IMAGE_OT_reload,
        
        ConfirmOpenBlendFileOperator,

        SCENE_OT_Open_Preset,
        SCENE_OT_RefreshRigList,
        SCENE_OT_toggle_face_camera,

        OBJECT_OT_FK_to_IK_snapper,
        OBJECT_OT_keyframe_all_properties,
        
        COLLECTION_OT_import_rig_collection,

        EXPERIMENTAL_OT_Null,
        EXPERIMENTAL_OT_set_pose,

        # UI Classes
        VIEW3D_PT_RigListPanel,
        VIEW3D_PT_visibility_settings,
        VIEW3D_PT_ui_Main,
        VIEW3D_CameraGizmo,
        #TestPanel
    ]

def load_rigs(scene):
    bpy.ops.squaredmedia.load_rigs()
    print("Rigs Loaded")

def register():
    for i in classes:
        bpy.utils.register_class(i)

    bpy.types.Scene.rigs = bpy.props.PointerProperty(type=RigListProperties)

    bpy.app.handlers.load_post.append(load_rigs)

def unregister():
    for i  in reversed(classes):
        bpy.utils.unregister_class(i)
    
    del bpy.types.Scene.rigs

    if load_rigs in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_rigs)

if __name__ == "__main__":
    register()