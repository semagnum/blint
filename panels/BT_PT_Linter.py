import bpy
from ..util import get_user_preferences


class BT_PT_Linter(bpy.types.Panel):
    bl_label = 'BLinter'
    bl_category = 'BLinter'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        layout = self.layout

        # TODO use UI list
        prefs = get_user_preferences(context)
        for lint in prefs.lint_rules.values():
            lint.draw(layout)
        # layout.template_list('BT_UL_Linter', '', prefs, 'lint_rules', context.scene, 'bl_lint_rule_active', columns=4)
