import bpy
import math

# Used as a way to bypass the effects of applying scale to an armature with animations
# This will create a new armature at a uniform scale of 1 and copies all the animations over to the new one

# Get the keyframes of an animation
def get_final_key(action):
    last_frame = 0
    for curves in action.fcurves:
        for keyframe in curves.keyframe_points:
            x, y = keyframe.co
            frame = math.ceil(x)
            if frame > last_frame:
                last_frame = frame
    return last_frame

armature_object = bpy.context.view_layer.objects.active
armature_scale_x = 0.01
armature_scale_y = 0.01
armature_scale_z = 0.01

if(armature_object):
    # Store data from old armature used to make new one
    bpy.ops.object.mode_set(mode='EDIT')

    names = []
    heads = {}
    tails = {}
    rolls = {}
    parents = {}

    #bpy.context.active_object = armature_object
    for bone in armature_object.data.edit_bones:
        names.append(bone.name)
        heads[bone.name] = (bone.head.x * armature_scale_x, -bone.head.z * armature_scale_y, bone.head.y * armature_scale_z)
        tails[bone.name] = (bone.tail.x * armature_scale_x, -bone.tail.z * armature_scale_y, bone.tail.y * armature_scale_z)
        rolls[bone.name] = bone.roll
        if(bone.parent):
            parents[bone.name] = bone.parent.name

    bpy.ops.object.mode_set(mode='OBJECT')

    # Create the armature
    bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0), rotation=(0,0,0))
    new_armature_object = bpy.context.active_object
    new_armature_object.name = 'FixedArmature'

    bpy.ops.object.mode_set(mode='EDIT')

    # Delete the default bone
    new_armature_object.data.edit_bones.remove(new_armature_object.data.edit_bones[0])


    for name in names:
        new_bone = new_armature_object.data.edit_bones.new(name)
        new_bone.head = heads[name]
        new_bone.tail = tails[name]
        new_bone.roll = rolls[name]

    # Parent all the bones
    for name in names:
        if (name in parents.keys()):
            new_armature_object.data.edit_bones[name].parent = new_armature_object.data.edit_bones[parents[name]]

    bpy.ops.object.mode_set(mode='POSE')

    # Bind the new armature to the old armature by constraints
    for bone in new_armature_object.pose.bones:
        location_constraint = bone.constraints.new("COPY_LOCATION")
        location_constraint.target = armature_object
        location_constraint.subtarget = bone.name
        
        rotation_constraint = bone.constraints.new("COPY_ROTATION")
        rotation_constraint.target = armature_object
        rotation_constraint.subtarget = bone.name
        
        scale_constraint = bone.constraints.new("COPY_SCALE")
        scale_constraint.target = armature_object
        scale_constraint.subtarget = bone.name
        scale_constraint.target_space = 'LOCAL'

    # Convert all actions over to the new armature
    # Leave the old ones with the suffix _OLD
    action_list = bpy.data.actions
    for action in action_list:
        armature_object.animation_data.action = action
        action_name = action.name
        action.name = action.name + '_OLD'

        print('Baking Action: ' + action_name)

        bpy.ops.nla.bake(frame_start = 1, frame_end=get_final_key(action), only_selected=False, visual_keying=True, clear_constraints=False, use_current_action=False, bake_types={'POSE'})

        for action in bpy.data.actions:
            if (action.name == "Action"):
                action.name = action_name
                action.use_fake_user = True
                break

    for bone in new_armature_object.pose.bones:
        for constraint in bone.constraints:
            bone.constraints.remove(constraint)