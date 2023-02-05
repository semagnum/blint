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

from ..icon_gen import format_icon_name
from ..model import LintRule

from ..config import PACKAGE_NAME

from ..operators import BT_OT_CreateRule
from ..operators import BT_OT_IconSelection
from ..operators import BT_OT_ReloadRules
from ..operators import BT_OT_SelectIterator


def lint_filepath_update(_self, context):
    reload_rules(context)


class SA_Preferences(bpy.types.AddonPreferences):
    """BLint preferences"""
    bl_idname = PACKAGE_NAME

    lint_rules: bpy.props.CollectionProperty(type=LintRule)
    """BLint rules to be checked in files."""

    lint_filepath: bpy.props.StringProperty(name='External lint rules filepath', default='',
                                            subtype='FILE_PATH', update=lint_filepath_update)
    """Path to external JSON file containing BLint rules."""

    def draw(self, context):
        """Draws BLint preference properties and operators, including rule creation."""
        layout = self.layout
        wm = context.window_manager

        layout.label(text='Rules')
        layout.template_list('BT_UL_Rules', '', self, 'lint_rules', context.window_manager, 'lint_rule_active',
                             columns=3)

        layout.separator()
        layout.prop(self, "lint_filepath")
        layout.operator(BT_OT_ReloadRules.bl_idname, icon='FILE_REFRESH')

        if self.lint_filepath:
            layout.separator()
            layout.prop(context.window_manager, "form_collapsed",
                        icon='TRIA_RIGHT' if wm.form_collapsed else 'TRIA_DOWN',
                        invert_checkbox=True)
            if not wm.form_collapsed:
                draw_rule_creation(layout, context)
        else:
            layout.label(text='No external filepath set, create a \".json\" file to create and store your own rules!',
                         icon='INFO')


def draw_rule_creation(layout, context):
    """Draws rule creation form.

    :param layout: Blender UILayout
    :param context: Blender context
    """

    def reload_form_issues(window_manager):
        """Reloads issue debugger.

        :param window_manager: Blender windows manager
        """
        window_manager.blint_form_issues.clear()
        r = window_manager.blint_form_rule
        for issue in r.get_issues():
            try:
                new_issue = window_manager.blint_form_issues.add()
                new_issue.description = issue.get('description')
                new_issue.severity_icon = issue.get('severity_icon')
                new_issue.category_icon = issue.get('category_icon')
                new_issue.fix_expr = issue.get('fix_expr')
            except ValueError as ex:
                print("Error with {}: {}".format(issue.get('description'), ex))

    wm = context.window_manager

    form_rule: LintRule = wm.blint_form_rule
    layout.prop(form_rule, 'enabled', text='Enabled by default?')
    layout.prop(form_rule, 'description')

    layout.label(text='Icons')
    icon_box = layout.box()
    icon_box.prop(form_rule, 'severity_icon')

    row = icon_box.row()
    row.label(text='Category: {}'.format(format_icon_name(form_rule.category_icon)), icon=form_rule.category_icon)
    op = row.operator(BT_OT_IconSelection.bl_idname, text='Select category icon', icon='IMAGE_DATA')
    op.attr_name = 'category_icon'

    row = layout.row(align=True)
    row.label(text='For each data item in')
    row.prop(form_rule, 'iterable_expr', text='')
    row.operator(BT_OT_SelectIterator.bl_idname, icon='FILE_BLEND')

    box = layout.box()
    box.prop(form_rule, 'prop_label_expr')

    box.separator()

    box.prop(form_rule, 'iterable_var', text='Variable name')
    box.prop(form_rule, 'issue_expr', text='An issue exists if')
    box.prop(form_rule, 'fix_expr', text='Issue fix (optional)')

    validation_errs = form_rule.check_for_errors()
    is_valid = len(validation_errs) == 0
    if is_valid:
        layout.label(text='Validation passed', icon='CHECKMARK')

        try:
            reload_form_issues(wm)

            layout.label(text='Debug')
            layout.template_list('BT_UL_Issues', '', wm, 'blint_form_issues', wm, 'blint_form_issue_active',
                                 columns=4)
        except Exception as e:
            print(e)
            layout.label(text='Issue debugging failed, check console', icon='ERROR')
    else:
        layout.label(text='Validation failed', icon='ERROR')
        for err in validation_errs:
            layout.label(text=err)

    # Create rule
    row = layout.row()
    row.operator(BT_OT_CreateRule.bl_idname, icon='TEXT')
    row.enabled = is_valid
