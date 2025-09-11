
import bpy
from ..msc.utils import get_skin_texture, get_rig, Material, get_material


class DummyOperator(bpy.types.Operator):
    bl_idname = "squaredmedia.dummy"
    bl_label = "Dummy"

    def execute(self, context):
        rig = get_rig(context)
        properties_bone = rig.pose.bones["WGT-UIProperties"]["enum"]
        print(properties_bone)
        return {"FINISHED"}

