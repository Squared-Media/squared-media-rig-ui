import bpy
import os
import urllib.request
from .utils import is_packed
from . import properties


blend_file = properties.Paths.blend_file
lib_folder = properties.Paths.lib_folder
rigID = properties.RigProperties.rigID
GitubRepo = properties.Paths.GitubRepo


class IMAGE_OT_pack(bpy.types.Operator):
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

class IMAGE_OT_reload(bpy.types.Operator):
    bl_idname = "squaredmedia.imgreload"
    bl_label = ""
    bl_description = "refreshes texture"

    id_name: bpy.props.StringProperty()

    def execute(self, context):
        bpy.data.images[self.id_name].reload()
        return {"FINISHED"}

class OBJECT_OT_keyframe_all_properties(bpy.types.Operator):
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
        
        # Keyframe all custom properties on the pose bones
        for bone in obj.pose.bones:
            for key in bone.keys():
                if key not in '_RNA_UI' and "Visible" not in key:  # Exclude Blender's internal property group
                    try:
                        bone.keyframe_insert(data_path=f'["{key}"]', frame=frame, keytype = 'GENERATED')
                        self.report({'INFO'}, f"Keyframe added to bone '{bone.name}' property: {key}")
                    except:
                        self.report({'WARNING'}, f"Failed to keyframe bone '{bone.name}' property: {key}")
        
        self.report({'INFO'}, f"Keyframed all custom properties in armature '{obj.name}'")
        return {'FINISHED'}

class COLLECTION_OT_import_rig_collection(bpy.types.Operator):
    """links the skin, armature and boneshapes into the current file"""
    bl_idname = "squaredmedia.import_rig"
    bl_label = "Check Rig File"
    bl_description = "links the skin, armature and boneshapes into the current file"
    bl_options = {'REGISTER', 'UNDO'}


    collection_name: bpy.props.StringProperty(name="Collection Name", default="SQM Character Rig")#type: ignore

    def execute(self, context):
        rig_blend_path = os.path.join(os.path.dirname(__file__),lib_folder, blend_file)
        collection_name = self.collection_name

        if not os.path.exists(rig_blend_path):
            self.report({'ERROR'}, f"Blend file not found: {rig_blend_path}")
            return {'CANCELLED'}
        
        
        preferences = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences

        # using blenders default operator to link collection
        if bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.DefaultImportOption == 'LINK':
            bpy.ops.wm.link(
                filepath=rig_blend_path, 
                directory=rig_blend_path + "/Collection/",  
                filename=collection_name,
            )
            bpy.ops.object.make_override_library()
            
            imported_collection = bpy.data.collections.get(collection_name)
            imported_collection.name = preferences.CollectionName

        elif bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.DefaultImportOption == 'APPEND':
            bpy.ops.wm.append(
                filepath=rig_blend_path, 
                directory=rig_blend_path + "/Collection/",  
                filename=collection_name,
            )

            imported_collection = bpy.data.collections.get(collection_name)
            imported_collection.name = preferences.CollectionName


        return {'FINISHED'}
    
class SCENE_OT_set_view_camera(bpy.types.Operator):
    bl_idname = "squaredmedia.set_camera" 
    bl_label ="sets Face Animation camera to be active"


    def execute(self, context):
        rig = bpy.context.active_object
        
        # since rig made by me and linked from addon structure itself, we know that rig will always have a custom property containing the face camera 
        SQM_Camera = rig["Cam"]
        bpy.context.space_data.use_local_camera = True
        bpy.context.space_data.camera = SQM_Camera
        bpy.context.space_data.lock_camera = True
        bpy.ops.view3d.view_camera()
        return {"FINISHED"}
    
class SCENE_OT_reset_view_camera(bpy.types.Operator):
    bl_idname = "squaredmedia.reset_camera" 
    bl_label="sets new camera to be active"
    
   
    def execute(self, context):
        bpy.context.space_data.use_local_camera = False
        bpy.context.space_data.lock_object = None
        bpy.context.space_data.lock_camera = False
        bpy.ops.view3d.view_camera()
        return {"FINISHED"}

class UPDATE_OT_install_latest(bpy.types.Operator):
    """Download and install an addon from GitHub"""
    bl_idname = "squaredmedia.download_latest_version"
    bl_label = "Download and Install Addon"
    
    url: bpy.props.StringProperty(
        name="Download URL",
        description="URL of the addon .zip file to download",
        default= GitubRepo
    )#type: ignore
    
    def execute(self, context):
        try:

            addon_dir = bpy.utils.user_resource('SCRIPTS')
            if not addon_dir:
                self.report({'ERROR'}, "Could not locate Blender's addon directory.")
                return {'CANCELLED'}
            
            file_path = os.path.join(addon_dir, properties.AddonProperties.module_name)
            
            urllib.request.urlretrieve(self.url, file_path)
            
            bpy.ops.preferences.addon_install(filepath=file_path, overwrite=True)
            bpy.ops.preferences.addon_enable(module=properties.AddonProperties.module_name)
            
            self.report({'INFO'}, "Addon downloaded, installed, and enabled.")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to download or install addon: {e}")
            return {'CANCELLED'}


#debug Operator
class EXPERIMENTAL_OT_Null(bpy.types.Operator):
    bl_idname = "squaredmedia.null"
    bl_label = "Null Operator"
    bl_description = "This operator does nothing"

    def execute(self, context):

        prefs = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences


        print(f"Current rig list: {prefs.DefaultImportOption}")
        return {"FINISHED"}