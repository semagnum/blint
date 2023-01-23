import bpy

from ..save_load_util import save_external_rules
from ..pref_util import get_user_preferences


class BT_OT_DeleteRule(bpy.types.Operator):
    """Deletes rule from the preferences."""
    bl_idname = 'blint.delete_rule'
    bl_label = 'Delete Rule'
    bl_description = 'Deletes this rule'
    bl_options = {'REGISTER', 'UNDO'}

    rule_index: bpy.props.IntProperty(default=-1)
    """Index of the rule to be deleted from BLint's list."""

    def execute(self, context):
        if self.rule_index == -1:
            self.report({'ERROR'}, 'Invalid rule specified')
            return {'CANCELLED'}
        addon_preferences = get_user_preferences(context)
        lint_rules = addon_preferences.lint_rules

        rule_description = lint_rules[self.rule_index].description
        is_internal = lint_rules[self.rule_index].is_internal

        lint_rules.remove(self.rule_index)
        if not is_internal:
            save_external_rules(context)
        self.report({'INFO'}, 'Rule \'{}\' deleted'.format(rule_description))
        return {'FINISHED'}
