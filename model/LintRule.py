import bpy


class LintRule(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(name='Enabled', default=True)

    description: bpy.props.StringProperty(name='Description', default='')
    severity_icon: bpy.props.StringProperty(name='Severity', default='INFO')
    category_icon: bpy.props.StringProperty(name='Category', default='SCENE_DATA')

    iterable_expr: bpy.props.StringProperty(name='Iterable Expression', default='')
    iterable_var: bpy.props.StringProperty(name='Iterable Variable', default='x')
    issue_expr: bpy.props.StringProperty(name='Issue', default='')
    fix_expr: bpy.props.StringProperty(name='Fix', default='')
    prop_label_expr: bpy.props.StringProperty(name='Identifier', default='')

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

    def draw(self, layout):
        row = layout.row(align=True)
        row.prop(self, 'enabled', text='', icon='CHECKBOX_HLT' if self.enabled else 'CHECKBOX_DEHLT')
        sub_row = row.row(align=True)
        sub_row.enabled = self.enabled
        sub_row.label(text='', icon=self.severity_icon)
        sub_row.label(text='', icon=self.category_icon)
        sub_row.label(text=self.description)

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
