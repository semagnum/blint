import bpy

from . import (
    issues_list,
    rules_list,
    issues_panel,
)

_registration_order = [
    issues_list.BT_UL_Issues,
    rules_list.BT_UL_Rules,
    issues_panel.BT_MT_context_menu,
    issues_panel.BT_PT_Issues,
]

if len(bpy.utils.register_classes_factory(_registration_order)) != 0:
    register, unregister = bpy.utils.register_classes_factory(_registration_order)
