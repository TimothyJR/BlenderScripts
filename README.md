# BlenderScripts
Custom Blender Scripts

Just a collection of scripts that I have used to help make assets from other sources more manageable.

## Script Summary:

### Animation Fixing:
ApplyObjectAnimationToRootBone:
Takes an object that has an animation on it and moves it to the root bone of an armature

ApplyTransformToArmature:
Script to help with getting uniform scale on an armature that has animations

### Animation Import:
BakeAnimationFromImportedEmptiesToArmature
This script is used when you have fbx files that are animating empties instead of an armature. With a copy of the source armature, animations can be brought from the set of empties to the armature

ImportDirectoryFBXAndRenameActionToFileName
Imports all the FBX files in a directory then renames their animation after the file name instead of a generic animation name that gets given to it

### Armature Scripts:
ConstrainBonesToEmpties
Matches a rig to a set of empties

AlignArmatureToEdges
Makes an armature match a set of edges. Useful when you represent your armature as a set of edges to use modifiers to change it (Such as a mesh deform). Intended purpose is to be used with the ConvertArmatureToEdges script

ConvertArmatureToEdges
Converts an armature to a set of edges so modifiers can be used on it