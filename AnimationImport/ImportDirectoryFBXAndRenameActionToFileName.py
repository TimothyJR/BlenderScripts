import bpy
import os
import glob

# Imports a directory of fbx files and renames their animation to the name of the fbx file

def listFiles(dir, ext):
    fileList = []
    for file in os.listdir(dir):
        print(file)
        if file[-len(ext):] == ext:
            fileList.append(file)
    return fileList

currentDir = bpy.path.abspath('//')

# If you want a further directory, just add it here
AniDir = currentDir+'Mvm_Start_Walk'
ext = '.fbx'

# Create a Temp Collection to work within
collection = bpy.data.collections.new('TempCollection')
bpy.context.scene.collection.children.link(collection)
layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
bpy.context.view_layer.active_layer_collection = layer_collection

# Import all the Animations and rename them to the Filename
AnimList = glob.glob(AniDir + '\*.fbx')

for animations in animList:
    print(animations)
    bpy.ops.import_scene.fbx(filepath=animations,use_anim=True, automatic_bone_orientation=True)
    obj = bpy.context.object
    animName = (bpy.path.display_name_from_filepath(os.path.basename(animations))).replace(prefixToRemove, prefixToAdd)
    obj.animation_data.action.name = animName
print('')