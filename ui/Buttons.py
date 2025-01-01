import bpy
from .. import properties

rigID = properties.RigProperties.rigID
category = properties.UIProperties.category


class VIEW3D_PT_buttons(bpy.types.Panel):
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
    

        if bpy.context.space_data.lock_camera:
            HelperBox.operator("squaredmedia.reset_camera", text = "End Face Anim")
        else:
            HelperBox.operator("squaredmedia.set_camera", text = "Start Face Anim")

