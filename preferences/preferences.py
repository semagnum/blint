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
import logging

from ..save_load import reload_rules

from ..icon_gen import format_icon_name
from ..model import LintRule

from ..config import PACKAGE_NAME

from ..operators import (
    BT_OT_CreateRule,
    BT_OT_DeleteRule,
    BT_OT_IconSelection,
    BT_OT_DebugFixIssue,
    BT_OT_ReloadRules,
    BT_OT_SaveRules,
    BT_OT_SelectIterator,
    BT_OT_RunOnFiles
)

log = logging.getLogger(__name__)


def lint_filepath_update(_self, context):
    context.window_manager.lint_rule_active = 0
    try:
        reload_rules(context)
    except Exception as e:
        log.error('Rule reload failed: ' + str(e))


class SA_Preferences(bpy.types.AddonPreferences):
    """BLint preferences"""
    bl_idname = PACKAGE_NAME

    lint_rules: bpy.props.CollectionProperty(type=LintRule)
    """BLint rules to be checked in files."""

    config_type: bpy.props.EnumProperty(name='Rule source', update=lint_filepath_update, default='INTERNAL', items=[
        ('INTERNAL', 'Internal', 'Internal BLint rules included with the add-on'),
        ('EXTERNAL', 'External', 'External JSON file')
    ])

    lint_filepath: bpy.props.StringProperty(name='External rule file',
                                            description='External JSON file containing rules',
                                            default='',
                                            subtype='FILE_PATH', update=lint_filepath_update)
    """Path to external JSON file containing BLint rules."""

    def draw(self, context):
        """Draws BLint preference properties and operators, including rule creation."""
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.label(text='Rule Source:')
        row.prop(self, 'config_type', expand=True)
        row = layout.row()
        row.active = self.config_type == 'EXTERNAL'
        row.prop(self, 'lint_filepath')
        row = layout.row(align=True)
        row.operator(BT_OT_ReloadRules.bl_idname, icon='FILE_REFRESH')
        row.operator(BT_OT_SaveRules.bl_idname, icon='FILE_TICK')

        layout.separator()

        row = layout.row()
        row.template_list('BT_UL_Rules', '', self, 'lint_rules', context.window_manager, 'lint_rule_active', columns=3)
        col = row.column(align=True)
        col.operator(BT_OT_CreateRule.bl_idname, icon='ADD', text='')
        col.operator(BT_OT_DeleteRule.bl_idname, icon='REMOVE', text='')

        layout.separator()
        layout.prop(context.window_manager, "edit_form_collapsed",
                    icon='TRIA_RIGHT' if wm.edit_form_collapsed else 'TRIA_DOWN',
                    invert_checkbox=True)
        if not wm.edit_form_collapsed:
            draw_rule_creation(layout, context, self)

        layout.separator()
        layout.prop(context.window_manager, "run_form_collapsed",
                    icon='TRIA_RIGHT' if wm.run_form_collapsed else 'TRIA_DOWN',
                    invert_checkbox=True)
        if not wm.run_form_collapsed:
            layout.label(icon='ERROR', text='This cannot be undone.')
            layout.prop(wm, 'blint_run_path')
            layout.prop(wm, 'blint_run_fix')

            if wm.blint_running_progress >= 0.0:
                layout.progress(
                    factor=wm.blint_running_progress,
                    text='({}%) Running, don\'t close Blender...'.format(
                        str(int(wm.blint_running_progress * 100))
                    )
                )
            else:
                op = layout.operator(BT_OT_RunOnFiles.bl_idname, icon='PLAY')
                op.path = wm.blint_run_path
                op.fix = wm.blint_run_fix


def draw_rule_creation(layout, context, preferences):
    """Draws rule creation form.

    :param layout: Blender UILayout
    :param context: Blender context
    :param preferences: Blender preferences
    """

    wm = context.window_manager

    rule_index = wm.lint_rule_active
    lint_rules = preferences.lint_rules

    if rule_index < 0 or rule_index >= len(lint_rules):
        layout.label(text='No rule selected')
        return

    form_rule: LintRule = lint_rules[rule_index]

    def reload_form_issues(window_manager):
        """Reloads issue debugger.

        :param window_manager: Blender windows manager
        """
        window_manager.blint_form_issues.clear()
        for issue in form_rule.get_issues():
            try:
                new_issue = window_manager.blint_form_issues.add()
                new_issue.description = issue.get('description')
                new_issue.severity_icon = issue.get('severity_icon')
                new_issue.category_icon = issue.get('category_icon')
                new_issue.fix_expr = issue.get('fix_expr')
            except ValueError as ex:
                raise ValueError("Error with {}: {}".format(issue.get('description'), ex))

    validation_errs = form_rule.check_for_errors()
    is_valid = len(validation_errs) == 0
    if is_valid:
        layout.label(text='Validation passed', icon='CHECKMARK')
    else:
        layout.label(text='Validation failed', icon='ERROR')
        error_box = layout.box()
        error_box.alert = True
        for err in validation_errs:
            error_box.label(text=err, icon='DOT')

    layout.separator()

    layout.prop(form_rule, 'description')
    layout.prop(form_rule, 'prop_label_expr', text='Issue identifier (optional)')
    layout.prop(form_rule, 'issue_expr', text='An issue exists if')
    layout.prop(form_rule, 'fix_expr', text='Issue fix (optional)')

    layout.separator()

    layout.prop(form_rule, 'severity_icon', text='Severity Icon')
    row = layout.row()
    row.label(text='Category icon:')
    row.label(text=format_icon_name(form_rule.category_icon), icon=form_rule.category_icon)
    op = row.operator(BT_OT_IconSelection.bl_idname, text='Select Category Icon', icon='IMAGE_DATA')
    op.attr_name = 'category_icon'

    layout.separator()

    layout.label(text='Data Iteration (optional):')
    row = layout.row()
    row.label(text='Data type:')
    row.prop(form_rule, 'iterable_expr', text='')
    row.operator(BT_OT_SelectIterator.bl_idname, icon='FILE_BLEND')
    layout.prop(form_rule, 'iterable_var')

    layout.separator()

    col = layout.column()
    col.active = is_valid

    try:
        reload_form_issues(wm)

        col.label(text='Debug Issues:')
        col.template_list('BT_UL_Issues', '', wm, 'blint_form_issues', wm, 'blint_form_issue_active', columns=4)
        col.operator(BT_OT_DebugFixIssue.bl_idname, text='Fix selected')
    except Exception as e:
        log.error(e)
        layout.label(text='Issue debugging failed, see console', icon='ERROR')
