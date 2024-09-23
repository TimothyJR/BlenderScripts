import bpy
import math
import os

# Used in conjunction with the Convert ArmatureToEdges. After applying any modifiers to the edges, apply this script to make the armature conform to the edges.

Meshname = "armature_mesh";

def convertVector(v):
    return [v.x,v.y,v.z]

def main():
    selected_armature = None
    selected_mesh = None
    for obj in bpy.context.selected_objects:
        if obj.type == 'ARMATURE':
            selected_armature = obj;

        if obj.type == 'MESH':
            selected_mesh = obj;

    if selected_armature is None or selected_mesh is None:
        print("Missing armature or mesh");
        return 1;

    selected_armature.select_set(True)
    bpy.ops.object.editmode_toggle()
    bones = bpy.context.selected_bones
    index = 0

    matrix_world_inv = selected_armature.matrix_world.inverted()
    for bone in selected_armature.data.edit_bones:
        #Set bone head to index
        bone.head = matrix_world_inv @ selected_mesh.data.vertices[index].co;
        #Set bone tail to index + 1
        index = index + 1;
        bone.tail = matrix_world_inv @ selected_mesh.data.vertices[index].co;
        index = index + 1;

    print("Made it to the end");

main();