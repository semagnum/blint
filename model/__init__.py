"""Data and utility classes used by BLint."""

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
