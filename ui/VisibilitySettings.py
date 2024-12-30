import bpy
from .. import properties

rigID = properties.RigProperties.rigID
category = properties.UIProperties.category

class VIEW3D_PT_visibility_settings(bpy.types.Panel):
    bl_label = "Visibility Settings"
    bl_idname = "OBJECT_PT_SquaredMediaVisibility"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return obj and obj.get("rig_id") == rigID
    def draw(self, context):
        rig = bpy.context.active_object
        
        layout = self.layout
        layers = rig.data.collections_all



        # Body Visibility
        BodyBox = layout.box()
        BodyBox.label(text="Body Visibility")
        col = BodyBox.column()
        col.prop(rig.data.collections_all["Face"], "is_visible", text="Face Bones", toggle=True)
        col.prop(layers["Menu"], "is_visible", text="Menu", toggle=True)   
        col.prop(layers["Debug"], "is_visible", text="Debug", toggle=True, icon = "SETTINGS")

        # IK Visibility
        box = layout.box()
        box.label(text="IK Visibility")
        
        #Arms
        row = box.row(align=True)
        row.prop(layers["IK Arm L"], "is_visible", text="IK Arm L", toggle=True)
        row.prop(layers["IK Arm R"], "is_visible", text="IK Arm R", toggle=True)
        
        #Legs
        row = box.row(align=True)
        row.prop(layers["IK Leg L"], "is_visible", text="IK Leg L", toggle=True)
        row.prop(layers["IK Leg R"], "is_visible", text="IK Leg R", toggle=True)
        
        #Poles
        row = box.row()
        row.prop(layers["Poles"], "is_visible", text="IK Poles", toggle=True)