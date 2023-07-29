# Copyright (C) 2023 Spencer Magnusson
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

from .. import get_user_preferences


class BT_OT_DeleteRule(bpy.types.Operator):
    """Deletes rule from the preferences."""
    bl_idname = 'blint.delete_rule'
    bl_label = 'Delete Rule'
    bl_description = 'Deletes this rule'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        addon_preferences = get_user_preferences(context)
        lint_rules = addon_preferences.lint_rules

        rule_index = context.window_manager.lint_rule_active

        if rule_index < 0 or rule_index >= len(lint_rules):
            self.report({'ERROR'}, 'Invalid rule specified')
            return {'CANCELLED'}

        lint_rules.remove(rule_index)

        return {'FINISHED'}
