import bpy
from .. import properties

rigID = properties.RigProperties.rigID
category = properties.UIProperties.category



def draw_buttons(self, context):
    layout = self.layout
    HelperBox = layout.box()
    HelperBox.label(text="Helper")
    HelperBox.operator("squaredmedia.keyframe_all_custom_properties")


    if bpy.context.space_data.lock_camera:
        HelperBox.operator("squaredmedia.reset_camera", text = "End Face Anim")
    else:
        HelperBox.operator("squaredmedia.set_camera", text = "Start Face Anim")
    
    #Snapper
    SnapperBox = layout.box()
    SnapperBox.label(text="Snapper")
    SnapArmsLeft = SnapperBox.operator("squaredmedia.snapper", text="Arm L FK -> IK", icon = "SNAP_ON")
    SnapArmsLeft.limb = 'Arm_L'
    SnapArmsLeft.mode = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.Snapping
    
    SnapArmsRight = SnapperBox.operator("squaredmedia.snapper", text="Arm R FK -> IK", icon = "SNAP_ON")
    SnapArmsRight.limb = 'Arm_R'
    SnapArmsRight.mode = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.Snapping


    #Retargeting
    rig = bpy.context.active_object
    retargeting_box = layout.box()
    retargeting_box.label(text="Retargeting")
    RetargetIcon = "RECORD_OFF"
    layout = self.layout
    if rig.pose.bones["Settings"]["Retargeting"]:
        RetargetIcon = "RECORD_ON"
    else:
        RetargetIcon = "RECORD_OFF"
    
    row = retargeting_box.column()
    row.prop(rig.pose.bones["Settings"], '["Retargeting"]', toggle=True, icon = RetargetIcon)
    row.prop(rig.pose.bones["Settings"], '["Show Mixamo Rig"]', toggle=True)

    #Optimizations

    optimization_box = layout.box()
    optimization_box.label(text="Optimizations")

    row = optimization_box.row(align=False)
    row.prop(rig.pose.bones["Settings"], '["Potato Mode"]', toggle=True, text="High Quality Preview")
    
    row = optimization_box.row(align=False)
    row.prop(rig.pose.bones["Settings"], '["Skin Layer 02"]', toggle=True)
    
    row = optimization_box.row(align=False)
    row.prop(rig.pose.bones["Settings"], '["SubD Viewport"]', toggle=True)
    row = optimization_box.row(align=False)
    row.prop(rig.pose.bones["Settings"], '["SubD Render"]', toggle=True)

    box = layout.box()
    row = box.row()