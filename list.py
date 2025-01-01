import bpy
from . import properties


class RigItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Rig Name")
    id: bpy.props.StringProperty(name="Rig ID")
    icon: bpy.props.StringProperty(name="Rig Icon")


class RigListProperties(bpy.types.PropertyGroup):
    rigs: bpy.props.CollectionProperty(type=RigItem)
    active_rig_index: bpy.props.IntProperty(name="Index", default=0)


class RigListUI(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name, icon=item.icon)


class VIEW3D_PT_RigListPanel(bpy.types.Panel):
    bl_label = "Rig Spawner"
    bl_idname = "VIEW3D_PT_rig_list"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SQM Rig UI'

   


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rig_props = scene.rigs
        preferences = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences

        # Draw UIList
        layout.template_list("RigListUI", "", rig_props, "rigs", rig_props, "active_rig_index")

        # Rig default import name
        layout.prop(preferences, "CollectionName", text="Name", expand=True, placeholder="(optional)")

        # Import and load buttons
        sublayout = layout.row(align=True)
        sublayout = sublayout.split(factor=0.85, align=True)
        sublayout.scale_y = 2
        
        import_op = sublayout.operator("squaredmedia.import_rig", text="Import Rig", icon="IMPORT")
        import_op.collection_name = rig_props.rigs[rig_props.active_rig_index].name
        import_op.rig_path = rig_props.rigs[rig_props.active_rig_index].id
        import_op.imported_name = preferences.CollectionName or rig_props.rigs[rig_props.active_rig_index].name
        
        sublayout.operator("squaredmedia.load_rigs", text="", icon="FILE_REFRESH")
        
        row = layout.row()
        row.enabled = False
        row.label(text=f"Mode = {preferences.DefaultImportOption.lower()}")


class SCENE_OT_RefreshRigList(bpy.types.Operator):
    bl_idname = "squaredmedia.load_rigs"
    bl_label = "Refresh Rig List"
    bl_description = "Refresh the list of rigs available to import"

    def execute(self, context):
        scene = context.scene
        rig_props = scene.rigs

        # Clear the list
        rig_props.rigs.clear()

        # Populate the rig list
        for rig in properties.Paths.rig_list:
            rig_item = rig_props.rigs.add()
            rig_item.name = rig[0]
            rig_item.id = rig[1]
            rig_item.icon = rig[2]

        return {"FINISHED"}


def register():
    bpy.utils.register_class(VIEW3D_PT_RigListPanel)
    bpy.utils.register_class(RigItem)
    bpy.utils.register_class(RigListProperties)
    bpy.utils.register_class(RigListUI)
    bpy.utils.register_class(SCENE_OT_RefreshRigList)


def unregister():
    bpy.utils.unregister_class(SCENE_OT_RefreshRigList)
    bpy.utils.unregister_class(RigListUI)
    bpy.utils.unregister_class(RigListProperties)
    bpy.utils.unregister_class(RigItem)
    bpy.utils.unregister_class(VIEW3D_PT_RigListPanel)


if __name__ == "__main__":
    register()
