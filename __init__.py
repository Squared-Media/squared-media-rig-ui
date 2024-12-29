import bpy
from .operators import ImgPack, ImgReload, KeyframeAllProperties, LinkRig, SetCamera, ResetCamera, GetUpdates, CheckForUpdates
from .ui.UIHeader import UI_Header
from .ui.SkinSettings import SkinSettingsUI
from .ui.Buttons import ButtonsUI
from .ui.VisibilitySettings import VisibilitySettingsUI
from .ui.RigSettings import RigSettingsUI, FaceSettings, ArmSettings, BodySettings, OptimisationSettings, LegSettings, RetargetingSettings, RoundnessSettings

bl_info = {
    "name": "Squared Media Rig UI Addon",
    "description": "Adds RIG UI for Supported Rigs",
    "author": "Squared Media, Fxnarji",
    "version": (1, 0, 1),
    "blender": (4, 3, 2),
    "location": "Npanel > SQMDefaultRig",
    "support": "COMMUNITY",
    "category": "UI",
}

class SQRMediaRigPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    # Example preferences
    some_setting: bpy.props.BoolProperty(
        name="Some Setting",
        description="A simple boolean setting",
        default=True) #type: ignore
    
    addon_version = bl_info["version"]

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "some_setting")

classes = [
        # Properties
        SQRMediaRigPreferences,

        # Operator classes
        ImgPack,
        ImgReload,
        KeyframeAllProperties,
        LinkRig,
        SetCamera,
        ResetCamera,
        GetUpdates,
        CheckForUpdates,

        # UI Classes
        UI_Header,
        SkinSettingsUI,
        ButtonsUI,
        VisibilitySettingsUI,
        RigSettingsUI,
        FaceSettings,
        ArmSettings,
        BodySettings,
        LegSettings,
        RoundnessSettings,
        OptimisationSettings,
        RetargetingSettings,

    ]

def register():
    for i in classes:
        bpy.utils.register_class(i)
        
def unregister():
    for i  in reversed(classes):
        bpy.utils.unregister_class(i)

if __name__ == "__main__":
    register()
