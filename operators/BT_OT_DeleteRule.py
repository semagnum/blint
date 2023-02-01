import bpy

from .. import get_user_preferences
from ..config import BT_OT_DELETE_RULE_IDNAME
from ..save_load import save_external_rules


class BT_OT_DeleteRule(bpy.types.Operator):
    """Deletes rule from the preferences."""
    bl_idname = BT_OT_DELETE_RULE_IDNAME
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
