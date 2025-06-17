import bpy
from ..msc.utils import get_material_object, is_packed
from .. import properties

rigID = properties.RigProperties.rigID
category = properties.UIProperties.category

def eye_settings(self, context, Eye, ParentBox, name):
    rig = bpy.context.active_object

    ParentBox.label(text=name, icon = "HIDE_OFF")
    row = ParentBox.column(align=True)

    row.prop(rig.pose.bones["Settings"],'["Eye Offset"]',expand = True, index = 1 if name == "Right" else 0)

    row = ParentBox.row()
    row.prop(Eye[0], "default_value", text = Eye[0].name)
    
    row = ParentBox.row()
    row.prop(Eye[1], "default_value", text =Eye[1].name)
    
    row = ParentBox.row()
    row.prop(Eye[2], "default_value", text =Eye[2].name)
    
    row = ParentBox.row()
    row.prop(Eye[3], "default_value", text = Eye[3].name, toggle = True)

    row = ParentBox.row()
    row.prop(Eye[4], "default_value", text = Eye[4].name)

def advanced_eye_settings(self, context, EyeR, ParentBox, name):
          #Advanced Settings

    ParentBox.label(text=name, icon = "HIDE_OFF")
    col = ParentBox.column()

    Pupil = col.box()
    Pupil.label(text="Pupil")
    Pupil = Pupil.column(align=True)
    Pupil.prop(EyeR[5], "default_value", text = EyeR[5].name)
    Pupil.prop(EyeR[6], "default_value", text = EyeR[6].name)
    Pupil.prop(EyeR[7], "default_value", text = EyeR[7].name)
    Pupil.prop(EyeR[8], "default_value", text = EyeR[8].name)
#
    Pupil.label(text="Iris")
    Pupil.prop(EyeR[9], "default_value", text = EyeR[9].name)
    Pupil.prop(EyeR[12], "default_value", text = EyeR[12].name)

#
#
    Reflection = col.box()
    Reflection.label(text="Reflection")
    Reflection = Reflection.column(align=True)
#
    Reflection.prop(EyeR[13], "default_value", text = EyeR[13].name)
    Reflection.prop(EyeR[14], "default_value", text = EyeR[14].name)
    
    row = Reflection.row()
    row = row.split(factor=0.5)
    row.label(text="Rotation")
    row.prop(EyeR[16], "default_value", text = "")

#-----------------

def draw_eyebrowBox(self,context,Eyebrow,Parentbox, name):
     Parentbox.label(text=name)
     row = Parentbox.row()
     row.prop(Eyebrow[0], "default_value", text = Eyebrow[0].name)

     row = Parentbox.row()
     row.prop(Eyebrow[1], "default_value", text = Eyebrow[1].name)

def draw_TextureBox(self,context,layout,rig,Mat_obj):  
    if Mat_obj is None:
            Errorbox = layout.box()
            Errorbox.label(text="ERROR: No material object found")
            return  
    
    TexutureBox = layout.box()
    TexutureBox.prop(rig.pose.bones["WGT-UIProperties"],'["SkinConf"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["SkinConf"] else "RIGHTARROW", emboss = False, text = "Skin Selector  ")
    if rig.pose.bones["WGT-UIProperties"]["SkinConf"]:

        img = Mat_obj.material_slots[0].material.node_tree.nodes["SkinTexture"].image

        left = TexutureBox.row(align=True)
        left.operator("squaredmedia.imgpack", icon="PACKAGE").id_name = img.name

        main = left.row(align=True)
        main.enabled = not is_packed(img)
        main.prop(img, "filepath", text="")
        main.operator("squaredmedia.imgreload", icon="FILE_REFRESH").id_name = img.name   

def draw_proportionBox(self,context,layout,rig):
     #Proportions
    ProportionsBox = layout.box()
    ProportionsBox.prop(rig.pose.bones["WGT-UIProperties"],'["FaceConfig"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["FaceConfig"] else "RIGHTARROW", emboss = False, text = "Face Configurator  ")

    
    if rig.pose.bones["WGT-UIProperties"]["FaceConfig"]:
        
        #General
        GenerablBox = ProportionsBox.box()
        GenerablBox.label(text="General")
        row = GenerablBox.row()
        row.prop(rig.pose.bones["MCH-FaceSlider"],'["FaceHeight"]', toggle = True, text = "Face Height")


        #Eyebrows
        Eyebrowbox = ProportionsBox.box()
        Eyebrowbox.label(text="Eybrows")
        row = Eyebrowbox.row()
        row.prop(rig.pose.bones["Settings"],'["Eyebrow_R_enabled"]', text="Eyebrow R", toggle = True)
        row.prop(rig.pose.bones["Settings"],'["Eyebrow_L_enabled"]', text="Eyebrow L", toggle = True)
        row = Eyebrowbox.row()
        row.prop(rig.pose.bones["MCH-Eyebrows_scale_ref"],'["EyebrowHeight"]', text="Eyebrow Height Offset", toggle = True)


        #Eyes
        Eyebox = ProportionsBox.box()
        Eyebox.label(text="Eyes")
        row = Eyebox.row()
        row.prop(rig.pose.bones["Settings"],'["Eye_R_enable"]', text="Eye R", toggle=True)
        row.prop(rig.pose.bones["Settings"],'["Eye_L_enable"]', text="Eye L", toggle=True)
        row=Eyebox.row()
        row.prop(rig.pose.bones["MCH-Eyes"],'["EyeHeight"]', text="Eye Height Offset", toggle=True)


        #Mouth
        Mouthbox = ProportionsBox.box()
        Mouthbox.label(text="Mouth")
        Mouthbox.prop(rig.pose.bones["Settings"],'["Mouth_enable"]', text = "Mouth", toggle = True)
        
        if rig.pose.bones["Settings"]["Mouth_enable"]:
            Mouthbox.box().prop(rig.pose.bones["Settings"],'["Teeth_enable"]', text = "Teeth", toggle = True)


        row = Mouthbox.row()
        row.prop(rig.pose.bones["MCH-Mouth"],'["MouthHeight"]', text="Mouth Height Offset")
        
        AdvancedBox = ProportionsBox.box()
        AdvancedBox.prop(rig.pose.bones["WGT-UIProperties"],'["Advanced_Face_Config"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["Advanced_Face_Config"] else "RIGHTARROW", emboss = False, text = "Advanced Face Settings")

        if rig.pose.bones["WGT-UIProperties"]["Advanced_Face_Config"]:
        
            AdvancedBox.label(text="Advanced")
            row = AdvancedBox.row()
            split = row.split(factor=0.5)
            col = split.column(align = True)
            col.prop(rig.pose.bones["MCH-Eyebrows"],'["Eyebrow_R"]',index = 0, text = "Eyebrow R Thickness")
            col.prop(rig.pose.bones["MCH-Eyebrows"],'["Eyebrow_R"]',index = 1, text = "Eyebrow R Height")
            col.prop(rig.pose.bones["MCH-Eyebrows"],'["Eyebrow_R_width"]', text = "Eyebrow R Width")


            col = split.column(align = True)
            col.prop(rig.pose.bones["MCH-Eyebrows"],'["Eyebrow_L"]',index = 0, text = "Eyebrow L Thickness")
            col.prop(rig.pose.bones["MCH-Eyebrows"],'["Eyebrow_L"]',index = 1, text = "Eyebrow L Height")
            col.prop(rig.pose.bones["MCH-Eyebrows"],'["Eyebrow_L_width"]', text = "Eyebrow L Width")

            row = AdvancedBox.row()
            row.prop(rig.pose.bones["MCH-Eyebrows"],'["Eyebrow_gap"]', toggle = True, text = "Eyebrow Gap")


            row = AdvancedBox.row()
            col = row.column(align=True)
            col.prop(rig.pose.bones["MCH-Eyes"],'["Eye_R_Height"]', toggle = True, text = "Eye R Height")
            col.prop(rig.pose.bones["MCH-Eyes"],'["Eye_R_Width"]', toggle = True, text = "Eye R Width")

            col = row.column(align=True)
            col.prop(rig.pose.bones["MCH-Eyes"],'["Eye_L_Height"]', toggle = True, text = "Eye L Height")
            col.prop(rig.pose.bones["MCH-Eyes"],'["Eye_L_Width"]', toggle = True, text = "Eye L Width")
            
            row = AdvancedBox.row()
            row.prop(rig.pose.bones["MCH-Eyes"],'["Eye_Gap"]', toggle = True, text = "Eye Gap")

def draw_eyebrowBox01(self,context,layout,rig,Mat_obj):
    #Eyebrows
    EyebrowBox = layout.box()
    EyebrowBox.prop(rig.pose.bones["WGT-UIProperties"],'["EyebrowConfig"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["EyebrowConfig"] else "RIGHTARROW", emboss = False, text = "Eyebrow Settings")
    if rig.pose.bones["WGT-UIProperties"]["EyebrowConfig"]:
        EyebrowL = Mat_obj.material_slots[3].material.node_tree.nodes["Eyebrow"].inputs
        EyebrowR = Mat_obj.material_slots[4].material.node_tree.nodes["Eyebrow"].inputs

        split = EyebrowBox.split(factor=0.5)
        draw_eyebrowBox(self, context, EyebrowR, split.box(), "Right")
        draw_eyebrowBox(self, context, EyebrowL, split.box(), "Left")

def draw_EyeBox(self,context,layout,rig,Mat_obj):
        #Eye Settings
    ColorBox = layout.box()
    ColorBox.prop(rig.pose.bones["WGT-UIProperties"],'["EyeConfig"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["EyeConfig"] else "RIGHTARROW", emboss = False, text = "Eye Settings")
    if rig.pose.bones["WGT-UIProperties"]["EyeConfig"]:
        Eye = ColorBox.row()

        if rig.pose.bones["Settings"]["Eye_R_enable"] and rig.pose.bones["Settings"]["Eye_L_enable"]:
            Eye = Eye.split(factor=0.5)
        
        EyeRBox = Eye.box()
        EyeLBox = Eye.box()

        EyeAdvanced = ColorBox.box()

        EyeAdvanced.prop(rig.pose.bones["Settings"],'["EyeAdvanced"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["Settings"]["EyeAdvanced"] else "RIGHTARROW", emboss = False, text = "Advanced Eye Settings")
        if rig.pose.bones["Settings"]["Eye_R_enable"] and rig.pose.bones["Settings"]["Eye_L_enable"]:
            EyeAdvanced = EyeAdvanced.split(factor=0.5)



        #Right Eye 
        if rig.pose.bones["Settings"]["Eye_R_enable"]:
            EyeR = Mat_obj.material_slots[1].material.node_tree.nodes["Eye.R"].inputs
            eye_settings(self, context, EyeR, EyeRBox, "Right")
            if rig.pose.bones["Settings"]["EyeAdvanced"]:
                EyeAdvancedR = EyeAdvanced.box()
                advanced_eye_settings(self, context, EyeR, EyeAdvancedR, "Right")
        else:
            EyeRBox.label(text="disabled")


        #Left Eye
        if rig.pose.bones["Settings"]["Eye_L_enable"]:
            EyeL = Mat_obj.material_slots[2].material.node_tree.nodes["Eye.L"].inputs
            eye_settings(self, context, EyeL, EyeLBox, "Left")
            if rig.pose.bones["Settings"]["EyeAdvanced"]:
                EyeAdvancedL = EyeAdvanced.box()
                advanced_eye_settings(self, context, EyeL, EyeAdvancedL, "Left")
        else:
            EyeLBox.label(text="disabled")

#-----------------

def draw_skin_settings(self, context):
    rig = bpy.context.active_object
    Mat_obj = get_material_object(rig)
    
    layout = self.layout
    draw_TextureBox(self,context,layout,rig,Mat_obj)
    draw_proportionBox(self,context,layout,rig)
    draw_eyebrowBox01(self,context,layout,rig,Mat_obj)
    draw_EyeBox(self,context,layout,rig,Mat_obj)
    