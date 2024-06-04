# Copyright (C) 2024 Spencer Magnusson
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

from ..save_load import get_user_preferences
from .. import icon_gen

ASSIGN_EXPR = "{} = {}"

BPY_DATA = 'bpy.data.'
NOT_EQ_EXPR = '{} != {}'


def is_iterable(o):
    return hasattr(o, '__iter__') and not isinstance(o, str)


def fill_rule(new_rule, full_path: str):
    """Sets rule attributes based on a Python expression of a Blender property.

    :param new_rule: new rule to be updated
    :param full_path: Python expression of a Blender property
    """
    # severity icon
    new_rule.severity_icon = 'INFO'

    data_end_idx = full_path.index('[')

    # value and description
    val = eval(full_path)
    if is_iterable(val):
        val = val[:]
    new_rule.description = '{} must be {}'.format(icon_gen.format_icon_name(full_path.rsplit('.', 1)[-1]), val)

    if full_path.startswith(BPY_DATA):
        data_type = full_path[len(BPY_DATA):(data_end_idx - 1)].lower()
        iterable_var = 'my_' + data_type
        iterable_splice_idx = full_path.index(']') + 1
        new_iterable_expr = full_path[:data_end_idx]
        issue_path = iterable_var + full_path[iterable_splice_idx:]

        new_rule.iterable_expr = new_iterable_expr
        new_rule.iterable_var = iterable_var
        new_rule.issue_expr = new_rule.issue_expr = NOT_EQ_EXPR.format(issue_path, repr(val))
        new_rule.fix_expr = ASSIGN_EXPR.format(issue_path, repr(val))
        new_rule.prop_label_expr = iterable_var + '.name'
    else:
        data_type = full_path
        new_rule.iterable_expr = ''
        new_rule.issue_expr = NOT_EQ_EXPR.format(full_path, repr(val))
        new_rule.fix_expr = ASSIGN_EXPR.format(full_path, repr(val))
        new_rule.prop_label_expr = ''

    new_rule.category_icon = next(
        (icon for _, _, _, icon, _ in icon_gen.bpy_data_enum() if data_type in icon.lower()),
        'SCENE_DATA'
    )


class BT_OT_ContextRule(bpy.types.Operator):
    """Generates a rule based on the currently selected property and its value."""
    bl_idname = "blint.rule_create_from_context"
    bl_label = "Add BLint rule"
    bl_description = "Creates a new rule, checking to ensure this property is the current value"

    @classmethod
    def poll(cls, _context):
        return bpy.ops.ui.copy_data_path_button.poll()

    def execute(self, context):
        window_manager = context.window_manager

        # get full data path
        bpy.ops.ui.copy_data_path_button(full_path=True)
        full_path: str = window_manager.clipboard

        # add and save rule
        addon_preferences = get_user_preferences(context)
        lint_rules = addon_preferences.lint_rules

        new_rule = lint_rules.add()
        fill_rule(new_rule, full_path)

        return {'FINISHED'}


class UI_MT_button_context_menu(bpy.types.Menu):
    """Enables adding the rule operator to the context menu.

    This class has to be exactly named this to insert an entry in the right click menu.
    """
    bl_label = "Add BLint"

    def draw(self, context):
        # leave as is
        pass


def menu_func(self, _context):
    """Adds the rule operator to the context menu."""
    layout = self.layout
    layout.separator()
    layout.operator(BT_OT_ContextRule.bl_idname)
