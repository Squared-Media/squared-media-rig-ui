import bpy
import os
import zipfile
import json
import os
import tomllib

from .. import properties
from enum import Enum

class Material(Enum):
    SKIN = 0
    EYE_R = 1
    EYE_L = 2
    EYEBROW_R = 3
    EYEBROW_L = 4
    EYE_BACKGROUND = 5
    MOUTH_INTERIOR = 6
    DEBUG_MATERIAL = 7

class Limbs(Enum):
    LEFT_ARM = 0
    RIGHT_ARM = 1
    LEFT_LEG = 2
    RIGHT_LEG = 3

class IK_Mode(Enum):
    AUTO = 0
    ON = 1
    OFF = 2



def is_packed(img):
    """Check if an image is packed in the .blend file."""
    try:
        return bool(img.packed_files)
    except Exception:
        return False

def get_material_object(rig):
    """Retrieve the material object associated with the given rig."""
    Mat_Obj = rig.data.bones["Data_Obj"]["Mat_Obj"]
    return Mat_Obj

def get_collections_from_blend(blend_path):
    """Returns a list of collections inside a .blend file."""
    collections = []
    currentfile = bpy.data.filepath
    if blend_path == currentfile:
       return [collection.name for collection in bpy.data.collections]
     
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, _):
        collections.extend(data_from.collections)  # Extract collections
    return collections

def find_collections_in_directory(dir,prefix):
    blend_files = [f for f in os.listdir(dir) if f.endswith(".blend")]
    collection_data = {}

    for blend_file in blend_files:
        print(f"found: {blend_file}")
        blend_path = os.path.join(dir, blend_file)
        collections = get_collections_from_blend(blend_path)
        
        for collection in collections:
            if collection.startswith(prefix):
                print(f"found:{collection} in {blend_file}")
                collection_data[collection] = blend_path

    return collection_data

def is_file_in_library(context):
    current_path = bpy.data.filepath
    preferences = get_preferences(context) 
    library_path = preferences.usr_file_path

    if not current_path or not library_path:
        return False  # Either the file hasn't been saved or the preference isn't set

    current_path = os.path.abspath(current_path)
    library_path = os.path.abspath(library_path)


    return os.path.commonpath([current_path, library_path]) == library_path

def has_name(rig):
    Name = rig.data.bones["Data_Obj"]["Name"]
    if not Name:
        return False
    if Name == "SQM-Default":
        return False
    return True

def get_preferences(context):
    prefernces = bpy.context.preferences.addons[properties.AddonProperties.module_name].preferences
    return prefernces

def get_library_prefix(context):
    preferences = get_preferences(context= context)
    return preferences.lib_prefix

def get_material(rig, material: Material):
    if rig is None:
        return None
    mat_obj = get_material_object(rig)
    return mat_obj.material_slots[material.value].material

def get_skin_texture(rig):
    mat = get_material(rig, Material.SKIN)

    #setting image_node to null
    image_node = ""
    if mat and mat.use_nodes:
        nodes = mat.node_tree.nodes
        image_node = nodes[properties.RigProperties.skin_node_name]
    
    if image_node and image_node.image:
        return image_node.image
       
def get_rig(context):
    active_object =  context.active_object
    if active_object is None:
        return None

    rig_id = active_object.get("rig_id")
    if rig_id is None:
        return None
    if rig_id == "SquaredMediaDefaultRig":
        return active_object

def save_files_to_zip(file_dict, zip_path):
    """
    Saves multiple files into a zip archive.
    
    Parameters:
        file_dict (dict): {filename_in_zip: data}  
                          - If `data` is a dict/list, it will be serialized to JSON.
                          - If `data` is bytes, it will be written directly.
                          - If `data` is a str path to a file, the file will be read and written.
        zip_path (str): Path to the output zip file.
    """
    if not zip_path.lower().endswith(".sqm"):
        zip_path += ".sqm"

    try:
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
            for filename, data in file_dict.items():
                if isinstance(data, (dict, list)):
                    zipf.writestr(filename, json.dumps(data, indent=4))
                elif isinstance(data, bytes):
                    zipf.writestr(filename, data)
                elif isinstance(data, str) and os.path.isfile(data):
                    zipf.write(data, arcname=filename)
                else:
                    raise TypeError(f"Unsupported data type for {filename}: {type(data)}")
        print(f"[INFO] Saved files to archive: {zip_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save archive: {e}")


def write_json(dictionary, path):
    """
    Writes a dictionary to a JSON file.

    Parameters:
        dictionary (dict): The data to save.
        path (str): File path to save the JSON to.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(dictionary, f, indent=4)
        print(f"[INFO] JSON saved to {path}")
    except Exception as e:
        print(f"[ERROR] Failed to write JSON to {path}: {e}")



def load_files_from_zip(zip_path):
    """
    Loads files from a zip archive into memory.

    Parameters:
        zip_path (str): Path to the zip file.

    Returns:
        dict: {filename_in_zip: data}  
              - JSON files are deserialized into dict/list.  
              - Other files are returned as bytes.
    """
    result = {}

    try:
        with zipfile.ZipFile(zip_path, "r") as zipf:
            for name in zipf.namelist():
                with zipf.open(name) as f:
                    content = f.read()
                    if name.lower().endswith(".json"):
                        try:
                            result[name] = json.loads(content.decode("utf-8"))
                        except Exception as e:
                            print(f"[WARNING] Failed to decode JSON {name}: {e}")
                            result[name] = content
                    else:
                        result[name] = content  # raw bytes for textures, etc.
        return result

    except Exception as e:
        print(f"[ERROR] Failed to read zip archive {zip_path}: {e}")
        return None
    
def get_toml_version():
    version_str = get_toml_key("version")
    version_tuple = tuple(int(x) for x in version_str.split("."))
    return version_tuple


def get_toml_key(key):
    toml_path = os.path.join(os.path.dirname((os.path.dirname(__file__))), "blender_manifest.toml")
    with open(toml_path, "rb") as f:
        manifest = tomllib.load(f)
    value = manifest.get(key, "0.0.0")
    return value
