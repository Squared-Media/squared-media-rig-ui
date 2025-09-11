import bpy
from ..msc.utils import get_rig, Limbs, IK_Mode


class RIG_OT_set_ik_display_override(bpy.types.Operator):
    bl_idname = "squaredmedia.set_ik_display_override"
    bl_label = "Set IK display Overrides"

    Limb: bpy.props.StringProperty(
        name="Limb",
        description="Select a limb",
        default='LEFT_ARM'
    )#type: ignore

    Mode: bpy.props.StringProperty(
        name="IK Mode",
        description="IK state",
        default='AUTO'
    )#type: ignore


    def execute(self, context):
        rig = get_rig(context)
        UIProperties_bone = rig.pose.bones["WGT-UIProperties"]
        ik_array_property = UIProperties_bone["IK-Visibility-Overrides"]

        #convert string back to enum
        mode_value = IK_Mode[self.Mode].value
        limb_value = Limbs[self.Limb].value

        #set values for IK matrix
        ik_array_property[limb_value] = mode_value

        return {"FINISHED"}

