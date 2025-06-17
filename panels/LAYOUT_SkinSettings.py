import bpy
from ..msc.utils import get_material_object, is_packed
from .. import properties

rigID = properties.RigProperties.rigID
category = properties.UIProperties.category

def eye_settings(self, context, Eye, ParentBox, name):
    rig = bpy.context.active_object

    ParentBox.label(text=name, icon = "HIDE_OFF")
    row = ParentBox.column(align=True)


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

def draw_advanced_Eyes(self, context, Eye, ParentBox, name):
          #Advanced Settings

    ParentBox.label(text=name, icon = "HIDE_OFF")
    col = ParentBox.column()

    Pupil = col.box()
    Pupil.label(text="Pupil")
    Pupil = Pupil.column(align=True)
    Pupil.prop(Eye[5], "default_value", text = Eye[5].name)
    Pupil.prop(Eye[6], "default_value", text = Eye[6].name)
    Pupil.prop(Eye[7], "default_value", text = Eye[7].name)
    Pupil.prop(Eye[8], "default_value", text = Eye[8].name)
#
    Pupil.label(text="Iris")
    Pupil.prop(Eye[9], "default_value", text = Eye[9].name)
    Pupil.prop(Eye[12], "default_value", text = Eye[12].name)

#
#
    Reflection = col.box()
    Reflection.label(text="Reflection")
    Reflection = Reflection.column(align=True)
#
    Reflection.prop(Eye[13], "default_value", text = Eye[13].name)
    Reflection.prop(Eye[14], "default_value", text = Eye[14].name)
    
    row = Reflection.row()
    row = row.split(factor=0.5)
    row.label(text="Rotation")
    row.prop(Eye[16], "default_value", text = "")

#-----------------

def draw_eyebrowBox(self,context,Eyebrow,Parentbox, name):
     Parentbox.label(text=name)
     row = Parentbox.row()
     row.prop(Eyebrow[0], "default_value", text = Eyebrow[0].name)

     #row = Parentbox.row()
     #row.prop(Eyebrow[1], "default_value", text = Eyebrow[1].name)

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
    ColorBox.prop(rig.pose.bones["WGT-UIProperties"],'["EyeConfig"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["EyeConfig"] else "RIGHTARROW", emboss = False, text = "Eye & Brow Settings")
    if rig.pose.bones["WGT-UIProperties"]["EyeConfig"]:

        #Eyes
        EyeBox = ColorBox.row().box()
        EyeBox.label(text="Eye Settings")
        Eye = EyeBox.split(factor=0.5) 
        EyeLBox = Eye.box()
        EyeRBox = Eye.box()

        #Right Eye 
        if rig.pose.bones["Settings"]["Eye_R_enable"]:
            EyeR = Mat_obj.material_slots[1].material.node_tree.nodes["Eye.R"].inputs
            eye_settings(self, context, EyeR, EyeRBox, "Right")
        else:
            EyeRBox.label(text="disabled")


        #Left Eye
        if rig.pose.bones["Settings"]["Eye_L_enable"]:
            EyeL = Mat_obj.material_slots[2].material.node_tree.nodes["Eye.L"].inputs
            eye_settings(self, context, EyeL, EyeLBox, "Left")
        else:
            EyeLBox.label(text="disabled")
        

        #Eyebrows
        EyebrowBox = ColorBox.row().box()
        EyebrowBox.label(text="Eyebrow Settings")
        Eyebrow = EyebrowBox.split(factor=0.5) 
        EyebrowLBox = Eyebrow.box()
        EyebrowRBox = Eyebrow.box()

        EyebrowL = Mat_obj.material_slots[3].material.node_tree.nodes["Eyebrow"].inputs
        EyebrowR = Mat_obj.material_slots[4].material.node_tree.nodes["Eyebrow"].inputs
        if rig.pose.bones["Settings"]["Eyebrow_R_enabled"]:
            draw_eyebrowBox(self, context, EyebrowR, EyebrowRBox.box(), "Right")
        else:
            EyebrowRBox.label(text="disabled")

        if rig.pose.bones["Settings"]["Eyebrow_L_enabled"]:
            draw_eyebrowBox(self, context, EyebrowL, EyebrowLBox.box(), "Right")
        else:
            EyebrowLBox.label(text="disabled")


def draw_advanced_EyeBox(self,context,layout,rig,Mat_obj):
        #Eye Settings
    ColorBox = layout.box()
    ColorBox.prop(rig.pose.bones["WGT-UIProperties"],'["EyeRigConf"]', toggle = True, icon = "DOWNARROW_HLT" if rig.pose.bones["WGT-UIProperties"]["EyeRigConf"] else "RIGHTARROW", emboss = False, text = "Advanced Eye Settings")
    if rig.pose.bones["WGT-UIProperties"]["EyeRigConf"]:
        Eye = ColorBox.row()

        if rig.pose.bones["Settings"]["Eye_R_enable"] and rig.pose.bones["Settings"]["Eye_L_enable"]:
            Eye = Eye.split(factor=0.5)
        
        EyeRBox = Eye.box()
        EyeLBox = Eye.box()


        #Right Eye 
        if rig.pose.bones["Settings"]["Eye_R_enable"]:
            EyeR = Mat_obj.material_slots[1].material.node_tree.nodes["Eye.R"].inputs
            draw_advanced_Eyes(self, context, EyeR, EyeRBox, "Right")
        else:
            EyeRBox.label(text="disabled")


        #Left Eye
        if rig.pose.bones["Settings"]["Eye_L_enable"]:
            EyeL = Mat_obj.material_slots[2].material.node_tree.nodes["Eye.L"].inputs
            draw_advanced_Eyes(self, context, EyeL, EyeLBox, "Left")
        else:
            EyeLBox.label(text="disabled")

#-----------------

def draw_skin_settings(self, context):
    rig = bpy.context.active_object
    Mat_obj = get_material_object(rig)
    
    layout = self.layout
    draw_TextureBox(self,context,layout,rig,Mat_obj)
    draw_proportionBox(self,context,layout,rig)
    draw_EyeBox(self,context,layout,rig,Mat_obj)
    draw_advanced_EyeBox(self, context, layout, rig, Mat_obj)
    