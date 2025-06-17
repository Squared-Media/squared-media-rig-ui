import bpy
import os
from .. import properties

class SQM_Rig_Preferences(bpy.types.AddonPreferences):
    bl_idname = properties.AddonProperties.module_name

    AppendOrLinkItems = [
        ('APPEND', "Append", "Use this if you want to modify the rig"),
        ('LINK', "Link", "Use this if you want to keep the rig as is"),
    ]

    SnappItems = [
        ('SMART', "Smart", "automatically places keyframes"),
        ('REGULAR', "Regular", "Normal IK / FK Snapping"),
    ]

    RigTabs = [
        ('SKIN', "Skin", "All character customization features"),
        ('RIG', "Rig", "All the rig Settings"),
        ('SETTINGS', "Functions", "Extra functionality"),
    ]



    DefaultImportOption: bpy.props.EnumProperty(
        name="Append or Link",  
        description="Choose whether to Append or Link the collection", 
        items=AppendOrLinkItems,  
        default='APPEND'
    )#type: ignore

    usr_file_path: bpy.props.StringProperty(
        name="Library Path",
        description="NOTE: The Collection to be appended needs to start with the prefix specified below. You can have multiple blend files with multiple characters. Subfolders are not supported",
        default= os.path.expanduser("~"),
        subtype="DIR_PATH"
    )   #type: ignore

    lib_prefix: bpy.props.StringProperty(
        name="Prefix",
        description="Prefix that the library looks for",
        default= "SQM_CH_",
    )   #type: ignore
    
    Snapping: bpy.props.EnumProperty(
        name="Smart Snapping",  
        description="Smart: automatically places keyframes for you\nRegular: Only snapps limbs, doesnt place any keyframes", 
        items=SnappItems,  
        default='SMART'
    )#type: ignore

    rigTab: bpy.props.EnumProperty(
        name="Rig Tab",
        description="Choose wich tab is open",
        items=RigTabs,
        default="SKIN"
    )#type: ignore

    ShowPrefixes: bpy.props.BoolProperty(
        description="Displays the required Prefix"
    )#type: ignore
    

    ShowExperimental: bpy.props.BoolProperty(default=False)#type: ignore
    
    built_in_path: bpy.props.StringProperty(default=properties.Paths.default_lib_path)                                  #type: ignore

    CollectionName: bpy.props.StringProperty()                                                                          #type: ignore
    selected_index: bpy.props.IntProperty()                                                                             #type: ignore

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Import Method")
        row.prop(self,"DefaultImportOption",expand=True)

        row = layout.row()
        row.prop(self,"usr_file_path")

        row = layout.row()
        row.prop(self,"lib_prefix")

        row = layout.row()
        row.label(text="Smart Snapping")
        row.prop(self,"Snapping",expand=True)

        #row= layout.row()
        #row.prop(self, "ShowExperimental", text= "Show Experimental", icon = "ERROR")
