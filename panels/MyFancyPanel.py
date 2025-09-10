import bpy

from ..msc.utils import IK_Mode, Limbs, get_rig

class TestPanel(bpy.types.Panel):
    bl_label = "My Fancy Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Test"
    bl_order = 2
    
    def get_limb_state(self, context, Limb: Limbs):
        rig = get_rig(context)
        UIProperties_bone = rig.pose.bones["WGT-UIProperties"]
        ik_array_property = UIProperties_bone["IK-Visibility-Overrides"]
        limb_index = Limb.value
        
        limb_state = ik_array_property[limb_index]
        if limb_state == 1:
            return IK_Mode.ON
        elif limb_state == 2:
            return IK_Mode.OFF
        else:
            return IK_Mode.AUTO


    def draw_limb(self, context, layout, Limb: Limbs):
        row = layout.row(align = True)
        row.label(text = Limb.name.replace("_"," ").capitalize())   #turns LEFT_ARM into Left arm

        on = row.operator("squaredmedia.set_ik_display_override", text = "On", depress = self.get_limb_state(context, Limb) == IK_Mode.ON)
        on.Limb = Limb.name
        on.Mode = IK_Mode.ON.name

        auto = row.operator("squaredmedia.set_ik_display_override", text = "Auto", depress = self.get_limb_state(context, Limb) == IK_Mode.AUTO)
        auto.Limb = Limb.name
        auto.Mode = IK_Mode.AUTO.name

        off = row.operator("squaredmedia.set_ik_display_override", text = "Off", depress = self.get_limb_state(context, Limb) == IK_Mode.OFF)
        off.Limb = Limb.name
        off.Mode = IK_Mode.OFF.name


    def draw(self, context):
        layout = self.layout
        arm_box = layout.box()

        #draw arms
        arm_box.label(text = "Arms")
        self.draw_limb(context, arm_box, Limbs.LEFT_ARM)
        self.draw_limb(context, arm_box, Limbs.RIGHT_ARM)

        #draw legs
        leg_box = layout.box()
        leg_box.label(text = "Legs")
        self.draw_limb(context, leg_box, Limbs.LEFT_LEG)
        self.draw_limb(context, leg_box, Limbs.RIGHT_LEG)

