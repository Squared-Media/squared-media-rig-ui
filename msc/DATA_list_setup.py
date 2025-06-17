import bpy
from .. import properties
import os


class RigItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Rig Name")
    id: bpy.props.StringProperty(name="Rig ID")
    icon: bpy.props.StringProperty(name="Rig Icon")

class RigListProperties(bpy.types.PropertyGroup):
    rigs: bpy.props.CollectionProperty(type=RigItem)
    active_rig_index: bpy.props.IntProperty(name="Index", default=0)

class RigListUI(bpy.types.UIList):

   
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        prefix = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.lib_prefix
        if bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.ShowPrefixes:
            label = item.name
        else:
            label = item.name.removeprefix(prefix)
        layout.label(text=label, icon=item.icon)
        Blendfile = layout.row()
        Blendfile.enabled = False

        Blendfile.label(text=os.path.basename(item.id))
        #layout.operator("squaredmedia.confirm_open_blend_file", text= "", icon = "GREASEPENCIL").filepath = item.id
