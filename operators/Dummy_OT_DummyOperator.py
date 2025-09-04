
import bpy
from ..msc.utils import get_skin_texture, get_rig, Material, get_material


class DummyOperator(bpy.types.Operator):
    bl_idname = "squaredmedia.dummy"
    bl_label = "Dummy"

    def execute(self, context):
        material = get_material(context, Material.SKIN)
        print(material)
        return {"FINISHED"}

