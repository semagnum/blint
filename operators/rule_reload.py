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
import bpy_extras.io_utils

from ..save_load import get_user_preferences, reload_rules, does_config_exist, save_external_rules


class BT_OT_ReloadRules(bpy.types.Operator):
    """Reloads rules from the selected config file."""
    bl_idname = 'blint.reload_rules'
    bl_label = 'Reload from Disk'
    bl_description = 'Reloads rules from the selected config file'
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
            self.report({'ERROR'}, 'Reload failed: ' + str(e))
            return {'CANCELLED'}


class BT_OT_SaveRules(bpy.types.Operator):
    """Saves rules to the selected config file."""
    bl_idname = 'blint.save_rules'
    bl_label = 'Save to Disk'
    bl_description = 'Saves rules to the selected config file'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            save_external_rules(context)
            self.report({'INFO'}, 'Successfully saved rules to disk')
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, 'Saving to config file failed: ' + str(e))
            return {'CANCELLED'}


class BT_OT_SaveRulesAs(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    """Saves linter rules to a new configuration file."""
    bl_idname = 'blint.save_rules_as'
    bl_label = 'Save to Disk as...'
    bl_description = 'Saves rules to a new config file, set as the current config'
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = '.json'

    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'})

    def execute(self, context):
        try:
            preferences = get_user_preferences(context)
            save_external_rules(context, filepath=self.filepath)
            self.report({'INFO'}, 'Successfully saved rules to disk')

            # set as new default
            preferences.config_type = 'EXTERNAL'
            preferences.lint_filepath = self.filepath

            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, 'Saving to config file failed: ' + str(e))
            return {'CANCELLED'}
