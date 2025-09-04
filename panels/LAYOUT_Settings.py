import bpy
from .. import properties
from ..msc.utils import get_rig

rigID = properties.RigProperties.rigID
category = properties.UIProperties.category
preferences = bpy.context.preferences.addons[properties.AddonProperties.module_name]

def draw_phenomes(self, context):
    layout = self.layout
    PhenomesBox = layout.box()
    rig = get_rig(context)
    PhenomesBox.prop(rig.pose.bones["WGT-UIProperties"],'["Phonemes"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["Phonemes"] else "RIGHTARROW", emboss = False, text = "Phonemes (Not Functional)")
    if rig.pose.bones["WGT-UIProperties"]["Phonemes"]:

        col = PhenomesBox.column(align=True)

        #rest

        row = col.row(align=True)
        row.operator("squaredmedia.set_pose", text = "Ah / A").phonem = "A"
        row.operator("squaredmedia.set_pose", text = "Ee / I").phonem = "OO"
        row.operator("squaredmedia.set_pose", text = "Oh / O").phonem = "OO"

        row = col.row(align=True)
        row.operator("squaredmedia.null", text = "Oo / U")
        row.operator("squaredmedia.null", text = "F / V")
        row.operator("squaredmedia.null", text = "M / B / P ")
        
        row = col.row(align=True)
        row.operator("squaredmedia.null", text = "L / D / N / T")
        row.operator("squaredmedia.null", text = "Th")
        row.operator("squaredmedia.null", text = "Ch / J / Sh")

        row = col.row(align=True)
        row.operator("squaredmedia.null", text = "S / Z")
        row.operator("squaredmedia.null", text = "Rest")
        row.operator("squaredmedia.null", text = "R")

        col = PhenomesBox.column(align=False) 
        col.operator("squaredmedia.null", text = "Generate Automatic Keyframes", icon = "KEYTYPE_KEYFRAME_VEC" )

def draw_snapper(self, context):
    #Snapper
    layout = self.layout
    SnapperBox = layout.box()
    rig = get_rig(context)
    SnapperBox.prop(rig.pose.bones["WGT-UIProperties"],'["Snapping"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["Snapping"] else "RIGHTARROW", emboss = False, text = "Snapping")
    if rig.pose.bones["WGT-UIProperties"]["Snapping"]:

        ArmL = SnapperBox.box()
        ArmL.label(text="Arm L")
        row = ArmL.row(align = True)

        SnapArmsLeft = row.operator("squaredmedia.snapper", text="From FK", icon = "SNAP_ON")
        SnapArmsLeft.limb = 'Arm_L'
        SnapArmsLeft.mode = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.Snapping
        SnapArmsLeft.direction = "IK_TO_FK"

        SnapArmsLeft = row.operator("squaredmedia.snapper", text="From IK", icon = "SNAP_OFF")
        SnapArmsLeft.limb = 'Arm_L'
        SnapArmsLeft.mode = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.Snapping
        SnapArmsLeft.direction = "FK_TO_IK"


        ArmR = SnapperBox.box()
        ArmR.label(text="Arm R")
        row = ArmR.row(align=True)

        SnapArmsRight = row.operator("squaredmedia.snapper", text="From FK", icon = "SNAP_ON")
        SnapArmsRight.limb = 'Arm_R'
        SnapArmsRight.mode = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.Snapping
        SnapArmsRight.direction = "IK_TO_FK"

        SnapArmsRight = row.operator("squaredmedia.snapper", text="From IK", icon = "SNAP_OFF")
        SnapArmsRight.limb = 'Arm_R'
        SnapArmsRight.mode = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.Snapping
        SnapArmsRight.direction = "FK_TO_IK"

def draw_retargeting(self,context):
    #Retargeting
    layout = self.layout
    rig = get_rig(context)
    retargeting_box = layout.box()
    retargeting_box.prop(rig.pose.bones["WGT-UIProperties"],'["Retargeting"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["Retargeting"] else "RIGHTARROW", emboss = False, text = "Retargeting")
    if rig.pose.bones["WGT-UIProperties"]["Retargeting"]:
        RetargetIcon = "RECORD_OFF"
        layout = self.layout
        if rig.pose.bones["Settings"]["Retargeting"]:
            RetargetIcon = "RECORD_ON"
        else:
            RetargetIcon = "RECORD_OFF"
        
        row = retargeting_box.column()
        row.prop(rig.pose.bones["Settings"], '["Retargeting"]', toggle=True, icon = RetargetIcon)
        row.prop(rig.pose.bones["Settings"], '["Show Mixamo Rig"]', toggle=True)

def draw_optimizations(self, context):
    #Optimizations
    rig = get_rig(context)
    layout = self.layout
    optimization_box = layout.box()
    optimization_box.prop(rig.pose.bones["WGT-UIProperties"],'["Optimization"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["Optimization"] else "RIGHTARROW", emboss = False, text = "Optimization")
    if rig.pose.bones["WGT-UIProperties"]["Optimization"]:

        #skin layer    
        row = optimization_box.row(align=False)
        Layer02 = rig.pose.bones["Settings"].get("Layer02", None) 
        row.prop(Layer02, "hide_viewport", text = "Layer 02 Viewport", invert_checkbox = True, icon = "LAYER_USED")

        
        #subD
        row = optimization_box.row(align=False)
        row.prop(rig.pose.bones["Settings"], '["SubD Viewport"]', toggle=True)
        row = optimization_box.row(align=False)
        row.prop(rig.pose.bones["Settings"], '["SubD Render"]', toggle=True)

        #proxies
        row = optimization_box.column()
        Proxies = rig.pose.bones["Settings"].get("Proxies", None) 
        row.prop(Proxies, "hide_viewport", text = "Proxies", invert_checkbox = True, icon = "LAYER_USED")
        Rendermesh = rig.pose.bones["Settings"].get("Render Mesh", None) 
        row.prop(Rendermesh, "hide_viewport", text = "Render Mesh", invert_checkbox = True, icon = "LAYER_USED")
        settings = rig.pose.bones["Settings"]
        row.prop(settings, '["ExpensiveGeoNodes"]', text = "Enable Geo Nodes", icon = "LAYER_USED")
        




def draw_all_settings(self, context):
    layout = self.layout
    HelperBox = layout.box()
    rig = get_rig(context)
    HelperBox.prop(rig.pose.bones["WGT-UIProperties"],'["HelperConf"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["HelperConf"] else "RIGHTARROW", emboss = False, text = "Helpers")
    if rig.pose.bones["WGT-UIProperties"]["HelperConf"]:

        HelperBox.operator("squaredmedia.keyframe_all_custom_properties")


    if preferences.preferences.ShowExperimental:
        draw_phenomes(self, context)

    draw_snapper(self, context)

    draw_retargeting(self, context)

    draw_optimizations(self,context)
    


    
    