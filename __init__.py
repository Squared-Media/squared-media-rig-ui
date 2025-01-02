#region
import bpy
from . import properties
from .ops.Snapper import OBJECT_OT_FK_to_IK_snapper  
from .operators import EXPERIMENTAL_OT_Null, IMAGE_OT_pack, IMAGE_OT_reload, OBJECT_OT_keyframe_all_properties, COLLECTION_OT_import_rig_collection, SCENE_OT_set_view_camera, SCENE_OT_reset_view_camera, UPDATE_OT_install_latest
from .ui.UIHeader import VIEW3D_PT_ui_Main
from .ui.VisibilitySettings import VIEW3D_PT_visibility_settings
from .ui.RigSettings import VIEW3D_PT_rig_settings, VIEW3D_PT_face_settings, VIEW3D_PT_arm_settings, VIEW3D_PT_body_settings, VIEW3D_PT_optimization_settings, VIEW3D_PT_leg_settings, VIEW3D_PT_roundness_settings
from .list import VIEW3D_PT_RigListPanel, RigListProperties, RigItem, RigListUI, SCENE_OT_RefreshRigList

bl_info = {
    "name": "Squared Media Rig UI Addon - EXPERIMENTAL",
    "description": "Adds RIG UI for Supported Rigs",
    "author": "Squared Media, Fxnarji",
    "version": (0, 2, 1),
    "blender": (4, 3, 2),
    "location": "Npanel > SQMDefaultRig",
    "support": "COMMUNITY",
    "category": "UI",
}

#endregion
class SQM_Rig_Preferences(bpy.types.AddonPreferences):
    bl_idname = "squared-media-rig-ui"
    __version__ = bl_info["version"]

    AppendOrLinkItems = [
        ('APPEND', "Append", "Use this if you want to modify the rig"),
        ('LINK', "Link", "Use this if you want to keep the rig as is"),
    ]

    SnappItems = [
        ('SMART', "Smart", "automatically places keyframes"),
        ('REGULAR', "Regular", "Normal IK / FK Snapping"),
    ]

    RigTabs = [
        ('SKIN', "Skin", "automatically places keyframes"),
        ('RIG', "Rig", "Normal IK / FK Snapping"),
        ('SETTINGS', "Misc", "Normal IK / FK Snapping"),
    ]
    DefaultImportOption: bpy.props.EnumProperty(
        name="Append or Link",  
        description="Choose whether to Append or Link the collection", 
        items=AppendOrLinkItems,  
        default='LINK'
    )#type: ignore
    
    Snapping: bpy.props.EnumProperty(
        name="Smart Snapping",  
        description="Choose whether to Append or Link the collection", 
        items=SnappItems,  
        default='SMART'
    )#type: ignore

    rigTab: bpy.props.EnumProperty(
        name="Rig Tab",
        description="Choose wich tab is open",
        items=RigTabs
    )                                                                         #type: ignore
    
    built_in_path: bpy.props.StringProperty(default=properties.Paths.default_lib_path)                                  #type: ignore

    CollectionName: bpy.props.StringProperty()                                                                          #type: ignore
    selected_index: bpy.props.IntProperty()                                                                             #type: ignore

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Default import preference")
        row.prop(self,"DefaultImportOption",expand=True)

        row = layout.row()
        row.label(text="Smart Snapping")
        row.prop(self,"Snapping",expand=True)




classes = [
        # Properties
        SQM_Rig_Preferences,
        RigItem,
        RigListProperties,
        RigListUI,

        # Operator classes
        SCENE_OT_RefreshRigList,
        IMAGE_OT_pack,
        IMAGE_OT_reload,

        SCENE_OT_set_view_camera,
        SCENE_OT_reset_view_camera,

        OBJECT_OT_FK_to_IK_snapper,
        OBJECT_OT_keyframe_all_properties,
        
        COLLECTION_OT_import_rig_collection,
        UPDATE_OT_install_latest,

        EXPERIMENTAL_OT_Null,

        # UI Classes
        VIEW3D_PT_ui_Main,
        VIEW3D_PT_visibility_settings,
        VIEW3D_PT_rig_settings,
        VIEW3D_PT_face_settings,
        VIEW3D_PT_arm_settings,
        VIEW3D_PT_body_settings,
        VIEW3D_PT_leg_settings,
        VIEW3D_PT_roundness_settings,
        VIEW3D_PT_optimization_settings,
        VIEW3D_PT_RigListPanel
    ]


#region
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
#endregion