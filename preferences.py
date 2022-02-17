import bpy
from .model.LintRule import LintRule, LintIssue
from .operators.BT_OT_ReloadRules import BT_OT_ReloadRules


def reload_issues(issues_collection, rules: list):
    issues_collection.clear()
    for r in rules:
        for issue in r.get_issues():
            new_issue = issues_collection.add()
            new_issue.description = issue.get('description')
            new_issue.severity_icon = issue.get('severity_icon')
            new_issue.category_icon = issue.get('category_icon')
            new_issue.fix_expr = issue.get('fix_expr')


class SA_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    lint_rules: bpy.props.CollectionProperty(type=LintRule)
    lint_issues: bpy.props.CollectionProperty(type=LintIssue, options={'SKIP_SAVE', 'HIDDEN'})
    lint_filepath: bpy.props.StringProperty(name='External lint rules filepath', default='', subtype='FILE_PATH')

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "lint_filepath")
        layout.operator(BT_OT_ReloadRules.bl_idname, icon='FILE_REFRESH')
