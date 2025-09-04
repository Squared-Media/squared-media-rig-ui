import bpy
from ..msc.utils import get_skin_texture, get_rig


class DummyOperator(bpy.types.Operator):
    bl_idname = "squaredmedia.dummy"
    bl_label = "Dummy"

    def execute(self, context):
        rig = get_rig(context)
        print(rig)
        return {"FINISHED"}

