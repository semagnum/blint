import bpy

from ..model.LintRule import LintRule


class BT_UL_Rules(bpy.types.UIList):

    def draw_item(self, context, layout, data, rule: LintRule, icon, active_data, active_propname, index):
        rule.draw(layout)

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

        _sort = [(idx, getattr(it, 'description', '')) for idx, it in enumerate(rules)]
        flt_neworder = helper_funcs.sort_items_helper(_sort, lambda e: e[1].lower())

        return flt_flags, flt_neworder