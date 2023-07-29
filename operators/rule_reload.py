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

from ..save_load import reload_rules, does_config_exist, save_external_rules


class BT_OT_ReloadRules(bpy.types.Operator):
    """Reloads linter rules from internal as well as external configuration."""
    bl_idname = 'blint.reload_rules'
    bl_label = 'Reload from Disk'
    bl_description = 'Reloads linter rules from the configuration file'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return does_config_exist(context)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        try:
            reload_rules(context)
            self.report({'INFO'}, 'Successfully reloaded rules from disk')
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, 'Reload error failed: ' + str(e))
            return {'CANCELLED'}


class BT_OT_SaveRules(bpy.types.Operator):
    """Saves linter rules to configuration file."""
    bl_idname = 'blint.save_rules'
    bl_label = 'Save to Disk'
    bl_description = 'Saves linter rules to the configuration file'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return does_config_exist(context)

    def execute(self, context):
        try:
            save_external_rules(context)
            self.report({'INFO'}, 'Successfully saved rules to disk')
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, 'Saving to config file failed: ' + str(e))
            return {'CANCELLED'}

