import bpy

from .icon_gen import get_icon_enum, get_severity_enum

severity_levels = ['ERROR', 'INFO']


def get_sort_value(lint_rule):
    # if not in the list, put at the end
    if lint_rule.severity_icon not in severity_levels:
        return len(severity_levels)
    return severity_levels.index(lint_rule.severity_icon)


class LintIssue(bpy.types.PropertyGroup):
    description: bpy.props.StringProperty(name='Description', default='')
    severity_icon: bpy.props.EnumProperty(name='Severity', default='INFO', items=get_severity_enum())
    category_icon: bpy.props.EnumProperty(name='Category', default='SCENE_DATA', items=get_icon_enum())
    fix_expr: bpy.props.StringProperty(name='Fix', default='')

    def draw(self, layout):
        row = layout.row(align=True)
        row.label(text='', icon=self.severity_icon)
        row.label(text='', icon=self.category_icon)
        row.label(text=self.description)
        if self.fix_expr:
            row.operator('scene_analyzer.fix_issue', text='', icon='FILE_TICK').fix = self.fix_expr
