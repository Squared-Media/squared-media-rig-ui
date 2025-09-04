import bpy
from .. import properties
from ..msc.utils import get_rig

blend_file = properties.Paths.blend_file
lib_folder = properties.Paths.lib_folder
rigID = properties.RigProperties.rigID

class SCENE_OT_toggle_face_camera(bpy.types.Operator):
    bl_idname = "squaredmedia.set_camera" 
    bl_label ="sets Face Animation camera to be active"
    bl_description = "Toggles Viewport snapping to Face"



    def execute(self, context):
        rig = get_rig(context)
        SQM_Camera = rig["Cam"]

        if SQM_Camera.hide_viewport: 
            SQM_Camera.hide_viewport = False
            bpy.context.space_data.use_local_camera = True
            bpy.context.space_data.camera = SQM_Camera
            bpy.context.space_data.lock_camera = True
            bpy.ops.view3d.view_camera()
            return {"FINISHED"}
        else:
            bpy.context.space_data.use_local_camera = False
            bpy.context.space_data.lock_object = None
            bpy.context.space_data.lock_camera = False
            SQM_Camera.hide_viewport = True
            bpy.ops.view3d.view_camera()
            return {"FINISHED"}

