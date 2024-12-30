import bpy
from . import properties

class VIEW3D_PT_rig_list(bpy.types.Panel):
    bl_label = "Rig List"
    bl_idname = "VIEW3D_PT_rig_list"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SQM - EXPERIMENTAL'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        addon_props = scene.rig_props

        # Draw UIList
        layout.template_list("RigListUI", "", addon_props, "rig_list", addon_props, "rig_index")
        sublayout = layout.row()
        sublayout.scale_y = 2
        sublayout.operator("squaredmedia.import_rig", text="Import Rig", icon="IMPORT")
class PopulateList(bpy.types.Operator):
    bl_idname = "squaredmedia.load_rigs"
    bl_label = "Populate Rig List"

    def execute(self, context):
        scene = context.scene
        addon_props = scene.rig_props

        # Clear the list
        addon_props.rig_list.clear()

        print(properties.Paths.rig_list)
        for i in properties.Paths.rig_list:
            item = addon_props.rig_list.add()
            print(i)
            item.name = i
            item.rigID = i

        return {"FINISHED"}

def register():
    bpy.utils.register_class(VIEW3D_PT_rig_list)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_rig_list)



if __name__ == "__main__":
    register()
