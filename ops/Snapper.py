import bpy
from .. import properties

# Define the operator to snap FK bones to IK bones
class OBJECT_OT_FK_to_IK_snapper(bpy.types.Operator):
    bl_idname = "squaredmedia.snapper"
    bl_label = "Snap Chains"
    bl_options = {'REGISTER', 'UNDO'}

    limb: bpy.props.EnumProperty(
        name = "Arm",
        items=[
            ('Arm_L', "Left", "Left Arm"),
            ('Arm_R', "Right", "Right Arm"),
        ],
        default='Arm_L'
    ) #type: ignore

    mode: bpy.props.EnumProperty(
        name="Smart Snapping", 
        default='SMART',
        items=[('SMART', "Smart", "automatically places keyframes"),
               ('REGULAR', "Regular", "Normal IK / FK Snapping")],
    ) #type: ignore

    def execute(self, context):
        armature = bpy.context.object
        
        # Upper First
        Arm_L_IK_bones = ['MCH-UpperArm.L', 'CTRL-IK-LowerArm.L']
        Arm_L_FK_bones = ['CTRL-FK-UpperArm.L', 'CTRL-FK-LowerArm.L']

        Arm_R_IK_bones = ['MCH-UpperArm.R', 'CTRL-IK-LowerArm.R']
        Arm_R_FK_bones = ['CTRL-FK-UpperArm.R', 'CTRL-FK-LowerArm.R']


        ik_bones = Arm_L_IK_bones
        fk_bones = Arm_L_FK_bones
        Arm_IK = bpy.context.active_object.pose.bones["CTRL-IK-LowerArm.L"]
        data = "IK Arm L"
        data_path = '["IK Arm L"]'

        if self.limb == 'Arm_R':
            ik_bones = Arm_R_IK_bones 
            fk_bones = Arm_R_FK_bones
            Arm_IK = bpy.context.active_object.pose.bones["CTRL-IK-LowerArm.R"]
            data = "IK Arm R"
            data_path = '["IK Arm R"]'
        
        if armature.type != 'ARMATURE' or armature.mode != 'POSE':
            self.report({'ERROR'}, "Selected object is not in pose mode or is not an armature.")
            return {'CANCELLED'}



        for i in range(len(ik_bones)):
            ik_bone_name = ik_bones[i]
            fk_bone_name = fk_bones[i]

            ik_bone = armature.pose.bones.get(ik_bone_name)
            fk_bone = armature.pose.bones.get(fk_bone_name)

            if ik_bone and fk_bone:
                fk_bone.matrix = ik_bone.matrix
                bpy.context.view_layer.update()
               
                if self.mode == 'SMART':
                    Arm_IK[data] = 1
                    Arm_IK.keyframe_insert(data_path=data_path, keytype = 'GENERATED')
                    fk_bone.keyframe_insert(data_path="location", keytype = 'GENERATED')
                    fk_bone.keyframe_insert(data_path="rotation_euler", keytype = 'GENERATED')
                    fk_bone.keyframe_insert(data_path="scale", keytype = 'GENERATED')
            
                    Arm_IK[data] = 0
                    Arm_IK.keyframe_insert(data_path=data_path, keytype = 'GENERATED', frame = bpy.context.scene.frame_current + 1)


                

            

            

        return {'FINISHED'}
