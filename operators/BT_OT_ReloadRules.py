import bpy

from ..util import get_user_preferences, reload_rules


class BT_OT_ReloadRules(bpy.types.Operator):
    bl_idname = 'blint.reload_rules'
    bl_label = 'Reload linter rules'
    bl_description = 'Reloads linter rules from internal as well as external configuration'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = get_user_preferences(context)
        preferences.lint_rules.clear()

        try:
            reload_rules(context)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}


