from __future__ import annotations

import bpy

from ..config import BT_OT_DELETE_RULE_IDNAME
from ..icon_gen import get_icon_enum, get_severity_enum


class LintRule(bpy.types.PropertyGroup):
    """Model class for BLint rule properties. Used for displaying within a UI list.
     BLint rules are violations that may be seen in the Blender file that can be fixed.
    """
    enabled: bpy.props.BoolProperty(name='Enabled', default=True)
    """If rule is enabled by default."""
    is_internal: bpy.props.BoolProperty(name='Internal', default=False)
    """If rule comes from BLint's internal list, else an external JSON file."""
    description: bpy.props.StringProperty(name='Description', default='')
    """Describes the issue based on its rule."""
    severity_icon: bpy.props.EnumProperty(name='Severity', default='INFO', items=get_severity_enum())
    """Name of Blender icon to represent severity."""
    category_icon: bpy.props.EnumProperty(name='Category', default='SCENE_DATA', items=get_icon_enum())
    """Name of Blender icon to represent the category of the issue's rule (meshes, animation, etc.)."""

    iterable_expr: bpy.props.StringProperty(name='Iterable Expression',
                                            description='Expression to find the collection'
                                                        'containing elements with potential issues',
                                            default='bpy.data.scenes')
    """String of Python code that evaluates to a list of properties. Optional.
    
    If provided, multiple issues can be found from one rule.
    """
    iterable_var: bpy.props.StringProperty(name='Iterable Variable',
                                           description='Variable to use for iterating over the collection',
                                           default='my_scene')
    """Required if ``iterable_expr`` is defined.
    
    If provided, any instance of ``iterable_var`` in ``issue_expr`` or ``fix_expr``
    will be replaced with the value of ``iterable_expr``.
    """
    issue_expr: bpy.props.StringProperty(name='Issue',
                                         description='Python expression that returns true if issue exists'
                                                     '(can reference iterable variable)',
                                         default='')
    """Optional. Python statement(s) that fix(es) the issue.
    
    A rule should only have a fix that will always work (no errors), is always what the user would want,
    and will remove the issue from the panel.
    """
    fix_expr: bpy.props.StringProperty(name='Fix',
                                       description='Statement(s) to fix the issue'
                                                   '(can reference iterable variable)',
                                       default='')
    """String representation of Python code that will fix the issue."""
    prop_label_expr: bpy.props.StringProperty(name='Identifier',
                                              description='Data attribute to get the name of the property',
                                              default='name')
    """Python expression that evaluates to an attribute to be used with the description in the UI.
    
    If ``iterable_var`` is used, then ``prop_label_expr`` is the attribute of each iterable element to be used with the description.
    
    For example, "name" with ``iterable_var`` "bpy.data.objects" means
    that each object's ``name`` attribute will be shown in the description).
    Otherwise, Python that evaluates it to a string used to label the issue.
    """

    def check_for_errors(self) -> list[str]:
        """Validates ``LintRule`` properties.

        Returns a list of errors to fix to make the LintRule valid.
        """
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
        """Resets rule to default property values."""
        self.enabled = True
        self.description = ''
        self.severity_icon = 'INFO'
        self.category_icon = 'SCENE_DATA'
        self.iterable_expr = 'bpy.data.scenes'
        self.iterable_var = 'my_scene'
        self.issue_expr = ''
        self.fix_expr = ''
        self.prop_label_expr = ''

    def copy(self, other_rule: LintRule) -> LintRule:
        """Copies self's properties to another rule, and returns the other rule.

        :param other_rule: target rule to have properties applied and then returned.
        """
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

    def get_list_str(self) -> str:
        """Generates a list of data items that violate the LintRule.

        Returns Python code to represent a Python list of LintIssue items.
        """
        expr = "[{} for {} in {} if {}]".format(self.iterable_var, self.iterable_var, self.iterable_expr,
                                                self.issue_expr)
        return expr

    def generate_fix(self, idx: int = -1) -> str:
        """Generates and returns a Python statement to fix a LintIssue instance of a rule.

        :param idx: element index within the issue list.
        """
        access_var = '{}[{}]'.format(self.get_list_str(), idx)
        return '{} = {}; '.format(self.iterable_var, access_var) + self.fix_expr

    def get_iterative_list(self) -> list:
        """Evaluates get_list_str() and returns a list to iterate for displaying and fixing issues."""
        expr = self.get_list_str()
        try:
            return eval(expr)
        except Exception as e:
            print('get_iterative_list failed:', e, expr)
            return []

    def does_issue_exist(self) -> bool:
        """Returns True if any issues exist that violate the rule, False otherwise."""
        try:
            return eval(self.issue_expr)
        except Exception as e:
            print('does_issue_exist failed:', e, self.issue_expr)
            return False

    def get_ui_identifier(self) -> str:
        """Retrieves a string-based data property that contains the rule violation."""
        if not self.prop_label_expr:
            return ''
        try:
            return eval(self.prop_label_expr)
        except Exception as e:
            print('get_ui_identifier failed', e)
            return ''

    def draw(self, layout: bpy.types.UILayout, index: int):
        """Draws rule in a panel."""
        row = layout.row(align=True)
        row.prop(self, 'enabled', text='', icon='CHECKBOX_HLT' if self.enabled else 'CHECKBOX_DEHLT')
        sub_row = row.row(align=True)
        sub_row.enabled = self.enabled
        sub_row.label(text='', icon=self.severity_icon)
        sub_row.label(text='', icon=self.category_icon)
        sub_row.label(text=self.description)
        op = sub_row.operator(BT_OT_DELETE_RULE_IDNAME, text='', icon='X')
        op.rule_index = index

    def get_issues(self) -> list[dict]:
        """Generates and returns a list of issues that violate rules."""
        if self.enabled:
            if self.iterable_expr:
                issues = []
                for idx, identifier in enumerate(self.get_iterative_list()):
                    issue = {
                        'description': str(getattr(identifier, self.prop_label_expr, '')) + ': ' + self.description,
                        'severity_icon': self.severity_icon,
                        'category_icon': self.category_icon,
                        'fix_expr': self.generate_fix(idx) if self.fix_expr else ''
                    }
                    issues.append(issue)
                return issues
            elif self.does_issue_exist():
                issue_id = self.get_ui_identifier()
                issue = {
                    'description': (str(issue_id) + ' ' + self.description) if issue_id else self.description,
                    'severity_icon': self.severity_icon,
                    'category_icon': self.category_icon,
                    'fix_expr': self.fix_expr
                }
                return [issue]
        return []
