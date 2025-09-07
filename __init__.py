import bpy
from .msc.utils import get_toml_version

#Operators
from .operators.FILE_OT_load_config                import FILE_OT_LoadJsonConfig
from .operators.FILE_OT_save_config              import FILE_OT_SaveConfigAsTomlOperator
from .operators.FILE_OT_NameCharacter                 import FILE_OT_NameCharacter
from .operators.COLLECTION_OT_import_rig_collection   import COLLECTION_OT_import_rig_collection
from .operators.SCENE_OT_Open_Preset                  import SCENE_OT_Open_Preset, ConfirmOpenBlendFileOperator
from .operators.SCENE_OT_toggle_face_camera           import SCENE_OT_toggle_face_camera
from .operators.SCENE_OT_RefreshRigList               import SCENE_OT_RefreshRigList
from .operators.IMAGE_OT_                             import IMAGE_OT_pack, IMAGE_OT_reload
from .operators.OBJECT_OT_keyframe_all_properties     import OBJECT_OT_keyframe_all_properties
from .operators.OBJECT_OT_FK_to_IK_snapper            import OBJECT_OT_FK_to_IK_snapper  
from .operators.OBJECT_OT_keyframe_all_properties     import OBJECT_OT_keyframe_all_properties
from .operators.Dummy_OT_DummyOperator                import DummyOperator
from .operators.EXPERIMENTAL_                         import EXPERIMENTAL_OT_Null, EXPERIMENTAL_OT_set_pose
from .operators.FILE_OT_open_rig_library              import FILE_OT_open_rig_library

#UI
from .panels.VIEW3D_PT_ui_Main                        import VIEW3D_PT_ui_Main
from .panels.VIEW3D_PT_VisibilitySettings             import VIEW3D_PT_visibility_settings
from .panels.VIEW3D_CameraGizmo                       import VIEW3D_CameraGizmo
from .panels.VIEW3D_PT_RigListPanel                   import VIEW3D_PT_RigListPanel
from .panels.MyFancyPanel                             import TestPanel

#misc       
from .msc.DATA_list_setup                             import RigListProperties, RigItem, RigListUI
from .msc.Preferences                                 import SQM_Rig_Preferences
from .msc.IMG_load_icons                              import load_icons, unload_icons

version_tuple = get_toml_version()

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
        DummyOperator,

        FILE_OT_open_rig_library,
        
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
        TestPanel,

        #File Classes
        FILE_OT_SaveConfigAsTomlOperator,
        FILE_OT_LoadJsonConfig,
        FILE_OT_NameCharacter,
    ]

def load_rigs(scene):
    bpy.ops.squaredmedia.load_rigs()
    print("Rigs Loaded")

def register():
    for i in classes:
        bpy.utils.register_class(i)

    bpy.types.Scene.rigs = bpy.props.PointerProperty(type=RigListProperties)

    bpy.app.handlers.load_post.append(load_rigs)
    
    load_icons()

def unregister():
    for i  in reversed(classes):
        bpy.utils.unregister_class(i)
    
    del bpy.types.Scene.rigs

    if load_rigs in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_rigs)

    unload_icons()

if __name__ == "__main__":
    register()