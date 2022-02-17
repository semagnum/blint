import bpy


class LintIssue(bpy.types.PropertyGroup):
    description: bpy.props.StringProperty(name='Description', default='', options={'SKIP_SAVE'})
    severity_icon: bpy.props.StringProperty(name='Severity', default='INFO', options={'SKIP_SAVE'})
    category_icon: bpy.props.StringProperty(name='Category', default='GENERAL', options={'SKIP_SAVE'})
    fix_expr: bpy.props.StringProperty(name='Fix', default='', options={'SKIP_SAVE'})

    def draw(self, layout):
        row = layout.row(align=True)
        row.label(text='', icon=self.severity_icon)
        row.label(text='', icon=self.category_icon)
        row.label(text=self.description)
        if self.fix_expr:
            row.operator('scene_analyzer.fix_issue', text='', icon='FILE_TICK').fix = self.fix_expr


class LintRule(bpy.types.PropertyGroup):
    description: bpy.props.StringProperty(name='Description', default='', options={'SKIP_SAVE'})
    severity_icon: bpy.props.StringProperty(name='Severity', default='INFO', options={'SKIP_SAVE'})
    category_icon: bpy.props.StringProperty(name='Category', default='GENERAL', options={'SKIP_SAVE'})

    iterable_expr: bpy.props.StringProperty(name='Iterable Expression', default='', options={'SKIP_SAVE'})
    iterable_var: bpy.props.StringProperty(name='Iterable Variable', default='x', options={'SKIP_SAVE'})
    issue_expr: bpy.props.StringProperty(name='Issue', default='', options={'SKIP_SAVE'})
    fix_expr: bpy.props.StringProperty(name='Fix', default='', options={'SKIP_SAVE'})
    prop_label_expr: bpy.props.StringProperty(name='Identifier', default='', options={'SKIP_SAVE'})

    def generate_fix(self, idx=-1) -> str:
        access_var = '{}[{}]'.format(self.iterable_expr, idx)
        return self.fix_expr.replace(self.iterable_var, access_var)

    def get_iterative_list(self):
        expr = "[{} for {} in {} if {}]".format(self.iterable_var, self.iterable_var, self.iterable_expr,
                                                self.issue_expr)
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

    def get_issues(self):
        if self.iterable_expr:
            issues = []
            for idx, identifier in enumerate(self.get_iterative_list()):
                issue = {
                    'description': getattr(identifier, self.prop_label_expr, '') + ' ' + self.description,
                    'severity_icon': self.severity_icon,
                    'category_icon': self.category_icon,
                    'fix_expr': self.generate_fix(idx) if self.fix_expr else ''
                }
                issues.append(issue)
            return issues
        elif self.does_issue_exist():
            issue_identifier = self.get_ui_identifier()
            issue = {
                'description': (issue_identifier + ' ' + self.description) if issue_identifier else self.description,
                'severity_icon': self.severity_icon,
                'category_icon': self.category_icon,
                'fix_expr': self.fix_expr
            }
            return [issue]
        return []
