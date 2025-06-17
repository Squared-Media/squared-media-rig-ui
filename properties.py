import os
import bpy

class RigProperties:
    rigID = "SquaredMediaDefaultRig"


class AddonProperties:
    module_name = __package__

class Paths:
    #Default Lib paths:
    blend_file = 'SQM-Default-Rig.blend'
    lib_folder = 'lib'
    default_rig_collection_name = 'SQM_CH_Default Rig'
    default_lib_path = os.path.join(os.path.dirname(__file__),lib_folder,blend_file)

class UIProperties:
    category = "SQM Rig UI"

#bpy.context.addons.preferences[AddonProperties.module_name].preferences