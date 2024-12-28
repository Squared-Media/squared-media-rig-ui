import bpy
from .operators import ImgPack, ImgReload, KeyframeAllProperties, LinkRig, SetCamera, ResetCamera
from .ui.UIHeader import UI_Header
from .ui.SkinSettings import SkinSettingsUI
from .ui.Buttons import ButtonsUI
from .ui.VisibilitySettings import VisibilitySettingsUI
from .ui.RigSettings import RigSettingsUI, FaceSettings, ArmSettings, BodySettings, OptimisationSettings, LegSettings, RetargetingSettings, RoundnessSettings
from .properties import SQMRigProperties

bl_info = {
    "name": "Squared Media Rig UI Addon",
    "description": "Adds RIG UI for Supported Rigs",
    "author": "Squared Media, Fxnarji",
    "version": (0, 15, 0),
    "blender": (4, 3, 2),
    "location": "Npanel > SQMDefaultRig",
    "support": "COMMUNITY",
    "category": "UI",
}


classes = [
        # Properties
        SQMRigProperties,

        # Operator classes
        ImgPack,
        ImgReload,
        KeyframeAllProperties,
        LinkRig,
        SetCamera,
        ResetCamera,

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
    bpy.types.Scene.my_properties = bpy.props.PointerProperty(type=SQMRigProperties)
        
def unregister():
    for i  in reversed(classes):
        bpy.utils.unregister_class(i)
    del bpy.types.Scene.my_properties

if __name__ == "__main__":
    register()
