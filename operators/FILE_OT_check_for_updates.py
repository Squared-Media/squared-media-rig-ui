import bpy
import requests
from ..msc.utils import get_toml_version, get_toml_key

class FILE_OT_check_for_updates(bpy.types.Operator):
    bl_idname = "squaredmedia.check_for_updates"
    bl_label = "check_for_updates"

    def get_releases(self, releases, include_prerelease=False):

        if not include_prerelease:
            releases = [r for r in releases if not r["prerelease"] and not r["draft"]]

        return releases

    def execute(self, context):
        
        current_version = get_toml_version()
        current_type = get_toml_key("release_channel")
        current_beta_version = ""
        if current_type == "beta":
            current_beta_version = get_toml_key("beta_version")

        current_string = f"{current_version[0]}.{current_version[1]}.{current_version[2]}-{current_type}{current_beta_version}"


        url = "https://api.github.com/repos/squared-media/squared-media-rig-ui/releases"
        response = requests.get(url)
        
        if response.status_code == 200:
            releases = response.json()   

            stable_releases = self.get_releases(releases, False)
            latest_stable_tag = stable_releases[0]["tag_name"]

            latest_beta = self.get_releases(releases, True)
            latest_beta_tag = latest_beta[0]["tag_name"]

            self.report({'INFO'}, f"Current Version: {current_string}, latest stable: {latest_stable_tag} latest beta version: {latest_beta_tag}")
            return {"FINISHED"}


