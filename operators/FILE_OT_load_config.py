import bpy
import json
import mathutils
from ..msc.utils import get_material_object, get_rig, get_material, Material

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

    def load_shader_properties(self, rig, material: Material, data: dict):
        """
        Restores shader node input values from a JSON block like:
        { "NodeName": { "SocketName": value, ... } }
        """
        mat = get_material(rig, material)
        print(mat)
        if not mat or not mat.use_nodes:
            print(f"[ERROR] Material {material.name} not found or has no node tree!")
            return

        # Each entry in `data` is {node_name: {socket_name: value}}
        for node_name, socket_props in data.items():
            node = mat.node_tree.nodes.get(node_name)
            if not node:
                print(f"[ERROR] Node '{node_name}' not found in material '{mat.name}'")
                continue

            for socket_name, value in socket_props.items():
                socket = node.inputs.get(socket_name)
                if not socket:
                    print(f"[WARNING] Socket '{socket_name}' not found in node '{node_name}'")
                    continue

                try:
                    socket.default_value = value
                except TypeError:
                    try:
                        socket.default_value = tuple(value)
                    except Exception as e:
                        print(f"[WARNING] Failed to set '{socket_name}' on '{node_name}': {e}")
                except Exception as e:
                    print(f"[WARNING] Unexpected error on '{socket_name}' in '{node_name}': {e}")

    def invoke(self, context, event):
        # Trigger the file dialog
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        rig = get_rig(context)
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.load_skin_cfg(rig, data)

        self.load_shader_properties(rig, Material.SKIN, data[1])
        self.load_shader_properties(rig, Material.EYE_R, data[2])
        self.load_shader_properties(rig, Material.EYE_L, data[3])
        self.load_shader_properties(rig, Material.EYEBROW_L, data[4])
        self.load_shader_properties(rig, Material.EYEBROW_R, data[5])


        return {"FINISHED"}

