import os

def is_packed(img):
    """Check if an image is packed in the .blend file."""
    try:
        return bool(img.packed_files)
    except Exception:
        return False

def get_material_object(rig):
    """Retrieve the material object associated with the given rig."""
    return next((child for child in rig.children if child.get('mat_id') == "SQM-MaterialObject"), None)
