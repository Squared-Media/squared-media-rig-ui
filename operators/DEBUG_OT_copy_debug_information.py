import bpy
import json
from ..msc.utils import get_toml_key

class DEBUG_OT_copy_debug_info(bpy.types.Operator):
    bl_idname = "squaredmedia.copy_debug_info"
    bl_label = "DEBUG_OT_copy_debug_info"
    bl_description = "Click here to Copy Debug Information!"

    def execute(self, context):
        self.report({'INFO'}, "Hello")

        #addon info
        addon_version = get_toml_key("version")
        addon_release_channel = get_toml_key("release_channel")
        addon_beta_version = get_toml_key("beta_version")
        try:
            addon_beta_version = int(addon_beta_version)
        except: 
            print("beta missing")

        #blender info
        blender_version = bpy.app.version
        platform = bpy.app.build_platform
        portable = bpy.app.portable
        render_engine = bpy.data.scenes[0].render.engine
        cycles_feature_set = "(disabled)"
        cycles_scene_device = "(disabled)"
        if render_engine == "CYCLES":
            cycles_feature_set = bpy.data.scenes[0].cycles.feature_set
            cycles_scene_device = bpy.data.scenes[0].cycles.device


        information_dict={
            "addon version": addon_version,
            "addon release": f"{addon_release_channel}",
            "addon beta": addon_beta_version,
            "Blender Version" : ".".join(map(str, blender_version)),
            "Platform": f"{platform}",
            "portable": portable,
            "render engine": f"{render_engine}",
            "Cycles Mode": f"{cycles_feature_set}",
            "Cycles Device": f"{cycles_scene_device}"
        }

        information_json = json.dumps(information_dict, indent = 4)
        discord_pretty = f"```{information_json}```"

        bpy.context.window_manager.clipboard = discord_pretty

        self.report({'INFO'},"Copied relevant Information to your Clipboard!")

        print(information_json)
        return {"FINISHED"}

