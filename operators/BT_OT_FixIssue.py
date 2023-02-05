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


class BT_OT_FixIssue(bpy.types.Operator):
    """Runs a given BLint fix on the scene."""
    bl_idname = 'scene_analyzer.fix_issue'
    bl_label = 'Fix issue'
    bl_description = 'Fix issue'
    bl_options = {'REGISTER', 'UNDO'}

    fix: bpy.props.StringProperty(default='')
    """Python expression to fix issue in scene."""

    def execute(self, context):
        print('Running:', self.fix)
        exec(self.fix)
        return {'FINISHED'}
