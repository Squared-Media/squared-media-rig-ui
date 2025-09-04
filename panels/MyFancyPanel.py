import bpy
from .. import properties

category = properties.UIProperties.category
preferences = bpy.context.preferences.addons[properties.AddonProperties.module_name]
         
class TestPanel(bpy.types.Panel):
    bl_label = "My Fancy Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Test"
    bl_order = 2
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Test")
        layout.operator("squaredmedia.dummy", icon="FILE_REFRESH")

