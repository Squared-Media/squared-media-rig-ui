import bpy  # type: ignore
from ..msc.utils import get_preferences
from .. import properties
import os


class VIEW3D_PT_RigListPanel(bpy.types.Panel):
    bl_label = "Rig Spawner"
    bl_idname = "VIEW3D_PT_rig_list"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = properties.UIProperties.category
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rig_props = scene.rigs
        preferences = bpy.context.preferences.addons[
            properties.AddonProperties.module_name
        ].preferences

        # Draw UIList
        box = layout.row()
        box.template_list(
            "RigListUI", "", rig_props, "rigs", rig_props, "active_rig_index"
        )
        box = box.column(align=True)
        box.prop(
            preferences,
            "ShowPrefixes",
            text="",
            expand=True,
            placeholder="(optional)",
            toggle=True,
            icon="HIDE_OFF",
        )
        box.operator("squaredmedia.open_rig_library", text="", icon="FILE_FOLDER")
        if len(rig_props.rigs) > 0:
            box.operator(
                "squaredmedia.confirm_open_blend_file", text="", icon="GREASEPENCIL"
            ).filepath = rig_props.rigs[rig_props.active_rig_index].id

        # Import and load buttons
        sublayout = layout.row(align=True)
        sublayout.scale_y = 2

        # Name / Create Character Button

        operator = ""
        preferences = get_preferences(context)
        usr_path = preferences.usr_file_path

        row = layout.row()
        row.scale_y = 2
        # TODO: implement the create character functionality!
        if bpy.data.filepath:
            current_file_abs = os.path.abspath(bpy.data.filepath)

            # makes sure the commonpath doesnt crash when trying to compare different drives
            drive1, _ = os.path.splitdrive(current_file_abs)
            drive2, _ = os.path.splitdrive(usr_path)

            if (
                drive1 == drive2
                and os.path.commonpath([current_file_abs, usr_path]) == usr_path
            ):
                operator = "squaredmedia.namecharacter"
                row.operator(operator, icon="SMALL_CAPS", text="Name your character")
            else:
                operator = "squaredmedia.create_character"
        else:
            operator = "squaredmedia.create_character"

        if len(rig_props.rigs) > 0:
            sublayout = sublayout.split(factor=0.85, align=True)
            import_row = sublayout.row(align=True)

            text = "Import Rig"
            import_op = import_row.operator(
                "squaredmedia.import_rig", text=text, icon="IMPORT"
            )
            import_op.collection_name = rig_props.rigs[rig_props.active_rig_index].name
            import_op.rig_path = rig_props.rigs[rig_props.active_rig_index].id

            sublayout.operator("squaredmedia.load_rigs", text="", icon="FILE_REFRESH")

            row = layout.row()
            row.enabled = False
            row.label(text=f"Mode = {preferences.DefaultImportOption.lower()}")
        else:
            sublayout.operator(
                "squaredmedia.load_rigs",
                text="Please click to refresh",
                icon="FILE_REFRESH",
            )
