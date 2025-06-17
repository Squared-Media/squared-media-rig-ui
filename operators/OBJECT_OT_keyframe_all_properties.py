import bpy

class OBJECT_OT_keyframe_all_properties(bpy.types.Operator):
    """Add keyframes to all custom properties except those containing 'Visible'"""
    bl_idname = "squaredmedia.keyframe_all_custom_properties"
    bl_label = "Keyframe all animatable Custom Properties"
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
