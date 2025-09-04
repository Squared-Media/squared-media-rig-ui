import bpy
import mathutils
import sys
import json
from ..msc.utils import get_material_object, get_rig

class FILE_OT_SaveConfigAsTomlOperator(bpy.types.Operator):
    bl_idname = "squaredmedia.saveconfig"
    bl_label = "Save Config to File"

    filepath: bpy.props.StringProperty(subtype = "FILE_PATH")

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

    def save_dict_to_json(self, data, filepath):
        """
        Saves the given dictionary of bone custom properties to a JSON file.

        Parameters:
            data (dict): Dictionary in the format returned by get_bone_custom_properties()
            filepath (str): Full path to the output .json file
        """
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"Saved bone properties to: {filepath}")
        except Exception as e:
            print(f"Failed to save bone properties: {e}")

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

    def get_shader_properties(self, obj, index, name):
        input_data = {}
        node = obj.material_slots[index].material.node_tree.nodes.get(name)

        if not node:
            self.report({'ERROR'}, f"Node '{name}' not found!")
            return None

        for input_socket in node.inputs:
            if input_socket.is_linked:
                self.report({'WARNING'}, f"Input '{input_socket.name}' is linked — skipping.")
                continue
            try:
                data = self.safe_convert(input_socket.default_value)
                input_data[input_socket.name] = data
            except AttributeError:
                self.report({'WARNING'}, f"Input '{input_socket.name}' has no default value — skipping.")
                continue

        # This wraps the inner dict under the node name
        result = {name: input_data}

        print(result)
        return result

    def invoke(self, context, event):
        # Trigger the file dialog
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        rig = get_rig(context)
        MatObj = get_material_object(rig)
        bone_dict  = self.get_bone_custom_properties(rig)
        Eye_R_Shader_dict = self.get_shader_properties(MatObj, 1, "Eye.R")
        Eye_L_Shader_dict = self.get_shader_properties(MatObj, 2, "Eye.L")

        
        
        combined = [bone_dict, Eye_R_Shader_dict, Eye_L_Shader_dict]
        
        self.save_dict_to_json(combined, self.filepath)

        #print(dictionary)
        return {"FINISHED"}

