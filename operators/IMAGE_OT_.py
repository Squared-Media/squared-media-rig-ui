import bpy
from ..msc.utils import is_packed
from .. import properties

blend_file = properties.Paths.blend_file
lib_folder = properties.Paths.lib_folder
rigID = properties.RigProperties.rigID


class IMAGE_OT_pack(bpy.types.Operator):
    bl_idname = "squaredmedia.imgpack"
    bl_label = ""
    bl_description = "packs or unpacks textures"

    id_name: bpy.props.StringProperty()

    def execute(self, context):
        img = bpy.data.images[self.id_name]
        if is_packed(img):
            if bpy.data.is_saved:
                img.unpack()
            else:
                img.unpack(method="USE_ORIGINAL")
        else:
            img.pack()
        return {"FINISHED"}

class IMAGE_OT_reload(bpy.types.Operator):
    bl_idname = "squaredmedia.imgreload"
    bl_label = ""
    bl_description = "refreshes texture"

    id_name: bpy.props.StringProperty()

    def execute(self, context):
        bpy.data.images[self.id_name].reload()
        return {"FINISHED"}
