import bpy
from .. import properties
from mathutils import Vector
preferences = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences

# Define the operator to snap FK bones to IK bones
class OBJECT_OT_FK_to_IK_snapper(bpy.types.Operator):
    bl_idname = "squaredmedia.snapper"
    bl_label = "Snap Chains"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
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

    direction: bpy.props.EnumProperty(
        name="direction",
        items=[
            ("IK_TO_FK", "IK to FK", ""),
            ("FK_TO_IK", "FK to IK", ""),
        ],
        default="IK_TO_FK",
    )#type: ignore

    def execute(self, context):
        armature = bpy.context.object
        
        # Upper First
        Arm_L_IK_bones = ['MCH-UpperArm.L', 'CTRL-IK-LowerArm.L']
        Arm_L_FK_bones = ['CTRL-FK-UpperArm.L', 'CTRL-FK-LowerArm.L']

        Arm_R_IK_bones = ['MCH-UpperArm.R', 'CTRL-IK-LowerArm.R']
        Arm_R_FK_bones = ['CTRL-FK-UpperArm.R', 'CTRL-FK-LowerArm.R']

        Hand_IK_L = "CTRL-Hand.L"
        Hand_Pole_L = "CTRL-IKArmTarget.L"

        Hand_IK_R = "CTRL-Hand.R"
        Hand_Pole_R = "CTRL-IKArmTarget.R"



        ik_bones = Arm_L_IK_bones
        fk_bones = Arm_L_FK_bones
        Arm_IK = bpy.context.active_object.pose.bones["CTRL-IK-LowerArm.L"]
        data = "IK Arm L"
        data_path = '["IK Arm L"]'
        pole = bpy.context.active_object.pose.bones[Hand_Pole_L]
        controller = bpy.context.active_object.pose.bones[Hand_IK_L]

        if self.limb == 'Arm_R':
            ik_bones = Arm_R_IK_bones 
            fk_bones = Arm_R_FK_bones
            Arm_IK = bpy.context.active_object.pose.bones["CTRL-IK-LowerArm.R"]
            data = "IK Arm R"
            data_path = '["IK Arm R"]'
            pole = bpy.context.active_object.pose.bones[Hand_Pole_R]
            controller = bpy.context.active_object.pose.bones[Hand_IK_R]

        
        if armature.type != 'ARMATURE' or armature.mode != 'POSE':
            self.report({'ERROR'}, "Selected object is not in pose mode or is not an armature.")
            return {'CANCELLED'}



        if self.direction == "FK_TO_IK":
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
        elif self.direction == "IK_TO_FK":
            
            fk_hand_bone = bpy.context.active_object.pose.bones.get(fk_bones[1])
            controller.matrix = fk_hand_bone.matrix
            bpy.context.view_layer.update()
            controller.matrix = fk_hand_bone.matrix
            controller.bone.select = True
            bpy.ops.transform.translate(value=(0,fk_hand_bone.length,0), orient_type="LOCAL")
            controller.bone.select = False


            pole.matrix = fk_hand_bone.matrix
            bpy.context.view_layer.update()
            pole.matrix = fk_hand_bone.matrix
            pole.bone.select = True
            bpy.ops.transform.translate(value=(0,-.4,0), orient_type="LOCAL")

            if self.mode == 'SMART':
                        Arm_IK[data] = 0
                        Arm_IK.keyframe_insert(data_path=data_path, keytype = 'GENERATED')
                        pole.keyframe_insert(data_path="location", keytype = 'GENERATED')
                        controller.keyframe_insert(data_path="location", keytype = 'GENERATED')
                        controller.keyframe_insert(data_path="rotation_quaternion", keytype = 'GENERATED')                     


                        Arm_IK[data] = 1
                        Arm_IK.keyframe_insert(data_path=data_path, keytype = 'GENERATED', frame = bpy.context.scene.frame_current + 1)


            print("Test")
        return {'FINISHED'}
