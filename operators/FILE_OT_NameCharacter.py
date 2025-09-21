import bpy  # type: ignore
from ..msc.utils import get_library_prefix, get_rig


class FILE_OT_NameCharacter(bpy.types.Operator):
    bl_idname = "squaredmedia.namecharacter"
    bl_label = "FILE_OT_NameCharacter"
    bl_options = {"REGISTER", "UNDO"}

    new_name: bpy.props.StringProperty(name="New Name:")  # type: ignore

    def switch_names(self, context):
        rig = get_rig(context)
        if rig is None:
            return
        DataBone = rig.data.bones["Data_Obj"]
        DataBone["OldName"] = DataBone["Name"]
        DataBone["Name"] = self.new_name

    def rename_collections(self, collection, context):
        for col in bpy.data.collections:
            print(f"found collection {col.name}")
            col.name = self.rename(context, col.name)
        return
        prefix = get_library_prefix(context)
        collection.name = f"{prefix}" + f"{self.new_name}"

    def rename_objects_in_collection(self, collection, context):
        data = collection.all_objects
        for d in data:
            d.name = self.rename(context, name=d.name)


    def rename_materials_and_nodetrees(self, context):
        rig = get_rig(context=context)

        # Sanity Checks
        if rig is None:
            return
        material_holder = rig.pose.bones["Material_Holder"]
        if material_holder is None:
            return

        #actual renaming going on
        for key, value in  material_holder.items():
            material_holder[key].name = self.rename(context,value.name)
        return


    def rename(self, context, name) -> str | None:
        rig = get_rig(context)
        if rig is None:
            return

        DataBone = rig.data.bones["Data_Obj"]
        Name = DataBone["Name"]
        OldName = DataBone["OldName"]

        prefix = f"{OldName}"
        if not name.startswith(prefix):
            return name

        second_half = name[(len(prefix)) :]

        new_name = f"{Name}{second_half}"
        print(new_name)
        return new_name

    def invoke(self, context, event):
        # Trigger the file dialog
        context.window_manager.invoke_props_dialog(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        rig = get_rig(context)
        if rig is None:
            self.report({'INFO'}, "operation cancelled, likely no (valid) rig selected")
            return{"CANCELLED"}
        DataBone = rig.data.bones["Data_Obj"]
        Collection = DataBone["Collection"]
        self.switch_names(context)
        self.rename_objects_in_collection(context=context, collection=Collection)
        self.rename_collections(context=context, collection=Collection)
        self.rename_materials_and_nodetrees(context=context)

        return {"FINISHED"}
