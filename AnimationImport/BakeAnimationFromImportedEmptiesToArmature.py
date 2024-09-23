bl_info = {
    "name": "Constrain Rigs to Empties",
    "author": "TimR",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Tool> Constrain Rig to Empties",
    "description": "Very specific script to import a series of FBX files that use empties as armatures and bake those animations to an armature that matches the original armature that was converted to empties",
    "category": "Animation"}

import bpy
import os
import math
from mathutils import Matrix

#####

class constrainer(bpy.types.Operator):
    """Constrains the selected rig to the selected empties where the bone names match the empty names."""
    bl_idname = "con.constrain_rig"
    bl_label = "constrain_rig"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "ARMATURE"

    def execute(self, context):
        use_global_undo = context.preferences.edit.use_global_undo
        context.preferences.edit.use_global_undo = False
        try:
            _constrain_rig()
        finally:
            context.preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}

######

def _constrain_rig():
    
    print("Starting constrain function")

    empties_name = []
    delete_object = []
    armature = bpy.context.active_object


    print("Getting FBX Names")
    path_to_fbx_dir = os.path.join('Z:\\', 'Documents\\3D Modeling and Game Assets\\Animations\\Katana\\')
    fbx_list = [item for item in sorted(os.listdir(path_to_fbx_dir)) if item.endswith('.fbx')]
    file_index = 0

    for fbx in fbx_list:
        # Import FBX
        print("Importing FBX")
        path_to_file = os.path.join(path_to_fbx_dir, fbx)
        bpy.ops.import_scene.fbx(filepath=path_to_file, global_scale=100)

        print("Gathering empties and objects to delete")
        # Find all entities and objects that have to be deleted
        empties_name.clear()
        delete_object.clear()
        for entity in bpy.context.selected_objects:
            if entity is not None:
                if entity.type == "EMPTY":
                    empties_name.append(entity.name)
                if entity.name.startswith('Bip01') or entity.name.startswith('Dummy'):
                    if entity.parent is None:
                        delete_object.append(entity)
                    
        print("Getting the final frame of animation")
        # Get frames
        last_frame = 0

        for anim in bpy.data.actions:
            if file_index == 0:
                if anim.name == "ball_l|Take 001|BaseLayer":
                    last_frame = get_final_key(anim)
            elif file_index < 10:
                if anim.name == "ball_l|Take 001|BaseLayer.00" + str(file_index):
                    last_frame = get_final_key(anim)
            elif file_index < 100:
                if anim.name == "ball_l|Take 001|BaseLayer.0" + str(file_index):
                    last_frame = get_final_key(anim)
            elif anim.name == "ball_l|Take 001|BaseLayer." + str(file_index):
                last_frame = get_final_key(anim)

        print("Deleting objects")
        # Deselect objects and select all objects to be deleted
        bpy.ops.object.select_all(action='DESELECT')
        for delete in delete_object:
            delete_hierarchy(delete)

        print("Return armature to origin")
        # Return armature to origin
        armature.select_set(True)
        armature.matrix_basis = Matrix()
        bpy.ops.object.mode_set(mode='POSE')

        print("Creating constraints")
        # Parent all bones of the armature
        for bone in armature.pose.bones:
            for empty_name in empties_name:
                if bone.name == empty_name:
                    location_constraint = bone.constraints.new("COPY_LOCATION")
                    rotation_constraint = bone.constraints.new("COPY_ROTATION")
                    current_empty = bpy.data.objects.get(empty_name)
                    location_constraint.target = current_empty
                    rotation_constraint.target = current_empty
                    break

        print("Baking animation")
        # Bake the animation
        bpy.ops.nla.bake(frame_start = 1, frame_end=last_frame, only_selected=False, visual_keying=True, clear_constraints=True, use_current_action=False, bake_types={'POSE'})

        print("Renaming animation")
        # Rename Animation
        for anim in bpy.data.actions:
            if anim.name == "Action":
                anim.name = "_" + fbx
                anim.use_fake_user = True
                break

        print("Delete empties")
        # Delete Empties
        bpy.ops.object.mode_set(mode='OBJECT') 
        bpy.ops.object.select_all(action='DESELECT')
        for empty in empties_name:
            current_empty = bpy.data.objects.get(empty)
            if current_empty is not None:
                current_empty.select_set(True)
        bpy.ops.object.delete()

        file_index += 1
######

def get_final_key(anim):
    last_frame = 0
    for curves in anim.fcurves:
        for keyframe in curves.keyframe_points:
            x, y = keyframe.co
            frame = math.ceil(x)
            if frame > last_frame:
                last_frame = frame
    return last_frame

######

def delete_hierarchy(object):
    bpy.ops.object.select_all(action='DESELECT')
    names = [object.name]

    print("Getting children names") 
    def get_child_names(object_with_children):
        if object_with_children.children:
            for child in object_with_children.children:
                names.append(child.name)
                get_child_names(child)

    get_child_names(object)

    print(names)
    print("Selecting everything to delete")
    for child_name in names:
        bpy.data.objects.get(child_name).animation_data_clear()
        bpy.data.objects.get(child_name).select_set(True)

    print("Deleting children") 
    bpy.ops.object.delete()

######

class CR_PT_menu(bpy.types.Panel):
    bl_label = "Constain Rig to Empties"
    bl_idname = "CR_PT_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("con.constrain_rig", text="Constrain Selected Rig")


def register():
    bpy.utils.register_class(CR_PT_menu)
    bpy.utils.register_class(constrainer)

def unregister():
    bpy.utils.unregister_class(CR_PT_menu)
    bpy.utils.unregister_class(constrainer)

if __name__ == "__main__":
    register()