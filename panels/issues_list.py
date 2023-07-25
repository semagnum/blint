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

from ..model import LintIssue, get_sort_value


class BT_UL_Issues(bpy.types.UIList):
    """Blender UI List to display issues. Includes filtering and sorting."""

    is_fixable: bpy.props.BoolProperty(
        name="Fixable Only",
        description="Only show issues with automated fixes",
        default=False
    )
    """Toggle to only show issues with automated fixes."""
    is_error: bpy.props.BoolProperty(
        name="Errors Only",
        description="Only show issues categorized as errors",
        default=False
    )
    """Toggle to only show issues categorized as errors."""

    def draw_item(self, context, layout, data, issue: LintIssue, icon, active_data, active_propname,
                  index):
        issue.draw(layout)

    def draw_filter(self, context, layout):
        row = layout.row()
        row.prop(self, 'filter_name', text='')
        row.prop(self, 'is_fixable', text='Fixable', toggle=1)
        row.prop(self, 'is_error', text='Error only', icon='ERROR')

    def filter_items(self, context, data, propname):
        issues = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = [self.bitflag_filter_item] * len(issues)
        flt_neworder = []

        # Filtering by name
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item,
                                                          issues, 'description')

        for idx in range(len(flt_flags)):
            issue: LintIssue = issues[idx]
            if ((self.is_fixable and len(issue.fix_expr) == 0)
                    or (self.is_error and issue.severity_icon != 'ERROR')
            ):
                flt_flags[idx] = 0

        _sort = [(idx, (get_sort_value(issue), getattr(issue, 'description', '').lower()))
                 for idx, issue in enumerate(issues)]
        flt_neworder = helper_funcs.sort_items_helper(_sort, lambda e: e[1])

        return flt_flags, flt_neworder
