import bpy
import os
from .. import properties

def is_packed(img):
    """Check if an image is packed in the .blend file."""
    try:
        return bool(img.packed_files)
    except Exception:
        return False

def get_material_object(rig):
    """Retrieve the material object associated with the given rig."""
    return next((child for child in rig.children if child.get('mat_id') == "SQM-MaterialObject"), None)



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