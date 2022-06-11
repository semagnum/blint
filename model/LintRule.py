import bpy

from ..operators.BT_OT_DeleteRule import BT_OT_DeleteRule
from .icon_gen import get_icon_enum, get_severity_enum


class LintRule(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(name='Enabled', default=True)
    is_internal: bpy.props.BoolProperty(name='Internal', default=False)

    description: bpy.props.StringProperty(name='Description', default='')
    severity_icon: bpy.props.EnumProperty(name='Severity', default='INFO', items=get_severity_enum())
    category_icon: bpy.props.EnumProperty(name='Category', default='SCENE_DATA', items=get_icon_enum())

    iterable_expr: bpy.props.StringProperty(name='Iterable Expression',
                                            description='Expression to find the collection'
                                                        'containing elements with potential issues',
                                            default='bpy.data.scenes')
    iterable_var: bpy.props.StringProperty(name='Iterable Variable',
                                           description='Variable to use for iterating over the collection',
                                           default='my_scene')
    issue_expr: bpy.props.StringProperty(name='Issue',
                                         description='Python expression that returns true if issue exists'
                                                     '(can reference iterable variable)',
                                         default='')
    fix_expr: bpy.props.StringProperty(name='Fix',
                                       description='Statement(s) to fix the issue'
                                                   '(can reference iterable variable)',
                                       default='')
    prop_label_expr: bpy.props.StringProperty(name='Identifier', default='name')

    def check_for_errors(self) -> list:
        issues = []
        if self.description == '':
            issues.append('Description cannot be empty')
        if self.category_icon == '':
            issues.append('Category icon cannot be empty')
        if self.severity_icon == '':
            issues.append('Severity icon cannot be empty')
        if self.issue_expr == '':
            issues.append('Issue expression cannot be empty')
        if self.prop_label_expr == '':
            issues.append('Prop label expression cannot be empty')
        if self.iterable_expr != '' and self.iterable_expr == '':
            issues.append('Iterable expression cannot be empty')
        return issues

    def reset(self):
        self.enabled = True
        self.description = ''
        self.severity_icon = 'INFO'
        self.category_icon = 'SCENE_DATA'
        self.iterable_expr = 'bpy.data.scenes'
        self.iterable_var = 'my_scene'
        self.issue_expr = ''
        self.fix_expr = ''
        self.prop_label_expr = ''

    def copy(self, other_rule):
        other_rule.enabled = self.enabled
        other_rule.description = self.description
        other_rule.severity_icon = self.severity_icon
        other_rule.category_icon = self.category_icon

        other_rule.iterable_expr = self.iterable_expr
        other_rule.iterable_var = self.iterable_var
        other_rule.issue_expr = self.issue_expr
        other_rule.fix_expr = self.fix_expr
        other_rule.prop_label_expr = self.prop_label_expr
        return other_rule

    def get_list_str(self):
        expr = "[{} for {} in {} if {}]".format(self.iterable_var, self.iterable_var, self.iterable_expr,
                                                self.issue_expr)
        return expr

    def generate_fix(self, idx=-1) -> str:
        access_var = '{}[{}]'.format(self.get_list_str(), idx)
        return self.fix_expr.replace(self.iterable_var, access_var)

    def get_iterative_list(self):
        expr = self.get_list_str()
        try:
            return eval(expr)
        except Exception as e:
            print('get_iterative_list failed:', e, expr)
            return []

    def does_issue_exist(self) -> bool:
        try:
            return eval(self.issue_expr)
        except Exception as e:
            print('does_issue_exist failed:', e, self.issue_expr)
            return False

    def get_ui_identifier(self):
        """
        :return: string representing which property has the issue
        """
        if not self.prop_label_expr:
            return ''
        try:
            return eval(self.prop_label_expr)
        except Exception as e:
            print('get_ui_identifier failed', e)
            return ''

    def draw(self, layout, index):
        row = layout.row(align=True)
        row.prop(self, 'enabled', text='', icon='CHECKBOX_HLT' if self.enabled else 'CHECKBOX_DEHLT')
        sub_row = row.row(align=True)
        sub_row.enabled = self.enabled
        sub_row.label(text='', icon=self.severity_icon)
        sub_row.label(text='', icon=self.category_icon)
        sub_row.label(text=self.description)
        op = sub_row.operator(BT_OT_DeleteRule.bl_idname, text='', icon='X')
        op.rule_index = index

    def get_issues(self):
        if self.enabled:
            if self.iterable_expr:
                issues = []
                for idx, identifier in enumerate(self.get_iterative_list()):
                    issue = {
                        'description': getattr(identifier, self.prop_label_expr, '') + ': ' + self.description,
                        'severity_icon': self.severity_icon,
                        'category_icon': self.category_icon,
                        'fix_expr': self.generate_fix(idx) if self.fix_expr else ''
                    }
                    issues.append(issue)
                return issues
            elif self.does_issue_exist():
                issue_id = self.get_ui_identifier()
                issue = {
                    'description': (issue_id + ' ' + self.description) if issue_id else self.description,
                    'severity_icon': self.severity_icon,
                    'category_icon': self.category_icon,
                    'fix_expr': self.fix_expr
                }
                return [issue]
        return []
