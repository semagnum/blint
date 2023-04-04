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

from .pref_access import get_user_preferences
from .save_load import reload_rules

from .model import LintRule
from .model import LintIssue

from .operators import BT_OT_ReloadRules
from .operators import BT_OT_FixIssue
from .operators import BT_OT_SelectIcon
from .operators import BT_OT_IconSelection
from .operators import BT_OT_SelectIterator
from .operators import BT_OT_CreateRule
from .operators import BT_OT_DeleteRule

from .panels import BT_UL_Rules
from .panels import BT_UL_Issues
from .panels import BT_PT_Issues

from .preferences import SA_Preferences

bl_info = {
    "name": 'BLint',
    "author": 'Spencer Magnusson',
    "version": (0, 2, 5),
    "blender": (2, 93, 0),
    "description": 'Custom project linting',
    "location": 'Scene',
    "support": 'COMMUNITY',
    "category_icon": 'Scene'
}
prop_groups = [LintIssue, LintRule, SA_Preferences]
operators_panels = [BT_OT_SelectIterator, BT_OT_SelectIcon, BT_OT_IconSelection, BT_OT_CreateRule, BT_OT_DeleteRule,
                    BT_UL_Rules, BT_UL_Issues,
                    BT_OT_ReloadRules, BT_OT_FixIssue,
                    BT_PT_Issues]

classes = prop_groups + operators_panels

properties = [
    ('lint_rule_active', bpy.props.IntProperty(default=0)),
    ('lint_issue_active', bpy.props.IntProperty(default=0)),
    ('lint_issues', bpy.props.CollectionProperty(type=LintIssue)),
    # form creator
    ('blint_form_rule', bpy.props.PointerProperty(type=LintRule)),
    ('blint_form_issue_active', bpy.props.IntProperty(default=0)),
    ('blint_form_issues', bpy.props.CollectionProperty(type=LintIssue)),
    ('form_collapsed', bpy.props.BoolProperty(name='Create Rules', default=True))
]


def register():
    window_manager = bpy.types.WindowManager

    for cls in classes:
        bpy.utils.register_class(cls)

    for name, prop in properties:
        setattr(window_manager, name, prop)

    reload_rules(bpy.context)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
