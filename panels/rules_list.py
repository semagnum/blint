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

from ..model import LintRule
from ..model import get_sort_value


class BT_UL_Rules(bpy.types.UIList):
    """Blender UI List to display rules in the preferences. Includes filtering and sorting."""

    def draw_item(self, context, layout, data, rule: LintRule, icon, active_data, active_propname, index):
        rule.draw(layout, index)

    def filter_items(self, context, data, propname):
        rules = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = []

        # Filtering by name
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item,
                                                          rules, 'description')

        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(rules)

        _sort = [(idx, (get_sort_value(rule), getattr(rule, 'description', '').lower()))
                 for idx, rule in enumerate(rules)]
        flt_neworder = helper_funcs.sort_items_helper(_sort, lambda e: e[1])

        return flt_flags, flt_neworder
