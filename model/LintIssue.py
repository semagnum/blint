import bpy


class LintIssue(bpy.types.PropertyGroup):
    description: bpy.props.StringProperty(name='Description', default='', options={'SKIP_SAVE'})
    severity_icon: bpy.props.StringProperty(name='Severity', default='INFO', options={'SKIP_SAVE'})
    category_icon: bpy.props.StringProperty(name='Category', default='SCENE_DATA', options={'SKIP_SAVE'})
    fix_expr: bpy.props.StringProperty(name='Fix', default='', options={'SKIP_SAVE'})

    def draw(self, layout):
        row = layout.row(align=True)
        row.label(text='', icon=self.severity_icon)
        row.label(text='', icon=self.category_icon)
        row.label(text=self.description)
        if self.fix_expr:
            row.operator('scene_analyzer.fix_issue', text='', icon='FILE_TICK').fix = self.fix_expr
