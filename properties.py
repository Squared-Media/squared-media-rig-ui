import bpy
class RigProperties:
    rigID = "SquaredMediaDefaultRig"

class Paths:
    blend_file = 'SQM-Minecraft-Rig.blend'
    lib_folder = 'lib'
    collection_name = 'SQM - Default Rig'
    GitubRepo = "https://github.com/Fxnarji/squared-media-rig-ui/archive/refs/heads/main.zip"

class UIProperties:
    category = "SQM Rig UI"

class AddonProperties:
    module_name = "squared-media-rig-ui"
    module_name_main = "squared-media-rig-ui-main"

    if bpy.context.preferences.addons.get(module_name):
        addon = bpy.context.preferences.addons[module_name].preferences
    else:
        if bpy.context.preferences.addons.get(module_name_main):
            addon = bpy.context.preferences.addons[module_name_main].preferences
        else:
            addon = None