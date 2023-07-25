if 'bpy' in locals():
    import importlib

    reloadable_modules = [
        'issues_list',
        'rules_list',
        'issues_panel',
    ]
    for module_name in reloadable_modules:
        if module_name in locals():
            importlib.reload(locals()[module_name])

import bpy

from . import (
    issues_list,
    rules_list,
    issues_panel,
)

_registration_order = [
    issues_list.BT_UL_Issues,
    rules_list.BT_UL_Rules,
    issues_panel.BT_PT_Issues,
]

register, unregister = bpy.utils.register_classes_factory(_registration_order)
