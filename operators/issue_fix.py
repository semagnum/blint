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
import os

import bpy

from ..model.lint_rule import import_from_file

log = logging.getLogger(__name__)


def run_fix(issue):
    if issue.rule_file:
        rule_file = bpy.path.abspath(issue.rule_file)
        if not os.path.isfile(rule_file):
            raise FileNotFoundError(rule_file)

        rule_module = import_from_file(rule_file)
        if not hasattr(rule_module, 'fix_issues') or not callable(rule_module.fix_issues):
            raise AttributeError(obj=rule_module, name='fix_issues')

        rule_module.fix_issues(issue.fix_expr)
    else:
        fix = issue.fix_expr
        log.debug('Running: {}'.format(fix))
        exec(fix)


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
        result = (
                0 <= idx < len(wm.lint_issues) and
                wm.lint_issues[idx].fix_expr
        )
        if not result:
            cls.poll_message_set('Selected issue has no defined fix')

        return result

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        wm = context.window_manager
        idx = wm.lint_issue_active
        try:
            run_fix(wm.lint_issues[idx])
        except Exception as e:
            self.report({'ERROR'}, str(e))
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
        result = (
                0 <= idx < len(wm.blint_form_issues) and
                wm.blint_form_issues[idx].fix_expr
        )

        if not result:
            cls.poll_message_set('This issue has no defined fix')

        return result

    def execute(self, context):
        wm = context.window_manager
        idx = wm.blint_form_issue_active
        try:
            run_fix(wm.blint_form_issues[idx])
        except Exception as e:
            self.report({'ERROR'}, str(e))
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
        result = (
                len(wm.lint_issues) and
                any([wm.lint_issues[idx].fix_expr for idx in range(len(wm.lint_issues))])
        )

        if not result:
            cls.poll_message_set('No issues present have a defined fix')

        return result

    def execute(self, context):
        wm = context.window_manager
        for idx in range(len(wm.lint_issues)):
            if not wm.lint_issues[idx].fix_expr:
                continue

            try:
                run_fix(wm.lint_issues[idx])
            except Exception as e:
                self.report({'ERROR'}, str(e))

        return {'FINISHED'}
