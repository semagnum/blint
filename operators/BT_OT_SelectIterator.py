import bpy
from ..model.icon_gen import bpy_data_enum


class BT_OT_SelectIterator(bpy.types.Operator):
    bl_idname = 'blint.form_select_iterator'
    bl_label = 'Select from blend data'
    bl_description = 'Selects a data collection from the blend data'
    bl_options = {'REGISTER', 'UNDO'}

    bpy_data_types: bpy.props.EnumProperty(name='Blend Data Type', default='scenes', items=bpy_data_enum())

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        if not self.bpy_data_types:
            self.report({'ERROR'}, 'No blend data type selected')
            return {'CANCELLED'}

        window_manager = context.window_manager
        form_rule = window_manager.blint_form_rule
        iterable_val = 'bpy.data.' + self.bpy_data_types
        try:
            setattr(form_rule, 'iterable_expr', iterable_val)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        return {'FINISHED'}
