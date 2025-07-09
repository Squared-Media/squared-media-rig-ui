import bpy
from ..msc.utils import has_name


class DummyOperator(bpy.types.Operator):
    bl_idname = "squaredmedia.dummy"
    bl_label = "Dummy"

    def execute(self, context):
        print(has_name(bpy.context.active_object))
        return {"FINISHED"}

