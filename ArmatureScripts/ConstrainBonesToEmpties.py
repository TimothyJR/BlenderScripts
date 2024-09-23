bl_info = {
    "name": "Constrain Rigs to Empties",
    "author": "TimR",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Tool> Constrain Rig to Empties",
    "description": "Constrains each bone of a selected rig to a selected empty with the same name. Useful when an animation gotten online imports with empties instead of an armature",
    "category": "Animation"}
    
import bpy

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
    empties_name = [i.name for i in bpy.context.selected_objects if i is not None and i.type == "EMPTY"]
          
    armature = bpy.context.active_object
    bpy.ops.object.mode_set(mode='POSE')
    
    for bone in armature.pose.bones:
        for empty_name in empties_name:
            if bone.name == empty_name:
                location_constraint = bone.constraints.new("COPY_LOCATION")
                rotation_constraint = bone.constraints.new("COPY_ROTATION")
                current_empty = bpy.data.objects.get(empty_name)
                location_constraint.target = current_empty
                rotation_constraint.target = current_empty
                continue
        

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