import bpy

class  SCENE_OT_Open_Preset(bpy.types.Operator):
    bl_idname = "squaredmedia.open_character"
    bl_label = "Open Blender File"
    bl_description = "Open the blendfile of the preset to make edits to it"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")#type: ignore
    
    def execute(self, context):
        bpy.ops.wm.open_mainfile(filepath=self.filepath)
        return {'FINISHED'}

class ConfirmOpenBlendFileOperator(bpy.types.Operator):
    """Confirmation operator before opening a .blend file"""
    bl_idname = "squaredmedia.confirm_open_blend_file"
    bl_label = "Open Preset file"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")#type: ignore
    
    def execute(self, context):
        # Open the file after confirmation
        bpy.ops.squaredmedia.open_character(filepath=self.filepath)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        message = f"Are you sure you want to open: {self.filepath}?\n\nUnsaved changes will be lost! \n\n(You can disable this Check in the preferences)"
        return context.window_manager.invoke_confirm(self, event, message=message)