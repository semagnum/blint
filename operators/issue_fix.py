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

import logging

import bpy

log = logging.getLogger(__name__)


class BT_OT_FixIssue(bpy.types.Operator):
    """Runs a given BLint fix on the scene."""
    bl_idname = 'scene_analyzer.fix_issue'
    bl_label = 'Fix issue'
    bl_description = 'Fix selected issue'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        idx = wm.lint_issue_active
        return 0 <= idx < len(wm.lint_issues) and wm.lint_issues[idx].fix_expr

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        wm = context.window_manager
        idx = wm.lint_issue_active
        fix = wm.lint_issues[idx].fix_expr
        log.info('Running: {}'.format(fix))
        exec(fix)
        return {'FINISHED'}


class BT_OT_DebugFixIssue(bpy.types.Operator):
    """Runs a given BLint fix on the scene."""
    bl_idname = 'scene_analyzer.fix_issue_debug'
    bl_label = 'Fix issue'
    bl_description = 'Fix selected issue'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        idx = wm.blint_form_issue_active
        return 0 <= idx < len(wm.blint_form_issues) and wm.blint_form_issues[idx].fix_expr

    def execute(self, context):
        wm = context.window_manager
        idx = wm.blint_form_issue_active
        fix = wm.blint_form_issues[idx].fix_expr
        exec(fix)
        return {'FINISHED'}


class BT_OT_FixIssueAll(bpy.types.Operator):
    """Runs a given BLint fix on the scene."""
    bl_idname = 'scene_analyzer.fix_issue_all'
    bl_label = 'Fix all issues'
    bl_description = 'Fixes all issues with an auto-fix defined'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        return len(wm.lint_issues) and any([wm.lint_issues[idx].fix_expr for idx in range(len(wm.lint_issues))])

    def execute(self, context):
        wm = context.window_manager
        for idx in range(len(wm.lint_issues)):
            fix = wm.lint_issues[idx].fix_expr
            if not fix:
                continue
            log.info('Running: {}'.format(fix))
            exec(fix)

        return {'FINISHED'}
