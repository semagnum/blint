# Copyright (C) 2023 Spencer Magnusson
# semagnum@gmail.com
# Created by Spencer Magnusson
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import annotations

import bpy

from ..icon_gen import get_icon_enum, get_severity_enum


class LintRule(bpy.types.PropertyGroup):
    """Model class for BLint rule properties. Used for displaying within a UI list.
     BLint rules are violations that may be seen in the Blender file that can be fixed.
    """
    enabled: bpy.props.BoolProperty(name='Enabled', default=True)
    """If rule is enabled by default."""
    description: bpy.props.StringProperty(name='Description', default='')
    """Describes the issue based on its rule."""
    severity_icon: bpy.props.EnumProperty(name='Severity', default='INFO', items=get_severity_enum())
    """Name of Blender icon to represent severity."""
    category_icon: bpy.props.EnumProperty(name='Category', default='SCENE_DATA', items=get_icon_enum())
    """Name of Blender icon to represent the category of the issue's rule (meshes, animation, etc.)."""

    iterable_expr: bpy.props.StringProperty(name='Data iteration type',
                                            description='Python expression representing Blender data '
                                                        'containing elements with potential issues',
                                            default='bpy.data.scenes')
    """String of Python code that evaluates to a list of properties. Optional.
    
    If provided, multiple issues can be found from one rule.
    """
    iterable_var: bpy.props.StringProperty(name='Variable',
                                           description='Variable name to reference data iteration element',
                                           default='my_scene')
    """Required if ``iterable_expr`` is defined.
    
    If provided, any instance of ``iterable_var`` in ``issue_expr``, ``fix_expr`` or ``prop_label_expr``
    will be replaced with the value of ``iterable_expr``.
    """
    issue_expr: bpy.props.StringProperty(name='Issue',
                                         description='Python expression that returns true if issue exists '
                                                     '(can reference data iteration variable)',
                                         default='')
    """Optional. Python statement(s) that fix(es) the issue.
    
    A rule should only have a fix that will always work (no errors), is always what the user would want,
    and will remove the issue from the panel.
    """
    fix_expr: bpy.props.StringProperty(name='Fix',
                                       description='Statement(s) to fix the issue '
                                                   '(can reference data iteration variable)',
                                       default='')
    """String representation of Python code that will fix the issue."""
    prop_label_expr: bpy.props.StringProperty(name='Issue identifier',
                                              description='Python expression to further identify issue'
                                                          'in its description (can reference data iteration variable)',
                                              default='')
    """Python expression that evaluates to an identifying label used with the issue description in the UI."""

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
        if self.iterable_expr != '' and self.iterable_var == '':
            issues.append('Iteration variable cannot be empty when using data iteration')
        return issues

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

    def generate_description(self, idx: int = -1) -> str:
        """Generates and returns a Python statement to fix a LintIssue instance of a rule.

        :param idx: element index within the issue list.
        """
        if not self.prop_label_expr:
            return self.description

        label_expr = self.prop_label_expr
        try:
            if idx != -1:
                locals()[self.iterable_var] = eval('{}[{}]'.format(self.get_list_str(), idx))

            label_val = str(eval(label_expr)) + ': ' + self.description
        except Exception as e:
            print('generate_iterative_label failed: ', e)
            label_val = self.description

        return label_val

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

    def draw(self, layout: bpy.types.UILayout):
        """Draws rule in a panel."""
        row = layout.row(align=True)
        row.alert = len(self.check_for_errors()) != 0
        row.prop(self, 'enabled', text='', icon='CHECKBOX_HLT' if self.enabled else 'CHECKBOX_DEHLT')
        sub_row = row.row(align=True)
        sub_row.enabled = self.enabled
        sub_row.label(text='', icon=self.severity_icon)
        sub_row.label(text='', icon=self.category_icon)
        sub_row.label(text=self.description)

    def get_issues(self) -> list[dict]:
        """Generates and returns a list of issues that violate rules."""
        if self.enabled:
            if self.iterable_expr:
                issues = []
                for idx, identifier in enumerate(self.get_iterative_list()):
                    issue = {
                        'description': self.generate_description(idx),
                        'severity_icon': self.severity_icon,
                        'category_icon': self.category_icon,
                        'fix_expr': self.generate_fix(idx) if self.fix_expr else ''
                    }
                    issues.append(issue)
                return issues
            elif self.does_issue_exist():
                issue = {
                    'description': self.generate_description(-1),
                    'severity_icon': self.severity_icon,
                    'category_icon': self.category_icon,
                    'fix_expr': self.fix_expr
                }
                return [issue]
        return []
