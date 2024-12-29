import bpy
import json
import urllib.request

def is_packed(img):
    """Check if an image is packed in the .blend file."""
    try:
        return bool(img.packed_files)
    except Exception:
        return False

def get_material_object(rig):
    """Retrieve the material object associated with the given rig."""
    return next((child for child in rig.children if child.get('mat_id') == "SQM-MaterialObject"), None)


def get_addon_version():
    return bpy.context.preferences.addons["squared-media-rig-ui"].preferences.addon_version



# Function to get the latest release from GitHub using the API
def get_latest_github_release(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/tags"
    
    try:
        # Send GET request to GitHub API
        with urllib.request.urlopen(url) as response:
            data = json.load(response)  # Parse the JSON response
            
            # Get the most recent tag (first item in the list)
            latest_tag = data[0]['name']
            try:
                latest_version = (int(latest_tag[1]),int(latest_tag[3]),int(latest_tag[5]))
            except:
                print("fuck")

            return latest_version
    except Exception as e:
        print(f"Error fetching tag from GitHub: {e}")
        return None