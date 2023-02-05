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

from ..save_load import reload_issues


class BT_PT_Issues(bpy.types.Panel):
    """Scene panel to display issues found in the Blender file."""
    bl_label = 'BLinter'
    bl_category = 'BLinter'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        layout = self.layout
        window_manager = context.window_manager

        reload_issues(context)
        layout.template_list('BT_UL_Issues', '',
                             window_manager, 'lint_issues',
                             window_manager, 'lint_issue_active', columns=4)
