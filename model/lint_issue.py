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


"""
Model class for BLint issue property groups.
Issues are instances of rule violations seen in the Blender file.
"""

import bpy

from ..icon_gen import get_icon_enum, get_severity_enum, severity_icons


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
        row.active = bool(self.fix_expr)
        row.label(text='', icon=self.severity_icon)
        row.label(text='', icon=self.category_icon)
        row.label(text=self.description)


def get_sort_value(issue: LintIssue) -> int:
    """Utility function generating a sort value for an issue based on its rule's severity.

    :param issue: LintIssue property
    """
    # if not in the list, put at the end
    if issue.severity_icon not in severity_icons:
        return len(severity_icons)
    return severity_icons.index(issue.severity_icon)
