import bpy
from .. import properties
from ..msc.utils import is_file_in_library

class VIEW3D_PT_RigListPanel(bpy.types.Panel):
    bl_label = "Rig Spawner"
    bl_idname = "VIEW3D_PT_rig_list"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = properties.UIProperties.category
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rig_props = scene.rigs
        preferences = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences

        # Draw UIList
        box = layout.row()
        box.template_list("RigListUI", "", rig_props, "rigs", rig_props, "active_rig_index")
        box = box.column(align=True)
        box.prop(preferences, "ShowPrefixes", text="", expand=True, placeholder="(optional)", toggle = True, icon ="HIDE_OFF" )
        box.operator("squaredmedia.open_rig_library", text = "", icon = "FILE_FOLDER")
        if len(rig_props.rigs) > 0:
            box.operator("squaredmedia.confirm_open_blend_file", text= "", icon = "GREASEPENCIL").filepath = rig_props.rigs[rig_props.active_rig_index].id



        # Import and load buttons
        sublayout = layout.row(align=True)
        sublayout.scale_y = 2

        # Name Character Button
        row = layout.row()
        row.scale_y = 2
        row.operator("squaredmedia.namecharacter", text="Name Your Character!", icon="SMALL_CAPS")


        if len(rig_props.rigs) > 0:
            sublayout = sublayout.split(factor=0.85, align=True)
            import_row = sublayout.row(align=True)

            text="Import Rig"


            if is_file_in_library(context):
                text = "Cannot Import into Rig files"
                import_row.enabled = False
            else:
                import_row.enabled = True

            import_op = import_row.operator("squaredmedia.import_rig", text = text, icon="IMPORT")
            import_op.collection_name = rig_props.rigs[rig_props.active_rig_index].name
            import_op.rig_path = rig_props.rigs[rig_props.active_rig_index].id



            sublayout.operator("squaredmedia.load_rigs", text="", icon="FILE_REFRESH")

            row = layout.row()
            row.enabled = False
            row.label(text=f"Mode = {preferences.DefaultImportOption.lower()}")
        else:
            sublayout.operator("squaredmedia.load_rigs", text="Please click to refresh", icon = "FILE_REFRESH")
