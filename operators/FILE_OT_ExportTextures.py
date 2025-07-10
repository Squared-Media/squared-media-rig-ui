import bpy
import zipfile
import os


class FILE_OT_UnpackArmorFilesOperator(bpy.types.Operator):
    bl_idname = "object.file_ot_unpackarmorfiles"
    bl_label = "FILE_OT_UnpackArmorFiles"
    output_dir = "/home/fxnarji/gh/squared-media-rig-ui/lib/textures/Armor/"

    filepath: bpy.props.StringProperty(subtype = "FILE_PATH")


    def unpack_jar_file(self, jar_path, output_dir):
        os.makedirs(output_dir, exist_ok=True)

        #Files are in /equipment/humanoid and equipment/humanoid_leggings, but because both folders 
        #are the only ones starting with humanoid, its enough to only check for humanoid

        target_folder = "assets/minecraft/textures/entity/equipment/humanoid"

        with zipfile.ZipFile(jar_path, 'r') as jar:
            for file in jar.namelist():
                if file.startswith(target_folder) and file.lower().endswith('.png'):
                    filename = os.path.basename(file)
                    
                    # skip if it's a directory
                    if not filename:
                        continue  

                    destination_path = os.path.join(output_dir, filename)

                    # Files are named ie "diamond.png" in both the leggings dir aswell as the regular dir. Leggings dir is searched first, so duplicates are recognized as chestplate
                    if os.path.exists(destination_path):
                        base, ext = os.path.splitext(filename)
                        while os.path.exists(destination_path):
                            destination_path = os.path.join(output_dir, f"{base}_chestplate{ext}")

                    with open(destination_path, "wb") as out_file:
                        out_file.write(jar.read(file))
                        print(f"Extracted: {file} → {destination_path}")


    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    

    def execute(self, context):

        jar_path = self.filepath()
        dest_path = 
        self.unpack_jar_file(jar_path= jar_path, output_dir= dest_path)
        return {"FINISHED"}

