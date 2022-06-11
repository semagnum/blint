import bpy

from ..save_load_util import reload_rules


class BT_OT_ReloadRules(bpy.types.Operator):
    bl_idname = 'blint.reload_rules'
    bl_label = 'Reload linter rules'
    bl_description = 'Reloads linter rules from internal as well as external configuration'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            reload_rules(context)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, 'Reload error failed: ' + str(e))
            return {'CANCELLED'}


