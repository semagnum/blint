import bpy
from .model.LintRule import LintRule
from .operators.BT_OT_ReloadRules import BT_OT_ReloadRules


class SA_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    lint_rules: bpy.props.CollectionProperty(type=LintRule)
    lint_filepath: bpy.props.StringProperty(default='', subtype='FILE_PATH')

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "lint_filepath")
        layout.operator(BT_OT_ReloadRules.bl_idname, icon='FILE_REFRESH')
