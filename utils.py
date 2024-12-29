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
    return bpy.context.preferences.addons["squared-media-rig-ui-main"].preferences.addon_version

def get_latest_github_release(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/tags"
    token = bpy.context.preferences.addons["squared-media-rig-ui-main"].preferences.GithubToken
    headers = {}

    # Add the Authorization header if a token is provided
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        # Prepare the request
        request = urllib.request.Request(url, headers=headers)

        # Send GET request to GitHub API
        with urllib.request.urlopen(request) as response:
            if response.status_code == 403:
                print("You are being rate limited.")
                
                return{'CANCELLED'}
            data = json.load(response)  # Parse the JSON response
            
            # Get the most recent tag (first item in the list)
            latest_tag = data[0]['name']
            
            try:
                # Convert the tag (e.g., "v1.2.3") into a tuple of integers
                latest_version = tuple(map(int, latest_tag.lstrip('v').split('.')))
            except Exception as parse_error:
                print(f"Error parsing version tag '{latest_tag}': {parse_error}")
                return None

            return latest_version
    except Exception as e:
        print(f"Error fetching tag from GitHub: {e}")
        bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Error 403: Too many Requests. Please try again later or provide a GitHub token"), title="Error", icon='ERROR')
        return None
    
def is_update_available():
    local_version = get_addon_version()
    latest_version = get_latest_github_release("Fxnarji","squared-media-rig-ui")

    if latest_version > local_version:
        return True
    else:   
        return False