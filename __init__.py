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
    import os
    import types

    # double-check this add-on is imported, so it can be referenced and reloaded
    import blint

    def reload_package(package):
        assert (hasattr(package, '__package__'))
        fn = package.__file__
        fn_dir = os.path.dirname(fn) + os.sep
        module_visit = {fn}
        del fn

        def reload_recursive_ex(module):
            module_iter = (
                module_child
                for module_child in vars(module).values()
                if isinstance(module_child, types.ModuleType)
            )
            for module_child in module_iter:
                fn_child = getattr(module_child, '__file__', None)
                if (fn_child is not None) and fn_child.startswith(fn_dir) and fn_child not in module_visit:
                    # print('Reloading:', fn_child, 'from', module)
                    module_visit.add(fn_child)
                    reload_recursive_ex(module_child)

            importlib.reload(module)

        return reload_recursive_ex(package)

    reload_package(blint)

import bpy

from . import save_load, model, operators, panels, preferences

bl_info = {
    'name': 'BLint',
    'author': 'Spencer Magnusson',
    'version': (1, 3, 0),
    'blender': (3, 6, 0),
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
    ('edit_form_collapsed', bpy.props.BoolProperty(name='Edit Selected Rule', default=True)),
    ('run_form_collapsed', bpy.props.BoolProperty(name='Run on File or Folder', default=True)),
    ('blint_running_progress', bpy.props.FloatProperty(default=-1.0, subtype='PERCENTAGE')),
    ('blint_run_path', bpy.props.StringProperty(
        name='File or Folder Path',
        description='.blend file to evaluate. When folder is selected, '
                    'BLint selects all .blend files in folder and subfolders.',
        subtype='FILE_PATH')
     ),
    ('blint_run_fix', bpy.props.BoolProperty(
        name='Fix Issues Found',
        description='Runs fixes on selected .blend files',
        default=False)
     ),
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
