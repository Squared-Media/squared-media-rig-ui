import bpy
#debug Operators:

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