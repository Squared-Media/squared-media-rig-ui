import bpy#type: ignore 
from .. import properties


class RigItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Rig Name") #type: ignore 
    id: bpy.props.StringProperty(name="Rig ID")#type: ignore 
    icon: bpy.props.StringProperty(name="Rig Icon")#type: ignore 

class RigListProperties(bpy.types.PropertyGroup):
    rigs: bpy.props.CollectionProperty(type=RigItem)#type: ignore 
    active_rig_index: bpy.props.IntProperty(name="Index", default=0)#type: ignore 

class RigListUI(bpy.types.UIList):

   
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        prefix = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.lib_prefix
        if bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.ShowPrefixes:
            label = item.name
        else:
            label = item.name.removeprefix(prefix)
        layout.label(text=label, icon=item.icon)

        #NOTE: blendfile entry has been removed due to clutter and easy access from the open operator

        # Blendfile = layout.row()
        # Blendfile.enabled = False
        # Blendfile.label(text=os.path.basename(item.id))
        #layout.operator("squaredmedia.confirm_open_blend_file", text= "", icon = "GREASEPENCIL").filepath = item.id
