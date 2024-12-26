import bpy
from ..utils import get_material_object
from .. import properties
rigID = properties.rigID
category = properties.category
         
class UI_Header(bpy.types.Panel):
    bl_label = "Squared Media Rig"
    bl_idname = "OBJECT_PT_SquaredMediaHeader"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category


    def draw(self, context):
        layout = self.layout
        header = layout.box()
        header.label(text="SQM Rig", icon="RENDER_ANIMATION")
        
        rig = bpy.context.active_object  # Example: The active object is the rig
        Mat_obj = None
        if rig:
            Mat_obj = get_material_object(rig)

        if not context.active_object or context.active_object.get("rig_id") != rigID:
            error = layout.box()
            error.label(text="No Compatible Rig Selected!", icon = "ERROR")
            layout.operator("squaredmedia.link_rig", text="Spawn New Rig")
        
        if Mat_obj is None:
            error = layout.box()
            error.label(text="No Material Object Found!", icon = "ERROR")




