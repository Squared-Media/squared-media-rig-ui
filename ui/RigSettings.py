import bpy
from .. import properties

rigID = properties.RigProperties.rigID
category = properties.UIProperties.category

class VIEW3D_PT_rig_settings(bpy.types.Panel):
    bl_label = "Rig Settings"
    bl_idname = "OBJECT_PT_SquaredMediaRigSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category


    @classmethod
    def poll(self, context):
        obj = context.active_object
        return obj and obj.get("rig_id") == rigID
    
    def draw(self,context):
        rig = bpy.context.active_object
        layout = self.layout  

        header = layout.box()
        header.label(text="General Rig Settings")

class VIEW3D_PT_face_settings(bpy.types.Panel):
    bl_label = "Face Settings"
    bl_parent_id = "OBJECT_PT_SquaredMediaRigSettings"
    bl_idname = "OBJECT_PT_SquaredMediaFaceSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category


    def draw(self, context):
        rig = bpy.context.active_object
        
        layout = self.layout
        EyeBox = layout.box()
        EyeBox.label(text="Eyes")

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

class VIEW3D_PT_arm_settings(bpy.types.Panel):
    bl_label = "Arm Settings"
    bl_parent_id = "OBJECT_PT_SquaredMediaRigSettings"
    bl_idname = "OBJECT_PT_SquaredMediaArmSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category

    def draw(self, context):
        rig = bpy.context.active_object
        
        layout = self.layout
        SlimArmBox = layout.box()
        SlimArmBox.label(text="Slim Arms")
        SlimArmBox.prop(rig.pose.bones["Settings"],'["Slim Arms"]', toggle = True)

        IKArmsBox = layout.box()
        IKArmsBox.label(text="IK Arms")
        col = IKArmsBox.column(align=False)
        col.prop(rig.pose.bones["CTRL-IK-LowerArm.L"], '["IK Arm L"]')
        col.prop(rig.pose.bones["CTRL-IK-LowerArm.R"], '["IK Arm R"]')

        StretchyBox = layout.box()
        StretchyBox.label(text="Stretchy Arms")
        col = StretchyBox.column(align=False)
        col.prop(rig.pose.bones["CTRL-IK-LowerArm.L"], '["Stretchy Arm L"]')
        col.prop(rig.pose.bones["CTRL-IK-LowerArm.R"], '["Stretchy Arm R"]')

        AttachmentBox = layout.box()
        AttachmentBox.label(text="Attachments")
        col = AttachmentBox.column(align=False)
        col.prop(rig.pose.bones["DEF-Attachment.L"], '["Parent to Arm"]', text="Parent to Arm L")
        col.prop(rig.pose.bones["DEF-Attachment.R"], '["Parent to Arm"]', text="Parent to Arm R")

class VIEW3D_PT_body_settings(bpy.types.Panel):
    bl_label = "Body Settings"
    bl_parent_id = "OBJECT_PT_SquaredMediaRigSettings"
    bl_idname = "OBJECT_PT_SquaredMediaBodySettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category

    def draw(self, context):
        rig = bpy.context.active_object
        layout = self.layout
        col = layout.column(align=False)
        col.prop(rig.pose.bones["CTRL-Torso"], '["InheritRotation"]', toggle=True, text="Torso Inherit Rotation")
        col.prop(rig.pose.bones["CTRL-Head"], '["InheritRotation"]', toggle=True, text="Head Inherit Rotation")
        col.prop(rig.pose.bones["CTRL-Pelvis"], '["HipBone"]', toggle=True, text="Hip Bone")

class VIEW3D_PT_leg_settings(bpy.types.Panel):
    bl_label = "Leg Settings"
    bl_parent_id = "OBJECT_PT_SquaredMediaRigSettings"
    bl_idname = "OBJECT_PT_SquaredMediaLegSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category

    def draw(self, context):
        rig = bpy.context.active_object
        
        layout = self.layout
        #Leg Settings
        row = layout.row()
        row.label(text="Leg Settings")
        # IK Legs
        IKLegsBox = layout.box()
        IKLegsBox.label(text="IK Legs")
        col = IKLegsBox.column(align=False)
        col.prop(rig.pose.bones["CTRL-LowerLeg.L"], '["IK Leg L"]')
        col.prop(rig.pose.bones["CTRL-LowerLeg.R"], '["IK Leg R"]')
        
        StretchyBox = layout.box()
        StretchyBox.label(text="Stretchy Legs")
        col = StretchyBox.column(align=False)
        col.prop(rig.pose.bones["CTRL-LowerLeg.L"], '["Stretchy Leg L"]')
        col.prop(rig.pose.bones["CTRL-LowerLeg.R"], '["Stretchy Leg R"]')
        # Fancy Feet
        FancyFeetBox = layout.box()
        FancyFeetBox.label(text="Fancy Feet")
        row = FancyFeetBox.row(align=False)
        row.prop(rig.pose.bones["CTRL-LowerLeg.L"], '["Fancy Feet L"]', toggle=True)
        row.prop(rig.pose.bones["CTRL-LowerLeg.R"], '["Fancy Feet R"]', toggle=True)
        #Detach
        DetachBox = layout.box()
        DetachBox.label(text="Detach")
        row = DetachBox.row(align=False)
        Icon_DetachLegL = "TIME"
        text_DetachLegL = "loading..."
        if(rig.pose.bones["CTRL-UpperLeg.L"]["Detach Leg L"]):
            Icon_DetachLegL = "UNLINKED"
            text_DetachLegL = "Attach Leg L"
        else:
            Icon_DetachLegL = "LINKED"
            text_DetachLegL = "Detach Leg L"
        row.prop(rig.pose.bones["CTRL-UpperLeg.L"], '["Detach Leg L"]', toggle=True, text = text_DetachLegL, icon = Icon_DetachLegL)
        Icon_DetachLegR = "TIME"
        text_DetachLegR = "loading..."
        if(rig.pose.bones["CTRL-UpperLeg.R"]["Detach Leg R"]):
            Icon_DetachLegR = "UNLINKED"
            text_DetachLegR = "Attach Leg R"
        else:
            Icon_DetachLegR = "LINKED"
            text_DetachLegR = "Detach Leg R"
        row.prop(rig.pose.bones["CTRL-UpperLeg.R"], '["Detach Leg R"]', toggle=True, text = text_DetachLegR, icon = Icon_DetachLegR)

class VIEW3D_PT_roundness_settings(bpy.types.Panel):
    bl_label = "Roundness Settings"
    bl_parent_id = "OBJECT_PT_SquaredMediaRigSettings"
    bl_idname = "OBJECT_PT_SquaredMediaRoundnessSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category

    def draw(self, context):
        rig = bpy.context.active_object
        
        layout = self.layout
        # Roundness Settings
        RoundnessBox = layout.box()
        row = RoundnessBox.row()
        row.label(text="Roundness Settings")

            
        HeadArea = RoundnessBox.row()
        HeadArea = HeadArea.split(factor=0.333)
        HeadArea.column()
        Head = HeadArea.box()
        Head.label(text="Head")
        col = Head.column(align = True)
        col.prop(rig.pose.bones["CTRL-Head"], '["Smooth - Viewport Head"]', toggle=True, icon="RESTRICT_VIEW_OFF", icon_only= True)
        col.prop(rig.pose.bones["CTRL-Head"], '["Smooth - Render Head"]', toggle=True, icon="RESTRICT_RENDER_OFF", icon_only= True)
        HeadArea.split()
        Body = RoundnessBox.row(align = False)
        ArmL = Body.box()
        ArmL.label(text="Arm Left")
        ArmL = ArmL.column(align = True)
        ArmL.prop(rig.pose.bones["CTRL-IK-UpperArm.L"], '["Smooth - Viewport Arm.L"]', toggle=True, icon="RESTRICT_VIEW_OFF", icon_only= True)
        ArmL.prop(rig.pose.bones["CTRL-IK-UpperArm.L"], '["Smooth - Render Arm.L"]', toggle=True, icon="RESTRICT_RENDER_OFF", icon_only= True)
        
        Torso = Body.box()
        Torso.label(text="Torso")
        Torso = Torso.column(align=True)
        Torso.prop(rig.pose.bones["CTRL-Pelvis"], '["Smooth - Viewport Body"]', toggle=True, icon="RESTRICT_VIEW_OFF", icon_only= True)
        Torso.prop(rig.pose.bones["CTRL-Pelvis"], '["Smooth - Render Body"]', toggle=True, icon="RESTRICT_RENDER_OFF", icon_only= True)
        ArmR = Body.box()
        ArmR.label(text="Arm Right")
        ArmR = ArmR.column(align=True)
        ArmR.prop(rig.pose.bones["CTRL-IK-UpperArm.R"], '["Smooth - Viewport Arm.R"]', toggle=True, icon="RESTRICT_VIEW_OFF", icon_only= True)
        ArmR.prop(rig.pose.bones["CTRL-IK-UpperArm.R"], '["Smooth - Render Arm.R"]', toggle=True, icon="RESTRICT_RENDER_OFF", icon_only= True)
        Legs = RoundnessBox.row(align=False)
        Legs = Legs.split(factor=0.5)
        LegL = Legs.split(factor=0.3)
        LegL.column()
        LegL = LegL.box()
        LegL.label(text="Leg Left")
        LegL = LegL.column(align=True)
        LegL.prop(rig.pose.bones["CTRL-UpperLeg.R"], '["Smooth - Viewport Leg.R"]', toggle=True, icon="RESTRICT_VIEW_OFF", icon_only= True)
        LegL.prop(rig.pose.bones["CTRL-UpperLeg.R"], '["Smooth - Render Leg.R"]', toggle=True, icon="RESTRICT_RENDER_OFF", icon_only= True)
        LegR = Legs.split(factor=0.7)
        LegR = LegR.box()
        LegR.label(text="Leg Right")
        LegR = LegR.column(align=True)
        LegR.prop(rig.pose.bones["CTRL-UpperLeg.L"], '["Smooth - Viewport Leg.L"]', toggle=True, icon="RESTRICT_VIEW_OFF", icon_only= True)
        LegR.prop(rig.pose.bones["CTRL-UpperLeg.L"], '["Smooth - Render Leg.L"]', toggle=True, icon="RESTRICT_RENDER_OFF", icon_only= True)


class VIEW3D_PT_optimization_settings(bpy.types.Panel):
    bl_label = "Optimisation Settings"
    bl_parent_id = "OBJECT_PT_SquaredMediaRigSettings"
    bl_idname = "OBJECT_PT_SquaredMediaOptimisationSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category


    def draw(self, context):
        rig = bpy.context.active_object
        
        layout = self.layout



