import bpy

from ..model import LintIssue, get_sort_value


class BT_UL_Issues(bpy.types.UIList):
    """Blender UI List to display issues. Includes filtering and sorting."""

    def draw_item(self, context, layout, data, issue: LintIssue, icon, active_data, active_propname,
                  index):
        issue.draw(layout)

    def filter_items(self, context, data, propname):
        issues = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = []
        flt_neworder = []

        # Filtering by name
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item,
                                                          issues, 'description')

        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(issues)

        _sort = [(idx, (get_sort_value(issue), getattr(issue, 'description', '').lower()))
                 for idx, issue in enumerate(issues)]
        flt_neworder = helper_funcs.sort_items_helper(_sort, lambda e: e[1])

        return flt_flags, flt_neworder
