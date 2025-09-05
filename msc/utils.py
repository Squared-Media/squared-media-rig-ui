import bpy
import os
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
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, _):
        collections.extend(data_from.collections)  # Extract collections
    return collections

def find_collections_in_directory(dir,prefix):
    blend_files = [f for f in os.listdir(dir) if f.endswith(".blend")]
    collection_data = {}

    for blend_file in blend_files:
        blend_path = os.path.join(dir, blend_file)
        collections = get_collections_from_blend(blend_path)
        
        for collection in collections:
            if collection.startswith(prefix):
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
