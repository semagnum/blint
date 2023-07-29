if 'bpy' in locals():
    import importlib

    reloadable_modules = [
        'issue_fix',
        'rule_reload',
        'select_icon',
        'select_iterator',
        'rule_context',
        'rule_create',
        'rule_delete'
    ]
    for module_name in reloadable_modules:
        if module_name in locals():
            importlib.reload(locals()[module_name])

import bpy

from . import (
    issue_fix,
    rule_reload,
    select_icon,
    select_iterator,
    rule_context,
    rule_create,
    rule_delete
)

from .issue_fix import BT_OT_FixIssue, BT_OT_FixIssueAll, BT_OT_DebugFixIssue
from .rule_reload import BT_OT_ReloadRules, BT_OT_SaveRules
from .select_icon import BT_OT_SelectIcon, BT_OT_IconSelection
from .select_iterator import BT_OT_SelectIterator
from .rule_create import BT_OT_CreateRule
from .rule_delete import BT_OT_DeleteRule


_registration_order = [
    select_iterator.BT_OT_SelectIterator,
    select_icon.BT_OT_SelectIcon,
    select_icon.BT_OT_IconSelection,
    rule_context.BT_OT_ContextRule,
    rule_context.UI_MT_button_context_menu,
    rule_create.BT_OT_CreateRule,
    rule_delete.BT_OT_DeleteRule,
    rule_reload.BT_OT_ReloadRules,
    rule_reload.BT_OT_SaveRules,
    issue_fix.BT_OT_FixIssue,
    issue_fix.BT_OT_DebugFixIssue,
    issue_fix.BT_OT_FixIssueAll
]

if len(bpy.utils.register_classes_factory(_registration_order)) != 0:
    _register, _unregister = bpy.utils.register_classes_factory(_registration_order)


def register():
    _register()
    bpy.types.UI_MT_button_context_menu.append(rule_context.menu_func)


def unregister():
    bpy.types.UI_MT_button_context_menu.remove(rule_context.menu_func)
    _unregister()
