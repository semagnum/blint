"""
Model class for BLint issue property groups.
Issues are instances of rule violations seen in the Blender file.
"""

import bpy

from .icon_gen import get_icon_enum, get_severity_enum

severity_levels = ['ERROR', 'INFO']
"""Accepted severity icons for rules, in the order of priority."""


class LintIssue(bpy.types.PropertyGroup):
    """Model class for BLint issue properties. Used for displaying within a UI list.

    BLint issues are instances of ``LintRule`` violations seen in the Blender file.
    """

    description: bpy.props.StringProperty(name='Description', default='')
    """Describes the issue based on its rule."""
    severity_icon: bpy.props.EnumProperty(name='Severity', default='INFO', items=get_severity_enum())
    """Name of Blender icon to represent severity."""
    category_icon: bpy.props.EnumProperty(name='Category', default='SCENE_DATA', items=get_icon_enum())
    """Name of Blender icon to represent the category of the issue's rule (meshes, animation, etc.)."""
    fix_expr: bpy.props.StringProperty(name='Fix', default='')
    """String representation of Python code that will fix the issue."""

    def draw(self, layout):
        """Draws the issue in a panel."""
        row = layout.row(align=True)
        row.label(text='', icon=self.severity_icon)
        row.label(text='', icon=self.category_icon)
        row.label(text=self.description)
        if self.fix_expr:
            row.operator('scene_analyzer.fix_issue', text='', icon='FILE_TICK').fix = self.fix_expr


def get_sort_value(lint_rule: LintIssue) -> int:
    """Utility function generating a sort value for an issue based on its rule's severity.

    :param lint_rule: LintIssue property
    """
    # if not in the list, put at the end
    if lint_rule.severity_icon not in severity_levels:
        return len(severity_levels)
    return severity_levels.index(lint_rule.severity_icon)
