import bpy
from .. import properties
from ..msc.utils import get_rig
rigID = properties.RigProperties.rigID
category = properties.UIProperties.category
preferences = bpy.context.preferences.addons[properties.AddonProperties.module_name]

def drawEyeSettings(self, context):
    rig = get_rig(context)
    
    layout = self.layout
    EyeBox = layout.box()
    EyeBox.prop(rig.pose.bones["WGT-UIProperties"],'["EyeRigConf"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["EyeRigConf"] else "RIGHTARROW", emboss = False, text = "Eye Settings")
    if rig.pose.bones["WGT-UIProperties"]["EyeRigConf"]:

        DynamicEyes = EyeBox.box()
        DynamicEyes.label(text="Dynamic Eyes")
        DynamicEyes.prop(rig.pose.bones["DEF-Pupil.L"], '["Dynamic Eye L"]', toggle=True)
        DynamicEyes.prop(rig.pose.bones["DEF-Pupil.R"], '["Dynamic Eye R"]', toggle=True)


        EyeTracking = EyeBox.box()
        EyeTracking.label(text="Eye Tracking")
        EyeTracking.prop(rig.pose.bones["Settings"], '["Track Eyes"]', toggle=True)
        
        if rig.pose.bones["Settings"]["Track Eyes"]:
            col = EyeTracking.box()
            col.label(text='Track Parent')
            col.prop(rig.pose.bones["CTRL-EyeParent"],'["ParentToFace"]', text = "Head" , toggle=True)
            col.prop(rig.pose.bones["CTRL-EyeParent"], '["ParentToRoot"]', text = "Root" , toggle=True)

def drawArmSettings(self, context):
    rig = get_rig(context)
    
    layout = self.layout
    ArmBox = layout.box()
    ArmBox.prop(rig.pose.bones["WGT-UIProperties"],'["ArmRigConf"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["ArmRigConf"] else "RIGHTARROW", emboss = False, text = "Arm Settings")
    if rig.pose.bones["WGT-UIProperties"]["ArmRigConf"]:

        IKArmsBox = ArmBox.box()
        IKArmsBox.label(text="IK Arms")
        col = IKArmsBox.column(align=False)
        col.prop(rig.pose.bones["CTRL-LowerArm.L"], '["IK Arm L"]')
        col.prop(rig.pose.bones["CTRL-LowerArm.R"], '["IK Arm R"]')

        StretchyBox = ArmBox.box()
        StretchyBox.label(text="Stretchy Arms")
        col = StretchyBox.column(align=False)
        col.prop(rig.pose.bones["CTRL-LowerArm.L"], '["Stretchy Arm L"]')
        col.prop(rig.pose.bones["CTRL-LowerArm.R"], '["Stretchy Arm R"]')

        AttachmentBox = ArmBox.box()
        AttachmentBox.label(text="Attachments")
        col = AttachmentBox.column(align=False)
        col.prop(rig.pose.bones["CTRL-HandAttachment.L"], '["Parent to Arm"]', text="Parent to Arm L")
        col.prop(rig.pose.bones["CTRL-HandAttachment.R"], '["Parent to Arm"]', text="Parent to Arm R")

def drawBodySettings(self, context):
    rig = get_rig(context)
    layout = self.layout
    BodyBox = layout.box()
    BodyBox.prop(rig.pose.bones["WGT-UIProperties"],'["BodyConf"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["BodyConf"] else "RIGHTARROW", emboss = False, text = "Body Settings  ")
    if rig.pose.bones["WGT-UIProperties"]["BodyConf"]:

        col = BodyBox.box()
        col.label(text="Body")
        col.prop(rig.pose.bones["CTRL-Torso"], '["InheritRotation"]', toggle=True, text="Torso Inherit Rotation")
        col.prop(rig.pose.bones["CTRL-Head"], '["InheritRotation"]', toggle=True, text="Head Inherit Rotation")
        col.prop(rig.pose.bones["CTRL-Pelvis"], '["HipBone"]', toggle=True, text="Hip Bone")

def drawLegSettings(self, context):
    rig = get_rig(context)
    layout = self.layout
    LegBox = layout.box()
    LegBox.prop(rig.pose.bones["WGT-UIProperties"],'["LegConf"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["LegConf"] else "RIGHTARROW", emboss = False, text = "Leg Settings  ")
    if rig.pose.bones["WGT-UIProperties"]["LegConf"]:

        #Leg Settings
        # IK Legs
        IKLegsBox = LegBox.box()
        IKLegsBox.label(text="IK Legs")
        col = IKLegsBox.column(align=False)
        col.prop(rig.pose.bones["CTRL-LowerLeg.L"], '["IK Leg L"]')
        col.prop(rig.pose.bones["CTRL-LowerLeg.R"], '["IK Leg R"]')
        
        StretchyBox = LegBox.box()
        StretchyBox.label(text="Stretchy Legs")
        col = StretchyBox.column(align=False)
        col.prop(rig.pose.bones["CTRL-LowerLeg.L"], '["Stretchy Leg L"]')
        col.prop(rig.pose.bones["CTRL-LowerLeg.R"], '["Stretchy Leg R"]')
        # Fancy Feet
        FancyFeetBox = LegBox.box()
        FancyFeetBox.label(text="Fancy Feet")
        row = FancyFeetBox.row(align=False)
        row.prop(rig.pose.bones["CTRL-LowerLeg.L"], '["Fancy Feet L"]', toggle=True)
        row.prop(rig.pose.bones["CTRL-LowerLeg.R"], '["Fancy Feet R"]', toggle=True)
        #Detach
       
def drawRoundnessSettings(self, context):
    rig = get_rig(context)
    
    # Roundness Settings
    layout = self.layout
    RoundnessBox = layout.box()
    RoundnessBox.prop(rig.pose.bones["WGT-UIProperties"],'["RoundnessConf"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["RoundnessConf"] else "RIGHTARROW", emboss = False, text = "Roundness Settings")
    if rig.pose.bones["WGT-UIProperties"]["RoundnessConf"]:
        SubDBox = RoundnessBox.box()
        SubDBox.label(text = "SubD Modifier")
        Roundrow = SubDBox.row(align = True)
        split = Roundrow.split(align = True)
        split.prop(rig.pose.bones["Settings"],'["subd_viewport"]', toggle = True, icon = "RESTRICT_VIEW_OFF" if rig.pose.bones["Settings"]["subd_viewport"] else "RESTRICT_VIEW_ON", icon_only = True)
        split.prop(rig.pose.bones["Settings"],'["subd_render"]', toggle = True, icon = "RESTRICT_RENDER_OFF" if rig.pose.bones["Settings"]["subd_render"] else "RESTRICT_RENDER_ON", icon_only = True)

        SubDBox.prop(rig.pose.bones["Settings"],'["subd_viewport_res"]', text = "Viewport Subdivisions")
        SubDBox.prop(rig.pose.bones["Settings"],'["subd_render_res"]', text = "Render Subdivisions")

def draw_all_rig_settings(self,context):
     drawEyeSettings(self, context)
     drawArmSettings(self, context)
     drawBodySettings(self, context)
     drawLegSettings(self, context)
     drawRoundnessSettings(self, context)
