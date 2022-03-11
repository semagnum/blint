import sys
import bpy

# get lint rules from preferences
blend_filename = bpy.data.filepath
try:
    from blint.model.LintIssue import get_sort_value
    from blint.preferences import reload_issues
except ImportError:
    print("blinter: blint not found, the blint addon must be installed and enabled!")
    sys.exit(1)

context = bpy.context
window_manager = context.window_manager

context.scene.render.engine = 'CYCLES'

reload_issues(context)

# print blender file name
try:
    if len(window_manager.lint_issues) == 0:
        print("blinter: no issues found")
    else:
        issues = window_manager.lint_issues
        issue_sort_vals = [(idx, get_sort_value(issue), issue.description) for idx, issue in enumerate(issues)]
        issue_sort_vals.sort(key=lambda x: (x[1], x[2]))
        for idx, _, _ in issue_sort_vals:
            issue = issues[idx]
            print("blinter: {}\t\t{}".format(issue.severity_icon, issue.description))

        num_fixable = len([True for issue in issues if issue.fix_expr])
        print("blinter: {} of {} issues can be automatically fixed".format(num_fixable, len(issues)))
except Exception as e:
    print("blinter: {}".format(e))
