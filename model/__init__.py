"""Data and utility classes used by BLint."""

if 'bpy' in locals():
    import importlib

    reloadable_modules = [
        'lint_issue',
        'lint_rule',
    ]
    for module_name in reloadable_modules:
        if module_name in locals():
            importlib.reload(locals()[module_name])

import bpy

from . import lint_issue, lint_rule

from .lint_issue import LintIssue, get_sort_value
from .lint_rule import LintRule

_registration_order = [
    LintIssue,
    LintRule
]

if len(bpy.utils.register_classes_factory(_registration_order)) != 0:
    register, unregister = bpy.utils.register_classes_factory(_registration_order)
