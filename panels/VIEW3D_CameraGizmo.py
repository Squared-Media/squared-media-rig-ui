import bpy

class VIEW3D_CameraGizmo(bpy.types.GizmoGroup):
    bl_idname = "CustomGizmos"
    bl_label = "Custom gizmos"
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"
    bl_options = {'PERSISTENT', 'SCALE'}
    bl_order = 3
    

    @classmethod
    def poll(cls, context):
        rig = bpy.context.active_object
        return rig and rig.get("rig_id") == "SquaredMediaDefaultRig"
    
    def draw_prepare(self, context):
        region_width = context.region.width
        region_height = context.region.height
    
    # Get the width of the N panel (right toolbar)
        n_panel_width = 0
        if context.area.ui_type == 'VIEW_3D' and context.space_data.show_region_ui:
            for region in context.area.regions:
                if region.type == 'UI':
                    n_panel_width = region.width

        # Set the initial position for the gizmos
        r_xpos = region_width -  n_panel_width  # Adjust this for the X position
        r_ypos = region_height
        ui_scale = context.preferences.view.ui_scale
        for gizmo in self.gizmos:
            gizmo.matrix_basis[0][3] = r_xpos - 22.5 * ui_scale
            gizmo.matrix_basis[1][3] = r_ypos - 300 * ui_scale


       
    def setup(self, context):
        mpr = self.gizmos.new("GIZMO_GT_button_2d")
        mpr.bl_idname = "RunForestButton"
        mpr.draw_options = {'BACKDROP', 'OUTLINE'}
        mpr.target_set_operator('squaredmedia.set_camera')
        mpr.alpha = 0.5
        mpr.color = 0.5, 0.1, 0.5
        mpr.color_highlight = 1.0, 1.0, 1.0
        mpr.alpha_highlight = 0.1
        mpr.scale_basis = (30) / 2
        mpr.use_tooltip = True
        mpr.show_drag = False
        mpr.use_draw_value = True
        mpr.icon = "LOCKVIEW_ON"  # Default icon

    #def draw(self, context):
        #rig = bpy.context.active_object
        #SQM_Camera = rig["Cam"]
        #layout = self.layout
        #layout.scale_y = 2.0  
        #layout.operator("squaredmedia.set_camera", icon ="LOCKVIEW_ON" if SQM_Camera.hide_viewport else "LOCKVIEW_OFF", text="Start Face Anim" if SQM_Camera.hide_viewport else "End Face Anim")
