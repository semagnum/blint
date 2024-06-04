# Copyright (C) 2024 Spencer Magnusson
# semagnum@gmail.com
# Created by Spencer Magnusson
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


import bpy

from ..icon_gen import bpy_data_enum
from ..save_load import get_user_preferences


class BT_OT_SelectIterator(bpy.types.Operator):
    """Selects a data collection from the blend data."""
    bl_idname = 'blint.form_select_iterator'
    bl_label = 'Select data type'
    bl_description = 'Selects a data collection from blend data types'
    bl_options = {'REGISTER', 'UNDO'}

    bpy_data_types: bpy.props.EnumProperty(name='Blend Data Type', default='scenes', items=bpy_data_enum())
    """List of Blend data types."""

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        if not self.bpy_data_types:
            self.report({'ERROR'}, 'No blend data type selected')
            return {'CANCELLED'}

        addon_preferences = get_user_preferences(context)
        lint_rules = addon_preferences.lint_rules

        rule_index = context.window_manager.lint_rule_active

        if rule_index < 0 or rule_index >= len(lint_rules):
            self.report({'ERROR'}, 'Invalid rule specified')
            return {'CANCELLED'}

        form_rule = lint_rules[rule_index]
        iterable_val = 'bpy.data.' + self.bpy_data_types
        try:
            setattr(form_rule, 'iterable_expr', iterable_val)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        return {'FINISHED'}
