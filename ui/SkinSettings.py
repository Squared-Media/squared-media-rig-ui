import bpy
from ..utils import get_material_object, is_packed
from .. import properties

rigID = properties.RigProperties.rigID
category = properties.UIProperties.category


def eye_settings(self, context, Eye, ParentBox, name):
    ParentBox.label(text=name, icon = "HIDE_OFF")
    row = ParentBox.row(align=True)
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

    Right = ParentBox.column()
    Right.label(text=name, icon = "HIDE_OFF")

    Pupil = Right.box()
    Pupil.label(text="Pupil")
    Pupil = Pupil.column(align=True)
    Pupil.prop(EyeR[5], "default_value", text = EyeR[5].name)
    Pupil.prop(EyeR[6], "default_value", text = EyeR[6].name)
    Pupil.prop(EyeR[7], "default_value", text = EyeR[7].name)
    Pupil.prop(EyeR[8], "default_value", text = EyeR[8].name)

    Pupil.label(text="Iris")
    Pupil.prop(EyeR[9], "default_value", text = EyeR[9].name)


    Reflection = Right.box()
    Reflection.label(text="Reflection")
    Reflection = Reflection.column(align=True)

    Reflection.prop(EyeR[12], "default_value", text = EyeR[12].name)
    Reflection.prop(EyeR[13], "default_value", text = EyeR[13].name)
    
    row = Reflection.row()
    row = row.split(factor=0.5)
    row.label(text="Rotation")
    row.prop(EyeR[14], "default_value", text = "")

def draw_skin_settings(self, context):
    rig = bpy.context.active_object
    Mat_obj = get_material_object(rig)
    
    layout = self.layout

    if Mat_obj is None:
            Errorbox = layout.box()
            Errorbox.label(text="ERROR: No material object found")
            return




    EyeR = Mat_obj.material_slots[1].material.node_tree.nodes["Eye.R"].inputs
    EyeL = Mat_obj.material_slots[2].material.node_tree.nodes["Eye.L"].inputs
    
    
    #Eye Color
    ColorBox = layout.box()
    ColorBox.label(text="Eye Settings")


    Eye = ColorBox.row()
    Eye = Eye.split(factor=0.5)
    eye_settings(self, context, EyeL, Eye.box(), "Left")
    eye_settings(self, context, EyeR, Eye.box(), "Right")

    Eye_Advanced = ColorBox.row()
    Eye_Advanced = Eye_Advanced.split(factor=0.5)
    advanced_eye_settings(self, context, EyeR, Eye_Advanced.box(), "Right")
    advanced_eye_settings(self, context, EyeL, Eye_Advanced.box(), "Left")


    



        




    # Second Skin Layer
    SecondLayerBox = layout.box()
    SecondLayerBox.label(text="Second Layer")
    left = SecondLayerBox.row(align=True)
    left.prop(rig.pose.bones["Settings"], '["Skin Layer 02"]', toggle=True, text = "Viewport", icon ="RESTRICT_VIEW_OFF")
    right = left.row(align=True)
    right.prop(rig.pose.bones["Settings"], '["Skin Layer 02 Render"]', toggle=True , text = "Render", icon = "RESTRICT_RENDER_OFF")


    #Texture Box
    TexutureBox = layout.box()
    TexutureBox.label(text="Skin Texture")
    img = Mat_obj.material_slots[0].material.node_tree.nodes["SkinTexture"].image

    left = TexutureBox.row(align=True)
    left.operator("squaredmedia.imgpack", icon="PACKAGE").id_name = img.name

    main = left.row(align=True)
    main.enabled = not is_packed(img)
    main.prop(img, "filepath", text="")
    main.operator("squaredmedia.imgreload", icon="FILE_REFRESH").id_name = img.name   