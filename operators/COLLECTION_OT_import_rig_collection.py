import bpy
import os
from .. import properties


class COLLECTION_OT_import_rig_collection(bpy.types.Operator):
    """imports the skin, armature and boneshapes into the current file according to Default Import Options in the properties"""
    bl_idname = "squaredmedia.import_rig"
    bl_label = "Check Rig File"
    bl_description = "imports the skin, armature and boneshapes into the current file according to Default Import Options in the properties"
    bl_options = {'REGISTER', 'UNDO'}


    collection_name:    bpy.props.StringProperty(name="Collection Name", default="SQM Character Rig")#type: ignore
    rig_path:           bpy.props.StringProperty(name="Rig Path", default=properties.Paths.default_lib_path)#type: ignore   

    def invoke(self, context, event):
        preferences = context.preferences.addons[properties.AddonProperties.module_name].preferences
        if event.alt:
            self.report({'INFO'}, "ALT key is pressed - Inverting Default Import Option.")
            # Invert the DefaultImportOption
            if preferences.DefaultImportOption == 'LINK':
                self.inverted_option = 'APPEND'
            else:
                self.inverted_option = 'LINK'
        else:
            self.inverted_option = preferences.DefaultImportOption

        return self.execute(context)

    def execute(self, context):
        rig_blend_path = self.rig_path
        collection_name = self.collection_name
        if not os.path.exists(rig_blend_path):
            self.report({'ERROR'}, f"Blend file not found: {rig_blend_path}")
            return {'CANCELLED'}
        
        

        # using blenders default operator to link collection
        if bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.DefaultImportOption == 'LINK':
            bpy.ops.wm.link(
                filepath=rig_blend_path, 
                directory=rig_blend_path + "/Collection/",  
                filename=collection_name,
            )
            bpy.ops.object.make_override_library()
            

        elif bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.DefaultImportOption == 'APPEND':
            bpy.ops.wm.append(
                filepath=rig_blend_path, 
                directory=rig_blend_path + "/Collection/",  
                filename=collection_name,
            )



        return {'FINISHED'}
  