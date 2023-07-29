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

if 'bpy' in locals():
    import importlib
    reloadable_modules = [
        'config',
        'pref_access',
        'save_load',
        'model',
        'operators',
        'panels',
        'preferences',
    ]
    for module_name in reloadable_modules:
        if module_name in locals():
            importlib.reload(locals()[module_name])

import bpy

from . import config, pref_access
from .pref_access import get_user_preferences
from . import save_load, model, operators, panels, preferences

bl_info = {
    'name': 'BLint',
    'author': 'Spencer Magnusson',
    'version': (1, 0, 0),
    'blender': (2, 93, 0),
    'description': 'Custom project linting',
    'location': 'Scene',
    'support': 'COMMUNITY',
    'category_icon': 'Scene',
    'doc_url': 'https://semagnum.github.io/blint/',
    'tracker_url': 'https://github.com/semagnum/blint/issues',
}

properties = [
    ('lint_rule_active', bpy.props.IntProperty(default=0)),
    ('lint_issue_active', bpy.props.IntProperty(default=0)),
    ('lint_issues', bpy.props.CollectionProperty(type=model.LintIssue)),
    ('blint_form_issue_active', bpy.props.IntProperty(default=0)),
    ('blint_form_issues', bpy.props.CollectionProperty(type=model.LintIssue)),
    ('form_collapsed', bpy.props.BoolProperty(name='Edit Selected Rule', default=True))
]


def register():
    window_manager = bpy.types.WindowManager

    model.register()
    preferences.register()
    operators.register()
    panels.register()

    for name, prop in properties:
        setattr(window_manager, name, prop)


def unregister():
    panels.unregister()
    operators.unregister()
    preferences.unregister()
    model.unregister()


if __name__ == '__main__':
    register()
