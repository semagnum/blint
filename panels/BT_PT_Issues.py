import bpy

from ..preferences import reload_issues


class BT_PT_Issues(bpy.types.Panel):
    bl_label = 'BLinter'
    bl_category = 'BLinter'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        layout = self.layout
        window_manager = context.window_manager

        reload_issues(context)
        layout.template_list('BT_UL_Issues', '', window_manager, 'lint_issues', window_manager, 'lint_issue_active', columns=4)
