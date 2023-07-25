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

from ..save_load import reload_rules


class BT_OT_ReloadRules(bpy.types.Operator):
    """Reloads linter rules from internal as well as external configuration."""
    bl_idname = 'blint.reload_rules'
    bl_label = 'Reload linter rules'
    bl_description = 'Reloads linter rules from internal as well as external configuration'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            reload_rules(context)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, 'Reload error failed: ' + str(e))
            return {'CANCELLED'}


