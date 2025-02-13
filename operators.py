import bpy
import os
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


    collection_name:    bpy.props.StringProperty(name="Collection Name", default="SQM Character Rig")#type: ignore
    rig_path:           bpy.props.StringProperty(name="Rig Path", default=properties.Paths.default_lib_path)#type: ignore   
    imported_name:      bpy.props.StringProperty(name="Imported Name")#type: ignore

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
            imported_collection.name = self.imported_name

        elif bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences.DefaultImportOption == 'APPEND':
            bpy.ops.wm.append(
                filepath=rig_blend_path, 
                directory=rig_blend_path + "/Collection/",  
                filename=collection_name,
            )

            imported_collection = bpy.data.collections.get(collection_name)
            imported_collection.name = self.imported_name


        return {'FINISHED'}
    
class SCENE_OT_toggle_face_camera(bpy.types.Operator):
    bl_idname = "squaredmedia.set_camera" 
    bl_label ="sets Face Animation camera to be active"


    def execute(self, context):
        rig = bpy.context.active_object
        SQM_Camera = rig["Cam"]

        if SQM_Camera.hide_viewport: 
            SQM_Camera.hide_viewport = False
            bpy.context.space_data.use_local_camera = True
            bpy.context.space_data.camera = SQM_Camera
            bpy.context.space_data.lock_camera = True
            bpy.ops.view3d.view_camera()
            return {"FINISHED"}
        else:
            bpy.context.space_data.use_local_camera = False
            bpy.context.space_data.lock_object = None
            bpy.context.space_data.lock_camera = False
            SQM_Camera.hide_viewport = True
            bpy.ops.view3d.view_camera()
            return {"FINISHED"}
#debug Operator
class EXPERIMENTAL_OT_Null(bpy.types.Operator):
    bl_idname = "squaredmedia.null"
    bl_label = "Null Operator"
    bl_description = "This operator does nothing"

    def execute(self, context):

        self.report({'INFO'}, "This operator did nothing")
        return {"FINISHED"}
    
class EXPERIMENTAL_OT_set_pose(bpy.types.Operator):
    bl_idname = "squaredmedia.set_pose"
    bl_label = "Set Pose"
    bl_description = "Setting Mouth Pose"

    phonem: bpy.props.StringProperty()

    def execute(self, context):
        armature = bpy.context.object 
        bpy.ops.object.mode_set(mode='POSE')
        
        source_action_name = self.phonem
        source_action = bpy.data.actions.get(source_action_name)
        target_action = armature.animation_data.action

        armature.active_selection_set = 0
        bpy.ops.pose.select_all(action="DESELECT")
        bpy.ops.pose.selection_set_select()



        for bone in bpy.context.selected_pose_bones:
            # Loop through the fcurves (keyframe data) of the source action
            for fcurve in source_action.fcurves:
                # Check if this fcurve is related to the current bone
                if bone.name in fcurve.data_path:
                    # Get the data for the current fcurve (location, rotation, scale)
                    data_path = fcurve.data_path
                    index = fcurve.array_index

                    target_fcurve = target_action.fcurves.find(data_path, index=index)
                    
                    if not target_fcurve:
                        target_fcurve = target_action.fcurves.new(data_path=data_path, index=index)

                    if not target_fcurve:
                        target_fcurve = target_action.fcurves.new(data_path=data_path, index=index)

                    # Copy each keyframe from the source action to the target action at the specified frame
                    for keyframe in fcurve.keyframe_points:
                        target_fcurve.keyframe_points.insert(bpy.context.scene.frame_current, keyframe.co.y)

            
        return {'FINISHED'}


