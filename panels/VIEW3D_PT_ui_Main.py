import bpy
from ..msc.utils import get_material_object, get_toml_version
from .. import properties
from .LAYOUT_SkinSettings   import draw_skin_settings
from .LAYOUT_Settings       import draw_all_settings
from .LAYOUT_RigSettings    import draw_all_rig_settings
from ..msc.IMG_load_icons   import preview_collections

rigID = properties.RigProperties.rigID
category = properties.UIProperties.category
preferences = bpy.context.preferences.addons[properties.AddonProperties.module_name]
         
class VIEW3D_PT_ui_Main(bpy.types.Panel):
    bl_label = "Squared Media Pro Rig v1"
    bl_idname = "OBJECT_PT_SquaredMediaHeader"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_order = 2

    #properties

    def draw(self, context):
        layout = self.layout
        header = layout.box()
        row = header.row()


        pcoll = preview_collections.get("main")
        if pcoll:
            icon_id = pcoll["sqm_logo"].icon_id
            row.label(text="Squared Media", icon_value=icon_id)

        else:
            row.label(text="Squared Media", icon="RENDER_ANIMATION")

        version_tuple = get_toml_version()

        row = row.row()
        row.enabled = False
        row.label(text=(f"v{str(version_tuple[0])}.{str(version_tuple[1])}.{str(version_tuple[2])}"))

        layout.separator()
        col = layout.row()
        col.scale_y = 1.5
        col.prop(preferences.preferences, "rigTab", text="Default Import Option", expand=True)

        sublayout = self.layout
        if not context.active_object or context.active_object.get("rig_id") != rigID:
            col.active = False
            row = layout.row()
            row.scale_y = 5
            row.label(text = "No Compatibled Rig Selected", icon = "INFO")
        

        #drawing main contents of Rig UI
        if context.active_object and context.active_object.get("rig_id") == rigID and get_material_object(context.active_object):
            layout.separator()
            if preferences.preferences.rigTab == "SKIN":
                draw_skin_settings(self, context)
            elif preferences.preferences.rigTab == "SETTINGS":
                draw_all_settings(self, context)
            elif preferences.preferences.rigTab == "RIG":
                draw_all_rig_settings(self,context)
    

    
        




