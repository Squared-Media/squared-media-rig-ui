import bpy
from .. import properties

rigID = properties.rigID
category = properties.category


class ButtonsUI(bpy.types.Panel):
    bl_label = "Buttons"
    bl_idname = "OBJECT_PT_SquaredMediaButtons"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category

    @classmethod
    def poll(self, context):
        obj = context.active_object
        return obj and obj.get("rig_id") == rigID
    
    def draw(self, context):
        layout = self.layout
        HelperBox = layout.box()
        HelperBox.label(text="Helper")
        HelperBox.operator("squaredmedia.keyframe_all_custom_properties")
        HelperBox.operator("squaredmedia.link_rig", text="Spawn New Rig")
