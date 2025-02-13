import bpy
from .. import properties

rigID = properties.RigProperties.rigID
category = properties.UIProperties.category
preferences = bpy.context.preferences.addons[properties.AddonProperties.module_name]
parentPanel = "OBJECT_PT_SquaredMediaHeader"


def drawEyeSettings(self, context):
    rig = bpy.context.active_object
    
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
    rig = bpy.context.active_object
    
    layout = self.layout
    ArmBox = layout.box()
    ArmBox.prop(rig.pose.bones["WGT-UIProperties"],'["ArmRigConf"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["ArmRigConf"] else "RIGHTARROW", emboss = False, text = "Arm Settings")
    if rig.pose.bones["WGT-UIProperties"]["ArmRigConf"]:


        SlimArmBox = ArmBox.box()
        SlimArmBox.label(text = "Slim Arm")
        SlimArmBox.prop(rig.pose.bones["Settings"],'["Slim Arms"]', toggle = True)

        IKArmsBox = ArmBox.box()
        IKArmsBox.label(text="IK Arms")
        col = IKArmsBox.column(align=False)
        col.prop(rig.pose.bones["CTRL-IK-LowerArm.L"], '["IK Arm L"]')
        col.prop(rig.pose.bones["CTRL-IK-LowerArm.R"], '["IK Arm R"]')

        StretchyBox = ArmBox.box()
        StretchyBox.label(text="Stretchy Arms")
        col = StretchyBox.column(align=False)
        col.prop(rig.pose.bones["CTRL-IK-LowerArm.L"], '["Stretchy Arm L"]')
        col.prop(rig.pose.bones["CTRL-IK-LowerArm.R"], '["Stretchy Arm R"]')

        AttachmentBox = ArmBox.box()
        AttachmentBox.label(text="Attachments")
        col = AttachmentBox.column(align=False)
        col.prop(rig.pose.bones["CTRL-HandAttachment.L"], '["Parent to Arm"]', text="Parent to Arm L")
        col.prop(rig.pose.bones["CTRL-HandAttachment.R"], '["Parent to Arm"]', text="Parent to Arm R")

def drawBodySettings(self, context):
    rig = bpy.context.active_object
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
    rig = bpy.context.active_object
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
        DetachBox = LegBox.box()
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

def drawRoundnessSettings(self, context):
    rig = bpy.context.active_object
    
    # Roundness Settings
    layout = self.layout
    RoundnessBox = layout.box()
    RoundnessBox.prop(rig.pose.bones["WGT-UIProperties"],'["RoundnessConf"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["RoundnessConf"] else "RIGHTARROW", emboss = False, text = "Roundness Settings")
    if rig.pose.bones["WGT-UIProperties"]["RoundnessConf"]:
        
        #Head 
        HeadArea = RoundnessBox.row()
        Head = HeadArea.box()
        Head.label(text="Head")
        col = Head.column(align = True)
        col.prop(rig.pose.bones["CTRL-Head"], '["Smooth - Viewport Head"]', toggle=True, icon="RESTRICT_VIEW_OFF", icon_only= True)
        col.prop(rig.pose.bones["CTRL-Head"], '["Smooth - Render Head"]', toggle=True, icon="RESTRICT_RENDER_OFF", icon_only= True)

        #Body
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
        
        
        #Legs
        Legs = RoundnessBox.row(align=False)
        LegL = Legs.box()
        LegL.label(text="Leg Left")
        LegL = LegL.column(align=True)
        LegL.prop(rig.pose.bones["CTRL-UpperLeg.R"], '["Smooth - Viewport Leg.R"]', toggle=True, icon="RESTRICT_VIEW_OFF", icon_only= True)
        LegL.prop(rig.pose.bones["CTRL-UpperLeg.R"], '["Smooth - Render Leg.R"]', toggle=True, icon="RESTRICT_RENDER_OFF", icon_only= True)

        LegR = Legs.box()
        LegR.label(text="Leg Right")
        LegR = LegR.column(align=True)
        LegR.prop(rig.pose.bones["CTRL-UpperLeg.L"], '["Smooth - Viewport Leg.L"]', toggle=True, icon="RESTRICT_VIEW_OFF", icon_only= True)
        LegR.prop(rig.pose.bones["CTRL-UpperLeg.L"], '["Smooth - Render Leg.L"]', toggle=True, icon="RESTRICT_RENDER_OFF", icon_only= True)

def draw_all_rig_settings(self,context):
     drawEyeSettings(self, context)
     drawArmSettings(self, context)
     drawBodySettings(self, context)
     drawLegSettings(self, context)
     drawRoundnessSettings(self, context)

class Test(bpy.types.GizmoGroup):
    bl_idname = "CustomGizmos"
    bl_label = "Custom gizmos"
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"
    bl_options = {'PERSISTENT', 'SCALE'}
    bl_order = 3
    

    @classmethod
    def poll(cls, context):
        rig = bpy.context.active_object
        return rig and rig.get("rig_id") == "SquaredMediaDefaultRig"
    
    def draw_prepare(self, context):
        region_width = context.region.width
        region_height = context.region.height
    
    # Get the width of the N panel (right toolbar)
        n_panel_width = 0
        if context.area.ui_type == 'VIEW_3D' and context.space_data.show_region_ui:
            for region in context.area.regions:
                if region.type == 'UI':
                    n_panel_width = region.width

        # Set the initial position for the gizmos
        r_xpos = region_width -  n_panel_width  # Adjust this for the X position
        r_ypos = region_height
        ui_scale = context.preferences.view.ui_scale
        for gizmo in self.gizmos:
            gizmo.matrix_basis[0][3] = r_xpos - 22.5 * ui_scale
            gizmo.matrix_basis[1][3] = r_ypos - 300 * ui_scale


       
    def setup(self, context):
        mpr = self.gizmos.new("GIZMO_GT_button_2d")
        mpr.bl_idname = "RunForestButton"
        mpr.draw_options = {'BACKDROP', 'OUTLINE'}
        mpr.target_set_operator('squaredmedia.set_camera')
        mpr.alpha = 0.5
        mpr.color = 0.5, 0.1, 0.5
        mpr.color_highlight = 1.0, 1.0, 1.0
        mpr.alpha_highlight = 0.1
        mpr.scale_basis = (30) / 2
        mpr.use_tooltip = True
        mpr.show_drag = False
        mpr.use_draw_value = True
        mpr.icon = "LOCKVIEW_ON"  # Default icon

    #def draw(self, context):
        #rig = bpy.context.active_object
        #SQM_Camera = rig["Cam"]
        #layout = self.layout
        #layout.scale_y = 2.0  
        #layout.operator("squaredmedia.set_camera", icon ="LOCKVIEW_ON" if SQM_Camera.hide_viewport else "LOCKVIEW_OFF", text="Start Face Anim" if SQM_Camera.hide_viewport else "End Face Anim")
