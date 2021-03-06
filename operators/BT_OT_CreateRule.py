import bpy

from ..save_load_util import save_external_rules
from ..pref_util import get_user_preferences


class BT_OT_CreateRule(bpy.types.Operator):
    bl_idname = 'scene_analyzer.form_create_rule'
    bl_label = 'Create Rule'
    bl_description = 'Creates new rule (external file source required)'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        preferences = get_user_preferences(context)
        return preferences.lint_filepath

    def execute(self, context):
        wm = context.window_manager
        form_rule = wm.blint_form_rule
        addon_preferences = get_user_preferences(context)
        lint_rules = addon_preferences.lint_rules

        new_rule = lint_rules.add()
        form_rule.copy(new_rule)

        # save rules
        try:
            save_external_rules(context)
        except Exception as e:
            self.report({'ERROR'}, 'Rule creation failed:' + str(e))
            return {'CANCELLED'}

        # clear form
        self.report({'INFO'}, 'Rule \'{}\' created'.format(new_rule.description))
        form_rule.reset()

        return {'FINISHED'}
