import bpy
import mathutils
from ..msc.utils import get_rig, get_material, save_files_to_zip, Material

class FILE_OT_SaveConfigAsTomlOperator(bpy.types.Operator):
    bl_idname = "squaredmedia.saveconfig"
    bl_label = "Save Config to File"

    filepath: bpy.props.StringProperty(subtype = "FILE_PATH") #type: ignore

    def get_bone_custom_properties(self,obj):
        """
        Returns a dict of all custom properties on pose bones of the given armature object,
        excluding internal Blender keys like _RNA_UI.
        
        Structure:
        {
            "bone_name": {
                "prop_name": value,
                ...
            },
            ...
        }
        """
        if not obj or obj.type != 'ARMATURE':
            raise TypeError("Expected an armature object")

        result = {}

        bone = obj.pose.bones["Skin_cfg"]
        bone_props = {
            key: bone[key]
            for key in bone.keys()
            if not key.startswith("_")
        }

        if bone_props:
            result[bone.name] = bone_props

        return result

    def safe_convert(self, value):

        # Recursively convert lists/tuples
        if isinstance(value, (list, tuple)):
            return [self.safe_convert(v) for v in value]

        # Convert mathutils.Vector, Color, Quaternion, Matrix to lists
        elif isinstance(value, (mathutils.Vector, mathutils.Color, mathutils.Quaternion)):
            return list(value)

        # For matrices, convert each row to list
        elif isinstance(value, mathutils.Matrix):
            return [list(row) for row in value]

        # For Blender RNA property arrays (bpy property array type)
        elif hasattr(value, "to_list"):
            # to_list() returns a list of the contained values
            return value.to_list()

        # Basic types just returned as-is
        elif isinstance(value, (str, int, float, bool, type(None))):
            return value

        # Fallback: try iterating over it if possible (rare edge case)
        try:
            iter(value)
            return [self.safe_convert(v) for v in value]
        except TypeError:
            pass

        # Last resort fallback to string (avoid for your case)
        return str(value)

    def get_shader_properties(self, rig, material: Material, node_name: str):
        """
        Returns a dictionary of the default input values of a shader node,
        keyed by socket name, for a specific material slot from a rig.
        Skips linked inputs and missing nodes.
        """

        # Get the material from the enum + rig
        mat = get_material(rig, material)
        if not mat or not mat.use_nodes:
            self.report({'ERROR'}, f"Material '{material.name}' not found or has no node tree!")
            return None

        # Get the node
        node = mat.node_tree.nodes.get(node_name)
        if not node:
            self.report({'ERROR'}, f"Node '{node_name}' not found in material '{material.name}'!")
            return None

        input_data = {}
        for input_socket in node.inputs:
            if input_socket.is_linked:
                self.report({'WARNING'}, f"Input '{input_socket.name}' is linked — skipping.")
                continue
            try:
                input_data[input_socket.name] = self.safe_convert(input_socket.default_value)
            except AttributeError:
                self.report({'WARNING'}, f"Input '{input_socket.name}' has no default value — skipping.")
                continue

        # Wrap under the node name
        result = {node_name: input_data}
        print(result)
        return result

    def invoke(self, context, event):
        # Trigger the file dialog
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        rig = get_rig(context)
        bone_dict  = self.get_bone_custom_properties(rig)

        Skin_Shader_dict = self.get_shader_properties(rig, Material.SKIN, "SkinShader")

        Eye_R_Shader_dict = self.get_shader_properties(rig, Material.EYE_R, "Eye.R")
        Eye_L_Shader_dict = self.get_shader_properties(rig, Material.EYE_L, "Eye.L")

        Eyebrow_L_Shader_dict = self.get_shader_properties(rig, Material.EYEBROW_L, "Eyebrow.L")
        Eyebrow_R_Shader_dict = self.get_shader_properties(rig, Material.EYEBROW_R, "Eyebrow.R")


        
        
        combined = [
            bone_dict, 
            Skin_Shader_dict,

            Eye_R_Shader_dict, 
            Eye_L_Shader_dict,

            Eyebrow_L_Shader_dict,
            Eyebrow_R_Shader_dict,
            ]
        

        save_files_to_zip({
            "config.json": combined,
            "skin.png": bpy.data.images['NoSkin.png'].filepath
        }, self.filepath)

        #print(dictionary)
        return {"FINISHED"}

