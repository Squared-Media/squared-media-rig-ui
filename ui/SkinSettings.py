import bpy
from ..utils import get_material_object, is_packed
from .. import properties

rigID = properties.rigID
category = properties.category

class SkinSettingsUI(bpy.types.Panel):
    bl_label = "Skin Settings"
    bl_idname = "OBJECT_PT_SquaredMediaSkinSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category


    @classmethod
    def poll(self, context):
        obj = context.active_object
        return obj and obj.get("rig_id") == rigID
    def draw(self, context):
        rig = bpy.context.active_object
        Mat_obj = get_material_object(rig)
        
        layout = self.layout

        if Mat_obj is None:
                Errorbox = layout.box()
                Errorbox.label(text="ERROR: No material object found")
                return
            
        DisplayEyeBox = rig.pose.bones["Settings"]["EyesVisible"]
        EyesBox = layout.box()
        row = EyesBox.row()
        row.label(text="Eye Settings")

        if DisplayEyeBox:
            EyeIcon = "HIDE_OFF"
        else:
            EyeIcon = "HIDE_ON"
        row.prop(rig.pose.bones["Settings"],'["EyesVisible"]', text = "", icon = EyeIcon)

        if DisplayEyeBox:    
            EyeR = Mat_obj.material_slots[1].material.node_tree.nodes["Eye.R"].inputs
            EyeL = Mat_obj.material_slots[2].material.node_tree.nodes["Eye.L"].inputs
            
            
            #Eye Color
            ColorBox = EyesBox.box()
            ColorBox.label(text="Eye Color")
            ColorBox.prop(rig.pose.bones["Settings"],'["Heterochromia"]')  
            row = ColorBox.row()                 
            
                
            if rig.pose.bones["Settings"]["Heterochromia"]:
                row.prop(EyeR[2], "default_value", text = "Eye R")
                row = ColorBox.row()
                row.prop(EyeL[2], "default_value", text = "Eye L")
            else:
                ColorBox.prop(rig.pose.bones["Settings"],'["Global Eye Color"]')
            
            #Eye Emission
            EyeEmissionBox = EyesBox.box()
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
            #main.operator("squaredmedia.imgreload", icon="FILE_REFRESH").id_name = img.name   