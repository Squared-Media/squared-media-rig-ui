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
<<<<<<< Updated upstream
        col.prop(rig.data.collections_all["Face"], "is_visible", text="Face Bones", toggle=True)
=======

        # Face Visibility
        col.prop(rig.data.collections_all["Isolate Face"], "is_visible", text="Isolate Face", toggle=True, invert_checkbox=True)
        
        row = col.row(align=True)
        row.prop(rig.data.collections_all["FaceSimple"], "is_visible", text="Face Simple", toggle=True)
        row.prop(rig.data.collections_all["FaceComplex"], "is_visible", text="Face Complex", toggle=True)
        
        # Misc Visibility
>>>>>>> Stashed changes
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