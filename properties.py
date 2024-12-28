import bpy


rigID = "SquaredMediaDefaultRig"
category = "SQM Rig UI"
blend_file = 'SQM-Minecraft-Rig.blend'
lib_folder = 'lib'
collection_name = 'SQM - Default Rig'

class SQMRigProperties(bpy.types.PropertyGroup):
    my_test_float : bpy.props.FloatProperty(name ="MyFloat", default = 1.0) # type: ignore
    my_test_String : bpy.props.StringProperty(name ="MyString", default = "Test") # type: ignore
