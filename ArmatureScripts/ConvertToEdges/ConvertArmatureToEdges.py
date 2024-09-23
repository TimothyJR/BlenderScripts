import bpy
import math
import os

# Convert an armature to edges. The purpose for this script is to be able to apply a mesh deform on the edges to match the one on the actual character mesh. Then later convert back to an armature.

Meshname = "armature_mesh";

def convertVector(v):
    return [v.x,v.y,v.z]

def main():
    # Make sure what we're going to work on is an actual armature.
    if bpy.context.active_object.type != 'ARMATURE':
        print("Active object must be an armature!!");
        return 1;

    selected_armature = bpy.context.active_object;

    # Time to copy the armature to mesh
    # Define our data containers for the new obj
    Verts=[]
    Edges=[]
    Faces=[]

    # Select the armature and enter edit mode, and get all the bones. 
    bpy.ops.object.editmode_toggle()
    bpy.ops.armature.select_all(action='SELECT')
    bones = bpy.context.selected_bones

    # Loop through the bones, putting all the coords in the data containers.
    for bone in bones :
        Verts.append(convertVector(bone.head))
        Verts.append(convertVector(bone.tail))
        VertID = len(Verts)
        Edges.append([VertID-2,VertID-1])


    bpy.ops.object.editmode_toggle()


    # Make the object and add all the data.
    new_mesh =bpy.data.meshes.new(Meshname)
    new_mesh .from_pydata(Verts,Edges,Faces)
    new_mesh.update()
    new_object = bpy.data.objects.new('new_object', new_mesh)
    new_collection = bpy.data.collections.new('new_collection')
    bpy.context.scene.collection.children.link(new_collection)
    new_collection.objects.link(new_object)

main();