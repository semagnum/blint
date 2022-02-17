import bpy

from ..preferences import reload_issues
from ..util import get_user_preferences


class BT_PT_Linter(bpy.types.Panel):
    bl_label = 'BLinter'
    bl_category = 'BLinter'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        layout = self.layout

        prefs = get_user_preferences(context)

        reload_issues(prefs.lint_issues, prefs.lint_rules)
        layout.template_list('BT_UL_Linter', '', prefs, 'lint_issues', context.scene, 'bl_lint_rule_active', columns=4)
