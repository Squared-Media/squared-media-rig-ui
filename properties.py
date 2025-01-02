import os
from . import utils

class RigProperties:
    rigID = "SquaredMediaDefaultRig"

class Paths:
    blend_file = 'SQM-Minecraft-Rig.blend'
    lib_folder = 'lib'
    collection_name = 'SQM - Default Rig'
    GitubRepo = "https://github.com/Fxnarji/squared-media-rig-ui/archive/refs/heads/main.zip"
    default_lib_path = os.path.join(os.path.dirname(__file__),lib_folder, blend_file)
    rig_list = [
        ("SQM - Default Rig",default_lib_path, "COLLECTION_COLOR_05"),
       ("SQM - Sheep",default_lib_path, "FILE_BLANK"),
       ("SQM - Pig",default_lib_path, "FILE_BLANK"),
    ]

    prefix = "SQM-"

class UIProperties:
    category = "SQM Rig UI"

class AddonProperties:
    module_name = "squared-media-rig-ui"