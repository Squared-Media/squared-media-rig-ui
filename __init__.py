import bpy
from .operators import IMAGE_OT_pack, IMAGE_OT_reload, OBJECT_OT_keyframe_all_properties, COLLECTION_OT_import_rig_collection, SCENE_OT_set_view_camera, SCENE_OT_reset_view_camera, UPDATE_OT_install_latest
from .ui.UIHeader import VIEW3D_PT_ui_Header
from .ui.SkinSettings import VIEW3D_PT_skin_settings
from .ui.Buttons import VIEW3D_PT_buttons
from .ui.VisibilitySettings import VIEW3D_PT_visibility_settings
from .ui.RigSettings import VIEW3D_PT_rig_settings, VIEW3D_PT_face_settings, VIEW3D_PT_arm_settings, VIEW3D_PT_body_settings, VIEW3D_PT_optimization_settings, VIEW3D_PT_leg_settings, VIEW3D_PT_retargeting_settings, VIEW3D_PT_roundness_settings

bl_info = {
    "name": "Squared Media Rig UI Addon",
    "description": "Adds RIG UI for Supported Rigs",
    "author": "Squared Media, Fxnarji",
    "version": (0, 1, 3),
    "blender": (4, 3, 2),
    "location": "Npanel > SQMDefaultRig",
    "support": "COMMUNITY",
    "category": "UI",
}

class SQM_Rig_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    __version__ = bl_info["version"]

    AppendOrLinkItems = [
        ('APPEND', "Append", "Append the collection"),
        ('LINK', "Link", "Link the collection"),
    ]
    DefaultImportOption: bpy.props.EnumProperty(
        name="Append or Link",  
        description="Choose whether to Append or Link the collection", 
        items=AppendOrLinkItems,  
        default='LINK'
    )#type: ignore

    CollectionName: bpy.props.StringProperty(default="SQM Character Rig")#type: ignore

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Default import preference")
        row.prop(self,"DefaultImportOption",expand=True)
        

classes = [
        # Properties
        SQM_Rig_Preferences,

        # Operator classes
        IMAGE_OT_pack,
        IMAGE_OT_reload,

        SCENE_OT_set_view_camera,
        SCENE_OT_reset_view_camera,

        OBJECT_OT_keyframe_all_properties,
        COLLECTION_OT_import_rig_collection,
        UPDATE_OT_install_latest,

        # UI Classes
        VIEW3D_PT_ui_Header,
        VIEW3D_PT_skin_settings,
        VIEW3D_PT_buttons,
        VIEW3D_PT_visibility_settings,
        VIEW3D_PT_rig_settings,
        VIEW3D_PT_face_settings,
        VIEW3D_PT_arm_settings,
        VIEW3D_PT_body_settings,
        VIEW3D_PT_leg_settings,
        VIEW3D_PT_roundness_settings,
        VIEW3D_PT_optimization_settings,
        VIEW3D_PT_retargeting_settings
    ]

def register():
    for i in classes:
        bpy.utils.register_class(i)
        
def unregister():
    for i  in reversed(classes):
        bpy.utils.unregister_class(i)

if __name__ == "__main__":
    register()
