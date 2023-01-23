"""Python file to run within Blender to run BLint.

If you wish to run BLint without opening Blender, use ``offline_blinter.py``.

"""
import sys
import bpy


def log(line: str):
    """Adds BLint prefix for logging.

    :param line: line to print.
    """
    if line[-1] != '\n':
        line = line + '\n'
    print('blinter' + line)


def print_issues(issue_iter: list['LintIssue'], issue_order: tuple):
    """Prints all issues.

    :param issue_iter: list of issues
    :param issue_order: indices determining order to print issue
    """
    for idx, _, _ in issue_order:
        issue = issue_iter[idx]
        log('{}\t{}'.format(issue.severity_icon, issue.description))


def fix_issues(issue_iter, issue_order):
    """Runs fixes on each issue that has a fix option.

    :param issue_iter: list of issues
    :param issue_order: indices determining order to print issue
    """
    orig_num_issues = len(issue_iter)
    for idx, _, _ in issue_order:
        issue = issues[idx]
        bpy.ops.scene_analyzer.fix_issue(fix=issue.fix_expr)
    reload_issues(context)
    curr_issues = window_manager.lint_issues
    curr_num_issues = len(curr_issues)
    num_fixed = orig_num_issues - curr_num_issues
    log('{} issues fixed'.format(num_fixed))
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    log('File saved')


if __name__ == '__main__':
    auto_fix = any('--blint-fix' == a for a in sys.argv)

    # get lint rules from preferences
    blend_filename = bpy.data.filepath
    try:
        from blint.model.LintIssue import get_sort_value
        from blint.preferences import reload_issues
    except ImportError:
        log('blint not found, the blint addon must be installed and enabled!')
        sys.exit(1)

    context = bpy.context
    window_manager = context.window_manager

    context.scene.render.engine = 'CYCLES'

    reload_issues(context)

    # print blender file name
    try:
        if len(window_manager.lint_issues) == 0:
            log('No issues found')
        else:
            issues = window_manager.lint_issues
            issue_sort_vals = [(idx, get_sort_value(issue), issue.description) for idx, issue in enumerate(issues)]
            issue_sort_vals.sort(key=lambda x: (x[1], x[2]))
            print_issues(issues, issue_sort_vals)

            num_fixable = len([True for issue in issues if issue.fix_expr])
            if auto_fix:
                log('Fixing {} of {} issues...'.format(num_fixable, len(issues)))
                fix_issues(issues, issue_sort_vals)
                reload_issues(context)
            elif num_fixable > 0:
                log('{} of {} issues can be automatically fixed'.format(num_fixable, len(issues)))

    except Exception as e:
        log(str(e))

    log('Closing file...')
