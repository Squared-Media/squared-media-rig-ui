import bpy
from ..utils import get_material_object, is_packed
from .. import properties

rigID = properties.RigProperties.rigID
category = properties.UIProperties.category


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
    ColorBox.label(text="Eye Color")
    ColorBox.prop(rig.pose.bones["Settings"],'["Heterochromia"]', toggle=True)  
    row = ColorBox.row()                 
    
        
    if rig.pose.bones["Settings"]["Heterochromia"]:
        row.prop(EyeR[2], "default_value", text = "Eye R")
        row = ColorBox.row()
        row.prop(EyeL[2], "default_value", text = "Eye L")
    else:
        ColorBox.prop(rig.pose.bones["Settings"],'["Global Eye Color"]')
    
    #Eye Emission
    EyeEmissionBox = layout.box()
    EyeEmissionBox.label(text="Eye Emission")
    row = EyeEmissionBox.row()  
    
    if rig.pose.bones["Settings"]["Heterochromia"]:
        row.prop(EyeR[4], "default_value", text = "Eye R")
        row = EyeEmissionBox.row()
        row.prop(EyeL[4], "default_value", text = "Eye L")
    else:
        EyeEmissionBox.prop(rig.pose.bones["Settings"],'["Global Eye Emission"]', text ="Eye Emission")
        
        
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