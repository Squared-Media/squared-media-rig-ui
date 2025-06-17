import bpy
from .. import properties

class VIEW3D_PT_RigListPanel(bpy.types.Panel):
    bl_label = "Rig Spawner"
    bl_idname = "VIEW3D_PT_rig_list"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SQM Rig UI'
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
        if len(rig_props.rigs) > 0:
            box.operator("squaredmedia.confirm_open_blend_file", text= "", icon = "GREASEPENCIL").filepath = rig_props.rigs[rig_props.active_rig_index].id

        # Rig default import name
        layout.prop(preferences, "CollectionName", text="Name", expand=True, placeholder="(optional)")

        # Import and load buttons
        sublayout = layout.row(align=True)
        sublayout.scale_y = 2
        
        if len(rig_props.rigs) > 0:
            sublayout = sublayout.split(factor=0.85, align=True)
            import_op = sublayout.operator("squaredmedia.import_rig", text="Import Rig", icon="IMPORT")
            import_op.collection_name = rig_props.rigs[rig_props.active_rig_index].name
            import_op.rig_path = rig_props.rigs[rig_props.active_rig_index].id
            import_op.imported_name = preferences.CollectionName or rig_props.rigs[rig_props.active_rig_index].name

            sublayout.operator("squaredmedia.load_rigs", text="", icon="FILE_REFRESH")

            row = layout.row()
            row.enabled = False
            row.label(text=f"Mode = {preferences.DefaultImportOption.lower()}")
        else:
            sublayout.operator("squaredmedia.load_rigs", text="Please click to refresh", icon = "FILE_REFRESH")