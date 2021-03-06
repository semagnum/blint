import bpy
from .model.LintRule import LintRule
from .operators.BT_OT_ReloadRules import BT_OT_ReloadRules
from .pref_util import get_user_preferences
from .model.icon_gen import format_icon_name

from .operators.BT_OT_SelectIcon import BT_OT_IconSelection
from .operators.BT_OT_CreateRule import BT_OT_CreateRule
from .operators.BT_OT_SelectIterator import BT_OT_SelectIterator


def reload_issues(context):
    issues_collection = context.window_manager.lint_issues
    rules = get_user_preferences(context).lint_rules
    issues_collection.clear()
    for r in rules:
        for issue in r.get_issues():
            try:
                new_issue = issues_collection.add()
                new_issue.description = issue.get('description')
                new_issue.severity_icon = issue.get('severity_icon')
                new_issue.category_icon = issue.get('category_icon')
                new_issue.fix_expr = issue.get('fix_expr')
            except ValueError as e:
                print("Error with {}: {}".format(issue.get('description'), e))


class SA_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    lint_rules: bpy.props.CollectionProperty(type=LintRule)
    lint_filepath: bpy.props.StringProperty(name='External lint rules filepath', default='', subtype='FILE_PATH')

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        layout.label(text='Rules')
        layout.template_list('BT_UL_Rules', '', self, 'lint_rules', context.window_manager, 'lint_rule_active',
                             columns=3)

        layout.separator()
        layout.prop(self, "lint_filepath")
        layout.operator(BT_OT_ReloadRules.bl_idname, icon='FILE_REFRESH')

        if self.lint_filepath:
            layout.separator()
            layout.prop(context.window_manager, "form_collapsed",
                        icon='TRIA_RIGHT' if wm.form_collapsed else 'TRIA_DOWN',
                        invert_checkbox=True)
            if not wm.form_collapsed:
                draw_rule_creation(layout, context)
        else:
            layout.label(text='No external filepath set, create a \".json\" file to create and store your own rules!', icon='INFO')


def draw_rule_creation(layout, context):

    def reload_form_issues(wm):
        wm.blint_form_issues.clear()
        r = wm.blint_form_rule
        for issue in r.get_issues():
            try:
                new_issue = wm.blint_form_issues.add()
                new_issue.description = issue.get('description')
                new_issue.severity_icon = issue.get('severity_icon')
                new_issue.category_icon = issue.get('category_icon')
                new_issue.fix_expr = issue.get('fix_expr')
            except ValueError as e:
                print("Error with {}: {}".format(issue.get('description'), e))

    wm = context.window_manager

    form_rule: LintRule = wm.blint_form_rule
    layout.prop(form_rule, 'enabled', text='Enabled by default?')
    layout.prop(form_rule, 'description')

    layout.label(text='Icons')
    icon_box = layout.box()
    icon_box.prop(form_rule, 'severity_icon')

    row = icon_box.row()
    row.label(text='Category: {}'.format(format_icon_name(form_rule.category_icon)), icon=form_rule.category_icon)
    op = row.operator(BT_OT_IconSelection.bl_idname, text='Select category icon', icon='IMAGE_DATA')
    op.attr_name = 'category_icon'

    row = layout.row(align=True)
    row.label(text='For each data item in')
    row.prop(form_rule, 'iterable_expr', text='')
    row.operator(BT_OT_SelectIterator.bl_idname, icon='FILE_BLEND')

    box = layout.box()
    box.prop(form_rule, 'prop_label_expr')

    box.separator()

    box.prop(form_rule, 'iterable_var', text='Variable name')
    box.prop(form_rule, 'issue_expr', text='An issue exists if')
    box.prop(form_rule, 'fix_expr', text='Issue fix (optional)')

    validation_errs = form_rule.check_for_errors()
    is_valid = len(validation_errs) == 0
    if is_valid:
        layout.label(text='Validation passed', icon='CHECKMARK')

        try:
            reload_form_issues(wm)

            layout.label(text='Debug')
            layout.template_list('BT_UL_Issues', '', wm, 'blint_form_issues', wm, 'blint_form_issue_active',
                                 columns=4)
        except Exception as e:
            print(e)
            layout.label(text='Issue debugging failed, check console', icon='ERROR')
    else:
        layout.label(text='Validation failed', icon='ERROR')
        for err in validation_errs:
            layout.label(text=err)

    # Create rule
    row = layout.row()
    row.operator(BT_OT_CreateRule.bl_idname, icon='TEXT')
    row.enabled = is_valid
