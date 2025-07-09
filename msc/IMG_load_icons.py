import bpy
import bpy.utils.previews
import os

preview_collections = {}

def load_icons():
    icons_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons")
    pcoll = bpy.utils.previews.new()
    pcoll.load("sqm_logo", os.path.join(icons_dir, "SQM_Tiny.png"), 'IMAGE')

    preview_collections["main"] = pcoll

def unload_icons():
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()