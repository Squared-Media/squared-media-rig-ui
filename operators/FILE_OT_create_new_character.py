import bpy  # type: ignore
from ..msc.utils import get_preferences


class FILE_OT_create_new_character(bpy.types.Operator):
    bl_idname = "squaredmedia.create_character"
    bl_label = "Create a new Character"

    name: bpy.props.StringProperty(
        description="lets the user confirm if the path is fine"
    )#type: ignore



    def execute(self, context):
        # needs to:
        # if the directory is default, ask for a new directory
        self.check_default_directory(context)
        # accept a name
        # make a new file
        # import the armature
        # run the rename Operator
        # save the file in the directory
        return {"FINISHED"}


    def invoke(self, context, event):
        using_default = self.check_default_directory(context)
        current_path = get_preferences(context).usr_file_path
        warning = ""

        if using_default: 
            warning = "you are still using the default directory, is this as intended?"
        
        message = f"{warning}\nabout to create a new file in this directory \n\n{current_path} \n\n {using_default}"
        

        return context.window_manager.invoke_confirm(self, event, message=message)

    def check_default_directory(self, context) -> bool:
        import os

        preferences = get_preferences(context)

        default = (os.path.expanduser("~"),)
        current = preferences.usr_file_path

        is_default = False

        if default[0] == current:
            is_default = True

        return is_default
