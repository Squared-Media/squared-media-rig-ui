import bpy
import json
import mathutils
from ..msc.utils import get_material_object, get_rig

class FILE_OT_LoadJsonConfig(bpy.types.Operator):
    bl_idname = "squaredmedia.loadconfig"
    bl_label = "Load Config from File"

    filepath: bpy.props.StringProperty(subtype = "FILE_PATH")

    def apply_bone_properties(self, obj, bone, properties):
        pose_bone = obj.pose.bones.get(bone)
        if not pose_bone:
            print(f"Bone '{bone}' not found!")
            return

        for prop_name, value in properties.items():
            pose_bone[prop_name] = value
        print(f"Applied {len(properties)} properties to bone '{bone}'")

    def load_skin_cfg(self, obj, data):
        skin_cfg_data = None

        for entry in data:
            if "Skin_cfg" in entry:
                skin_cfg_data = entry["Skin_cfg"]
                break

        if skin_cfg_data:
            self.apply_bone_properties(obj, "Skin_cfg", skin_cfg_data)
        else:
            print("No 'Skin_cfg' data found in JSON.")

    def convert_to_blender_value(self, value, expected_type=None):
        """
        Convert JSON-loaded value back to Blender-friendly type if needed.
        
        expected_type can be 'VECTOR', 'COLOR', or None.
        """
        if isinstance(value, list):
            if expected_type == 'VECTOR':
                # For 3D or 4D vectors
                if len(value) == 3:
                    return mathutils.Vector(value)
                elif len(value) == 4:
                    return mathutils.Vector(value)  # Blender often uses 4D vectors for colors
                else:
                    return value  # fallback to list
            elif expected_type == 'COLOR':
                # Colors are often 3 or 4 floats
                if len(value) in (3, 4):
                    return mathutils.Vector(value)  # mathutils.Color supports 3 components only
                else:
                    return value
            else:
                # No specific type expected, just return list
                return value
        else:
            # For primitives (int, float, bool), just return as is
            return value

    def load_shader_properties(self,obj, index, data_raw):
        data = data_raw[index]
        for node_name, props in data.items():
            node = obj.material_slots[index].material.node_tree.nodes.get(node_name)
            if not node:
                print(f"Node '{node_name}' not found!")
                continue

            for input_name, value in props.items():
                input_socket = node.inputs.get(input_name)
                if not input_socket:
                    print(f"Input '{input_name}' not found in node '{node_name}'")
                    continue

                if input_socket.is_linked:
                    print(f"Input '{input_name}' in node '{node_name}' is linked — skipping")
                    continue

                # Detect expected type
                if input_socket.type == 'VALUE':
                    expected_type = None
                elif input_socket.type == 'VECTOR':
                    expected_type = 'VECTOR'
                elif input_socket.type == 'RGBA':
                    expected_type = 'COLOR'
                else:
                    expected_type = None

                # Convert if needed
                converted_value = self.convert_to_blender_value(value, expected_type)

                try:
                    input_socket.default_value = converted_value
                except Exception as e:
                    print(f"Failed to set '{input_name}' on node '{node_name}': {e}")

    def invoke(self, context, event):
        # Trigger the file dialog
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        rig = get_rig(context)
        MatObj = get_material_object(rig)
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.load_skin_cfg(rig, data)
            self.load_shader_properties(MatObj, 1, data)
            self.load_shader_properties(MatObj, 2, data)


        return {"FINISHED"}

