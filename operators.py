import bpy
import os
from .utils import is_packed
from . import properties

blend_file = properties.blend_file
lib_folder = properties.lib_folder
collection_name = properties.collection_name

rigID = properties.rigID



class ImgPack(bpy.types.Operator):
    bl_idname = "squaredmedia.imgpack"
    bl_label = ""
    bl_description = "packs or unpacks textures"

    id_name: bpy.props.StringProperty()

    def execute(self, context):
        img = bpy.data.images[self.id_name]
        if is_packed(img):
            if bpy.data.is_saved:
                img.unpack()
            else:
                img.unpack(method="USE_ORIGINAL")
        else:
            img.pack()
        return {"FINISHED"}

class ImgReload(bpy.types.Operator):
    bl_idname = "squaredmedia.imgreload"
    bl_label = ""
    bl_description = "refreshes texture"

    id_name: bpy.props.StringProperty()

    def execute(self, context):
        bpy.data.images[self.id_name].reload()
        return {"FINISHED"}

class KeyframeAllProperties(bpy.types.Operator):
    """Add keyframes to all custom properties except those containing 'Visible'"""
    bl_idname = "squaredmedia.keyframe_all_custom_properties"
    bl_label = "Keyframe Custom Properties"
    bl_options = {'REGISTER', 'UNDO'}

    frame: bpy.props.IntProperty(name="Frame", default=1)

    def execute(self, context):
        obj = context.object  # Get the active object
        
        # Ensure the object is an armature
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Active object is not an armature")
            return {'CANCELLED'}
        
        frame = bpy.context.scene.frame_current  # Get the current frame
        
        # Keyframe all custom properties on the armature object
        for key in obj.keys():
            if key not in '_RNA_UI' and "Visible" not in key:  # Exclude Blender's internal property group
                try:
                    obj.keyframe_insert(data_path=f'["{key}"]', frame=frame)
                    self.report({'INFO'}, f"Keyframe added to armature property: {key}")
                except:
                    self.report({'WARNING'}, f"Failed to keyframe armature property: {key}")
        
        # Keyframe all custom properties on the pose bones
        for bone in obj.pose.bones:
            for key in bone.keys():
                if key not in '_RNA_UI' and "Visible" not in key:  # Exclude Blender's internal property group
                    try:
                        bone.keyframe_insert(data_path=f'["{key}"]', frame=frame)
                        self.report({'INFO'}, f"Keyframe added to bone '{bone.name}' property: {key}")
                    except:
                        self.report({'WARNING'}, f"Failed to keyframe bone '{bone.name}' property: {key}")
        
        self.report({'INFO'}, f"Keyframed all custom properties in armature '{obj.name}'")
        return {'FINISHED'}

class LinkRig(bpy.types.Operator):

    bl_idname = "squaredmedia.link_rig"
    bl_label = "Check Rig File"
    bl_description = "Checks if the rig .blend file is present in the blend folder"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Define the path to the rig blend file
        rig_blend_path = os.path.join(os.path.dirname(__file__),lib_folder, blend_file)
        
        # Check if the .blend file exists
        if not os.path.exists(rig_blend_path):
            self.report({'ERROR'}, f"Blend file not found: {rig_blend_path}")
            return {'CANCELLED'}
        
            
        
        bpy.ops.wm.link(
            filepath=rig_blend_path,  # Path to the .blend file
            directory=rig_blend_path + "/Collection/",  # Collection directory inside the blend file
            filename=collection_name,  # Name of the collection to link
        )


        bpy.ops.object.make_override_library()

        linked_collection = bpy.data.collections.get(collection_name)
        linked_collection.name = "wadwad"

        print(linked_collection)

        if not linked_collection:
            raise RuntimeError(f"Collection {collection_name} not found.")

        

        return {'FINISHED'}
    
class SetCamera(bpy.types.Operator):
    bl_idname = "squaredmedia.set_camera" 
    bl_label =   "sets Face Animation camera to be active"
    

    @classmethod
    def poll(self, context):
        obj = context.active_object
        return obj and obj.get("rig_id") == rigID


    def execute(self, context):
        rig = bpy.context.active_object
        SQM_Camera = rig["Cam"]
        bpy.context.space_data.use_local_camera = True
        bpy.context.space_data.camera = SQM_Camera
        bpy.context.space_data.lock_camera = True
        bpy.ops.view3d.view_camera()
        return {"FINISHED"}
    
class ResetCamera(bpy.types.Operator):
    bl_idname = "squaredmedia.reset_camera" 
    bl_label="sets new camera to be active"
 
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return obj and obj.get("rig_id") == rigID
    
   
    def execute(self, context):
        bpy.context.space_data.use_local_camera = False
        bpy.context.space_data.lock_object = None
        bpy.context.space_data.lock_camera = False
        bpy.ops.view3d.view_camera()
        return {"FINISHED"}
  