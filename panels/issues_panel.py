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
from ..operators import BT_OT_FixIssue, BT_OT_FixIssueAll

class BT_MT_context_menu(bpy.types.Menu):
    bl_label = "BLint Issues"

    def draw(self, _context):
        layout = self.layout
        layout.operator(BT_OT_FixIssue.bl_idname, text='Run Fix', icon='PLAY')
        layout.operator(BT_OT_FixIssueAll.bl_idname, text='Run All Fixes')


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
        row = layout.row()
        row.template_list('BT_UL_Issues', '',
                             window_manager, 'lint_issues',
                             window_manager, 'lint_issue_active', columns=4)

        if len(window_manager.lint_issues) != 0:
            if window_manager.lint_issue_active < 0:
                window_manager.lint_issue_active = 0
            elif window_manager.lint_issue_active >= len(window_manager.lint_issues):
                window_manager.lint_issue_active = len(window_manager.lint_issues) - 1

        row.menu("BT_MT_context_menu", icon='DOWNARROW_HLT', text="")
