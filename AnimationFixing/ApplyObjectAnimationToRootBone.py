import bpy
import math

# Get the keyframes of an animation
def get_keyframes(obj):
    keyframes = []
    anim = obj.animation_data
    if anim is not None and anim.action is not None:
        for fcu in anim.action.fcurves:
            for keyframe in fcu.keyframe_points:
                x, y = keyframe.co
                if x not in keyframes:
                    keyframes.append((math.ceil(x)))
    return keyframes

# Get the root bone of an armature. Used on the assumption that the root bone is named root
def get_root_bone():
    armature = bpy.context.view_layer.objects.active
    bpy.ops.object.mode_set(mode='POSE')
    for bone in armature.pose.bones:
        if bone.name.startswith('root') or bone.name.startswith('Root'):
            return bone

armature_object = bpy.context.view_layer.objects.active
root_bone = get_root_bone()
rotation_offset = 90
scale_offset = 100

bpy.ops.object.mode_set(mode='OBJECT')

if armature_object:

    for action in bpy.data.actions:
        armature_object.animation_data.action = action
        keys = get_keyframes(armature_object)
        
        #Fix the rotation and scale of the action
        for index in range(keys[-1]):
            bpy.context.scene.frame_set(index + 1)
            armature_object.rotation_euler[0] -= math.radians(rotation_offset)
            
            # Round to 0 if we are close so we don't get any slight root motion
            if(math.isclose(armature_object.rotation_euler[0], 0)):
                armature_object.rotation.rotation_euler[0] = 0
            armature_object.scale = (1,1,1)
            armature_object.keyframe_insert(data_path='rotation_euler', frame=(index+1))
            armature_object.keyframe_insert(data_path='scale', frame=(index+1))
            
            # Save our transforms
            location = (armature_object.location.x * scale_offset, armature_object.location.z * scale_offset, -armature_object.location.y * scale_offset)
            rotation = armature_object.rotation_euler
            scale = armature_object.scale
            
            # Apply transforms to root bone and keyframe
            bpy.ops.object.mode_set(mode='POSE')
            root_bone.location = location
            root_bone.rotation_euler = rotation
            root_bone.scale = scale
            root_bone.keyframe_insert(data_path='location', frame=(index+1))
            root_bone.keyframe_insert(data_path='rotation_euler', frame=(index+1))
            root_bone.keyframe_insert(data_path='scale', frame=(index+1))
            
            # Remove keyframes from original object
            bpy.ops.object.mode_set(mode='OBJECT')
            armature_object.keyframe_delete(data_path='location', frame=(index+1))
            armature_object.keyframe_delete(data_path='rotation_euler', frame=(index+1))
            armature_object.keyframe_delete(data_path='scale', frame=(index+1))