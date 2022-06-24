import bpy

from .panels.BT_UL_Rules import BT_UL_Rules
from .panels.BT_UL_Issues import BT_UL_Issues
from .panels.BT_PT_Issues import BT_PT_Issues

from .operators.BT_OT_ReloadRules import BT_OT_ReloadRules
from .operators.BT_OT_FixIssue import BT_OT_FixIssue
from .operators.BT_OT_SelectIcon import BT_OT_SelectIcon, BT_OT_IconSelection
from .operators.BT_OT_SelectIterator import BT_OT_SelectIterator
from .operators.BT_OT_CreateRule import BT_OT_CreateRule
from .operators.BT_OT_DeleteRule import BT_OT_DeleteRule

from .save_load_util import reload_rules
from .preferences import SA_Preferences
from .model.LintRule import LintRule
from .model.LintIssue import LintIssue

bl_info = {
    "name": 'BLint',
    "author": 'Spencer Magnusson',
    "version": (0, 2, 1),
    "blender": (2, 93, 0),
    "description": 'Custom project linting',
    "location": 'Scene',
    "support": 'COMMUNITY',
    "category_icon": 'Scene'
}
prop_groups = [LintIssue, LintRule, SA_Preferences]
operators_panels = [BT_OT_SelectIterator, BT_OT_SelectIcon, BT_OT_IconSelection, BT_OT_CreateRule, BT_OT_DeleteRule,
                    BT_UL_Rules, BT_UL_Issues,
                    BT_OT_ReloadRules, BT_OT_FixIssue,
                    BT_PT_Issues]

classes = prop_groups + operators_panels

properties = [
    ('lint_rule_active', bpy.props.IntProperty(default=0)),
    ('lint_issue_active', bpy.props.IntProperty(default=0)),
    ('lint_issues', bpy.props.CollectionProperty(type=LintIssue)),
    # form creator
    ('blint_form_rule', bpy.props.PointerProperty(type=LintRule)),
    ('blint_form_issue_active', bpy.props.IntProperty(default=0)),
    ('blint_form_issues', bpy.props.CollectionProperty(type=LintIssue)),
    ('form_collapsed', bpy.props.BoolProperty(name='Create Rules', default=True))
]


def security_check(expression: str):
    if 'eval(' in expression or 'exec(' in expression:
        raise ValueError('Expression contains insecure code: {}'.format(expression))


def register():
    window_manager = bpy.types.WindowManager

    for cls in classes:
        bpy.utils.register_class(cls)

    for name, prop in properties:
        setattr(window_manager, name, prop)

    reload_rules(bpy.context)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
